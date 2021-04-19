FROM rootproject/root
EXPOSE 80

# Install basic packages
RUN apt-get update -y && apt-get install -y \
    curl \
    iproute2 \
    python3 \
    python3-pip

WORKDIR /home
