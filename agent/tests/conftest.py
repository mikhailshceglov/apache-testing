import os
import time
import paramiko
import pytest

HOST = os.environ.get('TARGET_HOST', 'target')
USER = os.environ.get('TARGET_USER', 'root')
PASSWORD = os.environ.get('TARGET_PASS', 'rootpass')
SSH_PORT = int(os.environ.get('TARGET_SSH_PORT', '22'))

@pytest.fixture(scope="module")
def ssh_client():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    last_err = None
    for i in range(10):  
        try:
            client.connect(
                HOST,
                port=SSH_PORT,
                username=USER,
                password=PASSWORD,
                look_for_keys=False,
                allow_agent=False,
                timeout=5,
            )
            break
        except Exception as e:
            last_err = e
            time.sleep(3)
    else:
        pytest.skip(f"Unable connect to target: {last_err}")

    yield client
    client.close()

@pytest.fixture
def run_cmd(ssh_client):
    def _run(command: str):
        stdin, stdout, stderr = ssh_client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        out = stdout.read().decode()
        err = stderr.read().decode()
        return exit_status, out, err
    return _run
