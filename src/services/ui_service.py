import streamlit as st
from typing import Dict, Any, Optional
from core.interfaces import IControlRegistry, ISecurityControl


class UIService:
    def __init__(self, control_registry: IControlRegistry):
        self.control_registry = control_registry

    def setup_page_config(self):
        st.set_page_config(
            page_title="Windows Security Controls Generator",
            page_icon="🛡️",
            layout="wide",
            initial_sidebar_state="expanded",
        )

    def setup_custom_css(self):
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
        st.title("Windows Security Controls Generator")
        st.markdown(
            "Generate GPO policies, PowerShell scripts, and other artifacts for Windows security hardening."
        )

    def render_sidebar(self) -> str:
        st.sidebar.title("🛡️ Security Controls")
        st.sidebar.markdown("Generate Windows security artifacts")

        available_controls = list(self.control_registry.get_available_controls().keys())

        control_type = st.sidebar.selectbox("Select Control Type", available_controls)

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
        metadata = control.get_metadata()
        st.header(f"{metadata.name}")

        with st.expander("ℹ️ About This Control"):
            st.markdown(
                f"""
            **Purpose**: {metadata.purpose}
            
            **Risk Level**: {control.get_risk_level_display()}
            
            {f"**Common Targets**: {', '.join(metadata.common_targets)}" if metadata.common_targets else ""}
            """,
                unsafe_allow_html=True,
            )

    def render_artifacts_display(self, artifacts: Dict[str, str], control_name: str):
        st.subheader("Generated Artifacts")

        tab_names = []
        tab_contents = []

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
        st.subheader("📦 Complete Package")
        st.download_button(
            "Download Complete Package (ZIP)",
            package_data,
            file_name=f"{control_name}_Package.zip",
            mime="application/zip",
        )
