"""
base_generator.py

This module provides a base class for artifact generators, implementing the IArtifactGenerator
interface. It can be subclassed to create specific artifact generators for different formats.
"""

from abc import ABC
from typing import Dict, Any
from core.interfaces import IArtifactGenerator


class BaseArtifactGenerator(IArtifactGenerator):
    """
    Base class for artifact generators.

    By default, supports all settings. Subclasses should override methods as needed.
    """

    def supports_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Determines if the generator supports the provided settings.

        Args:
            settings (Dict[str, Any]): The settings to check.

        Returns:
            bool: True if supported (default), False otherwise.
        """
        return True
