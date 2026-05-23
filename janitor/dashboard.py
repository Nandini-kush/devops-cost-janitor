import json

# LOAD REPORT
with open("reports/scan_report.json", "r") as file:
    report = json.load(file)

# CREATE HTML
html_content = f"""
<html>

<head>
    <title>DevOps Cost Janitor Report</title>

    <style>

        body {{
            font-family: Arial;
            margin: 40px;
            background-color: #f4f4f4;
        }}

        h1 {{
            color: #333;
        }}

        .card {{
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        table, th, td {{
            border: 1px solid gray;
        }}

        th, td {{
            padding: 10px;
            text-align: left;
        }}

    </style>

</head>

<body>

    <h1>DevOps Cost Janitor Dashboard 🚀</h1>

    <div class="card">
        <h2>Scan Time</h2>
        <p>{report["scan_time"]}</p>
    </div>

    <div class="card">
        <h2>S3 Buckets</h2>
        <ul>
"""

# ADD BUCKETS
for bucket in report["buckets"]:
    html_content += f"<li>{bucket}</li>"

html_content += """
        </ul>
    </div>

    <div class="card">
        <h2>EBS Volumes</h2>
        <ul>
"""

# ADD VOLUMES
for volume in report["volumes"]:
    html_content += f"<li>{volume}</li>"

html_content += """
        </ul>
    </div>

    <div class="card">
        <h2>Detected Issues</h2>

        <table>
            <tr>
                <th>Resource</th>
                <th>Issue</th>
            </tr>
"""

# ADD ISSUES
for issue in report["issues"]:

    resource = issue.get("resource", "Unknown")
    problem = issue.get("issue", "Missing Tags")

    html_content += f"""
        <tr>
            <td>{resource}</td>
            <td>{problem}</td>
        </tr>
    """

html_content += """

        </table>

    </div>

</body>
</html>
"""

# SAVE HTML FILE
with open("reports/dashboard.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("Dashboard generated: reports/dashboard.html ✅")