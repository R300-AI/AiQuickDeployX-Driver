apt update -y && apt upgrade -y
apt install curl wget gnupg2 -y
source /etc/os-release
sh -c "echo 'deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /' > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list"
wget --no-check-certificate -nv https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable/xUbuntu_${VERSION_ID}/Release.key -O- | apt-key add -
apt update --fix-missing
apt update -qq -y
apt upgrade -y
apt -qq --yes install podman
alias docker="podman --storage-opt mount_program=/usr/bin/fuse-overlayfs"