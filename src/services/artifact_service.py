"""
artifact_service.py

This module provides the ArtifactService class, which is responsible for generating
artifacts for Windows security controls using registered generators, and packaging
them into a downloadable ZIP file. It also generates a README file with usage instructions.
"""

import zipfile
import io
from datetime import datetime
from typing import Dict, Any
from core.interfaces import IGeneratorRegistry
# TODO: Refactor code to allow for simpler artifact addition


class ArtifactService:
    """
    Service for generating and packaging artifacts for Windows security controls.
    Uses a generator registry to find compatible artifact generators.
    """

    def __init__(self, generator_registry: IGeneratorRegistry):
        """
        Initialize the ArtifactService.

        Args:
            generator_registry (IGeneratorRegistry): Registry of available artifact generators.
        """
        self.generator_registry = generator_registry

    def generate_all_artifacts(
        self, control_name: str, settings: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Generate all compatible artifacts for the given control and settings.

        Args:
            control_name (str): The name of the security control.
            settings (Dict[str, Any]): Settings for artifact generation.

        Returns:
            Dict[str, str]: Mapping of artifact type to generated content.
        """
        artifacts = {}
        # Retrieve all generators compatible with the provided settings
        compatible_generators = self.generator_registry.get_compatible_generators(
            settings
        )

        # Generate each artifact using its generator
        for artifact_type, generator in compatible_generators.items():
            artifacts[artifact_type] = generator.generate(control_name, settings)

        return artifacts

    def create_download_package(
        self, control_name: str, artifacts: Dict[str, str]
    ) -> bytes:
        """
        Package all generated artifacts and a README into a ZIP archive.

        Args:
            control_name (str): The name of the security control.
            artifacts (Dict[str, str]): Mapping of artifact type to content.

        Returns:
            bytes: The ZIP archive as bytes.
        """
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # Write each artifact to the ZIP file with an appropriate filename
            for artifact_type, content in artifacts.items():
                generator = self.generator_registry.get_generator(artifact_type)
                if generator:
                    # Determine filename based on artifact type
                    filename = f"{control_name}.{generator.get_file_extension()}"
                    if artifact_type == "gpo":
                        filename = f"{control_name}_GPO.xml"
                    elif artifact_type == "powershell":
                        filename = f"{control_name}_Script.ps1"
                    elif artifact_type == "registry":
                        filename = f"{control_name}_Registry.reg"
                    elif artifact_type == "batch":
                        filename = f"{control_name}_Deploy.bat"

                    zip_file.writestr(filename, content)

            # Add a README file with usage instructions
            readme_content = self._generate_readme(control_name)
            zip_file.writestr("README.txt", readme_content)

        return zip_buffer.getvalue()

    def _generate_readme(self, control_name: str) -> str:
        """
        Generate the content for the README file included in the ZIP package.

        Args:
            control_name (str): The name of the security control.

        Returns:
            str: The README content.
        """
        return f"""Windows Security Control Package
=================================

Control Name: {control_name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Files Included:
- {control_name}_GPO.xml: Group Policy Object export
- {control_name}_Script.ps1: PowerShell implementation script
- {control_name}_Registry.reg: Registry file for manual import
- {control_name}_Deploy.bat: Batch script for deployment

IMPORTANT: Always test these configurations in a non-production environment first!

Implementation Notes:
1. Run scripts with Administrator privileges
2. Backup your system before applying changes
3. Test thoroughly before deploying to production
4. Consider the impact on user workflows
"""
