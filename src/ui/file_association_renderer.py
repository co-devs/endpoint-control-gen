import streamlit as st
from typing import Dict, Any, Optional
from ui.base_renderer import BaseUIRenderer
from core.interfaces import ISecurityControl
from controls.file_association_control import FileAssociationControl


class FileAssociationRenderer(BaseUIRenderer):
    def can_render(self, control: ISecurityControl) -> bool:
        return isinstance(control, FileAssociationControl)

    def render_configuration(
        self, control: ISecurityControl
    ) -> Optional[Dict[str, Any]]:
        st.subheader("Configuration")

        schema = control.get_configuration_schema()
        dangerous_extensions = schema["dangerous_extensions"]
        safe_applications = schema["safe_applications"]

        st.markdown("**Select extensions to secure:**")
        selected_extensions = {}

        col1, col2 = st.columns(2)

        with col1:
            for ext in list(dangerous_extensions.keys())[:4]:
                if st.checkbox(f"{ext} - {dangerous_extensions[ext]}", key=ext):
                    app = st.selectbox(
                        f"Set {ext} to open with:",
                        safe_applications + ["Custom application"],
                        key=f"app_{ext}",
                    )
                    if app == "Custom application":
                        app = st.text_input(
                            f"Custom application for {ext}:", key=f"custom_{ext}"
                        )
                    elif app == "Block execution":
                        app = "notepad.exe"
                    selected_extensions[ext] = app

        with col2:
            for ext in list(dangerous_extensions.keys())[4:]:
                if st.checkbox(f"{ext} - {dangerous_extensions[ext]}", key=ext):
                    app = st.selectbox(
                        f"Set {ext} to open with:",
                        safe_applications + ["Custom application"],
                        key=f"app_{ext}",
                    )
                    if app == "Custom application":
                        app = st.text_input(
                            f"Custom application for {ext}:", key=f"custom_{ext}"
                        )
                    elif app == "Block execution":
                        app = "notepad.exe"
                    selected_extensions[ext] = app

        st.markdown("**Add custom extensions:**")
        custom_ext = st.text_input("Extension (e.g., .xyz):")
        if custom_ext:
            if not custom_ext.startswith("."):
                custom_ext = "." + custom_ext
            custom_app = st.text_input("Application path:")
            if custom_app:
                selected_extensions[custom_ext] = custom_app

        return (
            {"file_associations": selected_extensions} if selected_extensions else None
        )
