from typing import Dict, Any
from core.base_control import BaseSecurityControl
from core.interfaces import SecurityControlMetadata, RiskLevel


class NetworkTrafficControl(BaseSecurityControl):
    RISKY_BINARIES = {
        "regsvr32.exe": {
            "description": "Windows component registration utility often abused for proxy execution",
            "paths": [
                "%SystemRoot%\\System32\\regsvr32.exe",
                "%SystemRoot%\\SysWOW64\\regsvr32.exe",
            ],
        },
        "mshta.exe": {
            "description": "Microsoft HTML Application host used to execute HTA files",
            "paths": [
                "%SystemRoot%\\System32\\mshta.exe",
                "%SystemRoot%\\SysWOW64\\mshta.exe",
            ],
        },
        "bitsadmin.exe": {
            "description": "Background transfer utility often abused for file downloads",
            "paths": [
                "%SystemRoot%\\System32\\bitsadmin.exe",
                "%SystemRoot%\\SysWOW64\\bitsadmin.exe",
            ],
        },
        "certutil.exe": {
            "description": "Certificate utility often abused for file downloads and encoding",
            "paths": [
                "%SystemRoot%\\System32\\certutil.exe",
                "%SystemRoot%\\SysWOW64\\certutil.exe",
            ],
        },
        "msbuild.exe": {
            "description": "Microsoft Build Engine that can execute malicious MSBuild project files",
            "paths": [
                "C:\\Windows\\Microsoft.NET\\Framework\\v2.0.50727\\Msbuild.exe",
                "C:\\Windows\\Microsoft.NET\\Framework64\\v2.0.50727\\Msbuild.exe",
                "C:\\Windows\\Microsoft.NET\\Framework\\v3.5\\Msbuild.exe",
                "C:\\Windows\\Microsoft.NET\\Framework64\\v3.5\\Msbuild.exe",
                "C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\Msbuild.exe",
                "C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\Msbuild.exe",
            ],
        },
        "hh.exe": {
            "description": "HTML Help executable that can be abused to execute malicious CHM files",
            "paths": [
                "%SystemRoot%\\System32\\hh.exe",
                "%SystemRoot%\\SysWOW64\\hh.exe",
            ],
        },
        "makecab.exe": {
            "description": "Cabinet file creation utility that can be abused for data exfiltration",
            "paths": [
                "%SystemRoot%\\System32\\makecab.exe",
                "%SystemRoot%\\SysWOW64\\makecab.exe",
            ],
        },
        "ieexec.exe": {
            "description": "Internet Explorer process launcher that can execute .NET applications",
            "paths": [
                "C:\\Windows\\Microsoft.NET\\Framework\\v2.0.50727\\ieexec.exe",
                "C:\\Windows\\Microsoft.NET\\Framework64\\v2.0.50727\\ieexec.exe",
            ],
        },
        "expand.exe": {
            "description": "File expansion utility that can be abused for file operations",
            "paths": [
                "%SystemRoot%\\System32\\expand.exe",
                "%SystemRoot%\\SysWOW64\\expand.exe",
            ],
        },
        "rundll32.exe": {
            "description": "Windows utility for running DLL functions, commonly abused",
            "paths": [
                "%SystemRoot%\\System32\\rundll32.exe",
                "%SystemRoot%\\SysWOW64\\rundll32.exe",
            ],
        },
        "powershell.exe": {
            "description": "Windows PowerShell executable",
            "paths": [
                "%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
                "%SystemRoot%\\SysWOW64\\WindowsPowerShell\\v1.0\\powershell.exe",
            ],
        },
        "cmd.exe": {
            "description": "Windows Command Prompt",
            "paths": [
                "%SystemRoot%\\System32\\cmd.exe",
                "%SystemRoot%\\SysWOW64\\cmd.exe",
            ],
        },
        "wscript.exe": {
            "description": "Windows Script Host for VBScript/JScript execution",
            "paths": [
                "%SystemRoot%\\System32\\wscript.exe",
                "%SystemRoot%\\SysWOW64\\wscript.exe",
            ],
        },
        "cscript.exe": {
            "description": "Command-line Windows Script Host",
            "paths": [
                "%SystemRoot%\\System32\\cscript.exe",
                "%SystemRoot%\\SysWOW64\\cscript.exe",
            ],
        },
        "msiexec.exe": {
            "description": "Windows Installer service that can execute malicious MSI packages",
            "paths": [
                "%SystemRoot%\\System32\\msiexec.exe",
                "%SystemRoot%\\SysWOW64\\msiexec.exe",
            ],
        },
    }

    def __init__(self):
        metadata = SecurityControlMetadata(
            name="LOLBIN Firewall Rules",
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
        rules = []
        for binary_name, config in self.RISKY_BINARIES.items():
            for path in config["paths"]:
                rules.append(
                    {
                        "name": f"Block_{binary_name.replace('.exe', '')}_{path.split('\\')[-2] if 'SysWOW64' in path or 'Framework64' in path else 'x86'}_Outbound",
                        "program": path,
                    }
                )
        return {"firewall_rules": rules}

    def get_configuration_schema(self) -> Dict[str, Any]:
        return {
            "risky_binaries": {
                binary_name: f"{config['description']} ({len(config['paths'])} paths)"
                for binary_name, config in self.RISKY_BINARIES.items()
            }
        }
