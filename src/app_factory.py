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
    @staticmethod
    def create_control_registry() -> ControlRegistry:
        registry = ControlRegistry()

        registry.register_control(FileAssociationControl, FileAssociationRenderer)
        registry.register_control(NetworkTrafficControl, NetworkTrafficRenderer)
        registry.register_control(WinXMenuControl, WinXMenuRenderer)
        registry.register_control(CustomSecurityControl, CustomRenderer)

        return registry

    @staticmethod
    def create_generator_registry() -> GeneratorRegistry:
        registry = GeneratorRegistry()

        registry.register_generator("gpo", GPOXMLGenerator())
        registry.register_generator("powershell", PowerShellGenerator())
        registry.register_generator("registry", RegistryGenerator())
        registry.register_generator("batch", BatchGenerator())

        return registry

    @staticmethod
    def create_artifact_service(
        generator_registry: GeneratorRegistry,
    ) -> ArtifactService:
        return ArtifactService(generator_registry)

    @staticmethod
    def create_ui_service(control_registry: ControlRegistry) -> UIService:
        return UIService(control_registry)
