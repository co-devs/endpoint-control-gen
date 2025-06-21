"""
gpo_generator.py

This module provides a generator for creating XML representations of Group Policy Objects (GPOs)
with support for file associations and firewall rules. The generated XML can be used for configuring
Windows environments via GPO.
"""
# TODO: Ensure generation of XML file that is actually compliant
# TODO: Differentiate between Win 11 and Win 10 files (Win 11 is not backwards compatible) or specify support for one

import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from typing import Dict, Any
from generators.base_generator import BaseArtifactGenerator


class GPOXMLGenerator(BaseArtifactGenerator):
    """
    Generates XML artifacts for Group Policy Objects (GPOs) based on provided settings.
    Supports file associations and firewall rules.
    """

    def generate(self, control_name: str, settings: Dict[str, Any]) -> str:
        """
        Generate a GPO XML string based on the control name and settings.

        Args:
            control_name (str): The name of the GPO control.
            settings (Dict[str, Any]): Dictionary containing GPO settings, such as
                'file_associations' and/or 'firewall_rules'.

        Returns:
            str: A pretty-printed XML string representing the GPO.
        """
        root = ET.Element("GroupPolicyObject")

        # Add a unique identifier using the current timestamp
        identifier = ET.SubElement(root, "Identifier")
        # TODO: Use a more robust UUID generation method
        identifier.text = (
            f"{{12345678-1234-5678-9012-{datetime.now().strftime('%Y%m%d%H%M')}}}"
        )

        # Set the domain for the GPO
        domain = ET.SubElement(root, "Domain")
        domain.text = "example.com"

        # Set the name of the GPO
        name = ET.SubElement(root, "Name")
        name.text = control_name

        # Add computer configuration section
        computer_config = ET.SubElement(root, "Computer")
        enabled = ET.SubElement(computer_config, "Enabled")
        enabled.text = "true"

        # Add extension data for additional settings
        extensions = ET.SubElement(computer_config, "ExtensionData")

        # Add file association settings if present
        if "file_associations" in settings:
            self._add_file_association_config(extensions, settings["file_associations"])

        # Add firewall rule settings if present
        if "firewall_rules" in settings:
            self._add_firewall_config(extensions, settings["firewall_rules"])

        # Convert the ElementTree to a pretty-printed XML string
        rough_string = ET.tostring(root, "unicode")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def _add_file_association_config(
        self, extensions: ET.Element, file_associations: Dict[str, str]
    ):
        """
        Add file association configuration to the GPO XML.

        Args:
            extensions (ET.Element): The parent XML element for extensions.
            file_associations (Dict[str, str]): Mapping of file extensions to associated applications.
        """
        registry_ext = ET.SubElement(extensions, "Registry")
        for ext, app in file_associations.items():
            policy = ET.SubElement(registry_ext, "Policy")
            policy.set("State", "Enabled")
            policy.set("Key", f"HKEY_CLASSES_ROOT\\{ext}")
            policy.set("ValueName", "")
            policy.set("Value", app)

    def _add_firewall_config(self, extensions: ET.Element, firewall_rules: list):
        """
        Add firewall rule configuration to the GPO XML.

        Args:
            extensions (ET.Element): The parent XML element for extensions.
            firewall_rules (list): List of firewall rule dictionaries, each containing
                'program' and 'name' keys.
        """
        firewall_ext = ET.SubElement(extensions, "WindowsDefenderFirewall")
        for rule in firewall_rules:
            rule_elem = ET.SubElement(firewall_ext, "InboundRule")
            rule_elem.set("Action", "Block")
            rule_elem.set("Program", rule["program"])
            rule_elem.set("Name", rule["name"])

    def get_file_extension(self) -> str:
        """
        Returns the file extension for the generated artifact.

        Returns:
            str: The file extension ('xml').
        """
        return "xml"

    def get_mime_type(self) -> str:
        """
        Returns the MIME type for the generated artifact.

        Returns:
            str: The MIME type ('text/xml').
        """
        return "text/xml"

    def supports_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Checks if the provided settings are supported by this generator.

        Args:
            settings (Dict[str, Any]): The settings dictionary.

        Returns:
            bool: True if supported settings are present, False otherwise.
        """
        return "file_associations" in settings or "firewall_rules" in settings
