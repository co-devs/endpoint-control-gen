# Core Module

The core module provides the foundational interfaces, base classes, and registry implementations that define the application's architecture.

## Components

### Interfaces (`interfaces.py`)

Defines abstract contracts for all major system components:

#### Security Control Interfaces

- **`ISecurityControl`** - Contract for all security control implementations
- **`SecurityControlMetadata`** - Metadata structure for controls
- **`RiskLevel`** - Risk level enumeration (LOW, MEDIUM, HIGH)

#### Generator Interfaces  

- **`IArtifactGenerator`** - Contract for artifact generation engines
- **`IGeneratorRegistry`** - Registry management for generators

#### UI Interfaces

- **`IUIRenderer`** - Contract for user interface renderers
- **`IControlRegistry`** - Registry management for controls

### Base Classes (`base_control.py`)

**`BaseSecurityControl`** - Abstract base class providing common functionality:

- Settings validation and management
- Metadata handling
- Risk level display formatting
- Common property implementations

### Registry Implementations (`registries.py`)

#### ControlRegistry

- **Purpose**: Manages security control types and their UI renderers
- **Key Methods**:
  - `register_control()` - Register control class and UI renderer
  - `create_control()` - Instantiate control by name
  - `get_ui_renderer()` - Get UI renderer for control type
  - `get_available_controls()` - List all registered controls

#### GeneratorRegistry  

- **Purpose**: Manages artifact generator instances
- **Key Methods**:
  - `register_generator()` - Register generator instance
  - `get_generator()` - Get generator by name
  - `get_all_generators()` - Get all registered generators
  - `get_compatible_generators()` - Get generators compatible with settings

## Key Design Patterns

### Interface Segregation

Each interface defines a focused contract without unnecessary dependencies.

### Registry Pattern

Central registries enable dynamic component discovery and loose coupling.

### Template Method

Base classes define common algorithm structure while allowing subclass customization.

## Usage Examples

### Implementing a New Control

```python
from core.base_control import BaseSecurityControl
from core.interfaces import SecurityControlMetadata, RiskLevel

class MyControl(BaseSecurityControl):
    def __init__(self):
        metadata = SecurityControlMetadata(
            name="My Control",
            description="Custom security control",
            risk_level=RiskLevel.MEDIUM,
            purpose="Example control implementation"
        )
        super().__init__(metadata)
    
    def validate_settings(self, settings):
        # Validation logic
        return True
    
    def get_default_configuration(self):
        return {"key": "value"}
    
    def get_configuration_schema(self):
        return {"key": {"type": "string"}}
```

### Registering Components

```python
# In AppFactory
registry = ControlRegistry()
registry.register_control(MyControl, MyControlRenderer)
```

The core module ensures consistent behavior across all components while maintaining flexibility for extension.
