#!/usr/bin/env python3

import os
import aws_cdk as cdk

from step_work_flow.step_work_flow_stack import (
    StepWorkflowStack,
)

app = cdk.App()

StepWorkflowStack(
    app,
    "StepWorkflowStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION"),
    ),
)

app.synth()