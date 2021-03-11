import subprocess
import os


def test_texfile():
    subprocess.check_output(["make"], cwd="latex")
    assert os.path.exists(os.path.join("latex", "ms.pdf"))
