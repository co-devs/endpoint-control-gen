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
    """
    Security control for applying registry modifications to harden Windows security.
    """

    def __init__(self):
        """
        Initialize the RegistryHardeningControl with appropriate metadata.
        """
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
        """
        Validate the settings for registry modifications.

        Args:
            settings (Dict[str, Any]): The settings to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
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
        """
        Provide a default configuration for registry modifications.

        Returns:
            Dict[str, Any]: Default registry modifications.
        """
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
        """
        Provide a schema of common modifications and value types.

        Returns:
            Dict[str, Any]: Schema for UI rendering.
        """
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
    """
    UI renderer for the RegistryHardeningControl.

    Provides a Streamlit UI for selecting and configuring registry modifications.
    """

    def can_render(self, control) -> bool:
        """
        Determine if this renderer can handle the given control.

        Args:
            control: The control to check.

        Returns:
            bool: True if the control is a RegistryHardeningControl, else False.
        """
        return isinstance(control, RegistryHardeningControl)

    def render_configuration(self, control) -> Optional[Dict[str, Any]]:
        """
        Render the configuration UI for registry modifications.

        Args:
            control: The RegistryHardeningControl instance.

        Returns:
            Optional[Dict[str, Any]]: The configuration data if provided, else None.
        """
        st.subheader("Configuration")

        # Retrieve schema for common modifications and value types
        schema = control.get_configuration_schema()
        common_modifications = schema["common_modifications"]
        value_types = schema["value_types"]

        st.markdown("**Select common registry modifications:**")
        selected_modifications = []

        # Checkbox for each common modification
        for mod_name, mod_data in common_modifications.items():
            if st.checkbox(f"Apply: {mod_name}", key=f"reg_{mod_name}"):
                selected_modifications.append(mod_data)

        st.markdown("**Add custom registry modification:**")
        col1, col2 = st.columns(2)

        # Inputs for custom registry modification
        with col1:
            custom_key = st.text_input("Registry Key:")
            custom_value_name = st.text_input("Value Name:")

        with col2:
            custom_value_data = st.text_input("Value Data:")
            custom_value_type = st.selectbox("Value Type:", value_types)

        # Add custom modification if all fields are filled
        if all([custom_key, custom_value_name, custom_value_data, custom_value_type]):
            selected_modifications.append(
                {
                    "key": custom_key,
                    "value_name": custom_value_name,
                    "value_data": custom_value_data,
                    "value_type": custom_value_type,
                }
            )

        # Return configuration only if at least one modification is provided
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
