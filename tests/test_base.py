"""
Tests for the BaseMechanicalTest class.

Author: Tom Fleet
Created: 28/11/2020
"""

import collections
import json
from pathlib import Path

import altair as alt
import pandas as pd
import pytest
from numpy.testing import assert_almost_equal
from pandas.testing import assert_frame_equal, assert_series_equal

from pymechtest.base import BaseMechanicalTest

from .test_utils import (
    paths,
    paths_and_df_shapes_no_yield,
    paths_and_df_shapes_yield,
    paths_and_extract_values_series_no_yield,
    paths_and_extract_values_series_yield,
    paths_and_filenames,
    paths_and_moduli_no_yield,
    paths_and_moduli_yield,
    paths_and_specimen_ids,
    paths_and_yield_strengths,
    paths_for_no_id_test,
)


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
    base_no_yield_no_stress_strain_cols, df_with_good_stress_and_strain_cols
):

    df = df_with_good_stress_and_strain_cols

    obj = base_no_yield_no_stress_strain_cols

    obj._get_stress_strain_cols(df)

    assert obj.stress_col == "This one has stress in it"
    assert obj.strain_col == "This one has strain in it"


def test_default_stress_strain_cols_no_yield(base_no_yield_no_stress_strain_cols):

    obj = base_no_yield_no_stress_strain_cols

    # This method relies on knowing what the stress/strain cols are
    # It will raise a ValueError if it can't autodetect
    obj.summarise()


def test_default_stress_strain_cols_yield(base_yield_no_stress_strain_cols):

    obj = base_yield_no_stress_strain_cols

    # This method relies on knowing what the stress/strain cols are
    # It will raise a ValueError if it can't autodetect
    obj.summarise()


def test_default_stress_strain_cols_raises_when_no_match_stress(
    df_with_bad_stress_col, base_no_yield_no_stress_strain_cols
):

    df = df_with_bad_stress_col

    obj = base_no_yield_no_stress_strain_cols

    with pytest.raises(ValueError):
        obj._get_stress_strain_cols(df)


def test_default_stress_strain_cols_raises_when_no_match_strain(
    df_with_bad_strain_col, base_no_yield_no_stress_strain_cols
):

    df = df_with_bad_strain_col

    obj = base_no_yield_no_stress_strain_cols

    with pytest.raises(ValueError):
        obj._get_stress_strain_cols(df)


def test_default_stress_strain_cols_raises_when_no_match_both(
    df_with_bad_stress_and_strain_cols, base_no_yield_no_stress_strain_cols
):

    df = df_with_bad_stress_and_strain_cols

    obj = base_no_yield_no_stress_strain_cols

    with pytest.raises(ValueError):
        obj._get_stress_strain_cols(df)


@pytest.mark.parametrize("filepath, specimen_id", paths_and_specimen_ids)
def test_get_specimen_id(base_no_yield, filepath, specimen_id):

    obj = base_no_yield

    assert obj._get_specimen_id(filepath) == specimen_id


@pytest.mark.parametrize("filepath, filename", paths_and_filenames)
def test_get_specimen_id_default(base_no_yield_no_id, filepath, filename):

    obj = base_no_yield_no_id

    assert obj._get_specimen_id(filepath) == filename


@pytest.mark.parametrize("filepath", paths_for_no_id_test)
def test_get_specimen_id_raises_if_missing(base_no_yield, filepath):

    obj = base_no_yield

    with pytest.raises(ValueError):
        obj._get_specimen_id(filepath)


@pytest.mark.parametrize("filepath, modulus", paths_and_moduli_no_yield)
def test_calc_modulus_no_yield(base_no_yield, filepath, modulus):

    long_obj = base_no_yield

    assert_almost_equal(
        long_obj._calc_modulus(long_obj._load(filepath)), modulus, decimal=2
    )


@pytest.mark.parametrize("filepath, modulus", paths_and_moduli_yield)
def test_calc_modulus_yield(base_yield, filepath, modulus):

    trans_obj = base_yield

    assert_almost_equal(
        trans_obj._calc_modulus(trans_obj._load(filepath)), modulus, decimal=2
    )


@pytest.mark.parametrize("filepath, df_shape", paths_and_df_shapes_no_yield)
def test_load_no_yield(base_no_yield, filepath, df_shape):

    long_obj = base_no_yield

    assert long_obj._load(filepath).shape == df_shape


