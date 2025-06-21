"""
WinX Menu Renderer module for Streamlit-based Windows Security Controls Generator.

Defines the WinXMenuRenderer class, which provides a specialized UI for configuring
WinX menu security controls, allowing users to select and remove WinX menu items.
"""

import streamlit as st
from typing import Dict, Any, Optional
from ui.base_renderer import BaseUIRenderer
from core.interfaces import ISecurityControl
from controls.winx_menu_control import WinXMenuControl


class WinXMenuRenderer(BaseUIRenderer):
    """
    UI renderer for WinX menu security controls.

    Allows users to select WinX menu items to remove from the Windows context menu.
    """

    def can_render(self, control: ISecurityControl) -> bool:
        """
        Determine if this renderer can handle the given control.

        Args:
            control (ISecurityControl): The security control to check.

        Returns:
            bool: True if the control is a WinXMenuControl, else False.
        """
        return isinstance(control, WinXMenuControl)

    def render_configuration(
        self, control: ISecurityControl
    ) -> Optional[Dict[str, Any]]:
        """
        Render the configuration UI for WinX menu controls.

        Args:
            control (ISecurityControl): The WinX menu control to configure.

        Returns:
            Optional[Dict[str, Any]]: The configuration data if provided, else None.
        """
        st.subheader("Configuration")

        # Retrieve schema with available WinX menu items
        schema = control.get_configuration_schema()
        winx_items = schema["winx_items"]

        st.markdown("**Select WinX menu items to remove:**")
        selected_items = []

        # Split WinX items into two columns for better UI
        col1, col2 = st.columns(2)

        # Distribute items evenly between columns
        winx_list = list(winx_items.keys())
        mid_point = len(winx_list) // 2

        with col1:
            for item in winx_list[:mid_point]:
                # Checkbox for each item in the first column
                if st.checkbox(f"Remove {item}", key=f"winx_{item}"):
                    selected_items.append(winx_items[item])

        with col2:
            for item in winx_list[mid_point:]:
                # Checkbox for each item in the second column
                if st.checkbox(f"Remove {item}", key=f"winx_{item}"):
                    selected_items.append(winx_items[item])

        # Return configuration only if at least one item is selected
        return {"winx_removal": selected_items} if selected_items else None
