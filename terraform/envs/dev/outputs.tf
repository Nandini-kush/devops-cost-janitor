output "vpc_id" {
  value = module.network.vpc_id
}

output "subnet_id" {
  value = module.network.subnet_id
}

output "bucket_name" {
  value = module.storage.bucket_name
}

output "ebs_volume_id" {
  value = module.storage.ebs_volume_id
}