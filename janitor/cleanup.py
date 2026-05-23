import boto3
import json
import yaml
import argparse
import sys
from datetime import datetime

# LOAD CONFIG
with open("config/settings.yaml", "r") as file:
    config = yaml.safe_load(file)

# ARGUMENTS
parser = argparse.ArgumentParser()

parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Run scan only"
)

parser.add_argument(
    "--delete",
    action="store_true",
    help="Delete orphan resources"
)

args = parser.parse_args()

# REQUIRED TAGS
required_tags = config["required_tags"]

# AWS CONFIG
region = config["aws"]["region"]
endpoint = config["aws"]["endpoint"]

# CLIENTS
session = boto3.session.Session()

s3 = session.client(
    "s3",
    region_name=region,
    endpoint_url=endpoint,
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

ec2 = session.client(
    "ec2",
    region_name=region,
    endpoint_url=endpoint,
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# REPORT STRUCTURE
report = {
    "scan_timestamp": datetime.utcnow().isoformat(),
    "account_id": "000000000000",
    "region": region,
    "summary": {
        "total_orphans": 0,
        "estimated_monthly_waste_usd": 0
    },
    "findings": []
}

markdown_summary = "# DevOps Cost Janitor Report\n\n"

# ------------------------------------
# S3 BUCKET CHECK
# ------------------------------------

print("\nS3 Buckets")
print("----------------")

bucket_response = s3.list_buckets()

for bucket in bucket_response["Buckets"]:

    bucket_name = bucket["Name"]

    print(bucket_name)

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

            finding = {
                "resource_id": bucket_name,
                "resource_type": "s3_bucket",
                "reason": "missing_tags",
                "age_days": 0,
                "estimated_monthly_cost_usd": 5,
                "tags": {},
                "suggested_action": "review",
                "safe_to_auto_delete": False
            }

            report["findings"].append(finding)

    except Exception:
        print(f"Could not read tags for {bucket_name}")

# ------------------------------------
# EBS CHECK
# ------------------------------------

print("\nEBS Volumes")
print("----------------")

volume_response = ec2.describe_volumes()

for volume in volume_response["Volumes"]:

    volume_id = volume["VolumeId"]

    print(volume_id)

    attachments = volume.get("Attachments", [])

    if len(attachments) == 0:

        print(f"{volume_id} is unattached ⚠️")

        tags = volume.get("Tags", [])

        protected = False

        for tag in tags:
            if tag["Key"] == "Protected" and tag["Value"] == "true":
                protected = True

        finding = {
            "resource_id": volume_id,
            "resource_type": "ebs_volume",
            "reason": "unattached",
            "age_days": 10,
            "estimated_monthly_cost_usd": 8,
            "tags": {},
            "suggested_action": "delete",
            "safe_to_auto_delete": not protected
        }

        report["findings"].append(finding)

        # DELETE MODE
        if args.delete and not protected:

            print(f"Deleting {volume_id}")

            try:
                ec2.delete_volume(
                    VolumeId=volume_id
                )

            except Exception as error:
                print(error)

# ------------------------------------
# STOPPED EC2 CHECK
# ------------------------------------

print("\nEC2 Instances")
print("----------------")

instance_response = ec2.describe_instances()

for reservation in instance_response["Reservations"]:

    for instance in reservation["Instances"]:

        instance_id = instance["InstanceId"]

        state = instance["State"]["Name"]

        print(f"{instance_id} -> {state}")

        if state == "stopped":

            finding = {
                "resource_id": instance_id,
                "resource_type": "ec2_instance",
                "reason": "stopped_instance",
                "age_days": 20,
                "estimated_monthly_cost_usd": 15,
                "tags": {},
                "suggested_action": "terminate",
                "safe_to_auto_delete": False
            }

            report["findings"].append(finding)

# ------------------------------------
# ELASTIC IP CHECK
# ------------------------------------

print("\nElastic IPs")
print("----------------")

try:

    eip_response = ec2.describe_addresses()

    for address in eip_response["Addresses"]:

        allocation_id = address.get(
            "AllocationId",
            "unknown"
        )

        if "InstanceId" not in address:

            print(f"{allocation_id} is unused")

            finding = {
                "resource_id": allocation_id,
                "resource_type": "elastic_ip",
                "reason": "unused_eip",
                "age_days": 5,
                "estimated_monthly_cost_usd": 3,
                "tags": {},
                "suggested_action": "release",
                "safe_to_auto_delete": True
            }

            report["findings"].append(finding)

except Exception:
    print("No Elastic IPs found")

# ------------------------------------
# SUMMARY
# ------------------------------------

total_cost = 0

for finding in report["findings"]:
    total_cost += finding["estimated_monthly_cost_usd"]

report["summary"]["total_orphans"] = len(
    report["findings"]
)

report["summary"][
    "estimated_monthly_waste_usd"
] = total_cost

# ------------------------------------
# SAVE JSON REPORT
# ------------------------------------

with open(
    "reports/report.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        report,
        file,
        indent=4
    )

# ------------------------------------
# MARKDOWN REPORT
# ------------------------------------

markdown_summary += f"""
## Summary

Total Orphans: {report['summary']['total_orphans']}

Estimated Monthly Waste: ${total_cost}

---

## Findings

"""

for finding in report["findings"]:

    markdown_summary += f"""
### {finding['resource_id']}

- Type: {finding['resource_type']}
- Reason: {finding['reason']}
- Suggested Action: {finding['suggested_action']}
- Monthly Cost: ${finding['estimated_monthly_cost_usd']}

"""

with open(
    "reports/report.md",
    "w",
    encoding="utf-8"
) as file:

    file.write(markdown_summary)

# ------------------------------------
# EXIT CODE
# ------------------------------------

if args.dry_run and len(report["findings"]) > 0:

    print("\nOrphans detected ⚠️")

    sys.exit(1)

print("\nScan completed successfully ✅")