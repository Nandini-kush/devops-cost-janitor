output "vpc_id" {
  value = module.network.vpc_id
}

output "subnet1_id" {
  value = module.network.subnet1_id
}

output "subnet2_id" {
  value = module.network.subnet2_id
}

output "web1_id" {
  value = module.compute.web1_id
}

output "web2_id" {
  value = module.compute.web2_id
}