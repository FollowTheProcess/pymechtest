# pymechtest

[![License](https://img.shields.io/github/license/FollowTheProcess/pymechtest)](https://github.com/FollowTheProcess/pymechtest)
[![PyPI](https://img.shields.io/pypi/v/pymechtest.svg)](https://pypi.python.org/pypi/pymechtest)
![Code Style](https://img.shields.io/badge/code%20style-black-black)
[![CI](https://github.com/FollowTheProcess/pymechtest/workflows/CI/badge.svg)](https://github.com/FollowTheProcess/pymechtest/actions?query=workflow%3ACI)

*Python package to automate the boring bits of mechanical test data analysis!*

* **Source Code**: [https://github.com/FollowTheProcess/pymechtest](https://github.com/FollowTheProcess/pymechtest)

* **Documentation**: [https://FollowTheProcess.github.io/pymechtest/](https://FollowTheProcess.github.io/pymechtest/)

## What is it?

*:warning: Project under initial development*

pymechtest is a small, helpful(hopefully) python package to help engineers collate, process, analyse, and report on mechanical test data. I built pymechtest to help automate the things I did on a near-daily basis as an engineer. I hope it can prove some use to you too!

Have you ever had to process a bunch of csv output from a mechanical test machine, copying and pasting data into a hacky Excel template to calculate things like elastic modulus and yield strength?

**No more!**

pymechtest has a very simple goal: to reduce the amount of time engineers spend munging data after a batch of mechanical testing.

Here is a quick taste of how easy it is to go from raw data to a tabular summary and a stress-strain plot:

```python
from pymechtest import Tensile

# header and id_row are related to the structure of your csv files
tens = Tensile(folder = "path/to/raw/data", header = 8, id_row = 3)

# Load all data in the folder into a pandas dataframe
tens.load_all()

# Plot a really nice stress-strain curve with Altair
tens.plot_curves()

# Show a summary table with modulus and strength for each sample
tens.summarise()
```

The key features are:

* **Intuitive**: The API is very intuitive, with descriptive methods like `plot_curves` and `summarise`
* **Column Autodetection**: pymechtest will try to auto-detect which columns correspond to stress and strain, and ask you to clarify if it can't.
* **Sensible Defaults**: The API is designed around sensible defaults for things like modulus strain range, whether to expect a yield strength etc.
* **Automatic Calculations**: pymechtest will automatically calculate strength, elastic modulus, yield strength etc. for you.
* **Elegant Looking Stress Strain Curves**: pymechtest uses [altair] to plot amazing looking stress strain curves.
* **Reliable**: pymechtest uses battle-tested libraries like [pandas], [numpy] and [altair] to do most of the work. The API is really a domain-specific convenience wrapper. pymechtest also maintains high test coverage.

## Installation

```shell
pip install pymechtest
```

I also plan to make a conda package for this, once I've learned how to do it!

[altair]: https://altair-viz.github.io
[pandas]: https://pandas.pydata.org
[numpy]: https://numpy.org
