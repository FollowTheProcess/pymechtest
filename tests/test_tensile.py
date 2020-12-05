"""
Tests for the Tensile class.

Author: Tom Fleet
Created: 28/11/2020
"""

from pathlib import Path

import pandas as pd
import pytest
from numpy.testing import assert_almost_equal
from pandas.testing import assert_frame_equal, assert_series_equal

from pymechtest import Tensile

# Data for testing & development only
LONG_DATA = Path(__file__).parents[1].resolve().joinpath("data/Long")
TRANS_DATA = Path(__file__).parents[1].resolve().joinpath("data/Trans")

LONG_FILE = [f for f in LONG_DATA.rglob("*.csv")][0]
TRANS_FILE = [f for f in TRANS_DATA.rglob("*.csv")][0]


def test_tensile_init():

    obj = Tensile(
        folder="made/up/directory",
        stress_col="Tensile stress",
        strain_col="Tensile strain (Strain 1)",
        id_row=3,
        skip_rows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    assert obj.folder == "made/up/directory"
    assert obj.stress_col == "Tensile stress"
    assert obj.strain_col == "Tensile strain (Strain 1)"
    assert obj.id_row == 3
    assert obj.skip_rows == [0, 1, 2, 3, 4, 5, 6, 7, 8, 10]
    assert obj.strain1 == 0.05
    assert obj.strain2 == 0.15
    assert obj.expect_yield is False


paths_and_specimen_ids = [
    (LONG_DATA.joinpath("Specimen_RawData_1.csv"), "0038"),
    (LONG_DATA.joinpath("Specimen_RawData_2.csv"), "0031"),
    (LONG_DATA.joinpath("Specimen_RawData_3.csv"), "0040"),
    (LONG_DATA.joinpath("Specimen_RawData_4.csv"), "0032"),
    (LONG_DATA.joinpath("Specimen_RawData_5.csv"), "0033"),
    (LONG_DATA.joinpath("Specimen_RawData_6.csv"), "0034"),
    (TRANS_DATA.joinpath("Specimen_RawData_1.csv"), "009"),
    (TRANS_DATA.joinpath("Specimen_RawData_2.csv"), "008"),
    (TRANS_DATA.joinpath("Specimen_RawData_3.csv"), "007"),
    (TRANS_DATA.joinpath("Specimen_RawData_4.csv"), "006"),
    (TRANS_DATA.joinpath("Specimen_RawData_5.csv"), "005"),
    (TRANS_DATA.joinpath("Specimen_RawData_6.csv"), "004"),
]


@pytest.mark.parametrize("filepath, specimen_id", paths_and_specimen_ids)
def test_get_specimen_id(filepath, specimen_id):

    obj = Tensile._test_long()

    assert obj._get_specimen_id(filepath) == specimen_id


paths_and_moduli_long = [
    (LONG_DATA.joinpath("Specimen_RawData_1.csv"), 214.73703704359207),
    (LONG_DATA.joinpath("Specimen_RawData_10.csv"), 227.9269563135135),
    (LONG_DATA.joinpath("Specimen_RawData_2.csv"), 222.72607703734684),
    (LONG_DATA.joinpath("Specimen_RawData_3.csv"), 226.24042185043274),
    (LONG_DATA.joinpath("Specimen_RawData_4.csv"), 227.20719368480655),
    (LONG_DATA.joinpath("Specimen_RawData_5.csv"), 237.49691564169657),
    (LONG_DATA.joinpath("Specimen_RawData_6.csv"), 229.99812783980767),
    (LONG_DATA.joinpath("Specimen_RawData_7.csv"), 210.5774902227845),
    (LONG_DATA.joinpath("Specimen_RawData_8.csv"), 201.59969738297002),
    (LONG_DATA.joinpath("Specimen_RawData_9.csv"), 222.34006012040436),
]

paths_and_moduli_trans = [
    (TRANS_DATA.joinpath("Specimen_RawData_10.csv"), 171.04161005434793),
    (TRANS_DATA.joinpath("Specimen_RawData_1.csv"), 177.04030085330862),
    (TRANS_DATA.joinpath("Specimen_RawData_2.csv"), 190.00716803363935),
    (TRANS_DATA.joinpath("Specimen_RawData_3.csv"), 174.266659531658),
    (TRANS_DATA.joinpath("Specimen_RawData_4.csv"), 154.94934554636575),
    (TRANS_DATA.joinpath("Specimen_RawData_5.csv"), 178.20932823593682),
    (TRANS_DATA.joinpath("Specimen_RawData_6.csv"), 152.57936457584347),
    (TRANS_DATA.joinpath("Specimen_RawData_7.csv"), 145.24650168212222),
    (TRANS_DATA.joinpath("Specimen_RawData_8.csv"), 186.87429547855731),
    (TRANS_DATA.joinpath("Specimen_RawData_9.csv"), 182.94653227297943),
]


@pytest.mark.parametrize("filepath, modulus", paths_and_moduli_long)
def test_calc_modulus_long(filepath, modulus):

    long_obj = Tensile._test_long()

    assert_almost_equal(long_obj._calc_modulus(long_obj._load(filepath)), modulus)


@pytest.mark.parametrize("filepath, modulus", paths_and_moduli_trans)
def test_calc_modulus_trans(filepath, modulus):

    trans_obj = Tensile._test_trans()

    assert_almost_equal(trans_obj._calc_modulus(trans_obj._load(filepath)), modulus)


paths_and_df_shapes_long = [
    (LONG_DATA.joinpath("Specimen_RawData_1.csv"), (1467, 6)),
    (LONG_DATA.joinpath("Specimen_RawData_10.csv"), (1299, 6)),
    (LONG_DATA.joinpath("Specimen_RawData_2.csv"), (1066, 6)),
    (LONG_DATA.joinpath("Specimen_RawData_3.csv"), (1177, 6)),
    (LONG_DATA.joinpath("Specimen_RawData_4.csv"), (1214, 6)),
    (LONG_DATA.joinpath("Specimen_RawData_5.csv"), (1228, 6)),
    (LONG_DATA.joinpath("Specimen_RawData_6.csv"), (1238, 6)),
    (LONG_DATA.joinpath("Specimen_RawData_7.csv"), (1303, 6)),
    (LONG_DATA.joinpath("Specimen_RawData_8.csv"), (1245, 6)),
    (LONG_DATA.joinpath("Specimen_RawData_9.csv"), (1237, 6)),
]

paths_and_df_shapes_trans = [
    (TRANS_DATA.joinpath("Specimen_RawData_1.csv"), (279, 6)),
    (TRANS_DATA.joinpath("Specimen_RawData_10.csv"), (319, 6)),
    (TRANS_DATA.joinpath("Specimen_RawData_2.csv"), (309, 6)),
    (TRANS_DATA.joinpath("Specimen_RawData_3.csv"), (185, 6)),
    (TRANS_DATA.joinpath("Specimen_RawData_4.csv"), (288, 6)),
    (TRANS_DATA.joinpath("Specimen_RawData_5.csv"), (269, 6)),
    (TRANS_DATA.joinpath("Specimen_RawData_6.csv"), (469, 6)),
    (TRANS_DATA.joinpath("Specimen_RawData_7.csv"), (331, 6)),
    (TRANS_DATA.joinpath("Specimen_RawData_8.csv"), (297, 6)),
    (TRANS_DATA.joinpath("Specimen_RawData_9.csv"), (219, 6)),
]


@pytest.mark.parametrize("filepath, df_shape", paths_and_df_shapes_long)
def test_load_long(filepath, df_shape):

    long_obj = Tensile._test_long()

    assert long_obj._load(filepath).shape == df_shape


@pytest.mark.parametrize("filepath, df_shape", paths_and_df_shapes_trans)
def test_load_trans(filepath, df_shape):

    trans_obj = Tensile._test_trans()

    assert trans_obj._load(filepath).shape == df_shape


def test_load_all_long():

    obj = Tensile._test_long()

    df = obj.load_all()

    assert df.shape == (12474, 6)
    assert sorted(df.columns.to_list()) == [
        "Extension",
        "Load",
        "Specimen ID",
        "Tensile strain (Strain 1)",
        "Tensile stress",
        "Time",
    ]


def test_load_all_trans():

    obj = Tensile._test_trans()

    df = obj.load_all()

    assert df.shape == (2965, 6)
    assert sorted(df.columns.to_list()) == [
        "Extension",
        "Load",
        "Specimen ID",
        "Tensile strain (Strain 1)",
        "Tensile stress",
        "Time",
    ]


def test_specimen_id_column_long():

    obj = Tensile._test_long()

    df = obj.load_all()

    assert df["Specimen ID"].isnull().sum() == 0
    assert sorted(df["Specimen ID"].unique().tolist()) == [
        "0031",
        "0032",
        "0033",
        "0034",
        "0035",
        "0036",
        "0037",
        "0038",
        "0039",
        "0040",
    ]


def test_specimen_id_column_trans():

    obj = Tensile._test_trans()

    df = obj.load_all()

    assert df["Specimen ID"].isnull().sum() == 0
    assert sorted(df["Specimen ID"].unique().tolist()) == [
        "001",
        "002",
        "003",
        "004",
        "005",
        "006",
        "007",
        "008",
        "009",
        "010",
    ]


paths_and_yield_strengths = [
    (TRANS_DATA.joinpath("Specimen_RawData_10.csv"), 83.3453),
    (TRANS_DATA.joinpath("Specimen_RawData_1.csv"), 89.108),
    (TRANS_DATA.joinpath("Specimen_RawData_2.csv"), 85.1674),
    (TRANS_DATA.joinpath("Specimen_RawData_3.csv"), 88.398),
    (TRANS_DATA.joinpath("Specimen_RawData_4.csv"), 86.4215),
    (TRANS_DATA.joinpath("Specimen_RawData_5.csv"), 89.6358),
    (TRANS_DATA.joinpath("Specimen_RawData_6.csv"), 77.2231),
    (TRANS_DATA.joinpath("Specimen_RawData_7.csv"), 86.8556),
    (TRANS_DATA.joinpath("Specimen_RawData_8.csv"), 90.1102),
    (TRANS_DATA.joinpath("Specimen_RawData_9.csv"), 89.7818),
]


@pytest.mark.parametrize("filepath, yield_strength", paths_and_yield_strengths)
def test_calc_yield_strength(filepath, yield_strength):

    obj = Tensile._test_trans()

    assert_almost_equal(obj._calc_yield(obj._load(filepath)), yield_strength)


paths = [f for f in TRANS_DATA.rglob("*.csv")] + [f for f in LONG_DATA.rglob("*.csv")]


@pytest.mark.parametrize("filepath", paths)
def test_calc_yield_raises_attribute_error_if_yield_false(filepath):

    # _test_long means expect_yield = False
    obj = Tensile._test_long()

    # Trans specimens data (no yield expected)
    df = obj._load(fp=filepath)

    with pytest.raises(AttributeError):
        obj._calc_yield(df)


paths_and_extract_values_series_long = [
    (
        LONG_DATA.joinpath("Specimen_RawData_1.csv"),
        pd.Series(
            data={"Specimen ID": "0038", "UTS": 739.3342, "Modulus": 214.73703704359207}
        ),
    ),
    (
        LONG_DATA.joinpath("Specimen_RawData_10.csv"),
        pd.Series(
            data={"Specimen ID": "0039", "UTS": 805.4785, "Modulus": 227.92695631351344}
        ),
    ),
    (
        LONG_DATA.joinpath("Specimen_RawData_2.csv"),
        pd.Series(
            data={"Specimen ID": "0031", "UTS": 720.6285, "Modulus": 222.72607703734684}
        ),
    ),
    (
        LONG_DATA.joinpath("Specimen_RawData_3.csv"),
        pd.Series(
            data={"Specimen ID": "0040", "UTS": 806.6938, "Modulus": 226.24042185043274}
        ),
    ),
    (
        LONG_DATA.joinpath("Specimen_RawData_4.csv"),
        pd.Series(
            data={"Specimen ID": "0032", "UTS": 782.9673, "Modulus": 227.20719368480655}
        ),
    ),
    (
        LONG_DATA.joinpath("Specimen_RawData_5.csv"),
        pd.Series(
            data={"Specimen ID": "0033", "UTS": 764.4656, "Modulus": 237.49691564169657}
        ),
    ),
    (
        LONG_DATA.joinpath("Specimen_RawData_6.csv"),
        pd.Series(
            data={"Specimen ID": "0034", "UTS": 784.4911, "Modulus": 229.99812783980784}
        ),
    ),
    (
        LONG_DATA.joinpath("Specimen_RawData_7.csv"),
        pd.Series(
            data={"Specimen ID": "0036", "UTS": 784.1665, "Modulus": 210.5774902227845}
        ),
    ),
    (
        LONG_DATA.joinpath("Specimen_RawData_8.csv"),
        pd.Series(
            data={"Specimen ID": "0035", "UTS": 809.7581, "Modulus": 201.59969738297002}
        ),
    ),
    (
        LONG_DATA.joinpath("Specimen_RawData_9.csv"),
        pd.Series(
            data={"Specimen ID": "0037", "UTS": 778.8885, "Modulus": 222.34006012040436}
        ),
    ),
]

paths_and_extract_values_series_trans = [
    (
        TRANS_DATA.joinpath("Specimen_RawData_10.csv"),
        pd.Series(
            data={
                "Specimen ID": "010",
                "UTS": 180.2974,
                "Modulus": 171.04161005434793,
                "Yield Strength": 83.3453,
            }
        ),
    ),
    (
        TRANS_DATA.joinpath("Specimen_RawData_1.csv"),
        pd.Series(
            data={
                "Specimen ID": "009",
                "UTS": 188.4382,
                "Modulus": 177.04030085330862,
                "Yield Strength": 89.108,
            }
        ),
    ),
    (
        TRANS_DATA.joinpath("Specimen_RawData_2.csv"),
        pd.Series(
            data={
                "Specimen ID": "008",
                "UTS": 183.7281,
                "Modulus": 190.00716803363935,
                "Yield Strength": 85.1674,
            }
        ),
    ),
    (
        TRANS_DATA.joinpath("Specimen_RawData_3.csv"),
        pd.Series(
            data={
                "Specimen ID": "007",
                "UTS": 151.3554,
                "Modulus": 174.266659531658,
                "Yield Strength": 88.398,
            }
        ),
    ),
    (
        TRANS_DATA.joinpath("Specimen_RawData_4.csv"),
        pd.Series(
            data={
                "Specimen ID": "006",
                "UTS": 180.8582,
                "Modulus": 154.94934554636595,
                "Yield Strength": 86.4215,
            }
        ),
    ),
    (
        TRANS_DATA.joinpath("Specimen_RawData_5.csv"),
        pd.Series(
            data={
                "Specimen ID": "005",
                "UTS": 184.7623,
                "Modulus": 178.20932823593682,
                "Yield Strength": 89.6358,
            }
        ),
    ),
    (
        TRANS_DATA.joinpath("Specimen_RawData_6.csv"),
        pd.Series(
            data={
                "Specimen ID": "004",
                "UTS": 190.4115,
                "Modulus": 152.57936457584347,
                "Yield Strength": 77.2231,
            }
        ),
    ),
    (
        TRANS_DATA.joinpath("Specimen_RawData_7.csv"),
        pd.Series(
            data={
                "Specimen ID": "003",
                "UTS": 194.3136,
                "Modulus": 145.2465016821223,
                "Yield Strength": 86.8556,
            }
        ),
    ),
    (
        TRANS_DATA.joinpath("Specimen_RawData_8.csv"),
        pd.Series(
            data={
                "Specimen ID": "002",
                "UTS": 191.4301,
                "Modulus": 186.87429547855706,
                "Yield Strength": 90.1102,
            }
        ),
    ),
    (
        TRANS_DATA.joinpath("Specimen_RawData_9.csv"),
        pd.Series(
            data={
                "Specimen ID": "001",
                "UTS": 168.0556,
                "Modulus": 182.94653227297943,
                "Yield Strength": 89.7818,
            }
        ),
    ),
]


@pytest.mark.parametrize(
    "filepath, extracted_series", paths_and_extract_values_series_long
)
def test_extract_values_long(filepath, extracted_series):

    obj = Tensile._test_long()

    assert_series_equal(obj._extract_values(obj._load(filepath)), extracted_series)


@pytest.mark.parametrize(
    "filepath, extracted_series", paths_and_extract_values_series_trans
)
def test_extract_values_trans(filepath, extracted_series):

    obj = Tensile._test_trans()

    assert_series_equal(obj._extract_values(obj._load(filepath)), extracted_series)


def test_summarise_long():

    obj = Tensile._test_long()

    truth_df = pd.DataFrame.from_dict(
        {
            "Specimen ID": {
                0: "0034",
                1: "0036",
                2: "0033",
                3: "0032",
                4: "0038",
                5: "0040",
                6: "0031",
                7: "0037",
                8: "0035",
                9: "0039",
            },
            "UTS": {
                0: 784.4911,
                1: 784.1665,
                2: 764.4656,
                3: 782.9673,
                4: 739.3342,
                5: 806.6938,
                6: 720.6285,
                7: 778.8885,
                8: 809.7581,
                9: 805.4785,
            },
            "Modulus": {
                0: 229.99812783980784,
                1: 210.5774902227845,
                2: 237.49691564169657,
                3: 227.20719368480655,
                4: 214.73703704359207,
                5: 226.24042185043274,
                6: 222.72607703734684,
                7: 222.34006012040436,
                8: 201.59969738297002,
                9: 227.92695631351344,
            },
        }
    )

    assert_frame_equal(
        obj.summarise().sort_values(by="Specimen ID"),
        truth_df.sort_values(by="Specimen ID").convert_dtypes(),
    )


def test_summarise_trans():

    obj = Tensile._test_trans()

    truth_df = pd.DataFrame.from_dict(
        {
            "Specimen ID": {
                0: "004",
                1: "003",
                2: "005",
                3: "006",
                4: "009",
                5: "007",
                6: "008",
                7: "001",
                8: "002",
                9: "010",
            },
            "UTS": {
                0: 190.4115,
                1: 194.3136,
                2: 184.7623,
                3: 180.8582,
                4: 188.4382,
                5: 151.3554,
                6: 183.7281,
                7: 168.0556,
                8: 191.4301,
                9: 180.2974,
            },
            "Modulus": {
                0: 152.57936457584347,
                1: 145.2465016821223,
                2: 178.20932823593682,
                3: 154.94934554636595,
                4: 177.04030085330862,
                5: 174.266659531658,
                6: 190.00716803363935,
                7: 182.94653227297943,
                8: 186.87429547855706,
                9: 171.04161005434793,
            },
            "Yield Strength": {
                0: 77.2231,
                1: 86.8556,
                2: 89.6358,
                3: 86.4215,
                4: 89.108,
                5: 88.398,
                6: 85.1674,
                7: 89.7818,
                8: 90.1102,
                9: 83.3453,
            },
        }
    )

    assert_frame_equal(
        obj.summarise().sort_values(by="Specimen ID"),
        truth_df.sort_values(by="Specimen ID").convert_dtypes(),
    )
