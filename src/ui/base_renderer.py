"""
Base UI Renderer module for Streamlit-based Windows Security Controls Generator.

Defines the BaseUIRenderer class, which provides a default implementation for rendering
security control information in the Streamlit UI.
"""

import streamlit as st
from typing import Dict, Any, Optional
from core.interfaces import IUIRenderer, ISecurityControl


class BaseUIRenderer(IUIRenderer):
    """
    Default UI renderer for security controls.

    This renderer provides a generic way to display control metadata and details.
    """

    def can_render(self, control: ISecurityControl) -> bool:
        """
        Determine if this renderer can handle the given control.

        Args:
            control (ISecurityControl): The security control to check.

        Returns:
            bool: Always True for the base renderer.
        """
        return True

    def render_control_info(self, control: ISecurityControl):
        """
        Render detailed information about the given security control.

        Args:
            control (ISecurityControl): The security control to render.
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
