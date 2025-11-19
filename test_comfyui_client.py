# unit tests for comfyui_client.py

from comfyui_client import ComfyUIClient


# test get_available_workflows method
def test_get_available_workflows(tmp_path):
    client = ComfyUIClient("http://localhost:8188")
    workflow_ids = client.get_available_workflows()
    assert len(workflow_ids) > 1
    assert "basic_api_test" in workflow_ids


# test get_workflow method
def test_get_workflow(tmp_path):
    client = ComfyUIClient("http://localhost:8188")
    workflow_ids = client.get_available_workflows()

    # model parameters
    prompt = "A test prompt"
    width = None
    height = None
    model = None

    for workflow_id in workflow_ids:
        wf_file, wf = client.get_workflow(prompt, width, height, workflow_id, model)
        assert isinstance(wf, dict)
        assert prompt in str(wf)
