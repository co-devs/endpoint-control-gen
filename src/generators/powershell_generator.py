"""
powershell_generator.py

This module provides a generator for creating PowerShell scripts that implement
security controls such as file associations, firewall rules, and WinX menu modifications.
"""

from datetime import datetime
from typing import Dict, Any
from generators.base_generator import BaseArtifactGenerator


class PowerShellGenerator(BaseArtifactGenerator):
    """
    Generates PowerShell scripts to apply security controls based on provided settings.
    Supports file associations, firewall rules, and WinX menu modifications.
    """

    def generate(self, control_name: str, settings: Dict[str, Any]) -> str:
        """
        Generate a PowerShell script string based on the control name and settings.

        Args:
            control_name (str): The name of the security control.
            settings (Dict[str, Any]): Dictionary containing settings such as
                'file_associations', 'firewall_rules', and/or 'winx_removal'.

        Returns:
            str: The generated PowerShell script as a string.
        """
        script_lines = [
            "# Windows Security Control Implementation Script",
            f"# Control: {control_name}",
            f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "# Requires Administrator privileges",
            "if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {",
            "    Write-Error 'This script requires Administrator privileges'",
            "    exit 1",
            "}",
            "",
            "Write-Host 'Implementing security control...' -ForegroundColor Green",
            "",
        ]

        # Add file association commands if present in settings
        if "file_associations" in settings:
            script_lines.extend(
                self._generate_file_association_script(settings["file_associations"])
            )

        # Add firewall rule commands if present in settings
        if "firewall_rules" in settings:
            script_lines.extend(
                self._generate_firewall_script(settings["firewall_rules"])
            )

        # Add WinX menu modification commands if present in settings
        if "winx_removal" in settings:
            script_lines.extend(self._generate_winx_script(settings["winx_removal"]))

        script_lines.extend(
            [
                "Write-Host 'Security control implementation completed!' -ForegroundColor Green",
                "Write-Host 'Please reboot the system to ensure all changes take effect.' -ForegroundColor Cyan",
            ]
        )

        return "\n".join(script_lines)

    def _generate_file_association_script(
        self, file_associations: Dict[str, str]
    ) -> list:
        """
        Generate PowerShell commands for modifying file associations.

        Args:
            file_associations (Dict[str, str]): Mapping of file extensions to associated applications.

        Returns:
            list: List of PowerShell command strings.
        """
        lines = [
            "# File Association Security Control",
            "Write-Host 'Modifying file associations...' -ForegroundColor Yellow",
            "",
        ]

        for ext, app in file_associations.items():
            lines.extend(
                [
                    f"# Set {ext} to open with {app}",
                    f"cmd /c 'assoc {ext}={app}File'",
                    f'cmd /c \'ftype {app}File="{app}" "%1"\'',
                    "",
                ]
            )

        return lines

    def _generate_firewall_script(self, firewall_rules: list) -> list:
        """
        Generate PowerShell commands for adding firewall rules.

        Args:
            firewall_rules (list): List of firewall rule dictionaries, each containing
                'program' and 'name' keys.

        Returns:
            list: List of PowerShell command strings.
        """
        lines = [
            "# Windows Firewall Rules",
            "Write-Host 'Adding firewall rules...' -ForegroundColor Yellow",
            "",
        ]

        for rule in firewall_rules:
            lines.append(
                f"New-NetFirewallRule -DisplayName '{rule['name']}' -Direction Outbound -Program '{rule['program']}' -Action Block -Protocol TCP"
            )
        lines.append("")

        return lines

    def _generate_winx_script(self, winx_removal: list) -> list:
        """
        Generate PowerShell commands for modifying the WinX menu.

        Args:
            winx_removal (list): List of WinX menu item names to remove.

        Returns:
            list: List of PowerShell command strings.
        """
        lines = [
            "# WinX Menu Modification",
            "Write-Host 'Modifying WinX menu...' -ForegroundColor Yellow",
            '$winxPath = "$env:LOCALAPPDATA\\Microsoft\\Windows\\WinX"',
            "if (Test-Path $winxPath) {",
        ]

        for item in winx_removal:
            lines.append(
                f'    Remove-Item -Path "$winxPath\\*{item}*" -Force -ErrorAction SilentlyContinue'
            )

        lines.extend(
            [
                "}",
                "# Restart Explorer to apply changes",
                "Stop-Process -ProcessName explorer -Force",
                "Start-Process explorer",
                "",
            ]
        )

        return lines

    def get_file_extension(self) -> str:
        """
        Returns the file extension for the generated PowerShell script.

        Returns:
            str: The file extension ('ps1').
        """
        return "ps1"

    def get_mime_type(self) -> str:
        """
        Returns the MIME type for the generated PowerShell script.

        Returns:
            str: The MIME type ('text/plain').
        """
        return "text/plain"
