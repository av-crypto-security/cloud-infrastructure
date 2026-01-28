## Network layout

- Cloud network: 10.xxx.0.0/24
- On-prem network: xxx.xxx.0.0/24
- IPSec gateways have public static IPs
- Private instances have no public IPs

## Routing

- Static route from cloud subnet to on-prem CIDR
- Next hop: IPSec gateway internal IP

## Security assumptions

- PSK used for simplicity
- Only required subnets are exposed
- No inbound internet access to private VMs
