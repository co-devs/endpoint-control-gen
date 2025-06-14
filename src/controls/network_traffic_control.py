from typing import Dict, Any
from core.base_control import BaseSecurityControl
from core.interfaces import SecurityControlMetadata, RiskLevel


class NetworkTrafficControl(BaseSecurityControl):
    RISKY_BINARIES = {
        "powershell.exe": {"description": "PowerShell executable", "path": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"},
        "cmd.exe": {"description": "Command Prompt executable", "path": "C:\\Windows\\System32\\cmd.exe"},
        "wscript.exe": {"description": "Windows Script Host", "path": "C:\\Windows\\System32\\wscript.exe"},
        "cscript.exe": {"description": "Console Script Host", "path": "C:\\Windows\\System32\\cscript.exe"},
        "regsvr32.exe": {"description": "Microsoft Register Server", "path": "C:\\Windows\\System32\\regsvr32.exe"},
        "rundll32.exe": {"description": "Windows Run DLL", "path": "C:\\Windows\\System32\\rundll32.exe"},
        "mshta.exe": {"description": "Microsoft HTML Application Host", "path": "C:\\Windows\\System32\\mshta.exe"},
        "bitsadmin.exe": {"description": "Background Intelligent Transfer Service", "path": "C:\\Windows\\System32\\bitsadmin.exe"},
    }

    def __init__(self):
        metadata = SecurityControlMetadata(
            name="Network Traffic Control",
            description="Block network traffic from commonly abused Windows binaries",
            risk_level=RiskLevel.HIGH,
            purpose="Block network traffic from commonly abused Windows binaries to prevent data exfiltration and C2 communication",
            common_targets=list(self.RISKY_BINARIES.keys()),
            category="Network Security",
        )
        super().__init__(metadata)

    def validate_settings(self, settings: Dict[str, Any]) -> bool:
        if "firewall_rules" not in settings:
            return False

        firewall_rules = settings["firewall_rules"]
        if not isinstance(firewall_rules, list):
            return False

        for rule in firewall_rules:
            if not isinstance(rule, dict):
                return False
            if "name" not in rule or "program" not in rule:
                return False
            if not isinstance(rule["name"], str) or not isinstance(
                rule["program"], str
            ):
                return False

        return True

    def get_default_configuration(self) -> Dict[str, Any]:
        return {
            "firewall_rules": [
                {
                    "name": f"Block_{binary_name.replace('.exe', '')}_Outbound",
                    "program": config["path"],
                }
                for binary_name, config in self.RISKY_BINARIES.items()
            ]
        }

    def get_configuration_schema(self) -> Dict[str, Any]:
        return {
            "risky_binaries": {
                binary_name: f"{config['description']} ({config['path']})"
                for binary_name, config in self.RISKY_BINARIES.items()
            }
        }
