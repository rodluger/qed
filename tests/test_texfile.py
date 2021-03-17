import subprocess
import os


def test_texfile():
    cwd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "latex")
    subprocess.check_output(["make"], cwd=cwd)
    # TODO: Check that the equations were verified correctly
    assert os.path.exists(os.path.join(cwd, "ms.pdf"))