@pytest.mark.parametrize("filepath, df_shape", paths_and_df_shapes_yield)
def test_load_yield(base_yield, filepath, df_shape):

    trans_obj = base_yield

    assert trans_obj._load(filepath).shape == df_shape


def test_load_all_no_yield(base_no_yield):

    obj = base_no_yield

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


def test_load_all_yield(base_yield):

    obj = base_yield

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


def test_specimen_id_column_no_yield(base_no_yield):

    obj = base_no_yield

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


def test_specimen_id_column_yield(base_yield):

    obj = base_yield

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


@pytest.mark.parametrize("filepath, yield_strength", paths_and_yield_strengths)
def test_calc_yield_strength(base_yield, filepath, yield_strength):

    obj = base_yield

    assert_almost_equal(obj._calc_yield(obj._load(filepath)), yield_strength, decimal=2)


@pytest.mark.parametrize("filepath", paths)
def test_calc_yield_raises_attribute_error_if_yield_false(base_no_yield, filepath):

    # _test_no_yield means expect_yield = False
    obj = base_no_yield

    # Trans specimens data (no yield expected)
    df = obj._load(fp=filepath)

    with pytest.raises(AttributeError):
        obj._calc_yield(df)


@pytest.mark.parametrize(
    "filepath, extracted_series", paths_and_extract_values_series_no_yield
)
def test_extract_values_no_yield(base_no_yield, filepath, extracted_series):

    obj = base_no_yield

    assert_series_equal(
        obj._extract_values(obj._load(filepath)), extracted_series, atol=0.01
    )


@pytest.mark.parametrize(
    "filepath, extracted_series", paths_and_extract_values_series_yield
)
def test_extract_values_yield(base_yield, filepath, extracted_series):

    obj = base_yield

    assert_series_equal(
        obj._extract_values(obj._load(filepath)), extracted_series, atol=0.01
    )


def test_summarise_no_yield(base_no_yield):

    obj = base_no_yield

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


def test_summarise_yield(base_yield):

    obj = base_yield

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


def test_stats_no_yield(base_no_yield):

    obj = base_no_yield

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


def test_stats_yield(base_yield):

    obj = base_yield

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


def test_base_plot_curves_no_yield(base_no_yield):

    obj = base_no_yield

    plot = obj.plot_curves()

    assert isinstance(plot, alt.Chart)


def test_base_plot_curves_yield(base_yield):

    obj = base_yield

    plot = obj.plot_curves()

    assert isinstance(plot, alt.Chart)


def test_altair_schema_default_args(base_no_yield_no_stress_strain_cols):

    obj = base_no_yield_no_stress_strain_cols

    plot = obj.plot_curves()

    plot_json = json.loads(plot.to_json())

    truth_encoding = {
        "color": {"field": "Specimen ID", "title": "Specimen ID", "type": "nominal"},
        "x": {
            "field": "Tensile strain (Strain 1)",
            "title": "BaseMechanicalTest Strain (%)",
            "type": "quantitative",
        },
        "y": {
            "field": "Tensile stress",
            "title": "BaseMechanicalTest Stress (MPa)",
            "type": "quantitative",
        },
    }

    assert plot_json["encoding"] == truth_encoding
    assert plot_json["title"] == "BaseMechanicalTest Stress Strain Curves"


def test_altair_schema_passed_args(base_no_yield):

    obj = base_no_yield

    plot = obj.plot_curves(
        title="Totally Made Up Title", x_label="Silly x label", y_label="Silly y label"
    )

    plot_json = json.loads(plot.to_json())

    truth_encoding = {
        "color": {"field": "Specimen ID", "title": "Specimen ID", "type": "nominal"},
        "x": {
            "field": "Tensile strain (Strain 1)",
            "title": "Silly x label",
            "type": "quantitative",
        },
        "y": {
            "field": "Tensile stress",
            "title": "Silly y label",
            "type": "quantitative",
        },
    }

    assert plot_json["encoding"] == truth_encoding
    assert plot_json["title"] == "Totally Made Up Title"


def test_plot_curves_raises_on_invalid_save_method(base_no_yield):

    obj = base_no_yield

    with pytest.raises(ValueError):
        # Attempt to save a graph with an invalid save method
        obj.plot_curves(save_method="silly_method")
