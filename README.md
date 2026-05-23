# DevOps Cost Janitor 🚀

An automated DevOps cloud governance and cost optimization tool built using:

- Terraform
- Docker
- LocalStack
- Python
- GitHub Actions
- YAML Configuration

---

# Features

## Infrastructure as Code
- Terraform-based AWS infrastructure
- VPC
- Subnets
- EC2
- S3
- EBS

---

## AWS Resource Scanning
- Detect S3 buckets
- Detect EBS volumes
- Analyze infrastructure resources

---

## Governance Checks
- Required tag validation
- Missing tag detection

---

## Cost Optimization
- Detect unattached EBS volumes
- Simulate cleanup workflows

---

## Reporting
- JSON report generation
- HTML dashboard generation
- Logging support

---

## CI/CD
- GitHub Actions workflow
- Automatic validation
- Automated testing

---

## Configuration Management
- YAML-based configuration
- Reusable environments

---

# Project Structure

```bash
devops-assignment/
│
├── terraform/
├── janitor/
├── reports/
├── logs/
├── config/
├── .github/workflows/
```

# Setup Instructions

## Clone Repository

```bash
git clone YOUR_REPO_URL
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start LocalStack

```bash
docker run --rm -d -p 4566:4566 --name localstack localstack/localstack
```

## Run Cleanup Scanner

```bash
python janitor/cleanup.py
```

## Generate Dashboard

```bash
python janitor/dashboard.py
```

# CLI Commands

## Report Only

```bash
python janitor/cleanup.py --report-only
```

## Detect Orphans

```bash
python janitor/cleanup.py --detect-orphans
```

# Screenshots

Add dashboard screenshots here.

# Future Improvements

- Slack alerts
- Email notifications
- Automated cleanup
- Multi-region support
- Advanced analytics

# Author

Nandini Kushwah