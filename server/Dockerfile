FROM opensciencegrid/software-base:fresh
EXPOSE 1094

# Install basic packages
RUN yum update -y && yum install -y \
    osg-xrootd-standalone \
    tcpdump

# Make directory for data
RUN mkdir /data

# Update XRootD configurations
COPY xrootd.cfg /etc/xrootd/xrootd.cfg
COPY supervisor.conf /etc/supervisord.d/supervisor.conf
