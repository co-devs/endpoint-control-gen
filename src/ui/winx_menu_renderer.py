import streamlit as st
from typing import Dict, Any, Optional
from ui.base_renderer import BaseUIRenderer
from core.interfaces import ISecurityControl
from controls.winx_menu_control import WinXMenuControl


class WinXMenuRenderer(BaseUIRenderer):
    def can_render(self, control: ISecurityControl) -> bool:
        return isinstance(control, WinXMenuControl)

    def render_configuration(
        self, control: ISecurityControl
    ) -> Optional[Dict[str, Any]]:
        st.subheader("Configuration")

        schema = control.get_configuration_schema()
        winx_items = schema["winx_items"]

        st.markdown("**Select WinX menu items to remove:**")
        selected_items = []

        col1, col2 = st.columns(2)

        # Distribute extensions evenly between columns
        winx_list = list(winx_items.keys())
        mid_point = len(winx_list) // 2

        with col1:
            for item in winx_list[:mid_point]:
                if st.checkbox(f"Remove {item}", key=f"winx_{item}"):
                    selected_items.append(winx_items[item])

        with col2:
            for item in winx_list[mid_point:]:
                if st.checkbox(f"Remove {item}", key=f"winx_{item}"):
                    selected_items.append(winx_items[item])

        return {"winx_removal": selected_items} if selected_items else None
