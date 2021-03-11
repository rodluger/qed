import sys
import os
import shutil


def pytest_sessionstart(session):
    sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
