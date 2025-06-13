# Extension Guide

Complete step-by-step instructions for adding new security controls and generators to the application.

## Adding New Security Controls

### Step 1: Create the Control Class

Create a new file in `src/controls/` (e.g., `my_security_control.py`):

```python
from typing import Dict, Any
from core.base_control import BaseSecurityControl
from core.interfaces import SecurityControlMetadata, RiskLevel

class MySecurityControl(BaseSecurityControl):
    def __init__(self):
        metadata = SecurityControlMetadata(
            name="My Security Control",
            description="Brief description of what this control does",
            risk_level=RiskLevel.MEDIUM,  # LOW, MEDIUM, or HIGH
            purpose="Detailed explanation of security objective",
            common_targets=["target1", "target2"],  # Optional
            category="Security Category"  # Optional
        )
        super().__init__(metadata)
    
    def validate_settings(self, settings: Dict[str, Any]) -> bool:
        """Validate user configuration input"""
        # Example validation logic
        if "required_field" not in settings:
            return False
        
        # Add your validation logic here
        return True
    
    def get_default_configuration(self) -> Dict[str, Any]:
        """Provide default configuration values"""
        return {
            "required_field": "default_value",
            "optional_field": "default_optional"
        }
    
    def get_configuration_schema(self) -> Dict[str, Any]:
        """Define UI schema for configuration form"""
        return {
            "field_options": {
                "option1": "Description of option 1",
                "option2": "Description of option 2"
            },
            "field_types": {
                "text_field": "string",
                "numeric_field": "number",
                "boolean_field": "boolean"
            }
        }
```

### Step 2: Create the UI Renderer

Create a corresponding renderer in `src/ui/` (e.g., `my_security_renderer.py`):

```python
import streamlit as st
from typing import Dict, Any, Optional
from ui.base_renderer import BaseUIRenderer
from core.interfaces import ISecurityControl
from controls.my_security_control import MySecurityControl

class MySecurityRenderer(BaseUIRenderer):
    def can_render(self, control: ISecurityControl) -> bool:
        """Check if this renderer can handle the control type"""
        return isinstance(control, MySecurityControl)
    
    def render_configuration(self, control: ISecurityControl) -> Optional[Dict[str, Any]]:
        """Render the configuration form"""
        st.subheader("Configuration")
        
        # Get schema from control
        schema = control.get_configuration_schema()
        
        # Create form elements based on schema
        settings = {}
        
        # Example: Text input
        text_value = st.text_input(
            "Text Field Label",
            value="",
            help="Help text for this field"
        )
        if text_value:
            settings["text_field"] = text_value
        
        # Example: Selectbox
        options = list(schema["field_options"].keys())
        selected_option = st.selectbox(
            "Select Option",
            options,
            help="Choose from available options"
        )
        if selected_option:
            settings["selected_option"] = selected_option
        
        # Example: Checkbox
        checkbox_value = st.checkbox(
            "Enable Feature",
            value=False,
            help="Check to enable this feature"
        )
        settings["feature_enabled"] = checkbox_value
        
        # Example: Number input
        number_value = st.number_input(
            "Numeric Value",
            min_value=0,
            max_value=100,
            value=10,
            help="Enter a number between 0 and 100"
        )
        settings["numeric_value"] = number_value
        
        # Example: Multi-select
        multi_options = st.multiselect(
            "Multiple Selection",
            options=["Option A", "Option B", "Option C"],
            help="Select multiple options"
        )
        if multi_options:
            settings["multi_selection"] = multi_options
        
        # Only return settings if required fields are filled
        if text_value:  # Check required fields
            return settings
        
        return None
```

### Step 3: Register the Control

Update `src/app_factory.py` to register your new control:

```python
# Add import at the top
from controls.my_security_control import MySecurityControl
from ui.my_security_renderer import MySecurityRenderer

class AppFactory:
    @staticmethod
    def create_control_registry() -> ControlRegistry:
        registry = ControlRegistry()
        
        # Existing registrations...
        registry.register_control(FileAssociationControl, FileAssociationRenderer)
        registry.register_control(NetworkTrafficControl, NetworkTrafficRenderer)
        registry.register_control(WinXMenuControl, WinXMenuRenderer)
        registry.register_control(CustomSecurityControl, CustomRenderer)
        
        # Add your new control
        registry.register_control(MySecurityControl, MySecurityRenderer)
        
        return registry
```

### Step 4: Test the Control

1. **Run the application**: `streamlit run src/main.py`
2. **Check sidebar**: Your control should appear in the dropdown
3. **Test configuration**: Verify the UI form works correctly
4. **Test validation**: Try invalid inputs to ensure validation works
5. **Test generation**: Ensure compatible generators create artifacts

