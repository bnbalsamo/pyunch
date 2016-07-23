from setuptools import setup
from setuptools import find_packages

setup(
    name = "pyunch",
    description = "A minimalistic application launcher.",
    author = "Brian Balsamo",
    packages = find_packages(),
    entry_points = {
        'console_scripts':[
            'pyunch = pyunch.pyunch:main'
        ]
    }
)
