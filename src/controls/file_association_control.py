from typing import Dict, Any, List
from core.base_control import BaseSecurityControl
from core.interfaces import SecurityControlMetadata, RiskLevel


class FileAssociationControl(BaseSecurityControl):
    def __init__(self):
        metadata = SecurityControlMetadata(
            name="File Association Security",
            description="Prevent execution of malicious files by changing default applications for commonly abused extensions",
            risk_level=RiskLevel.MEDIUM,
            purpose="Prevent execution of malicious files by changing default applications for commonly abused extensions",
            common_targets=[
                ".scr",
                ".pif",
                ".com",
                ".bat",
                ".cmd",
                ".vbs",
                ".js",
                ".jar",
            ],
            category="File System Security",
        )
        super().__init__(metadata)

    def validate_settings(self, settings: Dict[str, Any]) -> bool:
        if "file_associations" not in settings:
            return False

        file_assoc = settings["file_associations"]
        if not isinstance(file_assoc, dict):
            return False

        for ext, app in file_assoc.items():
            if not isinstance(ext, str) or not ext.startswith("."):
                return False
            if not isinstance(app, str) or not app.strip():
                return False

        return True

    def get_default_configuration(self) -> Dict[str, Any]:
        return {
            "file_associations": {
                ".scr": "notepad.exe",
                ".pif": "notepad.exe",
                ".com": "notepad.exe",
            }
        }

    def get_configuration_schema(self) -> Dict[str, Any]:
        return {
            "dangerous_extensions": {
                ".scr": "Screen saver files (often malicious)",
                ".pif": "Program Information Files",
                ".com": "DOS executable files",
                ".bat": "Batch files",
                ".cmd": "Command files",
                ".vbs": "VBScript files",
                ".js": "JavaScript files",
                ".jar": "Java Archive files",
            },
            "safe_applications": ["notepad.exe", "wordpad.exe", "Block execution"],
        }
