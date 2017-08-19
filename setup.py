from setuptools import setup, find_packages


requires = open("requirements.txt").read().split("\n")

setup(
    name="fxdayu_sinta",
    version="0.1.2",
    packages=find_packages(),
    install_requires=requires,
    entry_points={"console_scripts": ["sinta = fxdayu_sinta.sinta:sinta",
                                      "rqadjust = fxdayu_sinta.adjust.rqadjust:rqadjust"]}
)
