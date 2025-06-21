"""
batch_generator.py

This module provides a generator for creating Windows batch scripts that implement
security controls such as file associations and firewall rules.
"""

from datetime import datetime
from typing import Dict, Any
from generators.base_generator import BaseArtifactGenerator


class BatchGenerator(BaseArtifactGenerator):
    """
    Generates Windows batch scripts to apply security controls based on provided settings.
    Supports file associations and firewall rules.
    """

    def generate(self, control_name: str, settings: Dict[str, Any]) -> str:
        """
        Generate a batch script string based on the control name and settings.

        Args:
            control_name (str): The name of the security control.
            settings (Dict[str, Any]): Dictionary containing settings such as
                'file_associations' and/or 'firewall_rules'.

        Returns:
            str: The generated batch script as a string.
        """
        batch_lines = [
            "@echo off",
            f"REM Windows Security Control: {control_name}",
            f"REM Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "REM Check for administrator privileges",
            "net session >nul 2>&1",
            "if %errorLevel% neq 0 (",
            "    echo This script requires Administrator privileges",
            "    pause",
            "    exit /b 1",
            ")",
            "",
            "echo Implementing security control...",
            "",
        ]

        # Add file association commands if present in settings
        if "file_associations" in settings:
            batch_lines.append("REM File Association Changes")
            for ext, app in settings["file_associations"].items():
                batch_lines.extend(
                    [
                        f"assoc {ext}={app}File",
                        f'ftype {app}File="{app}" "%%1"',
                    ]
                )
            batch_lines.append("")

        # Add firewall rule commands if present in settings
        if "firewall_rules" in settings:
            batch_lines.append("REM Windows Firewall Rules")
            for rule in settings["firewall_rules"]:
                batch_lines.append(
                    f"netsh advfirewall firewall add rule name=\"{rule['name']}\" dir=out action=block program=\"{rule['program']}\""
                )
            batch_lines.append("")

        batch_lines.extend(
            [
                "echo Security control implementation completed!",
                "echo Please reboot the system to ensure all changes take effect.",
                "pause",
            ]
        )

        return "\n".join(batch_lines)

    def get_file_extension(self) -> str:
        """
        Returns the file extension for the generated batch script.

        Returns:
            str: The file extension ('bat').
        """
        return "bat"

    def get_mime_type(self) -> str:
        """
        Returns the MIME type for the generated batch script.

        Returns:
            str: The MIME type ('text/plain').
        """
        return "text/plain"
