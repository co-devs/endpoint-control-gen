"""
Example: Adding a new artifact generator to the modular application

This example shows how to create a new "Ansible Playbook" generator
that creates Ansible playbooks for Linux/Unix systems, and a "Terraform" generator
for generating Terraform configurations.
"""

from datetime import datetime
from typing import Dict, Any
from ..generators.base_generator import BaseArtifactGenerator


class AnsiblePlaybookGenerator(BaseArtifactGenerator):
    """
    Artifact generator for creating Ansible playbooks based on security control settings.
    """

    def generate(self, control_name: str, settings: Dict[str, Any]) -> str:
        """
        Generate an Ansible playbook as a string.

        Args:
            control_name (str): The name of the security control.
            settings (Dict[str, Any]): The settings for the control.

        Returns:
            str: The generated Ansible playbook content.
        """
        playbook_lines = [
            "---",
            f"# Ansible Playbook for {control_name}",
            f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "- name: Apply security control",
            "  hosts: all",
            "  become: yes",
            "  tasks:",
        ]

        # Add file association tasks if present
        if "file_associations" in settings:
            playbook_lines.extend(
                self._generate_file_tasks(settings["file_associations"])
            )

        # Add firewall rule tasks if present
        if "firewall_rules" in settings:
            playbook_lines.extend(
                self._generate_firewall_tasks(settings["firewall_rules"])
            )

        # Add registry modification tasks if present
        if "registry_modifications" in settings:
            playbook_lines.extend(
                self._generate_registry_tasks(settings["registry_modifications"])
            )

        return "\n".join(playbook_lines)

    def _generate_file_tasks(self, file_associations: Dict[str, str]) -> list:
        """
        Generate Ansible tasks for file associations.

        Args:
            file_associations (Dict[str, str]): Mapping of file extensions to applications.

        Returns:
            list: List of Ansible task lines.
        """
        tasks = [
            "",
            "    # File association security (Linux equivalent - MIME types)",
        ]

        for ext, app in file_associations.items():
            tasks.extend(
                [
                    f"    - name: Set default application for {ext} files",
                    f"      command: xdg-mime default {app} application/x-{ext[1:]}",
                    f'      become_user: "{{{{ item }}}}"',
                    f'      with_items: "{{{{ ansible_user_list }}}}"',
                    "",
                ]
            )

        return tasks

    def _generate_firewall_tasks(self, firewall_rules: list) -> list:
        """
        Generate Ansible tasks for firewall rules.

        Args:
            firewall_rules (list): List of firewall rule dictionaries.

        Returns:
            list: List of Ansible task lines.
        """
        tasks = [
            "",
            "    # Firewall rules using UFW",
        ]

        for rule in firewall_rules:
            binary_name = (
                rule["program"].split("\\")[-1]
                if "\\" in rule["program"]
                else rule["program"]
            )
            tasks.extend(
                [
                    f"    - name: Block outbound traffic for {binary_name}",
                    f"      ufw:",
                    f"        rule: deny",
                    f"        direction: out",
                    f"        port: any",
                    f"        proto: tcp",
                    f"        comment: \"{rule['name']}\"",
                    "",
                ]
            )

        return tasks

    def _generate_registry_tasks(self, registry_modifications: list) -> list:
        """
        Generate Ansible tasks for registry modifications (Linux equivalent).

        Args:
            registry_modifications (list): List of registry modification dictionaries.

        Returns:
            list: List of Ansible task lines.
        """
        tasks = [
            "",
            "    # Registry modifications (Linux equivalent - system configurations)",
        ]

        for mod in registry_modifications:
            tasks.extend(
                [
                    f"    - name: Apply system configuration for {mod['value_name']}",
                    f"      lineinfile:",
                    f"        path: /etc/security/limits.conf",
                    f"        line: \"# {mod['key']}:{mod['value_name']}={mod['value_data']}\"",
                    f"        create: yes",
                    "",
                ]
            )

        return tasks

    def get_file_extension(self) -> str:
        """
        Get the file extension for Ansible playbooks.

        Returns:
            str: The file extension ("yml").
        """
        return "yml"

    def get_mime_type(self) -> str:
        """
        Get the MIME type for Ansible playbooks.

        Returns:
            str: The MIME type ("text/yaml").
        """
        return "text/yaml"

    def supports_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Determine if this generator supports the provided settings.

        Args:
            settings (Dict[str, Any]): The settings to check.

        Returns:
            bool: True if supported, False otherwise.
        """
        supported_keys = {
            "file_associations",
            "firewall_rules",
            "registry_modifications",
        }
        return bool(supported_keys.intersection(settings.keys()))


class TerraformGenerator(BaseArtifactGenerator):
    """
    Artifact generator for creating Terraform configurations based on security control settings.
    """

    def generate(self, control_name: str, settings: Dict[str, Any]) -> str:
        """
        Generate a Terraform configuration as a string.

        Args:
            control_name (str): The name of the security control.
            settings (Dict[str, Any]): The settings for the control.

        Returns:
            str: The generated Terraform configuration content.
        """
        tf_lines = [
            f"# Terraform configuration for {control_name}",
            f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "terraform {",
            "  required_providers {",
            "    aws = {",
            '      source  = "hashicorp/aws"',
            '      version = "~> 5.0"',
            "    }",
            "  }",
            "}",
            "",
        ]

        # Add security group rules if firewall_rules are present
        if "firewall_rules" in settings:
            tf_lines.extend(self._generate_security_group(settings["firewall_rules"]))

        return "\n".join(tf_lines)

    def _generate_security_group(self, firewall_rules: list) -> list:
        """
        Generate Terraform security group egress rules for firewall settings.

        Args:
            firewall_rules (list): List of firewall rule dictionaries.

        Returns:
            list: List of Terraform configuration lines.
        """
        lines = [
            'resource "aws_security_group" "security_control" {',
            '  name_prefix = "security-control-"',
            '  description = "Security group for hardened instances"',
            "",
        ]

        for rule in firewall_rules:
            lines.extend(
                [
                    "  egress {",
                    "    from_port   = 0",
                    "    to_port     = 65535",
                    '    protocol    = "tcp"',
                    '    cidr_blocks = ["0.0.0.0/0"]',
                    f"    description = \"{rule['name']}\"",
                    "  }",
                    "",
                ]
            )

        lines.append("}")
        return lines

    def get_file_extension(self) -> str:
        """
        Get the file extension for Terraform configurations.

        Returns:
            str: The file extension ("tf").
        """
        return "tf"

    def get_mime_type(self) -> str:
        """
        Get the MIME type for Terraform configurations.

        Returns:
            str: The MIME type ("text/plain").
        """
        return "text/plain"

    def supports_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Determine if this generator supports the provided settings.

        Args:
            settings (Dict[str, Any]): The settings to check.

        Returns:
            bool: True if "firewall_rules" is present, False otherwise.
        """
        return "firewall_rules" in settings


# To register these new generators with the application:
"""
# In app_factory.py, add to create_generator_registry method:
registry.register_generator("ansible", AnsiblePlaybookGenerator())
registry.register_generator("terraform", TerraformGenerator())
"""
