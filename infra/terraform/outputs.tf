output "droplet_ip" {
  description = "Droplet IP address"
  value       = digitalocean_droplet.main.ipv4_address
}

output "domain" {
  description = "Full domain"
  value       = "${var.subdomain}.${var.domain}"
}

output "ssh_command" {
  description = "SSH command to connect"
  value       = "ssh root@${digitalocean_droplet.main.ipv4_address}"
}