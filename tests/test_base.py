"""
Tests for the BaseMechanicalTest class.

Author: Tom Fleet
Created: 28/11/2020
"""

import collections
from pathlib import Path

import altair as alt
import pandas as pd
import pytest
from numpy.testing import assert_almost_equal
from pandas.testing import assert_frame_equal, assert_series_equal

from pymechtest.base import BaseMechanicalTest

# Data for testing & development only
TENS_NO_YIELD = Path(__file__).parent.resolve().joinpath("data/Tens_No_Yield")
TENS_YIELD = Path(__file__).parent.resolve().joinpath("data/Tens_Yield")
# Same as TENS_YIELD but with specimen ID removed to test exception handling
NO_IDS = Path(__file__).parent.resolve().joinpath("data/No_IDs")


def test_base_init():

    obj = BaseMechanicalTest(
        folder="made/up/directory",
        header=8,
        stress_col="BaseMechanicalTest stress",
        strain_col="BaseMechanicalTest strain (Strain 1)",
        id_row=3,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    assert obj.folder == "made/up/directory"
    assert obj.header == 8
    assert obj.stress_col == "BaseMechanicalTest stress"
    assert obj.strain_col == "BaseMechanicalTest strain (Strain 1)"
    assert obj.id_row == 3
    assert obj.strain1 == 0.05
    assert obj.strain2 == 0.15
    assert obj.expect_yield is False


def test_base_repr():

    obj = BaseMechanicalTest(
        folder="made/up/directory",
        stress_col="BaseMechanicalTest stress",
        strain_col="BaseMechanicalTest strain (Strain 1)",
        id_row=3,
        header=8,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    assert (
        obj.__repr__() == "BaseMechanicalTest(folder='made/up/directory', "
        "id_row=3, "
        "stress_col='BaseMechanicalTest stress', "
        "strain_col='BaseMechanicalTest strain (Strain 1)', "
        "header=8, "
        "strain1=0.05, strain2=0.15, expect_yield=False)"
    )


def test_base_eq():

    obj = BaseMechanicalTest(
        folder="made/up/directory",
        stress_col="BaseMechanicalTest stress",
        strain_col="BaseMechanicalTest strain (Strain 1)",
        id_row=3,
        header=8,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    same = BaseMechanicalTest(
        folder="made/up/directory",
        stress_col="BaseMechanicalTest stress",
        strain_col="BaseMechanicalTest strain (Strain 1)",
        id_row=3,
        header=8,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    diff = BaseMechanicalTest(
        folder="different/made/up/directory",
        stress_col="Different stress col",
        strain_col="This doesn't match either",
        id_row=6,
        header=8,
        strain1=0.025,
        strain2=0.3,
        expect_yield=True,
    )

    # Random different class, in this case a pathlib.Path
    different_class = Path(__file__)

    assert obj.__eq__(same) is True
    assert obj.__eq__(diff) is False
    assert obj.__eq__(different_class) is NotImplemented


def test_basic_default_get_stress_strain_cols(
    base_long_no_stress_strain_cols, df_with_good_stress_and_strain_cols
):

    df = df_with_good_stress_and_strain_cols

    obj = base_long_no_stress_strain_cols

    obj._get_stress_strain_cols(df)

    assert obj.stress_col == "This one has stress in it"
    assert obj.strain_col == "This one has strain in it"


def test_default_stress_strain_cols_long(base_long_no_stress_strain_cols):

    obj = base_long_no_stress_strain_cols

    # This method relies on knowing what the stress/strain cols are
    # It will raise a ValueError if it can't autodetect
    obj.summarise()


def test_default_stress_strain_cols_trans(base_trans_no_stress_strain_cols):

    obj = base_trans_no_stress_strain_cols

    # This method relies on knowing what the stress/strain cols are
    # It will raise a ValueError if it can't autodetect
    obj.summarise()


def test_default_stress_strain_cols_raises_when_no_match_stress(
    df_with_bad_stress_col, base_long_no_stress_strain_cols
):

    df = df_with_bad_stress_col

    obj = base_long_no_stress_strain_cols

    with pytest.raises(ValueError):
        obj._get_stress_strain_cols(df)


def test_default_stress_strain_cols_raises_when_no_match_strain(
    df_with_bad_strain_col, base_long_no_stress_strain_cols
):

    df = df_with_bad_strain_col

    obj = base_long_no_stress_strain_cols

    with pytest.raises(ValueError):
        obj._get_stress_strain_cols(df)


def test_default_stress_strain_cols_raises_when_no_match_both(
    df_with_bad_stress_and_strain_cols, base_long_no_stress_strain_cols
):

    df = df_with_bad_stress_and_strain_cols

    obj = base_long_no_stress_strain_cols

    with pytest.raises(ValueError):
        obj._get_stress_strain_cols(df)


paths_and_specimen_ids = [
    (TENS_NO_YIELD.joinpath("Specimen_RawData_1.csv"), "0038"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_2.csv"), "0031"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_3.csv"), "0040"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_4.csv"), "0032"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_5.csv"), "0033"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_6.csv"), "0034"),
    (TENS_YIELD.joinpath("Specimen_RawData_1.csv"), "009"),
    (TENS_YIELD.joinpath("Specimen_RawData_2.csv"), "008"),
    (TENS_YIELD.joinpath("Specimen_RawData_3.csv"), "007"),
    (TENS_YIELD.joinpath("Specimen_RawData_4.csv"), "006"),
    (TENS_YIELD.joinpath("Specimen_RawData_5.csv"), "005"),
    (TENS_YIELD.joinpath("Specimen_RawData_6.csv"), "004"),
]

paths_and_filenames = [
    (TENS_NO_YIELD.joinpath("Specimen_RawData_1.csv"), "Specimen_RawData_1.csv"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_2.csv"), "Specimen_RawData_2.csv"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_3.csv"), "Specimen_RawData_3.csv"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_4.csv"), "Specimen_RawData_4.csv"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_5.csv"), "Specimen_RawData_5.csv"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_6.csv"), "Specimen_RawData_6.csv"),
    (TENS_YIELD.joinpath("Specimen_RawData_1.csv"), "Specimen_RawData_1.csv"),
    (TENS_YIELD.joinpath("Specimen_RawData_2.csv"), "Specimen_RawData_2.csv"),
    (TENS_YIELD.joinpath("Specimen_RawData_3.csv"), "Specimen_RawData_3.csv"),
    (TENS_YIELD.joinpath("Specimen_RawData_4.csv"), "Specimen_RawData_4.csv"),
    (TENS_YIELD.joinpath("Specimen_RawData_5.csv"), "Specimen_RawData_5.csv"),
    (TENS_YIELD.joinpath("Specimen_RawData_6.csv"), "Specimen_RawData_6.csv"),
]

paths_for_no_id_test = [
    (NO_IDS.joinpath("Specimen_RawData_1.csv")),
    (NO_IDS.joinpath("Specimen_RawData_2.csv")),
    (NO_IDS.joinpath("Specimen_RawData_3.csv")),
    (NO_IDS.joinpath("Specimen_RawData_4.csv")),
    (NO_IDS.joinpath("Specimen_RawData_5.csv")),
    (NO_IDS.joinpath("Specimen_RawData_6.csv")),
    (NO_IDS.joinpath("Specimen_RawData_7.csv")),
    (NO_IDS.joinpath("Specimen_RawData_8.csv")),
    (NO_IDS.joinpath("Specimen_RawData_9.csv")),
    (NO_IDS.joinpath("Specimen_RawData_10.csv")),
]


@pytest.mark.parametrize("filepath, specimen_id", paths_and_specimen_ids)
def test_get_specimen_id(base_long, filepath, specimen_id):

    obj = base_long

    assert obj._get_specimen_id(filepath) == specimen_id


@pytest.mark.parametrize("filepath, filename", paths_and_filenames)
def test_get_specimen_id_default(base_long_no_id, filepath, filename):

    obj = base_long_no_id

    assert obj._get_specimen_id(filepath) == filename


@pytest.mark.parametrize("filepath", paths_for_no_id_test)
def test_get_specimen_id_raises_if_missing(base_long, filepath):

    obj = base_long

    with pytest.raises(ValueError):
        obj._get_specimen_id(filepath)


paths_and_moduli_long = [
    (TENS_NO_YIELD.joinpath("Specimen_RawData_1.csv"), 214.73703704359207),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_10.csv"), 227.9269563135135),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_2.csv"), 222.72607703734684),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_3.csv"), 226.24042185043274),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_4.csv"), 227.20719368480655),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_5.csv"), 237.49691564169657),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_6.csv"), 229.99812783980767),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_7.csv"), 210.5774902227845),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_8.csv"), 201.59969738297002),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_9.csv"), 222.34006012040436),
]

