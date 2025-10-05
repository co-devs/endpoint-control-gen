"""
registry_generator.py

This module provides a generator for creating Windows Registry (.reg) files that implement
security controls such as file associations.
"""

from datetime import datetime
from typing import Dict, Any
from generators.base_generator import BaseArtifactGenerator


class RegistryGenerator(BaseArtifactGenerator):
    """
    Generates Windows Registry files to apply security controls based on provided settings.
    Currently supports file associations.
    """

    def generate(self, control_name: str, settings: Dict[str, Any]) -> str:
        """
        Generate a .reg file string based on the control name and settings.

        Args:
            control_name (str): The name of the security control.
            settings (Dict[str, Any]): Dictionary containing settings such as 'file_associations'.

        Returns:
            str: The generated registry file as a string.
        """
        reg_lines = [
            "Windows Registry Editor Version 5.00",
            "",
            f"; Windows Security Control: {control_name}",
            f"; Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]

        # Add file association registry entries if present in settings
        if "file_associations" in settings:
            reg_lines.append("; File Association Changes")
            reg_lines.append("; Using HKLM\\SOFTWARE\\Classes instead of HKCR to avoid dynamic generation issues")
            for ext, app in settings["file_associations"].items():
                reg_lines.extend(
                    [
                        f"[HKEY_LOCAL_MACHINE\\SOFTWARE\\Classes\\{ext}]",
                        f'@="{app}File"',
                        "",
                        f"[HKEY_LOCAL_MACHINE\\SOFTWARE\\Classes\\{app}File\\shell\\open\\command]",
                        f'@="{app} \\"%1\\""',
                        "",
                    ]
                )

        return "\n".join(reg_lines)

    def get_file_extension(self) -> str:
        """
        Returns the file extension for the generated registry file.

        Returns:
            str: The file extension ('reg').
        """
        return "reg"

    def get_mime_type(self) -> str:
        """
        Returns the MIME type for the generated registry file.

        Returns:
            str: The MIME type ('text/plain').
        """
        return "text/plain"

    def supports_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Checks if the provided settings are supported by this generator.

        Args:
            settings (Dict[str, Any]): The settings dictionary.

        Returns:
            bool: True if 'file_associations' is present in settings, False otherwise.
        """
        return "file_associations" in settings
