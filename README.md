# Modular Windows Security Controls Generator
<!-- markdownlint-disable MD029 -->

A refactored, modular application for generating Windows security artifacts with support for easy extension of controls and generators.

## Architecture Overview

The application has been refactored into a modular architecture with clear separation of concerns:

### Core Components

- **`core/interfaces.py`** - Defines all interfaces and contracts
- **`core/base_control.py`** - Base implementation for security controls
- **`core/registries.py`** - Registry pattern for controls and generators

### Controls (`controls/`)

Each security control is now a separate module:

- `file_association_control.py` - Default App Associations (file association security)
- `network_traffic_control.py` - LOLBIN Firewall Rules (blocking network traffic from abused binaries)
- `winx_menu_control.py` - WinX Menu Hardening (removing dangerous menu items)
- `windows_hotkey_control.py` - Windows Hotkey Control (disabling Windows keyboard shortcuts)
- `custom_control.py` - User-defined controls (example only, not in navigation)

### Generators (`generators/`)

Artifact generators for different output formats:

- `gpo_generator.py` - Group Policy Object XML
- `powershell_generator.py` - PowerShell scripts
- `registry_generator.py` - Registry files
- `batch_generator.py` - Batch scripts

### UI Renderers (`ui/`)

Separate UI components for each control type:

- `file_association_renderer.py` - File extension selection with Select All/None buttons
- `network_traffic_renderer.py` - LOLBIN selection with Select All/None buttons
- `winx_menu_renderer.py` - WinX menu item selection with Select All/None buttons
- `windows_hotkey_renderer.py` - Hotkey selection with Select All/None buttons
- `custom_renderer.py` - Custom control renderer (example only)

### Services (`services/`)

Business logic services:

- `artifact_service.py` - Handles artifact generation and packaging
- `ui_service.py` - Common UI functionality

## Adding New Controls

To add a new security control:

1. **Create the control class** in `controls/`:

```python
from ..core.base_control import BaseSecurityControl
from ..core.interfaces import SecurityControlMetadata, RiskLevel

class MyNewControl(BaseSecurityControl):
    def __init__(self):
        metadata = SecurityControlMetadata(
            name="My New Control",
            description="Description of what this control does",
            risk_level=RiskLevel.MEDIUM,
            purpose="Detailed purpose",
            category="Security Category"
        )
        super().__init__(metadata)

    def validate_settings(self, settings):
        # Validation logic
        return True

    def get_default_configuration(self):
        return {}

    def get_configuration_schema(self):
        return {}
```

2. **Create the UI renderer** in `ui/`:

```python
from .base_renderer import BaseUIRenderer

class MyNewControlRenderer(BaseUIRenderer):
    def can_render(self, control):
        return isinstance(control, MyNewControl)

    def render_configuration(self, control):
        # Streamlit UI code
        return configuration_dict
```

3. **Register in app factory**:

```python
# In app_factory.py
registry.register_control(MyNewControl, MyNewControlRenderer)
```

## Adding New Generators

To add a new artifact generator:

1. **Create the generator** in `generators/`:

```python
from .base_generator import BaseArtifactGenerator

class MyNewGenerator(BaseArtifactGenerator):
    def generate(self, control_name, settings):
        # Generation logic
        return artifact_content

    def get_file_extension(self):
        return "ext"

    def get_mime_type(self):
        return "text/plain"

    def supports_settings(self, settings):
        return "my_setting" in settings
```

2. **Register in app factory**:

```python
# In app_factory.py
registry.register_generator("my_generator", MyNewGenerator())
```

## Key Benefits

1. **Modularity** - Each control and generator is independent
2. **Extensibility** - Easy to add new functionality without modifying existing code
3. **Registry Pattern** - Dynamic discovery and registration of components
4. **Separation of Concerns** - UI, business logic, and data are clearly separated
5. **Type Safety** - Strong interfaces ensure compatibility
6. **Maintainability** - Clear structure makes the codebase easier to maintain

## Examples

See the `examples/` directory for:

- `new_control_example.py` - How to create a new security control
- `new_generator_example.py` - How to create new artifact generators

## Running the Application

```bash
streamlit run src/main.py
```

The application uses Streamlit's native navigation with separate pages for each control. Navigate between controls using the sidebar navigation menu.
