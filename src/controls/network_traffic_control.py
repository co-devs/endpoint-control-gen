from typing import Dict, Any
from core.base_control import BaseSecurityControl
from core.interfaces import SecurityControlMetadata, RiskLevel


class NetworkTrafficControl(BaseSecurityControl):
    def __init__(self):
        metadata = SecurityControlMetadata(
            name="Network Traffic Control",
            description="Block network traffic from commonly abused Windows binaries",
            risk_level=RiskLevel.HIGH,
            purpose="Block network traffic from commonly abused Windows binaries to prevent data exfiltration and C2 communication",
            common_targets=[
                "powershell.exe",
                "cmd.exe",
                "wscript.exe",
                "cscript.exe",
                "regsvr32.exe",
                "rundll32.exe",
            ],
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
                    "name": "Block_powershell_Outbound",
                    "program": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
                },
                {
                    "name": "Block_cmd_Outbound",
                    "program": "C:\\Windows\\System32\\cmd.exe",
                },
            ]
        }

    def get_configuration_schema(self) -> Dict[str, Any]:
        return {
            "risky_binaries": {
                "powershell.exe": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
                "cmd.exe": "C:\\Windows\\System32\\cmd.exe",
                "wscript.exe": "C:\\Windows\\System32\\wscript.exe",
                "cscript.exe": "C:\\Windows\\System32\\cscript.exe",
                "regsvr32.exe": "C:\\Windows\\System32\\regsvr32.exe",
                "rundll32.exe": "C:\\Windows\\System32\\rundll32.exe",
                "mshta.exe": "C:\\Windows\\System32\\mshta.exe",
                "bitsadmin.exe": "C:\\Windows\\System32\\bitsadmin.exe",
            }
        }
