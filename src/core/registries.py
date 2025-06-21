"""
Registries module for Streamlit-based Windows Security Controls Generator.

Defines the ControlRegistry and GeneratorRegistry classes, which manage registration
and lookup of security controls, UI renderers, and artifact generators.
"""

from typing import Dict, Optional, Type
from core.interfaces import (
    ISecurityControl,
    IArtifactGenerator,
    IUIRenderer,
    IControlRegistry,
    IGeneratorRegistry,
)


class ControlRegistry(IControlRegistry):
    """
    Registry for security controls and their associated UI renderers.

    Allows registration, lookup, and instantiation of controls and UI renderer classes.
    """

    def __init__(self):
        """
        Initialize the control and UI renderer registries.
        """
        self._controls: Dict[str, Type[ISecurityControl]] = {}
        self._ui_renderers: Dict[str, Type[IUIRenderer]] = {}

    def register_control(
        self,
        control_class: Type[ISecurityControl],
        ui_renderer_class: Type[IUIRenderer] = None,
    ):
        """
        Register a security control and its UI renderer.

        Args:
            control_class (Type[ISecurityControl]): The control class to register.
            ui_renderer_class (Type[IUIRenderer], optional): The UI renderer class to register.
        """
        control_instance = control_class()
        control_name = control_instance.get_metadata().name
        self._controls[control_name] = control_class

        if ui_renderer_class:
            self._ui_renderers[control_name] = ui_renderer_class

    def get_available_controls(self) -> Dict[str, Type[ISecurityControl]]:
        """
        Get a copy of all registered controls.

        Returns:
            Dict[str, Type[ISecurityControl]]: Mapping of control names to control classes.
        """
        return self._controls.copy()

    def create_control(self, control_name: str) -> ISecurityControl:
        """
        Instantiate a control by its registered name.

        Args:
            control_name (str): The name of the control to instantiate.

        Returns:
            ISecurityControl: An instance of the requested control.

        Raises:
            ValueError: If the control is not found in the registry.
        """
        if control_name not in self._controls:
            raise ValueError(f"Control '{control_name}' not found in registry")
        return self._controls[control_name]()

    def get_ui_renderer(self, control_name: str) -> Optional[IUIRenderer]:
        """
        Instantiate the UI renderer for a given control name.

        Args:
            control_name (str): The name of the control.

        Returns:
            Optional[IUIRenderer]: An instance of the UI renderer, or None if not found.
        """
        if control_name not in self._ui_renderers:
            return None
        return self._ui_renderers[control_name]()


class GeneratorRegistry(IGeneratorRegistry):
    """
    Registry for artifact generators.

    Allows registration, lookup, and compatibility checking for artifact generators.
    """

    def __init__(self):
        """
        Initialize the generator registry.
        """
        self._generators: Dict[str, IArtifactGenerator] = {}

    def register_generator(self, name: str, generator: IArtifactGenerator):
        """
        Register an artifact generator by name.

        Args:
            name (str): The name/type of the generator.
            generator (IArtifactGenerator): The generator instance.
        """
        self._generators[name] = generator

    def get_generator(self, name: str) -> Optional[IArtifactGenerator]:
        """
        Retrieve a generator by name.

        Args:
            name (str): The name/type of the generator.

        Returns:
            Optional[IArtifactGenerator]: The generator instance, or None if not found.
        """
        return self._generators.get(name)

    def get_all_generators(self) -> Dict[str, IArtifactGenerator]:
        """
        Get a copy of all registered generators.

        Returns:
            Dict[str, IArtifactGenerator]: Mapping of generator names to generator instances.
        """
        return self._generators.copy()

    def get_compatible_generators(
        self, settings: Dict[str, any]
    ) -> Dict[str, IArtifactGenerator]:
        """
        Get all generators compatible with the provided settings.

        Args:
            settings (Dict[str, any]): The settings to check compatibility against.

        Returns:
            Dict[str, IArtifactGenerator]: Mapping of compatible generator names to instances.
        """
        compatible = {}
        for name, generator in self._generators.items():
            if generator.supports_settings(settings):
                compatible[name] = generator
        return compatible
