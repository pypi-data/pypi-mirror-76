import datetime
from setuptools import setup, find_packages


def read_requirements():
    with open("requirements.txt") as requirements_file:
        return requirements_file.readlines()


with open("README.rst") as description_file:
    setup(
        name="aiogram_mvc",
        version="0.1.{0}".format(int(datetime.datetime.now().timestamp())),
        description="aiogram MVC framework",
        long_description=description_file.read(),
        packages=find_packages(exclude=["tests"]),
        url="https://git.yurzs.dev/yurzs/aiogram_mvc",
        install_requires=read_requirements(),
    )
