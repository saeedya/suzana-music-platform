# Terraform — Music Platform Infrastructure

Provisions DigitalOcean + Cloudflare infrastructure for the music platform.

## What it creates

- DigitalOcean Droplet (Ubuntu 24.04, 2GB RAM, 1 vCPU)
- Firewall (SSH, HTTP, HTTPS)
- SSH Key
- Cloudflare DNS A record

## Prerequisites

- Terraform v1.0+
- DigitalOcean API token
- Cloudflare API token + Zone ID
- SSH key pair

## Setup

```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
```

## Usage

```bash
# Preview changes
terraform plan

# Apply
terraform apply

# Destroy
terraform destroy
```

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `do_token` | DigitalOcean API token | required |
| `cloudflare_api_token` | Cloudflare API token | required |
| `cloudflare_zone_id` | Cloudflare zone ID | required |
| `domain` | Domain name | `s10i.xyz` |
| `subdomain` | Subdomain | `music` |
| `region` | DigitalOcean region | `nyc1` |
| `droplet_size` | Droplet size | `s-1vcpu-2gb` |
| `ssh_public_key_path` | SSH public key path | `~/.ssh/id_rsa.pub` |

## Outputs

| Output | Description |
|--------|-------------|
| `droplet_ip` | Server IP address |
| `domain` | Full domain (music.s10i.xyz) |
| `ssh_command` | SSH connection command |