import json
from pathlib import Path


def load_definition():
    project_root = Path(__file__).resolve().parents[2]

    workflow_path = (
        project_root
        / "statemachines"
        / "workflow.asl.json"
    )

    with workflow_path.open(
        encoding="utf-8"
    ) as file:
        return json.load(file)


def test_start_state_exists():
    definition = load_definition()

    assert definition["StartAt"] in definition["States"]


def test_process_state_is_task():
    definition = load_definition()

    process_state = definition["States"]["Process"]

    assert process_state["Type"] == "Task"
    assert process_state["Resource"] == (
        "arn:aws:states:::lambda:invoke"
    )


def test_lambda_arn_is_parameterized():
    definition = load_definition()

    function_name = (
        definition["States"]["Process"]
        ["Parameters"]["FunctionName"]
    )

    assert function_name == "${ProcessFunctionArn}"