## Adding New Generators

### Step 1: Create the Generator Class

Create a new file in `src/generators/` (e.g., `my_generator.py`):

```python
from typing import Dict, Any
from generators.base_generator import BaseArtifactGenerator

class MyCustomGenerator(BaseArtifactGenerator):
    def generate(self, control_name: str, settings: Dict[str, Any]) -> str:
        """Generate artifact content from control settings"""
        
        # Start building the output
        output_lines = [
            f"# Generated artifact for {control_name}",
            f"# Created by My Custom Generator",
            f"# Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ""
        ]
        
        # Process different types of settings
        if "text_field" in settings:
            output_lines.append(f"text_setting={settings['text_field']}")
        
        if "numeric_value" in settings:
            output_lines.append(f"numeric_setting={settings['numeric_value']}")
        
        if "feature_enabled" in settings and settings["feature_enabled"]:
            output_lines.append("feature_status=enabled")
        
        if "multi_selection" in settings:
            for item in settings["multi_selection"]:
                output_lines.append(f"selected_item={item}")
        
        # Handle file associations (common setting type)
        if "file_associations" in settings:
            output_lines.append("\n# File Associations")
            for ext, app in settings["file_associations"].items():
                output_lines.append(f"associate {ext} with {app}")
        
        # Handle firewall rules (common setting type)  
        if "firewall_rules" in settings:
            output_lines.append("\n# Firewall Rules")
            for rule in settings["firewall_rules"]:
                output_lines.append(f"block {rule['program']} - {rule['name']}")
        
        return "\n".join(output_lines)
    
    def get_file_extension(self) -> str:
        """Return file extension for generated artifacts"""
        return "txt"  # or "conf", "yaml", "json", etc.
    
    def get_mime_type(self) -> str:
        """Return MIME type for downloads"""
        return "text/plain"  # or "application/json", "text/yaml", etc.
    
    def supports_settings(self, settings: Dict[str, Any]) -> bool:
        """Check if this generator can process the given settings"""
        # Define which settings this generator can handle
        supported_keys = {
            "text_field", 
            "numeric_value", 
            "feature_enabled",
            "file_associations",
            "firewall_rules"
        }
        
        # Return True if any supported setting is present
        return bool(supported_keys.intersection(settings.keys()))
```

### Step 2: Register the Generator

Update `src/app_factory.py` to register your new generator:

```python
# Add import at the top
from generators.my_generator import MyCustomGenerator

class AppFactory:
    @staticmethod
    def create_generator_registry() -> GeneratorRegistry:
        registry = GeneratorRegistry()
        
        # Existing registrations...
        registry.register_generator("gpo", GPOXMLGenerator())
        registry.register_generator("powershell", PowerShellGenerator())
        registry.register_generator("registry", RegistryGenerator())
        registry.register_generator("batch", BatchGenerator())
        
        # Add your new generator
        registry.register_generator("my_custom", MyCustomGenerator())
        
        return registry
```

### Step 3: Update Artifact Service (Optional)

If you want custom file naming, update `src/services/artifact_service.py`:

```python
def create_download_package(self, control_name: str, artifacts: Dict[str, str]) -> bytes:
    # ... existing code ...
    
    for artifact_type, content in artifacts.items():
        generator = self.generator_registry.get_generator(artifact_type)
        if generator:
            filename = f"{control_name}.{generator.get_file_extension()}"
            
            # Existing custom naming...
            if artifact_type == "gpo":
                filename = f"{control_name}_GPO.xml"
            elif artifact_type == "powershell":
                filename = f"{control_name}_Script.ps1"
            elif artifact_type == "registry":
                filename = f"{control_name}_Registry.reg"
            elif artifact_type == "batch":
                filename = f"{control_name}_Deploy.bat"
            # Add your custom naming
            elif artifact_type == "my_custom":
                filename = f"{control_name}_Custom.txt"
```

## Advanced Generator Examples

### JSON Configuration Generator

```python
import json
from datetime import datetime

class JSONConfigGenerator(BaseArtifactGenerator):
    def generate(self, control_name: str, settings: Dict[str, Any]) -> str:
        config = {
            "control_name": control_name,
            "generated_at": datetime.now().isoformat(),
            "settings": settings,
            "metadata": {
                "version": "1.0",
                "format": "json_config"
            }
        }
        return json.dumps(config, indent=2)
    
    def get_file_extension(self) -> str:
        return "json"
    
    def get_mime_type(self) -> str:
        return "application/json"
    
    def supports_settings(self, settings: Dict[str, Any]) -> bool:
        return True  # JSON can handle any settings
```

### Docker Compose Generator

