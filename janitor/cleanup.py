import boto3
import argparse
import json
import os

# ----------------------------
# ARGUMENT PARSER
# ----------------------------

parser = argparse.ArgumentParser()

parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Preview resources"
)

parser.add_argument(
    "--delete",
    action="store_true",
    help="Delete orphan resources"
)

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

# ----------------------------
# AWS CLIENTS
# ----------------------------

session = boto3.session.Session()

s3 = session.client(
    "s3",
    region_name="us-east-1",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

ec2 = session.client(
    "ec2",
    region_name="us-east-1",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# ----------------------------
# REQUIRED TAGS
# ----------------------------

required_tags = [
    "Project",
    "Environment",
    "Owner",
    "ManagedBy"
]

# ----------------------------
# S3 BUCKETS
# ----------------------------

bucket_response = s3.list_buckets()

print("\nS3 Buckets:")
print("----------------")

bucket_list = []

for bucket in bucket_response["Buckets"]:
    print(bucket["Name"])
    bucket_list.append(bucket["Name"])

# ----------------------------
# TAG VALIDATION
# ----------------------------

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
            print(f"{bucket_name} missing tags: {missing_tags}")
        else:
            print(f"{bucket_name} is properly tagged ✅")

    except Exception:
        print(f"Could not read tags for {bucket_name}")

# ----------------------------
# EBS VOLUMES
# ----------------------------

volume_response = ec2.describe_volumes()

print("\nEBS Volumes:")
print("----------------")

volume_ids = []

for volume in volume_response["Volumes"]:
    print(volume["VolumeId"])
    volume_ids.append(volume["VolumeId"])

# ----------------------------
# ORPHAN DETECTION
# ----------------------------

orphan_volumes = []

if args.detect_orphans:

    print("\nOrphan Volume Detection")
    print("------------------------")

    for volume in volume_response["Volumes"]:

        volume_id = volume["VolumeId"]

        if len(volume["Attachments"]) == 0:
            orphan_volumes.append(volume_id)
            print(f"{volume_id} is unattached ⚠️")
        else:
            print(f"{volume_id} is attached ✅")

# ----------------------------
# CLEANUP SIMULATION
# ----------------------------

print("\nCleanup Simulation")
print("-------------------")

for bucket in bucket_response["Buckets"]:
    print(f"Would inspect bucket: {bucket['Name']}")

for volume in volume_response["Volumes"]:
    print(f"Would inspect EBS volume: {volume['VolumeId']}")

# ----------------------------
# REPORT GENERATION
# ----------------------------

report = {
    "buckets": bucket_list,
    "volumes": volume_ids,
    "orphans": orphan_volumes
}

os.makedirs("reports", exist_ok=True)

with open("reports/scan_report.json", "w") as file:
    json.dump(report, file, indent=4)

# ----------------------------
# FLAGS
# ----------------------------

if args.dry_run:
    print("\nRunning in dry-run mode")

if args.report_only:
    print("\nRunning in report-only mode")

if args.delete:
    print("\nDelete mode enabled")

# ----------------------------
# SUCCESS
# ----------------------------

print("\nCost Janitor scan completed successfully ✅")
print("\nReport generated: reports/scan_report.json ✅")