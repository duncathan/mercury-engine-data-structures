"""
Helper class to handle objects that contain a pointer to objects of varied types, usually all with the same base type.
"""
import copy
from typing import Dict, Union, Type

import construct
from construct import Construct, Struct, Hex, Int64ul, Switch, Adapter

import mercury_engine_data_structures.dread_data
from mercury_engine_data_structures.construct_extensions.misc import ErrorWithMessage


class PointerAdapter(Adapter):
    types: Dict[int, Union[Construct, Type[Construct]]]

    def __init__(self, subcon, types):
        super().__init__(subcon)
        self.types = types

    @property
    def _allow_null(self):
        return mercury_engine_data_structures.dread_data.all_name_to_property_id()["void"] in self.types

    @property
    def _single_type(self):
        return len(self.types) == (2 if self._allow_null else 1)

    def _decode(self, obj: construct.Container, context, path):
        if obj.ptr is None:
            return None

        if self._single_type:
            return obj.ptr

        ret = construct.Container()
        ret["@type"] = mercury_engine_data_structures.dread_data.all_property_id_to_name()[obj.type]
        for key, value in obj.ptr.items():
            ret[key] = value
        return ret

    def _encode(self, obj: construct.Container, context, path):
        if obj is None:
            type_id = mercury_engine_data_structures.dread_data.all_name_to_property_id()["void"]

        elif self._single_type:
            type_id = list(self.types.keys())[1]

        else:
            obj = copy.copy(obj)
            type_name: str = obj.pop("@type")
            type_id = mercury_engine_data_structures.dread_data.all_name_to_property_id()[type_name]

        return construct.Container(
            type=type_id,
            ptr=obj,
        )


class PointerSet:
    types: Dict[int, Union[Construct, Type[Construct]]]

    def __init__(self, category: str, *, allow_null: bool = True):
        self.category = category
        self.types = {}
        if allow_null:
            self.add_option("void", construct.Pass)

    @classmethod
    def construct_pointer_for(cls, name: str, conn: Union[Construct, Type[Construct]]) -> Construct:
        ret = cls(name, allow_null=True)
        ret.add_option(name, conn)
        return ret.create_construct()

    def add_option(self, name: str, value: Union[Construct, Type[Construct]]) -> None:
        prop_id = mercury_engine_data_structures.dread_data.all_name_to_property_id()[name]
        if prop_id in self.types:
            raise ValueError(f"Attempting to add {name} to {self.category}, but already present.")
        self.types[prop_id] = name / value

    def create_construct(self) -> Construct:
        return PointerAdapter(Struct(
            type=Hex(Int64ul),
            ptr=Switch(
                construct.this.type,
                self.types,
                ErrorWithMessage(
                    lambda ctx: f"Property {ctx.type} ({mercury_engine_data_structures.dread_data.all_property_id_to_name().get(ctx.type)}) "
                                "without assigned type"),
            )
        ), self.types)
