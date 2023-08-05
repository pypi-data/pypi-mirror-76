from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name="expmcc",
    description="EXPand the Macro when compiling C/C++ files",
    version=(here / "expm" / "VERSION").read_text(encoding="utf-8"),
    url="https://github.com/xieby1/expm",
    author="xieby1",
    author_email="xieby1@outlook.com",
    keywords="c/c++, compiler, macro expansion",
    entry_points = {
        'console_scripts':
        [
            "expm-test=expm.commands:test",
            "expm=expm.expm:expm", # expm/expm.py:exmp()
            "expmxx=expm.expm_common:expmxx", # expm/expm_common.py:exmpxx()
            "expmcc=expm.expm_common:expmcc", # expm/expm_common.py:exmpcc()
        ],
    },
    packages=find_packages(include=['expm', 'expm.*']),
    package_data = {
        "expm": [
            "CONFIG",
            "VERSION",
            ]
    },
)
