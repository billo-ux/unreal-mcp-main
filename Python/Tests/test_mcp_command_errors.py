import pytest
import requests

# Adjust this URL if your MCP server runs on a different port
MCP_SERVER_URL = "http://localhost:8000"

@pytest.mark.parametrize("payload,expected_error", [
    ({"component_name": "CubeMesh", "property_name": "Mobility", "property_value": "Movable"}, "Missing 'blueprint_name' parameter"),
    ({"blueprint_name": "NonExistentBP", "component_name": "CubeMesh", "property_name": "Mobility", "property_value": "Movable"}, "Blueprint not found"),
    ({"blueprint_name": "RotatingCubeBP", "property_name": "Mobility", "property_value": "Movable"}, "Missing 'component_name' parameter"),
    ({"blueprint_name": "RotatingCubeBP", "component_name": "NonExistentComponent", "property_name": "Mobility", "property_value": "Movable"}, "Component not found"),
    ({"blueprint_name": "RotatingCubeBP", "component_name": "CubeMesh", "property_value": "Movable"}, "Missing 'property_name' parameter"),
    ({"blueprint_name": "RotatingCubeBP", "component_name": "CubeMesh", "property_name": "NonExistentProperty", "property_value": "Movable"}, "Property NonExistentProperty not found"),
])
def test_set_component_property_errors(payload, expected_error):
    resp = requests.post(f"{MCP_SERVER_URL}/set_component_property", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert not data.get("success", True)
    assert expected_error in data.get("error", "")

def test_add_component_to_blueprint_missing_params():
    resp = requests.post(f"{MCP_SERVER_URL}/add_component_to_blueprint", json={"blueprint_name": "RotatingCubeBP"})
    assert resp.status_code == 200
    data = resp.json()
    assert not data.get("success", True)
    assert "Missing 'type' parameter" in data.get("error", "")

def test_add_component_to_blueprint_invalid_blueprint():
    payload = {"blueprint_name": "NonExistentBP", "component_type": "StaticMeshComponent", "component_name": "TestMesh"}
    resp = requests.post(f"{MCP_SERVER_URL}/add_component_to_blueprint", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert not data.get("success", True)
    assert "Blueprint not found" in data.get("error", "") 