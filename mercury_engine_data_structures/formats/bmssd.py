from construct import (
    Struct, Construct, Const, Int32ul, PrefixedArray, CString, Byte, Array, Float32l, PaddedString,
    Int64ul
)

from mercury_engine_data_structures.formats import BaseResource
from mercury_engine_data_structures.game_check import Game

VectorArray = Array(3, Float32l)

BMSSD = Struct(
    magic=Const(b"MSSD"),
    unk1=Int32ul,
    part_info=PrefixedArray(
        Int32ul,
        Struct(
            model_name=CString("utf-8"),
            byte0=Byte,
            byte1=Byte,
            byte2=Byte,
            int3=Int32ul,
            byte4=Byte,
            farr4=VectorArray,
            farr5=VectorArray,
            farr6=VectorArray,
        )
    ),
    model_info=PrefixedArray(
        Int32ul,
        Struct(
            str1=CString("utf-8"),
            elems=PrefixedArray(
                Int32ul,
                Struct(
                    float1=VectorArray,
                    float2=VectorArray,
                    float3=VectorArray,
                )
            )
        )
    ),
    strings_a=PrefixedArray(
        Int32ul,
        CString("utf-8"),
    ),
    unk_structs_a=PrefixedArray(
        Int32ul,
        Struct(
            str1=CString("utf-8"),
            char2=Byte,
            char3=Byte,
            char4=Byte,
            int5=Int32ul,
            int6=Int32ul,
            int7=Int32ul,
            char8=Byte,
            char9=Byte,
            int10=Int32ul,
            str11=PaddedString(16, "utf-8"),
            int12=Int32ul,
            float13=VectorArray,
            float14=VectorArray,
            float15=VectorArray,
            int16=Int32ul,
            float17=VectorArray,
        )
    ),
    strings_b=PrefixedArray(
        Int32ul,
        CString("utf-8"),
    ),
    unk_structs_b=PrefixedArray(
        Int32ul,
        Struct(
            str1=CString("utf-8"),
            int2=Int32ul,
            struct4=PrefixedArray(
                Int32ul,
                Struct(
                    int1=Int32ul,
                    long3=PrefixedArray(Int32ul, Int64ul),
                )
            )
        )
    )
)


class Bmssd(BaseResource):
    @classmethod
    def construct_class(cls, target_game: Game) -> Construct:
        return BMSSD
