from abc import ABC
from typing import Dict, Any
from core.interfaces import IArtifactGenerator


class BaseArtifactGenerator(IArtifactGenerator):
    def supports_settings(self, settings: Dict[str, Any]) -> bool:
        return True
