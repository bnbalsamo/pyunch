from setuptools import setup, find_packages


def readme():
    with open("README.md", 'r') as f:
        return f.read()


setup(
    name="pyunch",
    description="A process launcher",
    version="0.2.0",
    long_description=readme(),
    author="Brian Balsamo",
    author_email="brian@brianbalsamo.com",
    packages=find_packages(
        exclude=[
        ]
    ),
    include_package_data=True,
    url='https://github.com/bnbalsamo/pyunch',
    entry_points={
        'console_scripts': [
            'pyunch = pyunch:main',
            'pyunch-index = pyunch:index_paths'
        ]
    },
    install_requires=[
    ],
    tests_require=[
        'pytest'
    ],
    test_suite='tests'
)
