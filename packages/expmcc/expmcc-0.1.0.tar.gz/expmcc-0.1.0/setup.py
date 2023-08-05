from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name="expmcc",
    description="EXPand the Macro when compiling C/C++ files",
    version=(here / "VERSION").read_text(encoding="utf-8"),
    url="https://github.com/xieby1/expm",
    author="xieby1",
    author_email="xieby1@outlook.com",
    keywords="c/c++, compiler, macro expansion",
    scripts=[
        "expm",
        "expmcc",
        "expmxx",
    ],
)
