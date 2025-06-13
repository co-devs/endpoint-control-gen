from typing import Dict, Any, Optional
import streamlit as st
from app_factory import AppFactory
from core.interfaces import ISecurityControl
from controls.custom_control import CustomSecurityControl


class ModularSecurityControlsApplication:
    def __init__(self):
        self.control_registry = AppFactory.create_control_registry()
        self.generator_registry = AppFactory.create_generator_registry()
        self.artifact_service = AppFactory.create_artifact_service(
            self.generator_registry
        )
        self.ui_service = AppFactory.create_ui_service(self.control_registry)

    def run(self):
        self.ui_service.setup_page_config()
        self.ui_service.setup_custom_css()
        self.ui_service.render_main_header()

        control_type = self.ui_service.render_sidebar()

        if control_type == "Custom Control":
            self._handle_custom_control()
        else:
            self._handle_standard_control(control_type)

    def _handle_standard_control(self, control_type: str):
        try:
            control = self.control_registry.create_control(control_type)

            self.ui_service.render_control_info(control)

            ui_renderer = self.control_registry.get_ui_renderer(control_type)
            if ui_renderer:
                config_data = ui_renderer.render_configuration(control)
            else:
                st.warning(f"No UI renderer found for {control_type}")
                return

            if config_data:
                control.settings = config_data

                control_name = control.get_control_name()
                artifacts = self.artifact_service.generate_all_artifacts(
                    control_name, control.settings
                )

                self.ui_service.render_artifacts_display(artifacts, control_name)

                package_data = self.artifact_service.create_download_package(
                    control_name, artifacts
                )
                self.ui_service.render_package_download(package_data, control_name)

        except ValueError as e:
            st.error(f"Configuration error: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    def _handle_custom_control(self):
        try:
            ui_renderer = self.control_registry.get_ui_renderer("Custom Control")
            if not ui_renderer:
                st.error("Custom control renderer not found")
                return

            control = CustomSecurityControl()
            self.ui_service.render_control_info(control)

            config_data = ui_renderer.render_configuration(control)

            if config_data:
                control_name = config_data["control_name"]
                control_description = config_data["control_description"]
                settings = config_data["settings"]

                custom_control = CustomSecurityControl(
                    control_name, control_description
                )
                custom_control.settings = settings

                artifacts = self.artifact_service.generate_all_artifacts(
                    control_name, settings
                )

                if artifacts:
                    self.ui_service.render_artifacts_display(artifacts, control_name)

                    package_data = self.artifact_service.create_download_package(
                        control_name, artifacts
                    )
                    self.ui_service.render_package_download(package_data, control_name)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


def main():
    app = ModularSecurityControlsApplication()
    app.run()


if __name__ == "__main__":
    main()
