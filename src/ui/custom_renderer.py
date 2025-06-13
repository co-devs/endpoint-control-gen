import streamlit as st
from typing import Dict, Any, Optional
from ui.base_renderer import BaseUIRenderer
from core.interfaces import ISecurityControl
from controls.custom_control import CustomSecurityControl


class CustomRenderer(BaseUIRenderer):
    def can_render(self, control: ISecurityControl) -> bool:
        return isinstance(control, CustomSecurityControl)

    def render_configuration(
        self, control: ISecurityControl
    ) -> Optional[Dict[str, Any]]:
        st.subheader("Configuration")

        control_name = st.text_input("Control Name:", placeholder="My_Custom_Control")
        control_description = st.text_area(
            "Description:", placeholder="Describe what this control does..."
        )

        if not control_name:
            return None

        has_file_assoc = st.checkbox("Include File Association Changes")
        has_firewall = st.checkbox("Include Firewall Rules")
        has_winx = st.checkbox("Include WinX Menu Changes")

        settings = {}

        if has_file_assoc:
            st.markdown("**File Associations:**")
            ext = st.text_input("File extension:", key="custom_ext")
            app = st.text_input("Application:", key="custom_app")
            if ext and app:
                if not ext.startswith("."):
                    ext = "." + ext
                settings["file_associations"] = {ext: app}

        if has_firewall:
            st.markdown("**Firewall Rules:**")
            binary_name = st.text_input("Binary name:", key="custom_binary")
            binary_path = st.text_input("Binary path:", key="custom_path")
            if binary_name and binary_path:
                settings["firewall_rules"] = [
                    {"name": f"Block_{binary_name}", "program": binary_path}
                ]

        if has_winx:
            st.markdown("**WinX Menu Items:**")
            winx_item = st.text_input("Item to remove:", key="custom_winx")
            if winx_item:
                settings["winx_removal"] = [winx_item]

        return (
            {
                "control_name": control_name,
                "control_description": control_description,
                "settings": settings,
            }
            if settings
            else None
        )
