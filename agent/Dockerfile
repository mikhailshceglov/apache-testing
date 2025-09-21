FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y python3 python3-pip python3-pytest python3-paramiko openssh-client && rm -rf /var/lib/apt/lists/*

COPY tests /tests

WORKDIR /tests
ENV PYTEST_DISABLE_PLUGIN_AUTOLOAD=1

CMD ["pytest", "-v"]

