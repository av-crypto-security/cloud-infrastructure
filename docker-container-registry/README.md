# Docker Image and Container Registry (Yandex Cloud)

This repository demonstrates building a Docker image,
publishing it to Yandex Container Registry,
and running a virtual machine based on a container image.

The lab shows how containers can be used
to deliver preconfigured software as an immutable artifact
without manual installation on virtual machines.

---

## What is implemented

- Docker image with NGINX
- Private Container Registry in Yandex Cloud
- Image push and pull via authenticated registry access
- Virtual machine launched from a container image
- No manual configuration inside the VM

---

## Architecture
```
Dockerfile
↓
Docker Image
↓
Yandex Container Registry
↓
Container Optimized VM
↓
NGINX running on VM
```


---

## Key concepts demonstrated

- Docker image vs container
- Immutable infrastructure
- Container registry as an artifact store
- Separation of build and runtime environments
- Image-based VM provisioning
- Reproducible infrastructure components

---

## Why containers here

This approach removes the need to:
- SSH into virtual machines
- Manually install software
- Maintain mutable VM state

Instead, the application and its environment
are delivered as a single immutable image,
which improves reproducibility and reliability.

---

## Result

A virtual machine is started directly from a Docker image,
and NGINX becomes available immediately after VM startup.

![NGINX running](./nginx-running.png)

---

## Notes

- All commands used to build and publish the image
  are documented in `commands.md`
- The same image can later be reused in:
  - Kubernetes
  - Instance Groups
  - CI/CD pipelines
