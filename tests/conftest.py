import sys
import os


def pytest_sessionstart(session):
    sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
