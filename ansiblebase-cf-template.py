{
    "Description": "Effective DevOps in AWS: HelloWorld web application",
    "Outputs": {
        "InstancePublicIp": {
            "Description": "Public IP of our instance.",
            "Value": {
                "Fn::GetAtt": [
                    "instance",
                    "PublicIp"
                ]
            }
        },
        "WebUrl": {
            "Description": "Application endpoint",
            "Value": {
                "Fn::Join": [
                    "",
                    [
                        "http://",
                        {
                            "Fn::GetAtt": [
                                "instance",
                                "PublicDnsName"
                            ]
                        },
                        ":",
                        "3000"
                    ]
                ]
            }
        }
    },
    "Parameters": {
        "KeyPair": {
            "ConstraintDescription": "must be the name of an existing EC2 KeyPair.",
            "Description": "Name of an existing EC2 KeyPair to SSH",
            "Type": "AWS::EC2::KeyPair::KeyName"
        }
    },
    "Resources": {
        "SecurityGroup": {
            "Properties": {
                "GroupDescription": "Allow SSH and TCP/3000 access",
                "SecurityGroupIngress": [
                    {
                        "CidrIp": "174.128.226.2/32",
                        "FromPort": "22",
                        "IpProtocol": "tcp",
                        "ToPort": "22"
                    },
                    {
                        "CidrIp": "0.0.0.0/0",
                        "FromPort": "3000",
                        "IpProtocol": "tcp",
                        "ToPort": "3000"
                    }
                ]
            },
            "Type": "AWS::EC2::SecurityGroup"
        },
        "instance": {
            "Properties": {
                "ImageId": "ami-098bb5d92c8886ca1",
                "InstanceType": "t2.micro",
                "KeyName": {
                    "Ref": "KeyPair"
                },
                "SecurityGroups": [
                    {
                        "Ref": "SecurityGroup"
                    }
                ],
                "UserData": {
                    "Fn::Base64": {
                        "Fn::Join": [
                            "\n",
                            [
                                "#!/bin/bash",
                                "yum install --enablerepo=epel -y git",
                                "pip install ansible",
                                "/usr/local/bin/ansible-pull -U https://github.com/EffectiveDevOpsWithAWS/ansible helloworld.yml -i localhost",
                                "echo '*/10 * * * * /usr/local/bin/ansible-pull -U https://github.com/EffectiveDevOpsWithAWS/ansible helloworld.yml -i localhost' > /etc/cron.d/ansible-pull"
                            ]
                        ]
                    }
                }
            },
            "Type": "AWS::EC2::Instance"
        }
    }
}
