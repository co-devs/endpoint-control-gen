"""
Base Security Control module for Streamlit-based Windows Security Controls Generator.

Defines the BaseSecurityControl class, which provides a foundation for all security controls,
including metadata management, settings validation, and risk level display.
"""

from typing import Dict, Any
from core.interfaces import ISecurityControl, SecurityControlMetadata, RiskLevel


class BaseSecurityControl(ISecurityControl):
    """
    Base class for all security controls.

    Handles metadata, settings management, and risk level display formatting.
    """

    def __init__(self, metadata: SecurityControlMetadata):
        """
        Initialize the base security control with metadata.

        Args:
            metadata (SecurityControlMetadata): Metadata describing the control.
        """
        self.metadata = metadata
        self._settings: Dict[str, Any] = {}

    @property
    def settings(self) -> Dict[str, Any]:
        """
        Get a copy of the current settings.

        Returns:
            Dict[str, Any]: The current settings dictionary.
        """
        return self._settings.copy()

    @settings.setter
    def settings(self, value: Dict[str, Any]) -> None:
        """
        Set the control's settings after validating them.

        Args:
            value (Dict[str, Any]): The settings to apply.

        Raises:
            ValueError: If the settings are invalid for this control.
        """
        if self.validate_settings(value):
            self._settings = value
        else:
            raise ValueError(f"Invalid settings for {self.metadata.name}")

    def get_metadata(self) -> SecurityControlMetadata:
        """
        Retrieve the metadata for this control.

        Returns:
            SecurityControlMetadata: The control's metadata.
        """
        return self.metadata

    def get_control_name(self) -> str:
        """
        Get a safe control name for use in filenames and identifiers.

        Returns:
            str: The control name with spaces replaced by underscores.
        """
        return self.metadata.name.replace(" ", "_")

    def get_risk_level_display(self) -> str:
        """
        Get an HTML-formatted string representing the control's risk level.

        Returns:
            str: The risk level as a colored HTML span.
        """
        risk_colors = {
            RiskLevel.LOW: "risk-low",
            RiskLevel.MEDIUM: "risk-medium",
            RiskLevel.HIGH: "risk-high",
        }
        return f"<span class='{risk_colors[self.metadata.risk_level]}'>{self.metadata.risk_level.value.title()}</span>"
