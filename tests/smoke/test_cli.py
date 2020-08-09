import os
import subprocess
from time import sleep


def test_cli_suite2p_gui_runs_when_is_called_locally():
    s2p = subprocess.Popen(['python', '-m', 'suite2p'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sleep(10)
    assert s2p.poll() is None  # Make sure process is running
    s2p.terminate()
    output, err = s2p.communicate(b'\n')
    assert "Error" not in err.decode('ascii')
