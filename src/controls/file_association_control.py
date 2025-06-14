from typing import Dict, Any, List
from core.base_control import BaseSecurityControl
from core.interfaces import SecurityControlMetadata, RiskLevel


class FileAssociationControl(BaseSecurityControl):
    DANGEROUS_EXTENSIONS = {
        ".scr": {"description": "Screen saver files (often malicious)", "default_app": "notepad.exe"},
        # ".pif": {"description": "Program Information Files", "default_app": "notepad.exe"},
        # ".com": {"description": "DOS executable files", "default_app": "notepad.exe"},
        ".cab": {"description": "Cabinet files", "default_app": "notepad.exe"},
        ".appx": {"description": "AppX package files", "default_app": "notepad.exe"},
        ".ps1": {"description": "PowerShell script files", "default_app": "notepad.exe"},
        ".bat": {"description": "Batch files", "default_app": "notepad.exe"},
        ".cmd": {"description": "Command files", "default_app": "notepad.exe"},
        ".vbs": {"description": "VBScript files", "default_app": "notepad.exe"},
        ".vbe": {"description": "VBScript Encoded Script files", "default_app": "notepad.exe"},
        ".hta": {"description": "HTML Application files", "default_app": "notepad.exe"},
        ".shs": {"description": "Shell Scrap Object files", "default_app": "notepad.exe"},
        ".shb": {"description": "Shell Scrap files", "default_app": "notepad.exe"},
        ".js": {"description": "JavaScript files", "default_app": "notepad.exe"},
        ".jse": {"description": "JScript Encoded Script files", "default_app": "notepad.exe"},
        ".jar": {"description": "Java Archive files", "default_app": "notepad.exe"},
        ".wsh": {"description": "Windows Script Host files", "default_app": "notepad.exe"},
        ".wsc": {"description": "Windows Script Component files", "default_app": "notepad.exe"},
        ".wsf": {"description": "Windows Script Files", "default_app": "notepad.exe"},
        ".sct": {"description": "Windows Scriptlet files", "default_app": "notepad.exe"},
        ".chm": {"description": "Compiled HTML Help files", "default_app": "notepad.exe"},
        ".iso": {"description": "ISO image files", "default_app": "notepad.exe"},
    }

    def __init__(self):
        metadata = SecurityControlMetadata(
            name="File Association Security",
            description="Prevent execution of malicious files by changing default applications for commonly abused extensions",
            risk_level=RiskLevel.LOW,
            purpose="Prevent execution of malicious files by changing default applications for commonly abused extensions",
            common_targets=list(self.DANGEROUS_EXTENSIONS.keys()),
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
                ext: config["default_app"] 
                for ext, config in self.DANGEROUS_EXTENSIONS.items()
            }
        }

    def get_configuration_schema(self) -> Dict[str, Any]:
        return {
            "dangerous_extensions": {
                ext: config["description"] 
                for ext, config in self.DANGEROUS_EXTENSIONS.items()
            },
            "safe_applications": ["notepad.exe", "wordpad.exe", "Block execution"],
        }
