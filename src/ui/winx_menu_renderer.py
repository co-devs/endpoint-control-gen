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

        # Dynamically create up to 3 columns based on number of items
        winx_list = list(winx_items.keys())
        num_items = len(winx_list)

        # Determine number of columns (1-3 based on item count)
        if num_items <= 5:
            num_cols = 1
        elif num_items <= 12:
            num_cols = 2
        else:
            num_cols = 3

        # Calculate items per column
        items_per_col = (num_items + num_cols - 1) // num_cols

        # Create columns
        cols = st.columns(num_cols)

        # Distribute items across columns
        for i, item in enumerate(winx_list):
            col_idx = i // items_per_col
            if col_idx >= num_cols:  # Safety check
                col_idx = num_cols - 1

            with cols[col_idx]:
                if st.checkbox(f"Remove {item}", key=f"winx_{item}"):
                    selected_items.append(winx_items[item])

        # Return configuration only if at least one item is selected
        return {"winx_removal": selected_items} if selected_items else None
