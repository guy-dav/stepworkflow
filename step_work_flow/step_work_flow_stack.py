from pathlib import Path

from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    aws_lambda as lambda_,
    aws_stepfunctions as sfn,
)
from constructs import Construct


class StepWorkflowStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs,
    ):
        super().__init__(scope, construct_id, **kwargs)

        project_root = Path(__file__).resolve().parent.parent

        # 1. Create the Lambda function
        process_fn = lambda_.Function(
            self,
            "ProcessFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="app.handler",
            code=lambda_.Code.from_asset(
                str(project_root / "lambdas" / "process")
            ),
            timeout=Duration.seconds(30),
        )

        # 2. Load the ASL definition
        workflow_file = (
            project_root
            / "statemachines"
            / "workflow.asl.json"
        )

        # 3. Create the Step Functions state machine
        state_machine = sfn.StateMachine(
            self,
            "ProcessingWorkflow",
            definition_body=sfn.DefinitionBody.from_file(
                str(workflow_file)
            ),
            definition_substitutions={
                "ProcessFunctionArn": process_fn.function_arn
            },
            state_machine_type=sfn.StateMachineType.STANDARD,
            timeout=Duration.minutes(5),
        )

        # 4. Grant the state machine permission to invoke Lambda
        process_fn.grant_invoke(state_machine.role)

        # 5. Export the state machine ARN
        CfnOutput(
            self,
            "StateMachineArn",
            value=state_machine.state_machine_arn,
        )