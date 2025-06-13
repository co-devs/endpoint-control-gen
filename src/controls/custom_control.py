from typing import Dict, Any
from core.base_control import BaseSecurityControl
from core.interfaces import SecurityControlMetadata, RiskLevel


class CustomSecurityControl(BaseSecurityControl):
    def __init__(
        self,
        name: str = "Custom Control",
        description: str = "User-defined security control",
        risk_level: RiskLevel = RiskLevel.MEDIUM,
    ):
        metadata = SecurityControlMetadata(
            name=name,
            description=description,
            risk_level=risk_level,
            purpose=description,
            category="Custom",
        )
        super().__init__(metadata)

    def validate_settings(self, settings: Dict[str, Any]) -> bool:
        return isinstance(settings, dict)

    def get_default_configuration(self) -> Dict[str, Any]:
        return {}

    def get_configuration_schema(self) -> Dict[str, Any]:
        return {}
