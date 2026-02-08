# Docker Image and Yandex Container Registry

This is to demonstrate how to build a Docker image,
push it to Yandex Container Registry,
and run a virtual machine using a container-based image.

The goal is to show how containers allow delivering
preconfigured software without manual installation
inside virtual machines.

---

## Prerequisites

- Ubuntu Linux host
- Yandex Cloud account
- `yc` CLI configured
- Docker Engine installed

---

## 1. Install Docker Engine

Official Docker installation guide:
https://docs.docker.com/engine/install/ubuntu/

Short version:

```bash
sudo apt remove docker docker-engine docker.io containerd runc
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" \
| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
sudo systemctl enable docker
sudo systemctl start docker

