# Commands — Docker Image and Container Registry

## Docker installation (Ubuntu)

Follow official Docker Engine installation guide:
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

sudo usermod -aG docker $USER
newgrp docker

docker run hello-world
```
---

## Create container registry
```bash
yc container registry create --name my-registry
```

## Authenticate Docker to Yandex Container Registry
This allows Docker to push images to your private registry.
```bash
yc container registry configure-docker
```

## Build the Docker Image
```bash
docker build . -t cr.yandex/<REGISTRY_ID>/ubuntu-nginx:latest
```

## Push the Image to the Registry
```bash
docker push cr.yandex/<REGISTRY_ID>/ubuntu-nginx:latest
```

## Grant Pull Access
In Yandex Cloud Console:
Open your Container Registry
Go to Access bindings
Grant roles:
viewer
container-registry.images.puller
Assign them to All users
This allows virtual machines to pull images from the registry.

## Run a VM Using the Container Image
Create a new virtual machine
Choose Container Optimized Image
Select the image from your registry:
```bash
cr.yandex/<REGISTRY_ID>/ubuntu-nginx:latest
```
Leave other settings default and create the VM

## Verify Result
Once the VM is running:
Find its public IP address
Open it in a browser
You should see the NGINX welcome page

## Result
Using a Docker image, we deployed a virtual machine
with preinstalled and configured software
without manually connecting to the VM.
This demonstrates the core benefit of containers:
packaging application and environment together
into a reusable, immutable artifact.
