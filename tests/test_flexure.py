"""
Tests for the Flexure class.

Author: Tom Fleet
Created: 01/01/2021
"""

from pathlib import Path

from pymechtest import Flexure


def test_flexure_init():

    obj = Flexure(
        folder="made/up/directory",
        header=8,
        stress_col="Flexure stress",
        strain_col="Flexure strain (Strain 1)",
        id_row=3,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    assert obj.folder == "made/up/directory"
    assert obj.header == 8
    assert obj.stress_col == "Flexure stress"
    assert obj.strain_col == "Flexure strain (Strain 1)"
    assert obj.id_row == 3
    assert obj.strain1 == 0.05
    assert obj.strain2 == 0.15
    assert obj.expect_yield is False


def test_flexure_repr():

    obj = Flexure(
        folder="made/up/directory",
        header=8,
        stress_col="Flexure stress",
        strain_col="Flexure strain (Strain 1)",
        id_row=3,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    assert (
        obj.__repr__() == "Flexure(folder='made/up/directory', "
        "header=8, "
        "stress_col='Flexure stress', "
        "strain_col='Flexure strain (Strain 1)', "
        "id_row=3, "
        "strain1=0.05, strain2=0.15, expect_yield=False)"
    )


def test_flexure_eq():

    obj = Flexure(
        folder="made/up/directory",
        header=8,
        stress_col="Flexure stress",
        strain_col="Flexure strain (Strain 1)",
        id_row=3,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    same = Flexure(
        folder="made/up/directory",
        header=8,
        stress_col="Flexure stress",
        strain_col="Flexure strain (Strain 1)",
        id_row=3,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    diff = Flexure(
        folder="different/made/up/directory",
        header=8,
        stress_col="Different stress col",
        strain_col="This doesn't match either",
        id_row=6,
        strain1=0.025,
        strain2=0.3,
        expect_yield=True,
    )

    # Random different class, in this case a pathlib.Path
    different_class = Path(__file__)

    assert obj.__eq__(same) is True
    assert obj.__eq__(diff) is False
    assert obj.__eq__(different_class) is NotImplemented
