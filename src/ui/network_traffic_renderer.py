"""
Network Traffic Renderer module for Streamlit-based Windows Security Controls Generator.

Defines the NetworkTrafficRenderer class, which provides a specialized UI for configuring
network traffic security controls, allowing users to block network access for risky binaries.
"""

import streamlit as st
from typing import Dict, Any, Optional
from ui.base_renderer import BaseUIRenderer
from core.interfaces import ISecurityControl
from controls.network_traffic_control import NetworkTrafficControl


class NetworkTrafficRenderer(BaseUIRenderer):
    """
    UI renderer for network traffic security controls.

    Allows users to select binaries to block from network access and add custom rules.
    """

    def can_render(self, control: ISecurityControl) -> bool:
        """
        Determine if this renderer can handle the given control.

        Args:
            control (ISecurityControl): The security control to check.

        Returns:
            bool: True if the control is a NetworkTrafficControl, else False.
        """
        return isinstance(control, NetworkTrafficControl)

    def render_configuration(
        self, control: ISecurityControl
    ) -> Optional[Dict[str, Any]]:
        """
        Render the configuration UI for network traffic controls.

        Args:
            control (ISecurityControl): The network traffic control to configure.

        Returns:
            Optional[Dict[str, Any]]: The configuration data if provided, else None.
        """
        st.subheader("Configuration")

        # Retrieve schema with risky binaries
        schema = control.get_configuration_schema()
        risky_binaries = schema["risky_binaries"]

        st.markdown("**Select binaries to block network access:**")
        selected_rules = []

        # Split binaries into two columns for better UI
        col1, col2 = st.columns(2)

        with col1:
            for binary in list(risky_binaries.keys())[:4]:
                # Checkbox for each binary in the first column
                if st.checkbox(f"Block {binary}", key=f"fw_{binary}"):
                    selected_rules.append(
                        {
                            "name": f"Block_{binary}_Outbound",
                            "program": risky_binaries[binary],
                        }
                    )

        with col2:
            for binary in list(risky_binaries.keys())[4:]:
                # Checkbox for each binary in the second column
                if st.checkbox(f"Block {binary}", key=f"fw_{binary}"):
                    selected_rules.append(
                        {
                            "name": f"Block_{binary}_Outbound",
                            "program": risky_binaries[binary],
                        }
                    )

        # Allow user to add a custom binary and its path
        st.markdown("**Add custom binary:**")
        custom_binary_name = st.text_input("Binary name (e.g., mybinary.exe):")
        custom_binary_path = st.text_input("Full path to binary:")
        if custom_binary_name and custom_binary_path:
            selected_rules.append(
                {
                    "name": f"Block_{custom_binary_name}_Outbound",
                    "program": custom_binary_path,
                }
            )

        # Return configuration only if at least one rule is provided
        return {"firewall_rules": selected_rules} if selected_rules else None
