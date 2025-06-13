from datetime import datetime
from typing import Dict, Any
from generators.base_generator import BaseArtifactGenerator


class BatchGenerator(BaseArtifactGenerator):
    def generate(self, control_name: str, settings: Dict[str, Any]) -> str:
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
        return "bat"

    def get_mime_type(self) -> str:
        return "text/plain"
