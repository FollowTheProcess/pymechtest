"""
Tests for the Compression class.

Author: Tom Fleet
Created: 01/01/2021
"""


from pymechtest import Compression


def test_compression_init():

    obj = Compression(
        folder="made/up/directory",
        header=8,
        stress_col="Compression stress",
        strain_col="Compression strain (Strain 1)",
        id_row=3,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    assert obj.folder == "made/up/directory"
    assert obj.header == 8
    assert obj.stress_col == "Compression stress"
    assert obj.strain_col == "Compression strain (Strain 1)"
    assert obj.id_row == 3
    assert obj.strain1 == 0.05
    assert obj.strain2 == 0.15
    assert obj.expect_yield is False


def test_compression_repr():

    obj = Compression(
        folder="made/up/directory",
        stress_col="Compression stress",
        strain_col="Compression strain (Strain 1)",
        id_row=3,
        header=8,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    assert (
        obj.__repr__() == "Compression(folder='made/up/directory', "
        "id_row=3, "
        "stress_col='Compression stress', "
        "strain_col='Compression strain (Strain 1)', "
        "header=8, "
        "strain1=0.05, strain2=0.15, expect_yield=False)"
    )
