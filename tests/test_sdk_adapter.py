import pytest
from dh_harness.sdk.adapter import AntigravitySDKAdapter

def test_sdk_adapter_initialization():
    adapter = AntigravitySDKAdapter(safe_mode=True)
    assert adapter.is_available() is True
    info = adapter.get_runtime_info()
    assert "version" in info
    assert info["package"] == "google.antigravity"

def test_sdk_adapter_agent_config():
    adapter = AntigravitySDKAdapter(safe_mode=True)
    config = adapter.create_local_agent_config(
        system_instructions="You are a test assistant.",
        enable_write_tools=False
    )
    assert config is not None
