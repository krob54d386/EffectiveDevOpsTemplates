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
                        "8080"
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
        "InstanceProfile": {
            "Properties": {
                "Path": "/",
                "Roles": [
                    {
                        "Ref": "Role"
                    }
                ]
            },
            "Type": "AWS::IAM::InstanceProfile"
        },
        "Role": {
            "Properties": {
                "AssumeRolePolicyDocument": {
                    "Statement": [
                        {
                            "Action": [
                                "sts:AssumeRole"
                            ],
                            "Effect": "Allow",
                            "Principal": {
                                "Service": [
                                    "ec2.amazonaws.com"
                                ]
                            }
                        }
                    ]
                }
            },
            "Type": "AWS::IAM::Role"
        },
        "SecurityGroup": {
            "Properties": {
                "GroupDescription": "Allow SSH and TCP/8080 access",
                "SecurityGroupIngress": [
                    {
                        "CidrIp": "199.115.98.234/32",
                        "FromPort": "22",
                        "IpProtocol": "tcp",
                        "ToPort": "22"
                    },
                    {
                        "CidrIp": "0.0.0.0/0",
                        "FromPort": "8080",
                        "IpProtocol": "tcp",
                        "ToPort": "8080"
                    }
                ]
            },
            "Type": "AWS::EC2::SecurityGroup"
        },
        "instance": {
            "Properties": {
                "IamInstanceProfile": {
                    "Ref": "InstanceProfile"
                },
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
                                "/usr/local/bin/ansible-pull -U https://github.com/krob54d386/ansible jenkins.yml -i localhost",
                                "echo '*/10 * * * * /usr/local/bin/ansible-pull -U https://github.com/krob54d386/ansible jenkins.yml -i localhost' > /etc/cron.d/ansible-pull"
                            ]
                        ]
                    }
                }
            },
            "Type": "AWS::EC2::Instance"
        }
    }
}
