FROM python:3.10-slim

# Install required system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        make \
        pkg-config \
        clang \
        g++ \
        libtool \
        libprotobuf-dev \
        protobuf-compiler \
        curl \
        libcap-dev \
        libseccomp-dev \
        zlib1g-dev \
        bison \
        flex \
        libnl-3-dev \
        libnl-route-3-dev \
    && rm -rf /var/lib/apt/lists/*



# Set workdir and copy files
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install nsjail
RUN git clone https://github.com/google/nsjail /opt/nsjail && \
    cd /opt/nsjail && make && cp nsjail /usr/bin/nsjail
ENV USE_NSJAIL=1

EXPOSE 8080
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
