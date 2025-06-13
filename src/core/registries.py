from typing import Dict, Optional, Type
from core.interfaces import (
    ISecurityControl,
    IArtifactGenerator,
    IUIRenderer,
    IControlRegistry,
    IGeneratorRegistry,
)


class ControlRegistry(IControlRegistry):
    def __init__(self):
        self._controls: Dict[str, Type[ISecurityControl]] = {}
        self._ui_renderers: Dict[str, Type[IUIRenderer]] = {}

    def register_control(
        self,
        control_class: Type[ISecurityControl],
        ui_renderer_class: Type[IUIRenderer] = None,
    ):
        control_instance = control_class()
        control_name = control_instance.get_metadata().name
        self._controls[control_name] = control_class

        if ui_renderer_class:
            self._ui_renderers[control_name] = ui_renderer_class

    def get_available_controls(self) -> Dict[str, Type[ISecurityControl]]:
        return self._controls.copy()

    def create_control(self, control_name: str) -> ISecurityControl:
        if control_name not in self._controls:
            raise ValueError(f"Control '{control_name}' not found in registry")
        return self._controls[control_name]()

    def get_ui_renderer(self, control_name: str) -> Optional[IUIRenderer]:
        if control_name not in self._ui_renderers:
            return None
        return self._ui_renderers[control_name]()


class GeneratorRegistry(IGeneratorRegistry):
    def __init__(self):
        self._generators: Dict[str, IArtifactGenerator] = {}

    def register_generator(self, name: str, generator: IArtifactGenerator):
        self._generators[name] = generator

    def get_generator(self, name: str) -> Optional[IArtifactGenerator]:
        return self._generators.get(name)

    def get_all_generators(self) -> Dict[str, IArtifactGenerator]:
        return self._generators.copy()

    def get_compatible_generators(
        self, settings: Dict[str, any]
    ) -> Dict[str, IArtifactGenerator]:
        compatible = {}
        for name, generator in self._generators.items():
            if generator.supports_settings(settings):
                compatible[name] = generator
        return compatible
