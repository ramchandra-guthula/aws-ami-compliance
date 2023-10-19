# aws-ami-compliance
## About
Script used to scan the AMI's which are used with instances and notify the team if the AMI is older than 30 days old to
mitigate the security issues as per the AMI compliance process

## Pre-requisites
- Create an IAM role to have permissions to scan AMI and configure CLI
- Create SNS topic and subscribe to the topic to get an emails

## How to run
```python aws_client_conf.py```

[WIP]
- Create Cloudformation or Terraform template to automate the deployment
- Create Flow chart to explain the script and deployment architecture
- Improve the code with unit testcase either pytest or unittest