```python
class DockerComposeGenerator(BaseArtifactGenerator):
    def generate(self, control_name: str, settings: Dict[str, Any]) -> str:
        compose_lines = [
            "version: '3.8'",
            "",
            "services:",
            f"  {control_name.lower().replace(' ', '-')}:",
            "    image: security-hardened:latest",
            "    environment:",
        ]
        
        # Convert settings to environment variables
        for key, value in settings.items():
            if isinstance(value, (str, int, bool)):
                compose_lines.append(f"      - {key.upper()}={value}")
        
        return "\n".join(compose_lines)
    
    def get_file_extension(self) -> str:
        return "yml"
    
    def get_mime_type(self) -> str:
        return "text/yaml"
    
    def supports_settings(self, settings: Dict[str, Any]) -> bool:
        # Only support if settings contain simple key-value pairs
        return all(isinstance(v, (str, int, bool)) for v in settings.values())
```

## Testing Your Extensions

### Manual Testing Checklist

#### For New Controls

- [ ] Control appears in sidebar dropdown
- [ ] Configuration form renders correctly
- [ ] All form fields work as expected
- [ ] Validation prevents invalid submissions
- [ ] Settings are passed correctly to generators
- [ ] Risk level displays with correct color
- [ ] Control info expander shows metadata
- [ ] Compatible generators create artifacts

#### For New Generators

- [ ] Generator registered successfully
- [ ] Compatible with intended control types
- [ ] Generates valid output format
- [ ] File extension is correct
- [ ] MIME type enables proper download
- [ ] Appears in generated artifacts tabs
- [ ] Included in download package
- [ ] Custom filename (if implemented) works

### Automated Testing Template

```python
import unittest
from controls.my_security_control import MySecurityControl
from generators.my_generator import MyCustomGenerator

class TestMyExtensions(unittest.TestCase):
    def setUp(self):
        self.control = MySecurityControl()
        self.generator = MyCustomGenerator()
    
    def test_control_validation(self):
        """Test control settings validation"""
        valid_settings = {"required_field": "test_value"}
        self.assertTrue(self.control.validate_settings(valid_settings))
        
        invalid_settings = {}
        self.assertFalse(self.control.validate_settings(invalid_settings))
    
    def test_generator_compatibility(self):
        """Test generator settings compatibility"""
        compatible_settings = {"text_field": "test"}
        self.assertTrue(self.generator.supports_settings(compatible_settings))
        
        incompatible_settings = {"unknown_field": "test"}
        self.assertFalse(self.generator.supports_settings(incompatible_settings))
    
    def test_artifact_generation(self):
        """Test artifact content generation"""
        settings = {"text_field": "test", "numeric_value": 42}
        artifact = self.generator.generate("Test_Control", settings)
        
        self.assertIn("Test_Control", artifact)
        self.assertIn("text_setting=test", artifact)
        self.assertIn("numeric_setting=42", artifact)

if __name__ == "__main__":
    unittest.main()
```

## Troubleshooting Common Issues

### Control Not Appearing in Sidebar

1. **Check imports** in `app_factory.py`
2. **Verify registration** in `create_control_registry()`
3. **Check for syntax errors** in control class
4. **Restart Streamlit** application

### UI Form Not Rendering

1. **Check renderer imports** and registration
2. **Verify `can_render()` method** returns `True`
3. **Check for Streamlit widget conflicts** (unique keys)
4. **Review browser console** for JavaScript errors

### Generator Not Creating Artifacts

1. **Verify `supports_settings()`** returns `True` for test settings
2. **Check generator registration** in `app_factory.py`
3. **Review `generate()` method** for exceptions
4. **Test with minimal settings** first

### Generated Content Issues

1. **Check file extension** and MIME type
2. **Validate output format** meets target system requirements
3. **Test with different settings** combinations
4. **Review error handling** in generation logic

## Best Practices

### Control Development

- **Single Responsibility**: Each control should handle one security domain
- **Clear Validation**: Provide specific validation error feedback
- **Comprehensive Schema**: Include all options users might need
- **Risk Assessment**: Accurately categorize impact level
- **Documentation**: Include clear descriptions and help text

### Generator Development

- **Format Compliance**: Ensure output follows target platform standards
- **Error Handling**: Gracefully handle missing or invalid settings
- **Template Structure**: Use consistent formatting and organization
- **Cross-Platform**: Consider portability when possible
- **Performance**: Optimize for large settings objects

### UI Design

- **User Experience**: Intuitive, logical form organization
- **Progressive Disclosure**: Hide complex options until needed
- **Validation Feedback**: Real-time validation with clear messages
- **Help Text**: Provide context and examples
- **Accessibility**: Clear labels and logical tab order

Following these detailed instructions will enable you to successfully extend the application with new security controls and generators that integrate seamlessly with the existing architecture.
