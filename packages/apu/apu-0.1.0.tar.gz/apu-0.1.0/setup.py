#!/usr/bin/env python

"""apu: Antons Python Utilities."""

# Third party
from setuptools import setup

requires_datetime = ["pytz"]
requires_setup = ["GitPython"]
requires_all = (
    requires_datetime
    + requires_setup
)

setup(
    version="0.1.0",
    package_data={"apu": []},
    extras_require={
        "all": requires_all,
        "datetime": requires_datetime,
        "setup": requires_setup,
    },
)