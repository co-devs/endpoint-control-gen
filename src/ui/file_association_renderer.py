"""
File Association Renderer module for Streamlit-based Windows Security Controls Generator.

Defines the FileAssociationRenderer class, which provides a specialized UI for configuring
file association security controls, allowing users to select extensions and assign safe applications.
"""

import streamlit as st
from typing import Dict, Any, Optional
from ui.base_renderer import BaseUIRenderer
from core.interfaces import ISecurityControl
from controls.file_association_control import FileAssociationControl


class FileAssociationRenderer(BaseUIRenderer):
    """
    UI renderer for file association security controls.

    Allows users to select dangerous file extensions and assign them to safe applications.
    """

    def can_render(self, control: ISecurityControl) -> bool:
        """
        Determine if this renderer can handle the given control.

        Args:
            control (ISecurityControl): The security control to check.

        Returns:
            bool: True if the control is a FileAssociationControl, else False.
        """
        return isinstance(control, FileAssociationControl)

    def render_configuration(
        self, control: ISecurityControl
    ) -> Optional[Dict[str, Any]]:
        """
        Render the configuration UI for file association controls.

        Args:
            control (ISecurityControl): The file association control to configure.

        Returns:
            Optional[Dict[str, Any]]: The configuration data if provided, else None.
        """
        st.subheader("Configuration")

        # Retrieve schema with dangerous extensions and safe applications
        schema = control.get_configuration_schema()
        dangerous_extensions = schema["dangerous_extensions"]
        safe_applications = schema["safe_applications"]

        st.markdown("**Select extensions to secure:**")
        selected_extensions_list = []

        # Split extensions into two columns for better UI
        col1, col2 = st.columns(2)
        extensions_list = list(dangerous_extensions.keys())
        mid_point = len(extensions_list) // 2

        with col1:
            for ext in extensions_list[:mid_point]:
                # Checkbox for each extension in the first column
                if st.checkbox(f"{ext} - {dangerous_extensions[ext]}", key=ext):
                    selected_extensions_list.append(ext)

        with col2:
            for ext in extensions_list[mid_point:]:
                # Checkbox for each extension in the second column
                if st.checkbox(f"{ext} - {dangerous_extensions[ext]}", key=ext):
                    selected_extensions_list.append(ext)

        selected_extensions = {}

        # If any extensions are selected, prompt for application assignment
        if selected_extensions_list:
            st.markdown(f"**Selected {len(selected_extensions_list)} extension(s). Choose application for all:**")
            app = st.selectbox(
                "Set all selected extensions to open with:",
                safe_applications + ["Custom application"],
                key="global_app",
            )
            if app == "Custom application":
                app = st.text_input("Custom application path:", key="global_custom")
            elif app == "Block execution":
                # Special case: block execution by assigning to notepad.exe
                app = "notepad.exe"

            # Assign the selected application to all selected extensions
            if app:
                for ext in selected_extensions_list:
                    selected_extensions[ext] = app

        # Allow user to add custom extensions and assign applications
        st.markdown("**Add custom extensions:**")
        custom_ext = st.text_input("Extension (e.g., .xyz):")
        if custom_ext:
            if not custom_ext.startswith("."):
                custom_ext = "." + custom_ext
            custom_app = st.text_input("Application path:")
            if custom_app:
                selected_extensions[custom_ext] = custom_app

        # Return configuration only if at least one association is provided
        return (
            {"file_associations": selected_extensions} if selected_extensions else None
        )
