from datetime import datetime
from typing import Dict, Any
from generators.base_generator import BaseArtifactGenerator


class RegistryGenerator(BaseArtifactGenerator):
    def generate(self, control_name: str, settings: Dict[str, Any]) -> str:
        reg_lines = [
            "Windows Registry Editor Version 5.00",
            "",
            f"; Windows Security Control: {control_name}",
            f"; Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]

        if "file_associations" in settings:
            reg_lines.append("; File Association Changes")
            for ext, app in settings["file_associations"].items():
                reg_lines.extend(
                    [
                        f"[HKEY_CLASSES_ROOT\\{ext}]",
                        f'@="{app}File"',
                        "",
                        f"[HKEY_CLASSES_ROOT\\{app}File\\shell\\open\\command]",
                        f'@="{app} \\"%1\\""',
                        "",
                    ]
                )

        return "\n".join(reg_lines)

    def get_file_extension(self) -> str:
        return "reg"

    def get_mime_type(self) -> str:
        return "text/plain"

    def supports_settings(self, settings: Dict[str, Any]) -> bool:
        return "file_associations" in settings
