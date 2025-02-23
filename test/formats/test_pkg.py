from mercury_engine_data_structures.formats.pkg import PKG
from mercury_engine_data_structures.game_check import Game
from test.test_lib import parse_and_build_compare


def test_compare_dread(dread_path):
    parse_and_build_compare(
        PKG, Game.DREAD, dread_path.joinpath("packs/system/system.pkg")
    )
