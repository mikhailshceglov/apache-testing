import os
import time
import paramiko
import pytest
from utils import run_cmd

HOST = os.environ.get('TARGET_HOST', 'target')
USER = os.environ.get('TARGET_USER', 'root')
PASSWORD = os.environ.get('TARGET_PASS', 'rootpass')
SSH_PORT = int(os.environ.get('TARGET_SSH_PORT', '22'))

@pytest.fixture(scope="module")
def ssh_client():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for _ in range(10):
        try:
            client.connect(HOST, username=USER, password=PASSWORD, port=SSH_PORT, timeout=3)
            break
        except Exception:
            time.sleep(3)
    else:
        pytest.skip("Unable to connect to target via SSH")
    yield client
    client.close()

