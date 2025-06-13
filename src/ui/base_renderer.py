import streamlit as st
from typing import Dict, Any, Optional
from core.interfaces import IUIRenderer, ISecurityControl


class BaseUIRenderer(IUIRenderer):
    def can_render(self, control: ISecurityControl) -> bool:
        return True

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
