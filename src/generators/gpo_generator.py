import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from typing import Dict, Any
from generators.base_generator import BaseArtifactGenerator


class GPOXMLGenerator(BaseArtifactGenerator):
    def generate(self, control_name: str, settings: Dict[str, Any]) -> str:
        root = ET.Element("GroupPolicyObject")

        identifier = ET.SubElement(root, "Identifier")
        identifier.text = (
            f"{{12345678-1234-5678-9012-{datetime.now().strftime('%Y%m%d%H%M')}}}"
        )

        domain = ET.SubElement(root, "Domain")
        domain.text = "example.com"

        name = ET.SubElement(root, "Name")
        name.text = control_name

        computer_config = ET.SubElement(root, "Computer")
        enabled = ET.SubElement(computer_config, "Enabled")
        enabled.text = "true"

        extensions = ET.SubElement(computer_config, "ExtensionData")

        if "file_associations" in settings:
            self._add_file_association_config(extensions, settings["file_associations"])

        if "firewall_rules" in settings:
            self._add_firewall_config(extensions, settings["firewall_rules"])

        rough_string = ET.tostring(root, "unicode")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def _add_file_association_config(
        self, extensions: ET.Element, file_associations: Dict[str, str]
    ):
        registry_ext = ET.SubElement(extensions, "Registry")
        for ext, app in file_associations.items():
            policy = ET.SubElement(registry_ext, "Policy")
            policy.set("State", "Enabled")
            policy.set("Key", f"HKEY_CLASSES_ROOT\\{ext}")
            policy.set("ValueName", "")
            policy.set("Value", app)

    def _add_firewall_config(self, extensions: ET.Element, firewall_rules: list):
        firewall_ext = ET.SubElement(extensions, "WindowsDefenderFirewall")
        for rule in firewall_rules:
            rule_elem = ET.SubElement(firewall_ext, "InboundRule")
            rule_elem.set("Action", "Block")
            rule_elem.set("Program", rule["program"])
            rule_elem.set("Name", rule["name"])

    def get_file_extension(self) -> str:
        return "xml"

    def get_mime_type(self) -> str:
        return "text/xml"

    def supports_settings(self, settings: Dict[str, Any]) -> bool:
        return "file_associations" in settings or "firewall_rules" in settings
