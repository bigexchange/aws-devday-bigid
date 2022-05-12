import aws_cdk as core
import aws_cdk.assertions as assertions

from account_setup.account_setup_stack import AccountSetupStack

# example tests. To run these tests, uncomment this file along with the example
# resource in account_setup/account_setup_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AccountSetupStack(app, "account-setup")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
