from aws_client_conf import aws_client
from datetime import datetime, timedelta


def how_old_is_ami(ami_date: str):
    split_date: list = ami_date.split(":")
    grab_ami_date: datetime = datetime.strptime(split_date[0], '%Y-%m-%dT%H')
    ami_days = datetime.today() - grab_ami_date
    return ami_days


class AmiCompliance:
    def __init__(self):
        self.ec2_client = aws_client('ap-south-1', 'ec2')
        self.sns_client = aws_client('ap-south-1', 'sns')

    def find_instance_ami(self):
        instances = dict()
        response = self.ec2_client.describe_instances()
        for _i in response['Reservations']:
            for _instances in _i['Instances']:
                instance_id = _instances['InstanceId']
                image_id = _instances['ImageId']
                instances[instance_id] = image_id
        print(instances)
        return instances

    def describe_ami(self):
        ami_details = []
        for key, value in self.find_instance_ami().items():
            ami_info = dict()
            response = self.ec2_client.describe_images(ImageIds=[value])
            create_date = response['Images']
            ami_info['ami_id'] = value
            ami_info['create_date'] = create_date[0]['CreationDate']
            ami_info['instance_id'] = key
            ami_details.append(ami_info)
        return ami_details

    def publish_email_via_sns(self):
        ami_info = self.describe_ami()
        for _instance in ami_info:
            print(f"Scanning through instance: {_instance['instance_id']}")
            get_ami_creation_days = how_old_is_ami(_instance['create_date'])
            if get_ami_creation_days > timedelta(days=30):
                print(f"AMI was creates- {get_ami_creation_days.days} ago and its older then 30 days, please do update")
                topic_arn = "arn:aws:sns:ap-south-1:014198614797:AWS_AMI_compliance_alerts"
                msg = """
                    ------------------------------------------------------------------------------------
                                                AMI Compliance scan
                    ------------------------------------------------------------------------------------
                    Summary of the process:
                    ------------------------------------------------------------------------------------
                    Instance ID             :   {instance_id}
                    Image ID                :   {ami}
                    Creation Date           :   {date}
                    Number of days old      :   {ami_days}
                    Status                  :   Need to update the AMI
                    ------------------------------------------------------------------------------------
                
                """.format(
                    instance_id=_instance['instance_id'],
                    ami=_instance['ami_id'],
                    date=_instance['create_date'],
                    ami_days=get_ami_creation_days.days
                )

                response = self.sns_client.publish(
                    TopicArn=topic_arn,
                    Message=msg,
                    Subject="/!\\ AWS AMI compliance Engine /!\\"
                )
                return response


val = AmiCompliance()
val.publish_email_via_sns()
