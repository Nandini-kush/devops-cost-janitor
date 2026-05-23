output "bucket_name" {
  value = aws_s3_bucket.bucket.bucket
}

output "ebs_volume_id" {
  value = aws_ebs_volume.ebs.id
}