paths_and_moduli_trans = [
    (TENS_YIELD.joinpath("Specimen_RawData_10.csv"), 171.04161005434793),
    (TENS_YIELD.joinpath("Specimen_RawData_1.csv"), 177.04030085330862),
    (TENS_YIELD.joinpath("Specimen_RawData_2.csv"), 190.00716803363935),
    (TENS_YIELD.joinpath("Specimen_RawData_3.csv"), 174.266659531658),
    (TENS_YIELD.joinpath("Specimen_RawData_4.csv"), 154.94934554636575),
    (TENS_YIELD.joinpath("Specimen_RawData_5.csv"), 178.20932823593682),
    (TENS_YIELD.joinpath("Specimen_RawData_6.csv"), 152.57936457584347),
    (TENS_YIELD.joinpath("Specimen_RawData_7.csv"), 145.24650168212222),
    (TENS_YIELD.joinpath("Specimen_RawData_8.csv"), 186.87429547855731),
    (TENS_YIELD.joinpath("Specimen_RawData_9.csv"), 182.94653227297943),
]


@pytest.mark.parametrize("filepath, modulus", paths_and_moduli_long)
def test_calc_modulus_long(base_long, filepath, modulus):

    long_obj = base_long

    assert_almost_equal(
        long_obj._calc_modulus(long_obj._load(filepath)), modulus, decimal=2
    )


