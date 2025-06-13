from typing import Dict, Any
from core.base_control import BaseSecurityControl
from core.interfaces import SecurityControlMetadata, RiskLevel


class WinXMenuControl(BaseSecurityControl):
    def __init__(self):
        metadata = SecurityControlMetadata(
            name="WinX Menu Hardening",
            description="Remove potentially dangerous entries from the Windows+X menu",
            risk_level=RiskLevel.LOW,
            purpose="Remove potentially dangerous entries from the Windows+X (WinX) menu to limit user access to administrative tools",
            common_targets=[
                "Command Prompt",
                "PowerShell",
                "Computer Management",
                "Event Viewer",
            ],
            category="User Interface Security",
        )
        super().__init__(metadata)

    def validate_settings(self, settings: Dict[str, Any]) -> bool:
        if "winx_removal" not in settings:
            return False

        winx_removal = settings["winx_removal"]
        if not isinstance(winx_removal, list):
            return False

        for item in winx_removal:
            if not isinstance(item, str) or not item.strip():
                return False

        return True

    def get_default_configuration(self) -> Dict[str, Any]:
        return {
            "winx_removal": ["Command Prompt (Admin)", "Windows PowerShell (Admin)"]
        }

    def get_configuration_schema(self) -> Dict[str, Any]:
        return {
            "winx_items": {
                "Command Prompt": "Command Prompt (Admin)",
                "PowerShell": "Windows PowerShell (Admin)",
                "Computer Management": "Computer Management",
                "Event Viewer": "Event Viewer",
                "Task Manager": "Task Manager",
                "Settings": "Settings",
                "File Explorer": "File Explorer",
                "Device Manager": "Device Manager",
                "Network Connections": "Network Connections",
                "Disk Management": "Disk Management",
            }
        }
