from typing import Dict, Any
from core.interfaces import ISecurityControl, SecurityControlMetadata, RiskLevel


class BaseSecurityControl(ISecurityControl):
    def __init__(self, metadata: SecurityControlMetadata):
        self.metadata = metadata
        self._settings: Dict[str, Any] = {}

    @property
    def settings(self) -> Dict[str, Any]:
        return self._settings.copy()

    @settings.setter
    def settings(self, value: Dict[str, Any]) -> None:
        if self.validate_settings(value):
            self._settings = value
        else:
            raise ValueError(f"Invalid settings for {self.metadata.name}")

    def get_metadata(self) -> SecurityControlMetadata:
        return self.metadata

    def get_control_name(self) -> str:
        return self.metadata.name.replace(" ", "_")

    def get_risk_level_display(self) -> str:
        risk_colors = {
            RiskLevel.LOW: "risk-low",
            RiskLevel.MEDIUM: "risk-medium",
            RiskLevel.HIGH: "risk-high",
        }
        return f"<span class='{risk_colors[self.metadata.risk_level]}'>{self.metadata.risk_level.value.title()}</span>"