@pytest.mark.parametrize("filepath, modulus", paths_and_moduli_trans)
def test_calc_modulus_trans(base_trans, filepath, modulus):

    trans_obj = base_trans

    assert_almost_equal(
        trans_obj._calc_modulus(trans_obj._load(filepath)), modulus, decimal=2
    )


paths_and_df_shapes_long = [
    (TENS_NO_YIELD.joinpath("Specimen_RawData_1.csv"), (1467, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_10.csv"), (1299, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_2.csv"), (1066, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_3.csv"), (1177, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_4.csv"), (1214, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_5.csv"), (1228, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_6.csv"), (1238, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_7.csv"), (1303, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_8.csv"), (1245, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_9.csv"), (1237, 6)),
]

paths_and_df_shapes_trans = [
    (TENS_YIELD.joinpath("Specimen_RawData_1.csv"), (279, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_10.csv"), (319, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_2.csv"), (309, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_3.csv"), (185, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_4.csv"), (288, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_5.csv"), (269, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_6.csv"), (469, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_7.csv"), (331, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_8.csv"), (297, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_9.csv"), (219, 6)),
]


@pytest.mark.parametrize("filepath, df_shape", paths_and_df_shapes_long)
def test_load_long(base_long, filepath, df_shape):

    long_obj = base_long

    assert long_obj._load(filepath).shape == df_shape


@pytest.mark.parametrize("filepath, df_shape", paths_and_df_shapes_trans)
def test_load_trans(base_trans, filepath, df_shape):

    trans_obj = base_trans

    assert trans_obj._load(filepath).shape == df_shape


def test_load_all_long(base_long):

    obj = base_long

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


def test_load_all_trans(base_trans):

    obj = base_trans

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


def test_specimen_id_column_long(base_long):

    obj = base_long

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


def test_specimen_id_column_trans(base_trans):

    obj = base_trans

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
    (TENS_YIELD.joinpath("Specimen_RawData_10.csv"), 83.7694),
    (TENS_YIELD.joinpath("Specimen_RawData_1.csv"), 90.1206),
    (TENS_YIELD.joinpath("Specimen_RawData_2.csv"), 85.9652),
    (TENS_YIELD.joinpath("Specimen_RawData_3.csv"), 89.1603),
    (TENS_YIELD.joinpath("Specimen_RawData_4.csv"), 87.1522),
    (TENS_YIELD.joinpath("Specimen_RawData_5.csv"), 90.5217),
    (TENS_YIELD.joinpath("Specimen_RawData_6.csv"), 78.2747),
    (TENS_YIELD.joinpath("Specimen_RawData_7.csv"), 87.7896),
    (TENS_YIELD.joinpath("Specimen_RawData_8.csv"), 90.7741),
    (TENS_YIELD.joinpath("Specimen_RawData_9.csv"), 90.9967),
]


@pytest.mark.parametrize("filepath, yield_strength", paths_and_yield_strengths)
def test_calc_yield_strength(base_trans, filepath, yield_strength):

    obj = base_trans

    assert_almost_equal(obj._calc_yield(obj._load(filepath)), yield_strength, decimal=2)


paths = [f for f in TENS_YIELD.rglob("*.csv")] + [
    f for f in TENS_NO_YIELD.rglob("*.csv")
]


@pytest.mark.parametrize("filepath", paths)
def test_calc_yield_raises_attribute_error_if_yield_false(base_long, filepath):

    # _test_long means expect_yield = False
    obj = base_long

    # Trans specimens data (no yield expected)
    df = obj._load(fp=filepath)

    with pytest.raises(AttributeError):
        obj._calc_yield(df)


paths_and_extract_values_series_long = [
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_1.csv"),
        pd.Series(
            data={
                "Specimen ID": "0038",
                "Strength": 739.3342,
                "Modulus": 214.73703704359207,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_10.csv"),
        pd.Series(
            data={
                "Specimen ID": "0039",
                "Strength": 805.4785,
                "Modulus": 227.92695631351344,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_2.csv"),
        pd.Series(
            data={
                "Specimen ID": "0031",
                "Strength": 720.6285,
                "Modulus": 222.72607703734684,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_3.csv"),
        pd.Series(
            data={
                "Specimen ID": "0040",
                "Strength": 806.6938,
                "Modulus": 226.24042185043274,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_4.csv"),
        pd.Series(
            data={
                "Specimen ID": "0032",
                "Strength": 782.9673,
                "Modulus": 227.20719368480655,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_5.csv"),
        pd.Series(
            data={
                "Specimen ID": "0033",
                "Strength": 764.4656,
                "Modulus": 237.49691564169657,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_6.csv"),
        pd.Series(
            data={
                "Specimen ID": "0034",
                "Strength": 784.4911,
                "Modulus": 229.99812783980784,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_7.csv"),
        pd.Series(
            data={
                "Specimen ID": "0036",
                "Strength": 784.1665,
                "Modulus": 210.5774902227845,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_8.csv"),
        pd.Series(
            data={
                "Specimen ID": "0035",
                "Strength": 809.7581,
                "Modulus": 201.59969738297002,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_9.csv"),
        pd.Series(
            data={
                "Specimen ID": "0037",
                "Strength": 778.8885,
                "Modulus": 222.34006012040436,
            }
        ),
    ),
]

paths_and_extract_values_series_trans = [
    (
        TENS_YIELD.joinpath("Specimen_RawData_10.csv"),
        pd.Series(
            data={
                "Specimen ID": "010",
                "Strength": 180.2974,
                "Modulus": 171.04161005434793,
                "Yield Strength": 83.7694,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_1.csv"),
        pd.Series(
            data={
                "Specimen ID": "009",
                "Strength": 188.4382,
                "Modulus": 177.04030085330862,
                "Yield Strength": 90.1206,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_2.csv"),
        pd.Series(
            data={
                "Specimen ID": "008",
                "Strength": 183.7281,
                "Modulus": 190.00716803363935,
                "Yield Strength": 85.9652,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_3.csv"),
        pd.Series(
            data={
                "Specimen ID": "007",
                "Strength": 151.3554,
                "Modulus": 174.266659531658,
                "Yield Strength": 89.1603,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_4.csv"),
        pd.Series(
            data={
                "Specimen ID": "006",
                "Strength": 180.8582,
                "Modulus": 154.94934554636595,
                "Yield Strength": 87.1522,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_5.csv"),
        pd.Series(
            data={
                "Specimen ID": "005",
                "Strength": 184.7623,
                "Modulus": 178.20932823593682,
                "Yield Strength": 90.5217,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_6.csv"),
        pd.Series(
            data={
                "Specimen ID": "004",
                "Strength": 190.4115,
                "Modulus": 152.57936457584347,
                "Yield Strength": 78.2747,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_7.csv"),
        pd.Series(
            data={
                "Specimen ID": "003",
                "Strength": 194.3136,
                "Modulus": 145.2465016821223,
                "Yield Strength": 87.7896,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_8.csv"),
        pd.Series(
            data={
                "Specimen ID": "002",
                "Strength": 191.4301,
                "Modulus": 186.87429547855706,
                "Yield Strength": 90.7741,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_9.csv"),
        pd.Series(
            data={
                "Specimen ID": "001",
                "Strength": 168.0556,
                "Modulus": 182.94653227297943,
                "Yield Strength": 90.9967,
            }
        ),
    ),
]


@pytest.mark.parametrize(
    "filepath, extracted_series", paths_and_extract_values_series_long
)
def test_extract_values_long(base_long, filepath, extracted_series):

    obj = base_long

    assert_series_equal(
        obj._extract_values(obj._load(filepath)), extracted_series, atol=0.01
    )


@pytest.mark.parametrize(
    "filepath, extracted_series", paths_and_extract_values_series_trans
)
def test_extract_values_trans(base_trans, filepath, extracted_series):

    obj = base_trans

    assert_series_equal(
        obj._extract_values(obj._load(filepath)), extracted_series, atol=0.01
    )


def test_summarise_long(base_long):

    obj = base_long

    truth_dict = collections.OrderedDict(
        {
            "Specimen ID": [
                "0034",
                "0036",
                "0033",
                "0032",
                "0038",
                "0040",
                "0031",
                "0037",
                "0035",
                "0039",
            ],
            "Strength": [
                784.4911,
                784.1665,
                764.4656,
                782.9673,
                739.3342,
                806.6938,
                720.6285,
                778.8885,
                809.7581,
                805.4785,
            ],
            "Modulus": [
                229.99812783980784,
                210.5774902227845,
                237.49691564169657,
                227.20719368480655,
                214.73703704359207,
                226.24042185043274,
                222.72607703734684,
                222.34006012040436,
                201.59969738297002,
                227.92695631351344,
            ],
        }
    )

    test_df = (
        obj.summarise()
        .sort_values("Specimen ID")
        .reset_index()
        .drop(columns=["index"])
        .convert_dtypes()
    )
    truth_df = (
        pd.DataFrame(truth_dict)
        .sort_values("Specimen ID")
        .reset_index()
        .drop(columns=["index"])
        .convert_dtypes()
    )

    assert_frame_equal(test_df, truth_df, atol=0.01)


def test_summarise_trans(base_trans):

    obj = base_trans

    truth_dict = collections.OrderedDict(
        {
            "Specimen ID": [
                "004",
                "003",
                "005",
                "006",
                "009",
                "007",
                "008",
                "001",
                "002",
                "010",
            ],
            "Strength": [
                190.4115,
                194.3136,
                184.7623,
                180.8582,
                188.4382,
                151.3554,
                183.7281,
                168.0556,
                191.4301,
                180.2974,
            ],
            "Modulus": [
                152.57936457584347,
                145.2465016821223,
                178.20932823593682,
                154.94934554636595,
                177.04030085330862,
                174.266659531658,
                190.00716803363935,
                182.94653227297943,
                186.87429547855706,
                171.04161005434793,
            ],
            "Yield Strength": [
                78.2747,
                87.7896,
                90.5217,
                87.1522,
                90.1206,
                89.1603,
                85.9652,
                90.9967,
                90.7741,
                83.7694,
            ],
        }
    )

    test_df = (
        obj.summarise()
        .sort_values("Specimen ID")
        .reset_index()
        .drop(columns=["index"])
        .convert_dtypes()
    )
    truth_df = (
        pd.DataFrame(truth_dict)
        .sort_values("Specimen ID")
        .reset_index()
        .drop(columns=["index"])
        .convert_dtypes()
    )

    assert_frame_equal(test_df, truth_df, atol=0.01)


def test_stats_long(base_long):

    obj = base_long

    truth_df = pd.DataFrame.from_dict(
        {
            "Strength": {
                "count": 10.0,
                "mean": 777.68721,
                "std": 29.176355245508496,
                "cov%": 3.7516825364157005,
                "min": 720.6285,
                "25%": 768.071325,
                "50%": 783.5669,
                "75%": 800.23165,
                "max": 809.7581,
            },
            "Modulus": {
                "count": 10.0,
                "mean": 222.0849977137355,
                "std": 10.457940035367969,
                "cov%": 4.708980860043554,
                "min": 201.59969738297002,
                "25%": 216.63779281279514,
                "50%": 224.4832494438898,
                "75%": 227.7470156563367,
                "max": 237.49691564169657,
            },
        }
    )

    test_df = obj.stats()

    assert_frame_equal(test_df, truth_df, atol=0.01)


def test_stats_trans(base_trans):

    obj = base_trans

    truth_df = pd.DataFrame.from_dict(
        {
            "Strength": {
                "count": 10.0,
                "mean": 181.36503999999996,
                "std": 12.897374951964279,
                "cov%": 7.111279523310713,
                "min": 151.3554,
                "25%": 180.4376,
                "50%": 184.2452,
                "75%": 189.91817500000002,
                "max": 194.3136,
            },
            "Modulus": {
                "count": 10.0,
                "mean": 171.3161106264759,
                "std": 15.327189004438782,
                "cov%": 8.946729498112978,
                "min": 145.2465016821223,
                "25%": 158.97241167336142,
                "50%": 175.6534801924833,
                "75%": 181.76223126371877,
                "max": 190.00716803363935,
            },
            "Yield Strength": {
                "count": 10.0,
                "mean": 87.45245,
                "std": 3.989748300401363,
                "cov%": 4.562191568562531,
                "min": 78.2747,
                "25%": 86.26195,
                "50%": 88.47495,
                "75%": 90.421425,
                "max": 90.9967,
            },
        }
    )

    test_df = obj.stats()

    assert_frame_equal(test_df, truth_df, atol=0.01)


def test_base_plot_curves_long(base_long):

    obj = base_long

    plot = obj.plot_curves()

    # Not sure what else to do for plots?
    assert isinstance(plot, alt.Chart)


def test_base_plot_curves_trans(base_trans):

    obj = base_trans

    plot = obj.plot_curves()

    assert isinstance(plot, alt.Chart)
