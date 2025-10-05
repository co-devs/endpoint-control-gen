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
        Generate PowerShell commands for modifying file associations via registry.

        Args:
            file_associations (Dict[str, str]): Mapping of file extensions to associated applications.

        Returns:
            list: List of PowerShell command strings.
        """
        lines = [
            "# File Association Security Control",
            "Write-Host 'Modifying file associations via registry...' -ForegroundColor Yellow",
            "",
        ]

        # Get unique applications to avoid setting ftype multiple times
        unique_apps = set(file_associations.values())

        # Set up file types (ftype equivalents) for each unique application
        lines.append("# Set up file type handlers")
        for app in unique_apps:
            lines.extend(
                [
                    f"New-Item -Path 'HKLM:\\SOFTWARE\\Classes\\{app}File\\shell\\open\\command' -Force | Out-Null",
                    f"Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Classes\\{app}File\\shell\\open\\command' -Name '(Default)' -Value '\"{app}\" \"%1\"'",
                ]
            )
        lines.append("")

        # Associate extensions with their file types
        lines.append("# Associate extensions with handlers")
        for ext, app in file_associations.items():
            lines.extend(
                [
                    f"New-Item -Path 'HKLM:\\SOFTWARE\\Classes\\{ext}' -Force | Out-Null",
                    f"Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Classes\\{ext}' -Name '(Default)' -Value '{app}File'",
                ]
            )
        lines.append("")

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
        Generate PowerShell commands for modifying the WinX menu for all users and default profile.

        Args:
            winx_removal (list): List of WinX menu item names to remove.

        Returns:
            list: List of PowerShell command strings.
        """
        lines = [
            "# WinX Menu Modification - Apply to all users and default profile",
            "Write-Host 'Modifying WinX menu for all users...' -ForegroundColor Yellow",
            "",
            "# Get all user profile paths",
            '$userProfiles = Get-ChildItem "C:\\Users" -Directory | Where-Object { $_.Name -notin @("Public", "Default", "All Users", "Default User") }',
            "",
            "# Modify WinX for each existing user",
            "foreach ($userProfile in $userProfiles) {",
            '    $winxPath = Join-Path $userProfile.FullName "AppData\\Local\\Microsoft\\Windows\\WinX"',
            "    if (Test-Path $winxPath) {",
            '        Write-Host "  Processing: $($userProfile.Name)" -ForegroundColor Cyan',
        ]

        for item in winx_removal:
            lines.append(
                f'        Remove-Item -Path "$winxPath\\*{item}*" -Recurse -Force -ErrorAction SilentlyContinue'
            )

        lines.extend(
            [
                "    }",
                "}",
                "",
                "# Modify default user profile for new users",
                '$defaultWinxPath = "C:\\Users\\Default\\AppData\\Local\\Microsoft\\Windows\\WinX"',
                "if (Test-Path $defaultWinxPath) {",
                '    Write-Host "  Processing: Default User Profile" -ForegroundColor Cyan',
            ]
        )

        for item in winx_removal:
            lines.append(
                f'    Remove-Item -Path "$defaultWinxPath\\*{item}*" -Recurse -Force -ErrorAction SilentlyContinue'
            )

        lines.extend(
            [
                "}",
                "",
                "# Restart Explorer to apply changes",
                "Stop-Process -ProcessName explorer -Force -ErrorAction SilentlyContinue",
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
