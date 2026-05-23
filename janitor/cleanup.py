import boto3
import json
import logging
from datetime import datetime
import yaml
import argparse

with open("config/settings.yaml", "r") as file:
    config = yaml.safe_load(file)

parser = argparse.ArgumentParser()

parser.add_argument(
    "--report-only",
    action="store_true",
    help="Generate report only"
)

parser.add_argument(
    "--detect-orphans",
    action="store_true",
    help="Detect unattached EBS volumes"
)

args = parser.parse_args()

logging.basicConfig(
    filename="logs/janitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# CREATE AWS SESSION
session = boto3.session.Session()

# REQUIRED TAGS
required_tags = config["required_tags"]

report = {
    "scan_time": str(datetime.now()),
    "buckets": [],
    "volumes": [],
    "issues": []
}

# S3 CLIENT
s3 = session.client(
    "s3",
    region_name=config["aws"]["region"],
    endpoint_url=config["aws"]["endpoint"],
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# EC2 CLIENT
ec2 = session.client(
    "ec2",
    region_name=config["aws"]["region"],
    endpoint_url=config["aws"]["endpoint"],
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# =========================
# LIST S3 BUCKETS
# =========================

bucket_response = s3.list_buckets()

print("\nS3 Buckets:")
print("----------------")

for bucket in bucket_response["Buckets"]:
    print(bucket["Name"])
    report["buckets"].append(bucket["Name"])

# =========================
# TAG VALIDATION
# =========================

print("\nTag Validation:")
print("----------------")

for bucket in bucket_response["Buckets"]:

    bucket_name = bucket["Name"]

    try:
        tagging = s3.get_bucket_tagging(
            Bucket=bucket_name
        )

        existing_tags = [
            tag["Key"]
            for tag in tagging["TagSet"]
        ]

        missing_tags = []

        for tag in required_tags:
            if tag not in existing_tags:
                missing_tags.append(tag)

        if missing_tags:
            report["issues"].append({
              "resource": bucket_name,
              "missing_tags": missing_tags
            })
            print(f"{bucket_name} missing tags: {missing_tags}")
        else:
            print(f"{bucket_name} is properly tagged ✅")

    except Exception:
        print(f"Could not read tags for {bucket_name}")

# =========================
# LIST EBS VOLUMES
# =========================

volume_response = ec2.describe_volumes()

print("\nEBS Volumes:")
if args.detect_orphans:
   print("\nOrphan Volume Detection")
   print("------------------------")

   for volume in volume_response["Volumes"]:

     volume_id = volume["VolumeId"]

     attachments = volume.get("Attachments", [])

     if len(attachments) == 0:

        print(f"{volume_id} is unattached ⚠️")

        report["issues"].append({
            "resource": volume_id,
            "issue": "Unattached EBS Volume"
        })

     else:
        print(f"{volume_id} is attached ✅")
    
print("----------------")

for volume in volume_response["Volumes"]:
    print(volume["VolumeId"])
    report["volumes"].append(volume["VolumeId"])

# =========================
# CLEANUP SIMULATION
# =========================

print("\nCleanup Simulation")
print("-------------------")

for bucket in bucket_response["Buckets"]:
    print(f"Would inspect bucket: {bucket['Name']}")

for volume in volume_response["Volumes"]:
    print(f"Would inspect EBS volume: {volume['VolumeId']}")

if args.report_only:
    print("\nRunning in report-only mode")
print("\nCost Janitor scan completed successfully ✅")
logging.info("Cost Janitor scan completed successfully")

with open("reports/scan_report.json", "w") as file:
    json.dump(report, file, indent=4)

print("\nReport generated: reports/scan_report.json ✅")