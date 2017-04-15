# !/bin/bash
# Author: yzhao@redhat.com

# ova_version = "rhvm-appliance-4.1.20170221.0-1.el7ev.4.1.rpm"

# Clean up the nfs storage
rm -rf /home/zyh/nfs1/*

# Confirm nfs service start
service nfs start

# Delete the known_hosts
rm -rf /root/.ssh/known_hosts

# Upload the ova file
# scp /home/zyh/Downloads/$(ova_version) root@10.73.131.65:/opt
