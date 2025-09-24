from datetime import datetime
import pytest
from utils import run_cmd
import allure

@allure.feature("Apache")
@allure.story("Process")
def test_apache_running(ssh_client):
    exit_status, output, error = run_cmd(ssh_client, "pidof apache2")
    assert exit_status == 0, "Apache2 process is not running"
    assert output.strip() != "", "Apache2 process ID not found"

@allure.feature("Apache")
@allure.story("Process")
def test_error_logs(ssh_client):
    exit_status, curr_time_str, _ = run_cmd(ssh_client, "date +%s")
    
    assert exit_status == 0 and curr_time_str.strip().isdigit(), "Failed to get time from target"
    
    curr_time = int(curr_time_str.strip())
    ten_minutes_ago = curr_time - 600
    sftp = ssh_client.open_sftp()
    try:
        log_file = sftp.open('/var/log/apache2/error.log')
        log_lines = log_file.read().decode().splitlines()
    finally:
        log_file.close()
        sftp.close()
    recent_errors = []
    for line in log_lines:
        if 'error' in line.lower():
            try:
                if line.startswith('['):
                    end_idx = line.find(']')
                    date_str = line[1:end_idx]  
                    parts = date_str.split()
                    parts = parts[1:]  
                    parts[3] = parts[3].split('.')[0]
                    date_str_clean = ' '.join(parts)
                    log_time = datetime.strptime(date_str_clean, "%b %d %H:%M:%S %Y")
                    log_timestamp = int(log_time.timestamp())
                else:
                    log_timestamp = 0
            except Exception:
                log_timestamp = 0
            if log_timestamp >= ten_minutes_ago:
                recent_errors.append(line)
    assert not recent_errors, f"Error entries found in Apache logs within last 10 minutes: {recent_errors}"

@allure.feature("Apache")
@allure.story("Process")
def test_index_page(ssh_client):
    i, body, j = run_cmd(ssh_client, "curl -s http://localhost/index")
    i, status_code, j = run_cmd(ssh_client, "curl -s -o /dev/null -w '%{http_code}' http://localhost/index")
    assert status_code.strip() == "200", f"Expected HTTP 200, got {status_code}"
    assert "Hello from Apache container" in body, "Index page content is incorrect or not served"

@allure.feature("Apache")
@allure.story("Process")
def test_404_page(ssh_client):
    i, status_code, j = run_cmd(ssh_client, "curl -s -o /dev/null -w '%{http_code}' http://localhost/nonexistent_page")
    assert status_code.strip() == "404", f"Expected 404 for nonexistent page, got {status_code}"

