from datetime import datetime
from typing import Dict, Any
from generators.base_generator import BaseArtifactGenerator


class PowerShellGenerator(BaseArtifactGenerator):
    def generate(self, control_name: str, settings: Dict[str, Any]) -> str:
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

        if "file_associations" in settings:
            script_lines.extend(
                self._generate_file_association_script(settings["file_associations"])
            )

        if "firewall_rules" in settings:
            script_lines.extend(
                self._generate_firewall_script(settings["firewall_rules"])
            )

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
        return "ps1"

    def get_mime_type(self) -> str:
        return "text/plain"
