"""
Custom UI Renderer module for Streamlit-based Windows Security Controls Generator.

Defines the CustomRenderer class, which provides a specialized UI for configuring
custom security controls with user-defined settings.
"""

import streamlit as st
from typing import Dict, Any, Optional
from ui.base_renderer import BaseUIRenderer
from core.interfaces import ISecurityControl
from controls.custom_control import CustomSecurityControl


class CustomRenderer(BaseUIRenderer):
    """
    UI renderer for custom security controls.

    Allows users to input custom configuration details and settings for their own controls.
    """

    def can_render(self, control: ISecurityControl) -> bool:
        """
        Determine if this renderer can handle the given control.

        Args:
            control (ISecurityControl): The security control to check.

        Returns:
            bool: True if the control is a CustomSecurityControl, else False.
        """
        return isinstance(control, CustomSecurityControl)

    def render_configuration(
        self, control: ISecurityControl
    ) -> Optional[Dict[str, Any]]:
        """
        Render the configuration UI for a custom security control.

        Args:
            control (ISecurityControl): The custom security control to configure.

        Returns:
            Optional[Dict[str, Any]]: The configuration data if provided, else None.
        """
        st.subheader("Configuration")

        # Input for control name and description
        control_name = st.text_input("Control Name:", placeholder="My_Custom_Control")
        control_description = st.text_area(
            "Description:", placeholder="Describe what this control does..."
        )

        # Require a control name to proceed
        if not control_name:
            return None

        # Options for additional settings
        has_file_assoc = st.checkbox("Include File Association Changes")
        has_firewall = st.checkbox("Include Firewall Rules")
        has_winx = st.checkbox("Include WinX Menu Changes")

        settings = {}

        # File association configuration
        if has_file_assoc:
            st.markdown("**File Associations:**")
            ext = st.text_input("File extension:", key="custom_ext")
            app = st.text_input("Application:", key="custom_app")
            if ext and app:
                if not ext.startswith("."):
                    ext = "." + ext
                settings["file_associations"] = {ext: app}

        # Firewall rules configuration
        if has_firewall:
            st.markdown("**Firewall Rules:**")
            binary_name = st.text_input("Binary name:", key="custom_binary")
            binary_path = st.text_input("Binary path:", key="custom_path")
            if binary_name and binary_path:
                settings["firewall_rules"] = [
                    {"name": f"Block_{binary_name}", "program": binary_path}
                ]

        # WinX menu item removal configuration
        if has_winx:
            st.markdown("**WinX Menu Items:**")
            winx_item = st.text_input("Item to remove:", key="custom_winx")
            if winx_item:
                settings["winx_removal"] = [winx_item]

        # Return configuration only if at least one setting is provided
        return (
            {
                "control_name": control_name,
                "control_description": control_description,
                "settings": settings,
            }
            if settings
            else None
        )
