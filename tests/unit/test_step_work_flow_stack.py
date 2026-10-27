import aws_cdk as cdk
from aws_cdk.assertions import Template

from step_work_flow.step_work_flow_stack import StepWorkflowStack


def create_template():
    app = cdk.App()
    stack = StepWorkflowStack(app, "TestStack")

    return Template.from_stack(stack)


def test_stack_creates_lambda():
    template = create_template()

    template.resource_count_is(
        "AWS::Lambda::Function",
        1,
    )


def test_stack_creates_state_machine():
    template = create_template()

    template.resource_count_is(
        "AWS::StepFunctions::StateMachine",
        1,
    )


def test_lambda_configuration():
    template = create_template()

    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Runtime": "python3.12",
            "Handler": "app.handler",
        },
    )


def test_state_machine_type():
    template = create_template()

    template.has_resource_properties(
        "AWS::StepFunctions::StateMachine",
        {
            "StateMachineType": "STANDARD",
        },
    )