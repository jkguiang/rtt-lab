FROM rootproject/root:6.22.02-centos7

# Install basic packages
RUN yum update -y && yum install -y \
    curl \
    iproute2 \
    python3 \
    xrootd-client

# Install conda
RUN curl -O -L https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b && rm Miniconda3-latest-Linux-x86_64.sh
# Set temporary env variable to make our lives easier
ENV CONDA=/root/miniconda3/bin/conda
# conda will be on $PATH when you log in
RUN $CONDA init
# Configure conda
RUN $CONDA config --set auto_activate_base false && $CONDA config --add channels conda-forge
# Set up an environment
RUN $CONDA create --name rtt-env -y && \
    $CONDA install -n rtt-env -y uproot xrootd awkward numba pandas

WORKDIR /home
