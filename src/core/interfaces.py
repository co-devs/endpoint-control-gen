from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

if TYPE_CHECKING:
    import streamlit as st


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class SecurityControlMetadata:
    name: str
    description: str
    risk_level: RiskLevel
    purpose: str
    common_targets: Optional[List[str]] = None
    category: Optional[str] = None


class ISecurityControl(ABC):
    @abstractmethod
    def get_metadata(self) -> SecurityControlMetadata:
        pass

    @abstractmethod
    def validate_settings(self, settings: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def get_default_configuration(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_configuration_schema(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_control_name(self) -> str:
        pass

    @property
    @abstractmethod
    def settings(self) -> Dict[str, Any]:
        pass

    @settings.setter
    @abstractmethod
    def settings(self, value: Dict[str, Any]) -> None:
        pass


class IArtifactGenerator(ABC):
    @abstractmethod
    def generate(self, control_name: str, settings: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def get_file_extension(self) -> str:
        pass

    @abstractmethod
    def get_mime_type(self) -> str:
        pass

    @abstractmethod
    def supports_settings(self, settings: Dict[str, Any]) -> bool:
        pass


class IUIRenderer(ABC):
    @abstractmethod
    def render_configuration(
        self, control: ISecurityControl
    ) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def can_render(self, control: ISecurityControl) -> bool:
        pass


class IControlRegistry(ABC):
    @abstractmethod
    def register_control(self, control_class: type, ui_renderer_class: type = None):
        pass

    @abstractmethod
    def get_available_controls(self) -> Dict[str, type]:
        pass

    @abstractmethod
    def create_control(self, control_name: str) -> ISecurityControl:
        pass

    @abstractmethod
    def get_ui_renderer(self, control_name: str) -> Optional[IUIRenderer]:
        pass


class IGeneratorRegistry(ABC):
    @abstractmethod
    def register_generator(self, name: str, generator: IArtifactGenerator):
        pass

    @abstractmethod
    def get_generator(self, name: str) -> Optional[IArtifactGenerator]:
        pass

    @abstractmethod
    def get_all_generators(self) -> Dict[str, IArtifactGenerator]:
        pass

    @abstractmethod
    def get_compatible_generators(
        self, settings: Dict[str, Any]
    ) -> Dict[str, IArtifactGenerator]:
        pass
