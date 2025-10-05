"""
Windows Hotkey Renderer module for Streamlit-based Windows Security Controls Generator.

Defines the WindowsHotkeyRenderer class, which provides a specialized UI for configuring
Windows hotkey security controls, allowing users to disable all or specific hotkeys.
"""

import streamlit as st
from typing import Dict, Any, Optional
from ui.base_renderer import BaseUIRenderer
from core.interfaces import ISecurityControl
from controls.windows_hotkey_control import WindowsHotkeyControl


class WindowsHotkeyRenderer(BaseUIRenderer):
    """
    UI renderer for Windows hotkey security controls.

    Allows users to disable all hotkeys or select specific hotkeys to disable.
    """

    def can_render(self, control: ISecurityControl) -> bool:
        """
        Determine if this renderer can handle the given control.

        Args:
            control (ISecurityControl): The security control to check.

        Returns:
            bool: True if the control is a WindowsHotkeyControl, else False.
        """
        return isinstance(control, WindowsHotkeyControl)

    def render_configuration(
        self, control: ISecurityControl
    ) -> Optional[Dict[str, Any]]:
        """
        Render the configuration UI for Windows hotkey controls.

        Args:
            control (ISecurityControl): The Windows hotkey control to configure.

        Returns:
            Optional[Dict[str, Any]]: The configuration data if provided, else None.
        """
        st.subheader("Configuration")

        # Retrieve schema with available hotkeys
        schema = control.get_configuration_schema()
        common_hotkeys = schema["common_hotkeys"]

        # Option 1: Disable all Windows hotkeys
        st.markdown("### Option 1: Disable All Windows Hotkeys")
        disable_all = st.checkbox(
            "Disable ALL Windows hotkeys (NoWinKeys policy)",
            help="This will disable all Windows key combinations system-wide via registry policy. This is the most restrictive option.",
        )

        # Option 2: Disable specific hotkeys
        st.markdown("### Option 2: Disable Specific Hotkeys")
        st.markdown(
            "Select individual hotkeys to disable (applies per user via HKCU registry):"
        )

        selected_hotkeys = []

        # Dynamically create up to 3 columns based on number of items
        hotkey_list = list(common_hotkeys.keys())
        num_items = len(hotkey_list)

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
        for i, hotkey in enumerate(hotkey_list):
            col_idx = i // items_per_col
            if col_idx >= num_cols:  # Safety check
                col_idx = num_cols - 1

            with cols[col_idx]:
                if st.checkbox(
                    f"Win+{hotkey}",
                    key=f"hotkey_{hotkey}",
                    help=common_hotkeys[hotkey],
                    disabled=disable_all,
                ):
                    selected_hotkeys.append(hotkey)

        # Show warning if disabling all
        if disable_all:
            st.warning(
                "⚠️ **WARNING**: Disabling all Windows hotkeys will prevent users from using any Windows key shortcuts, including Win+L (lock screen). Use with caution!"
            )

        # Return configuration if at least one option is selected
        if disable_all or selected_hotkeys:
            return {
                "disable_all_hotkeys": disable_all,
                "disabled_hotkeys": selected_hotkeys,
            }

        return None
