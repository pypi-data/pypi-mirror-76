from setuptools import setup
import os


package_path = os.path.abspath(os.path.dirname(__file__))
init_path = package_path + "/wes/__init__.py"
with open(init_path, "r") as f:
    version = f.readline().split("=")[1].strip().strip('"')

setup(
    name="wes",
    version="0.1.7",
    description="Use Wes Anderson Color Palettes in Matplotlib & Seaborn",
    url="https://github.com/ljwolf/wampl",
    author="Levi John Wolf",
    author_email="levi.john.wolf@gmail.com",
    license="CC-BY-SA",
    packages=["wes"],
    install_requires=["matplotlib"],
    include_package_data=True,
    zip_safe=False,
)
