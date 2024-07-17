import subprocess
import pytest
import time
from tests import APP_FILE


@pytest.fixture(scope="module")
def start_app():
    cmd = f"python {APP_FILE}"
    process = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(5)
    yield process
    process.terminate()
    process.wait()


def test_streamlit(subtests, start_app):
    with subtests.test(msg="server up"):
        assert start_app.poll() is None, "app failed to start"

    with subtests.test(msg="streamlit down"):
        start_app.terminate()
        time.sleep(2)
        assert start_app.poll() is not None, "app failed to stop"

