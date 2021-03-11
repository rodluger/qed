import sys
import os
import shutil


def pytest_sessionstart(session):
    sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    shutil.copyfile(
        os.path.join(ROOT, "qed.sty"),
        os.path.join(ROOT, "tests", "latex", "qed.sty"),
    )
