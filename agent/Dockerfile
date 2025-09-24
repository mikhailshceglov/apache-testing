FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    openssh-client curl \
 && rm -rf /var/lib/apt/lists/*

# Создаём виртуальное окружение
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

RUN pip install --no-cache-dir pytest paramiko allure-pytest
RUN mkdir -p /reports/allure-results

COPY tests /tests
WORKDIR /tests

CMD ["pytest", "-v", "--alluredir=/reports/allure-results"]
