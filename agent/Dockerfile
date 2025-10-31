FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-client \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /tests

COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r /tmp/requirements.txt

COPY tests /tests

CMD ["pytest", "-v", "--alluredir=/reports/allure-results"]
