"""
Example: Adding a new security control to the modular application

This example shows how to create a new "Registry Hardening" control
and its corresponding UI renderer.
"""

from typing import Dict, Any, Optional
import streamlit as st
from ..core.base_control import BaseSecurityControl
from ..core.interfaces import SecurityControlMetadata, RiskLevel
from ..ui.base_renderer import BaseUIRenderer


class RegistryHardeningControl(BaseSecurityControl):
    def __init__(self):
        metadata = SecurityControlMetadata(
            name="Registry Hardening",
            description="Apply registry modifications to harden Windows security",
            risk_level=RiskLevel.HIGH,
            purpose="Apply critical registry modifications to improve Windows security posture",
            common_targets=[
                "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies",
                "HKLM\\System\\CurrentControlSet\\Services",
            ],
            category="Registry Security",
        )
        super().__init__(metadata)

    def validate_settings(self, settings: Dict[str, Any]) -> bool:
        if "registry_modifications" not in settings:
            return False

        modifications = settings["registry_modifications"]
        if not isinstance(modifications, list):
            return False

        for mod in modifications:
            if not isinstance(mod, dict):
                return False
            required_keys = ["key", "value_name", "value_data", "value_type"]
            if not all(key in mod for key in required_keys):
                return False

        return True

    def get_default_configuration(self) -> Dict[str, Any]:
        return {
            "registry_modifications": [
                {
                    "key": "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System",
                    "value_name": "EnableLUA",
                    "value_data": "1",
                    "value_type": "DWORD",
                }
            ]
        }

    def get_configuration_schema(self) -> Dict[str, Any]:
        return {
            "common_modifications": {
                "Enable UAC": {
                    "key": "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System",
                    "value_name": "EnableLUA",
                    "value_data": "1",
                    "value_type": "DWORD",
                },
                "Disable autorun": {
                    "key": "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer",
                    "value_name": "NoDriveTypeAutoRun",
                    "value_data": "255",
                    "value_type": "DWORD",
                },
                "Disable remote desktop": {
                    "key": "HKLM\\System\\CurrentControlSet\\Control\\Terminal Server",
                    "value_name": "fDenyTSConnections",
                    "value_data": "1",
                    "value_type": "DWORD",
                },
            },
            "value_types": ["DWORD", "REG_SZ", "REG_MULTI_SZ", "REG_BINARY"],
        }


class RegistryHardeningRenderer(BaseUIRenderer):
    def can_render(self, control) -> bool:
        return isinstance(control, RegistryHardeningControl)

    def render_configuration(self, control) -> Optional[Dict[str, Any]]:
        st.subheader("Configuration")

        schema = control.get_configuration_schema()
        common_modifications = schema["common_modifications"]
        value_types = schema["value_types"]

        st.markdown("**Select common registry modifications:**")
        selected_modifications = []

        for mod_name, mod_data in common_modifications.items():
            if st.checkbox(f"Apply: {mod_name}", key=f"reg_{mod_name}"):
                selected_modifications.append(mod_data)

        st.markdown("**Add custom registry modification:**")
        col1, col2 = st.columns(2)

        with col1:
            custom_key = st.text_input("Registry Key:")
            custom_value_name = st.text_input("Value Name:")

        with col2:
            custom_value_data = st.text_input("Value Data:")
            custom_value_type = st.selectbox("Value Type:", value_types)

        if all([custom_key, custom_value_name, custom_value_data, custom_value_type]):
            selected_modifications.append(
                {
                    "key": custom_key,
                    "value_name": custom_value_name,
                    "value_data": custom_value_data,
                    "value_type": custom_value_type,
                }
            )

        return (
            {"registry_modifications": selected_modifications}
            if selected_modifications
            else None
        )


# To register this new control with the application:
"""
# In app_factory.py, add to create_control_registry method:
registry.register_control(RegistryHardeningControl, RegistryHardeningRenderer)
"""
