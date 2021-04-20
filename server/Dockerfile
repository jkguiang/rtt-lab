FROM opensciencegrid/software-base:fresh
EXPOSE 1094

# Install basic packages
RUN yum update -y && yum install -y \
    osg-xrootd-standalone

# Upload data
COPY inputs /data

# Update XRootD configurations
COPY xrootd.cfg /etc/xrootd/xrootd.cfg
COPY supervisor.conf /etc/supervisord.d/supervisor.conf
