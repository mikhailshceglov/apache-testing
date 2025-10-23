FROM debian:bookworm-slim

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Создаём виртуальное окружение
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

RUN pip install --no-cache-dir pytest paramiko allure-pytest
RUN mkdir -p /reports/allure-results

COPY tests /tests
WORKDIR /tests

CMD ["pytest", "-v", "--alluredir=/reports/allure-results"]
