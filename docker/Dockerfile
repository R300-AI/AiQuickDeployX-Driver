FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

COPY ../Xdriver /workspace/Xdriver
ENV DEBIAN_FRONTEND=noninteractive 
#RUN /bin/bash -c '/workspace/Xdriver/setup.sh'
#RUN apt-get -y update
#RUN apt-get -y install git
#RUN pip install -r /workspace/Xdriver/requirements.txt
ENV docker="podman --storage-opt mount_program=/usr/bin/fuse-overlayfs"
EXPOSE 3000
EXPOSE 5000

CMD ["/bin/bash"]
