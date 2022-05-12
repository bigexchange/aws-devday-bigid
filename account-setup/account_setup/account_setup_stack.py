from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_rds as rds,
    aws_dynamodb as dynamodb,
    aws_codebuild as codebuild,
    custom_resources as cr,
    aws_s3_deployment as s3deploy
)
import aws_cdk as aws_cdk

from constructs import Construct

URL="https://bigid-devday-public-training-dataset.s3.us-east-1.amazonaws.com/rockstream-20220511T083415Z-001.zip?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFIaCWV1LXdlc3QtMyJGMEQCIGf1IWbiKcqssAxnkwpThJa3Dh552Hs3A7STJqNuiLcFAiAEB4tSvYrwJjyfAW%2FEC1In57%2BFdM4GAYGoglnjXiImNCrmAwgrEAEaDDk1MzgzNDEzNDYzOSIMZmmTJZjL4NQa1EYkKsMDEpeaJAcF1jmtr%2BpuBNpDfooi%2FfEITT4odoQ2cT294Bx56gxADMUR5nA6fgPHxWD6OfO0N7mooQisVl9AuhfIAxczyIyDPOHgSJUb%2FP%2BeLur8JhQJtHStLfopeef4BItUESWdFsDt7x2q4gV5e8Gl0jR%2Bx19%2BU3Xq9HwGOkFdagSh84YGkftHA9t00SgBcDiH0u5zxJsXdWjyN2jL9l2US8WVANTLCmBp7I69JMZVDj51ZOxAzPKIDZRPvAQGp0Y%2B%2B6gacwMxHJdPuCZkSZKjU%2Fl2UAhFuEiR5upRmQUmH0YNVZAVn1NxUeXHFpeuQHRFs064MNB1PCzR4q9w2Vsxc%2Fi6Qbfb90K5%2FQGxIxhR41e9jkDPBDxDCpwDRdwiLOj6A68kdKlvIt11mFrH%2FVu5SWbnKCagVszuKz%2BVIlhkJxQqEOxCLSpti7O4UDKAf08kvJoJnaxAw%2B9cYyUh4vUmepWMDAXDfAKDRWMCXwLW7eUTS2mP8n6ZWVfLoBkt%2FFhwWVFEIEeDaG1qWgyFRk5iKdpeinhXRm8P4Q%2BDMv%2BvJRC16bWJKpW2UKV06yPAFNdzLK9IGFteNBYkDsW38gPU%2BL8wezDKhe6TBjqVAuU%2F59lV4%2B7dV9cYy9la2pna%2FrXLtNuZy%2F2vbBcUstooBFwKG%2By9LFAupb42amc2GhGphObKR%2FQ%2FMhEgScsu26mBTLRsl5VznUtcYX5crbvlvgaGc5keEMJGZFtSDxKxExDvTw4T%2Bylll5cW8BGX1kqdCc9qLhoslGzV9dY1VDUKB4VwY7%2B1Dsy01rnJGWaDk0CgiFf7mjYD6CVygApC4mpC7akBrIAu8FGDeZgT%2FX%2FadbK%2BJtJ4Yxn%2BGbH%2BYyU%2FSnIoV4xdQkmuHpkCdqlKAvNDn7j4TtPW3ZseCflmK%2FdAtNx6hYIc25TjIZSodaDIlPtaovLEbRUTA0uvYnzkOjl61mZYKsVYOz2XerttIn9zQlujjz4%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220511T094833Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA54FHR3RXUDGU2H4F%2F20220511%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=3cf48cde0eb7e175ae2259c09f40d0606c7115ff38cdf2d55e71ed84ad091f66"

class AccountSetupStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpc = ec2.Vpc(self, "db_vpc", cidr="10.0.0.0/16", max_azs=2)

        bucket = s3.Bucket(self, "MyFirstBucket",
                           auto_delete_objects=True,
                           removal_policy=aws_cdk.RemovalPolicy.DESTROY,
                           versioned=False)
        db = rds.DatabaseInstance(self, "example_db",
                                  engine=rds.DatabaseInstanceEngine.mysql(
                                      version=rds.MysqlEngineVersion.VER_8_0_28),
                                  vpc=vpc,
                                  vpc_subnets=ec2.SubnetSelection(
                                      subnet_type=ec2.SubnetType.PUBLIC
                                  ),
                                  publicly_accessible=True,
                                  security_groups=
                                  )
        bucket_source = s3.Bucket.from_bucket_name(self,
                                                   "source_bucket",
                                                   "bigid-devday-public-training-dataset")

        s3deploy.BucketDeployment(self, "DeployDataset",
                                  sources=[s3deploy.Source.bucket(
                                      bucket_source, "rockstream-20220511T083415Z-001.zip")],
                                  destination_bucket=bucket,
                                  retain_on_delete=False,
                                  destination_key_prefix="training-data-import")
        table = dynamodb.Table(self, "Table",
                               removal_policy=aws_cdk.RemovalPolicy.DESTROY,
                               partition_key=dynamodb.Attribute(name="id",
                                                                type=dynamodb.AttributeType.STRING))
        s3import = codebuild.Project(self, "import-db-from-s3",
                                    environment=codebuild.BuildEnvironment(
                                        build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
                                        environment_variables={
                                            "MYSQL_HOST": codebuild.BuildEnvironmentVariable(
                                                value=db.db_instance_endpoint_address
                                            ),
                                            "MYSQL_TCP_PORT": codebuild.BuildEnvironmentVariable(
                                                value=db.db_instance_endpoint_port
                                            )
                                        }
                                    ),
                                     build_spec=codebuild.BuildSpec.from_object({
                                         "version": "0.2",
                                         "phases": {
                                             "install": {
                                                 "commands": [
                                                     "apt-key adv --refresh-keys --keyserver keyserver.ubuntu.com",
                                                     "apt-get update",
                                                     "apt-get install mysql-client -y"
                                                 ]
                                             },
                                             "build": {
                                                 "commands": ["mysql show database "]
                                             }
                                         }
                                     }))
        trigger_build = cr.AwsSdkCall(
                                 service="CodeBuild",
                                 action="startBuild",
                                 parameters= {
                                     "projectName" : s3import.project_name
                                 },
                                 physical_resource_id=cr.PhysicalResourceId.from_response('build.arn'),
                             )

        cr.AwsCustomResource(self, "trigger-codebuild-import-db",
                             policy=cr.AwsCustomResourcePolicy.from_sdk_calls(
                                 resources=cr.AwsCustomResourcePolicy.ANY_RESOURCE,
                             ),
                             on_create=trigger_build,
                             on_update=trigger_build).node.add_dependency(s3import)