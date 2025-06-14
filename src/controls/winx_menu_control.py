from typing import Dict, Any
from core.base_control import BaseSecurityControl
from core.interfaces import SecurityControlMetadata, RiskLevel


class WinXMenuControl(BaseSecurityControl):
    WINX_ITEMS = {
        "Command Prompt": {"description": "Command Prompt with admin privileges", "menu_name": "Command Prompt (Admin)"},
        "PowerShell": {"description": "PowerShell with admin privileges", "menu_name": "Windows PowerShell (Admin)"},
        "Computer Management": {"description": "Computer Management console", "menu_name": "Computer Management"},
        "Event Viewer": {"description": "Windows Event Viewer", "menu_name": "Event Viewer"},
        "Task Manager": {"description": "Windows Task Manager", "menu_name": "Task Manager"},
        "Settings": {"description": "Windows Settings app", "menu_name": "Settings"},
        "File Explorer": {"description": "Windows File Explorer", "menu_name": "File Explorer"},
        "Device Manager": {"description": "Device Manager console", "menu_name": "Device Manager"},
        "Network Connections": {"description": "Network Connections settings", "menu_name": "Network Connections"},
        "Disk Management": {"description": "Disk Management console", "menu_name": "Disk Management"},
    }

    def __init__(self):
        metadata = SecurityControlMetadata(
            name="WinX Menu Hardening",
            description="Remove potentially dangerous entries from the Windows+X menu",
            risk_level=RiskLevel.LOW,
            purpose="Remove potentially dangerous entries from the Windows+X (WinX) menu to limit user access to administrative tools",
            common_targets=list(self.WINX_ITEMS.keys()),
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
        default_removals = ["Command Prompt", "PowerShell"]
        return {
            "winx_removal": [
                self.WINX_ITEMS[item]["menu_name"]
                for item in default_removals
                if item in self.WINX_ITEMS
            ]
        }

    def get_configuration_schema(self) -> Dict[str, Any]:
        return {
            "winx_items": {
                item_key: config["menu_name"]
                for item_key, config in self.WINX_ITEMS.items()
            }
        }
