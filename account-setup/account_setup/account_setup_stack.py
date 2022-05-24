from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
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

class AccountSetupStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpc = ec2.Vpc(self, "db_vpc", cidr="10.0.0.0/16", max_azs=2)

        #create a bucket
        bucket = s3.Bucket(self, "MyFirstBucket",
                           auto_delete_objects=True,
                           removal_policy=aws_cdk.RemovalPolicy.DESTROY,
                           versioned=False)

        #RDS setup
        db_sg = ec2.SecurityGroup(self,
                                  "db_sg", vpc=vpc, allow_all_outbound=True)
        db_sg.add_ingress_rule(peer=ec2.Peer.any_ipv4(),
                               connection=ec2.Port.tcp(3306),
                               description="allow inbound mysql connections")
        db = rds.DatabaseInstance(self, "example_db",
                                  engine=rds.DatabaseInstanceEngine.mysql(
                                      version=rds.MysqlEngineVersion.VER_8_0_28),
                                  vpc=vpc,
                                  vpc_subnets=ec2.SubnetSelection(
                                      subnet_type=ec2.SubnetType.PUBLIC
                                  ),
                                  publicly_accessible=True,
                                  security_groups=[db_sg])

        #find existing source bucket (to share)
        bucket_source = s3.Bucket.from_bucket_name(self,
                                                   "source_bucket",
                                                   "bigid-devday-public-training-dataset")

        #copy data from source bucket to new bucket
        deploy_prefix = "landing"
        db_name_in_zip = "rockstream/rockstream.sql"
        s3deploy.BucketDeployment(self, "DeployDataset",
                                  sources=[
                                      s3deploy.Source.bucket(bucket_source,
                                                             "rockstream-20220511T083415Z-001.zip"),
                                      s3deploy.Source.asset('./assets')],
                                  destination_bucket=bucket,
                                  retain_on_delete=False,
                                  destination_key_prefix=deploy_prefix)
        #declare dynamodb
        table = dynamodb.Table(self, "Table",
                               removal_policy=aws_cdk.RemovalPolicy.DESTROY,
                               partition_key=dynamodb.Attribute(name="UserID",
                                                                type=dynamodb.AttributeType.STRING))

        build_spec = codebuild.BuildSpec.from_object({
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
                    "commands": [
                        "mysql -u admin -e 'DROP DATABASE rockstream;' 2>/dev/null || echo 'db was not there'",
                        "mysql -u admin -e 'create database rockstream character set UTF8mb4 collate utf8mb4_bin;'",
                        "mysql -u $MYSQL_USER < " + db_name_in_zip,
                        "python import-to-dynamo.py rockstream-usersUS.csv " + table.table_name
                    ]
                }
            }
        })

        data_import = codebuild.Project(self, "import-db-from-s3",
                                     source=codebuild.Source.s3(
                                         bucket=bucket, path=deploy_prefix + '/'),
                                     environment=codebuild.BuildEnvironment(
                                         build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
                                         environment_variables={
                                             "MYSQL_HOST": codebuild.BuildEnvironmentVariable(
                                                 value=db.db_instance_endpoint_address
                                             ),
                                             "MYSQL_TCP_PORT": codebuild.BuildEnvironmentVariable(
                                                 value=db.db_instance_endpoint_port
                                             ),
                                             "MYSQL_USER": codebuild.BuildEnvironmentVariable(
                                                 type=codebuild.BuildEnvironmentVariableType.SECRETS_MANAGER,
                                                 value=db.secret.secret_full_arn + ":username"
                                             ),
                                             "MYSQL_PWD": codebuild.BuildEnvironmentVariable(
                                                 type=codebuild.BuildEnvironmentVariableType.SECRETS_MANAGER,
                                                 value=db.secret.secret_full_arn + ":password"
                                             )
                                         }
                                     ),
                                     build_spec=build_spec)
        bucket.grant_read(data_import)
        table.grant_read_write_data(data_import)
        trigger_build = cr.AwsSdkCall(service="CodeBuild",
                                      action="startBuild",
                                      parameters={
                                          "projectName": data_import.project_name
                                      },
                                      physical_resource_id=cr.PhysicalResourceId.from_response('build.arn'))

        cr.AwsCustomResource(self, "trigger-codebuild-import-db",
                             policy=cr.AwsCustomResourcePolicy.from_sdk_calls(
                                 resources=cr.AwsCustomResourcePolicy.ANY_RESOURCE),
                             on_create=trigger_build,
                             on_update=trigger_build)
