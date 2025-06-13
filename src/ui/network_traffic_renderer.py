import streamlit as st
from typing import Dict, Any, Optional
from ui.base_renderer import BaseUIRenderer
from core.interfaces import ISecurityControl
from controls.network_traffic_control import NetworkTrafficControl


class NetworkTrafficRenderer(BaseUIRenderer):
    def can_render(self, control: ISecurityControl) -> bool:
        return isinstance(control, NetworkTrafficControl)

    def render_configuration(
        self, control: ISecurityControl
    ) -> Optional[Dict[str, Any]]:
        st.subheader("Configuration")

        schema = control.get_configuration_schema()
        risky_binaries = schema["risky_binaries"]

        st.markdown("**Select binaries to block network access:**")
        selected_rules = []

        col1, col2 = st.columns(2)

        with col1:
            for binary in list(risky_binaries.keys())[:4]:
                if st.checkbox(f"Block {binary}", key=f"fw_{binary}"):
                    selected_rules.append(
                        {
                            "name": f"Block_{binary}_Outbound",
                            "program": risky_binaries[binary],
                        }
                    )

        with col2:
            for binary in list(risky_binaries.keys())[4:]:
                if st.checkbox(f"Block {binary}", key=f"fw_{binary}"):
                    selected_rules.append(
                        {
                            "name": f"Block_{binary}_Outbound",
                            "program": risky_binaries[binary],
                        }
                    )

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

        return {"firewall_rules": selected_rules} if selected_rules else None
