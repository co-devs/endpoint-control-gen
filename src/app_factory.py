"""
App Factory module for Streamlit-based Windows Security Controls Generator.

Defines the AppFactory class, which provides static methods to create and configure
registries, services, and UI components for the application.
"""

from core.registries import ControlRegistry, GeneratorRegistry
from services.artifact_service import ArtifactService
from services.ui_service import UIService

from controls.file_association_control import FileAssociationControl
from controls.network_traffic_control import NetworkTrafficControl
from controls.winx_menu_control import WinXMenuControl
from controls.custom_control import CustomSecurityControl

from generators.gpo_generator import GPOXMLGenerator
from generators.powershell_generator import PowerShellGenerator
from generators.registry_generator import RegistryGenerator
from generators.batch_generator import BatchGenerator

from ui.file_association_renderer import FileAssociationRenderer
from ui.network_traffic_renderer import NetworkTrafficRenderer
from ui.winx_menu_renderer import WinXMenuRenderer
from ui.custom_renderer import CustomRenderer


class AppFactory:
    """
    Factory class for creating and configuring application components.

    Provides static methods to instantiate control registries, generator registries,
    artifact services, and UI services.
    """

    @staticmethod
    def create_control_registry() -> ControlRegistry:
        """
        Create and configure the control registry with available controls and renderers.

        Returns:
            ControlRegistry: The configured control registry.
        """
        registry = ControlRegistry()

        # Register each control with its corresponding renderer
        registry.register_control(FileAssociationControl, FileAssociationRenderer)
        registry.register_control(NetworkTrafficControl, NetworkTrafficRenderer)
        registry.register_control(WinXMenuControl, WinXMenuRenderer)
        registry.register_control(CustomSecurityControl, CustomRenderer)

        return registry

    @staticmethod
    def create_generator_registry() -> GeneratorRegistry:
        """
        Create and configure the generator registry with available artifact generators.

        Returns:
            GeneratorRegistry: The configured generator registry.
        """
        registry = GeneratorRegistry()

        # Register each artifact generator by type
        registry.register_generator("gpo", GPOXMLGenerator())
        registry.register_generator("powershell", PowerShellGenerator())
        registry.register_generator("registry", RegistryGenerator())
        registry.register_generator("batch", BatchGenerator())

        return registry

    @staticmethod
    def create_artifact_service(
        generator_registry: GeneratorRegistry,
    ) -> ArtifactService:
        """
        Create the artifact service using the provided generator registry.

        Args:
            generator_registry (GeneratorRegistry): The generator registry to use.

        Returns:
            ArtifactService: The artifact service instance.
        """
        return ArtifactService(generator_registry)

    @staticmethod
    def create_ui_service(control_registry: ControlRegistry) -> UIService:
        """
        Create the UI service using the provided control registry.

        Args:
            control_registry (ControlRegistry): The control registry to use.

        Returns:
            UIService: The UI service instance.
        """
        return UIService(control_registry)
