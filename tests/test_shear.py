"""
Tests for the Shear class.

Author: Tom Fleet
Created: 01/01/2021
"""

from pathlib import Path

from pymechtest import Shear


def test_shear_init():

    obj = Shear(
        folder="made/up/directory",
        stress_col="Shear stress",
        strain_col="Shear strain (Strain 1)",
        id_row=3,
        skip_rows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    assert obj.folder == "made/up/directory"
    assert obj.stress_col == "Shear stress"
    assert obj.strain_col == "Shear strain (Strain 1)"
    assert obj.id_row == 3
    assert obj.skip_rows == [0, 1, 2, 3, 4, 5, 6, 7, 8, 10]
    assert obj.strain1 == 0.05
    assert obj.strain2 == 0.15
    assert obj.expect_yield is False


def test_shear_repr():

    obj = Shear(
        folder="made/up/directory",
        stress_col="Shear stress",
        strain_col="Shear strain (Strain 1)",
        id_row=3,
        skip_rows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    assert (
        obj.__repr__() == "Shear(folder='made/up/directory', "
        "stress_col='Shear stress', "
        "strain_col='Shear strain (Strain 1)', "
        "id_row=3, skip_rows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10], "
        "strain1=0.05, strain2=0.15, expect_yield=False)"
    )


def test_shear_eq():

    obj = Shear(
        folder="made/up/directory",
        stress_col="Shear stress",
        strain_col="Shear strain (Strain 1)",
        id_row=3,
        skip_rows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    same = Shear(
        folder="made/up/directory",
        stress_col="Shear stress",
        strain_col="Shear strain (Strain 1)",
        id_row=3,
        skip_rows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    diff = Shear(
        folder="different/made/up/directory",
        stress_col="Different stress col",
        strain_col="This doesn't match either",
        id_row=6,
        skip_rows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
        strain1=0.025,
        strain2=0.3,
        expect_yield=True,
    )

    # Random different class, in this case a pathlib.Path
    different_class = Path(__file__)

    assert obj.__eq__(same) is True
    assert obj.__eq__(diff) is False
    assert obj.__eq__(different_class) is NotImplemented
