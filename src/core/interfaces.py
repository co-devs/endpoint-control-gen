"""
interfaces.py

This module defines abstract base classes (interfaces) and data structures for the core
components of the security control generation system. These interfaces standardize how
security controls, artifact generators, UI renderers, and registries interact.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

if TYPE_CHECKING:
    import streamlit as st


class RiskLevel(Enum):
    """
    Enum representing the risk level of a security control.
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class SecurityControlMetadata:
    """
    Data class for storing metadata about a security control.
    """
    name: str
    description: str
    risk_level: RiskLevel
    purpose: str
    common_targets: Optional[List[str]] = None
    category: Optional[str] = None


class ISecurityControl(ABC):
    """
    Interface for a security control.
    Implementations must provide metadata, validation, configuration, and settings management.
    """

    @abstractmethod
    def get_metadata(self) -> SecurityControlMetadata:
        """
        Returns metadata describing the security control.
        """
        pass

    @abstractmethod
    def validate_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Validates the provided settings for the control.

        Args:
            settings (Dict[str, Any]): The settings to validate.

        Returns:
            bool: True if settings are valid, False otherwise.
        """
        pass

    @abstractmethod
    def get_default_configuration(self) -> Dict[str, Any]:
        """
        Returns the default configuration for the control.
        """
        pass

    @abstractmethod
    def get_configuration_schema(self) -> Dict[str, Any]:
        """
        Returns a schema describing the configuration options for the control.
        """
        pass

    @abstractmethod
    def get_control_name(self) -> str:
        """
        Returns the unique name of the control.
        """
        pass

    @property
    @abstractmethod
    def settings(self) -> Dict[str, Any]:
        """
        Gets the current settings for the control.
        """
        pass

    @settings.setter
    @abstractmethod
    def settings(self, value: Dict[str, Any]) -> None:
        """
        Sets the current settings for the control.

        Args:
            value (Dict[str, Any]): The new settings.
        """
        pass


class IArtifactGenerator(ABC):
    """
    Interface for artifact generators that produce configuration artifacts (e.g., scripts, XML).
    """

    @abstractmethod
    def generate(self, control_name: str, settings: Dict[str, Any]) -> str:
        """
        Generate the artifact content based on the control name and settings.

        Args:
            control_name (str): The name of the control.
            settings (Dict[str, Any]): The settings for artifact generation.

        Returns:
            str: The generated artifact content.
        """
        pass

    @abstractmethod
    def get_file_extension(self) -> str:
        """
        Returns the file extension for the generated artifact.
        """
        pass

    @abstractmethod
    def get_mime_type(self) -> str:
        """
        Returns the MIME type for the generated artifact.
        """
        pass

    @abstractmethod
    def supports_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Checks if the generator supports the provided settings.

        Args:
            settings (Dict[str, Any]): The settings to check.

        Returns:
            bool: True if supported, False otherwise.
        """
        pass


class IUIRenderer(ABC):
    """
    Interface for UI renderer classes that render configuration UIs for controls.
    """

    @abstractmethod
    def render_configuration(
        self, control: ISecurityControl
    ) -> Optional[Dict[str, Any]]:
        """
        Render the configuration UI for the given control.

        Args:
            control (ISecurityControl): The control to render.

        Returns:
            Optional[Dict[str, Any]]: The updated settings, or None if unchanged.
        """
        pass

    @abstractmethod
    def can_render(self, control: ISecurityControl) -> bool:
        """
        Determines if this renderer can render the given control.

        Args:
            control (ISecurityControl): The control to check.

        Returns:
            bool: True if rendering is supported, False otherwise.
        """
        pass


class IControlRegistry(ABC):
    """
    Interface for a registry that manages available security controls and their UI renderers.
    """

    @abstractmethod
    def register_control(self, control_class: type, ui_renderer_class: type = None):
        """
        Register a new control and optionally its UI renderer.

        Args:
            control_class (type): The control class to register.
            ui_renderer_class (type, optional): The UI renderer class to register.
        """
        pass

    @abstractmethod
    def get_available_controls(self) -> Dict[str, type]:
        """
        Returns a mapping of control names to control classes.
        """
        pass

    @abstractmethod
    def create_control(self, control_name: str) -> ISecurityControl:
        """
        Instantiate a control by its name.

        Args:
            control_name (str): The name of the control.

        Returns:
            ISecurityControl: The instantiated control.
        """
        pass

    @abstractmethod
    def get_ui_renderer(self, control_name: str) -> Optional[IUIRenderer]:
        """
        Get the UI renderer for a given control name.

        Args:
            control_name (str): The name of the control.

        Returns:
            Optional[IUIRenderer]: The UI renderer, or None if not found.
        """
        pass


class IGeneratorRegistry(ABC):
    """
    Interface for a registry that manages artifact generators.
    """

    @abstractmethod
    def register_generator(self, name: str, generator: IArtifactGenerator):
        """
        Register a new artifact generator.

        Args:
            name (str): The name of the generator.
            generator (IArtifactGenerator): The generator instance.
        """
        pass

    @abstractmethod
    def get_generator(self, name: str) -> Optional[IArtifactGenerator]:
        """
        Retrieve a generator by name.

        Args:
            name (str): The name of the generator.

        Returns:
            Optional[IArtifactGenerator]: The generator instance, or None if not found.
        """
        pass

    @abstractmethod
    def get_all_generators(self) -> Dict[str, IArtifactGenerator]:
        """
        Returns all registered generators as a mapping from name to generator.
        """
        pass

    @abstractmethod
    def get_compatible_generators(
        self, settings: Dict[str, Any]
    ) -> Dict[str, IArtifactGenerator]:
        """
        Returns all generators compatible with the provided settings.

        Args:
            settings (Dict[str, Any]): The settings to check.

        Returns:
            Dict[str, IArtifactGenerator]: Mapping of generator names to compatible generators.
        """
        pass
