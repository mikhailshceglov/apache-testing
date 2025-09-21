FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y apache2 openssh-server curl tar && rm -rf /var/lib/apt/lists/*

RUN echo "root:rootpass" | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

RUN mkdir -p /var/run/sshd

RUN echo 'Hello from Apache container!! :3' > /var/www/html/index.html && \
    cp /var/www/html/index.html /var/www/html/index

EXPOSE 80 22

# Copy entrypoint script and set execute permission
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

