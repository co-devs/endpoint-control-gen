"""
UI Service module for Streamlit-based Windows Security Controls Generator.

This module provides the UIService class, which encapsulates all Streamlit UI rendering
and configuration logic for the application, including page setup, sidebar, control info,
artifact display, and download functionality.
"""

import streamlit as st
from typing import Dict, Any, Optional
from core.interfaces import IControlRegistry, ISecurityControl


class UIService:
    """
    Service class responsible for rendering and managing the Streamlit UI components.
    """

    def __init__(self, control_registry: IControlRegistry):
        """
        Initialize the UIService with a control registry.

        Args:
            control_registry (IControlRegistry): Registry providing available security controls.
        """
        self.control_registry = control_registry

    def setup_page_config(self):
        """
        Configure the Streamlit page settings (title, icon, layout, sidebar).
        """
        st.set_page_config(
            page_title="Windows Security Controls Generator",
            page_icon="🛡️",
            layout="wide",
            initial_sidebar_state="expanded",
        )

    def setup_custom_css(self):
        """
        Inject custom CSS styles for control cards and risk level indicators.
        """
        st.markdown(
            """
        <style>
            .control-card {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 16px;
                margin: 8px 0;
                background-color: #f8f9fa;
            }
            .risk-high { color: #dc3545; font-weight: bold; }
            .risk-medium { color: #fd7e14; font-weight: bold; }
            .risk-low { color: #28a745; font-weight: bold; }
        </style>
        """,
            unsafe_allow_html=True,
        )

    def render_main_header(self):
        """
        Render the main header and description for the application.
        """
        st.title("Windows Security Controls Generator")
        st.markdown(
            "Generate GPO policies, PowerShell scripts, and other artifacts for Windows security hardening."
        )

    def render_sidebar(self) -> str:
        """
        Render the sidebar UI, including control selection and notices.

        Returns:
            str: The selected control type.
        """
        st.sidebar.title("🛡️ Security Controls")
        st.sidebar.markdown("Generate Windows security artifacts")

        # Get available control types from the registry
        available_controls = list(self.control_registry.get_available_controls().keys())

        # Dropdown for selecting control type
        control_type = st.sidebar.selectbox("Select Control Type", available_controls)

        # Security notice and documentation info
        st.sidebar.markdown("---")
        st.sidebar.markdown("**⚠️ Security Notice**")
        st.sidebar.markdown(
            "Always test configurations in a non-production environment first!"
        )
        st.sidebar.markdown("**📝 Documentation**")
        st.sidebar.markdown(
            "Each download includes implementation instructions and security considerations."
        )

        return control_type

    def render_control_info(self, control: ISecurityControl):
        """
        Render detailed information about the selected security control.

        Args:
            control (ISecurityControl): The selected security control instance.
        """
        metadata = control.get_metadata()
        st.header(f"{metadata.name}")

        with st.expander("ℹ️ About This Control"):
            # Display control purpose, risk level, and common targets if available
            st.markdown(
                f"""
            **Purpose**: {metadata.purpose}
            
            **Risk Level**: {control.get_risk_level_display()}
            
            {f"**Common Targets**: {', '.join(metadata.common_targets)}" if metadata.common_targets else ""}
            """,
                unsafe_allow_html=True,
            )

    def render_artifacts_display(self, artifacts: Dict[str, str], control_name: str):
        """
        Render tabs for each generated artifact and provide download buttons.

        Args:
            artifacts (Dict[str, str]): Mapping of artifact type to content.
            control_name (str): Name of the control for file naming.
        """
        st.subheader("Generated Artifacts")

        tab_names = []
        tab_contents = []

        # Prepare tabs and content for each artifact type
        if "powershell" in artifacts:
            tab_names.append("PowerShell Script")
            tab_contents.append(("powershell", artifacts["powershell"], "ps1"))

        if "gpo" in artifacts:
            tab_names.append("GPO XML")
            tab_contents.append(("xml", artifacts["gpo"], "xml"))

        if "registry" in artifacts:
            tab_names.append("Registry File")
            tab_contents.append(("text", artifacts["registry"], "reg"))

        if "batch" in artifacts:
            tab_names.append("Batch Script")
            tab_contents.append(("batch", artifacts["batch"], "bat"))

        if tab_names:
            tabs = st.tabs(tab_names)

            # Render each tab with code and download button
            for i, (language, content, extension) in enumerate(tab_contents):
                with tabs[i]:
                    st.code(content, language=language)
                    st.download_button(
                        f"Download {tab_names[i]}",
                        content,
                        file_name=f"{control_name}.{extension}",
                        mime="text/plain",
                    )

    def render_package_download(self, package_data: bytes, control_name: str):
        """
        Render a download button for the complete package (ZIP file).

        Args:
            package_data (bytes): The ZIP package data.
            control_name (str): Name of the control for file naming.
        """
        st.subheader("📦 Complete Package")
        st.download_button(
            "Download Complete Package (ZIP)",
            package_data,
            file_name=f"{control_name}_Package.zip",
            mime="application/zip",
        )
