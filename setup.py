import os
import sys
from setuptools import find_packages, setup, Command


class antlr(Command):
    """Generate code with antlr4"""

    description = "generate parser code from antlr grammars"
    user_options = []

    def __init__(self, *args):
        self.args = args[0]  # so we can pass it to other classes
        Command.__init__(self, *args)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.environ["QED_BUILD_LATEX_ANTLR"] = "1"
        from qed._build_latex_antlr import build_parser

        if not build_parser():
            sys.exit(-1)


setup(
    name="qed",
    author="Rodrigo Luger",
    author_email="rodluger@gmail.com",
    url="https://github.com/rodluger/qed",
    description="latex math unit tests",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    data_files=["qed/qed.sty", "qed/LaTeX.g4"],
    use_scm_version={
        "write_to": os.path.join("qed", "qed_version.py"),
        "write_to_template": '__version__ = "{version}"\n',
    },
    cmdclass={"antlr": antlr},
    install_requires=[
        "setuptools_scm",
        "sympy>=1.7.1",
        "antlr4-python3-runtime==4.7.2",
    ],
    setup_requires=["setuptools_scm"],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "qed=qed.entry_points:qed",
            "qed-setup=qed.entry_points:qed_setup",
            "qed-clean=qed.entry_points:qed_clean",
        ]
    },
)
