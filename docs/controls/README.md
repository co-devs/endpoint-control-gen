# Controls Module

Security control implementations that define policies, validation logic, and configuration schemas.

## Available Controls

### File Association Control (`file_association_control.py`)

**Purpose**: Prevent execution of malicious files by changing default applications for commonly abused extensions.

- **Risk Level**: Medium
- **Category**: File System Security
- **Common Targets**: `.scr`, `.pif`, `.com`, `.bat`, `.cmd`, `.vbs`, `.js`, `.jar`

**Configuration Schema**:

- `file_associations` - Dictionary mapping file extensions to safe applications
- Supports custom extensions and applications
- Built-in safe applications: `notepad.exe`, `wordpad.exe`, "Block execution"

**Example Settings**:

```python
{
    "file_associations": {
        ".scr": "notepad.exe",
        ".pif": "notepad.exe", 
        ".com": "notepad.exe"
    }
}
```

### Network Traffic Control (`network_traffic_control.py`)

**Purpose**: Block or monitor specific network traffic patterns.

- **Risk Level**: High
- **Category**: Network Security
- **Features**: Firewall rule generation, traffic monitoring

**Configuration Schema**:

- `firewall_rules` - List of firewall rules with action, program, and name
- Support for both inbound and outbound rules

### WinX Menu Control (`winx_menu_control.py`)

**Purpose**: Customize Windows X menu (Win+X) for security hardening.

- **Risk Level**: Low
- **Category**: User Interface Security
- **Features**: Menu item management, access control

### Custom Control (`custom_control.py`)

**Purpose**: User-defined security control with flexible configuration.

- **Risk Level**: Medium (configurable)
- **Category**: Custom
- **Features**:

  - Dynamic control name and description
  - Flexible settings schema
  - Compatible with all generators

**Configuration**:

- `control_name` - User-defined control name
- `control_description` - User-defined description
- `settings` - Arbitrary configuration dictionary

## Control Architecture

### Base Implementation

All controls extend `BaseSecurityControl` and implement:

1. **`validate_settings()`** - Input validation logic
2. **`get_default_configuration()`** - Default settings
3. **`get_configuration_schema()`** - UI schema definition
4. **`get_control_name()`** - File-safe control name

### Metadata Structure

Each control defines:

- **Name** - Display name
- **Description** - Purpose and functionality
- **Risk Level** - Impact assessment (LOW, MEDIUM, HIGH)
- **Purpose** - Security objective
- **Common Targets** - Typical affected resources
- **Category** - Functional grouping

### Settings Management

- Settings stored as validated dictionaries
- Automatic validation on assignment
- Support for complex nested configurations
- Schema-driven UI generation

## Adding New Controls

**For complete step-by-step instructions on creating and integrating new security controls, including:**

- **Full code templates and examples**
- **File creation and placement**
- **UI renderer implementation**
- **Registration in AppFactory**
- **Testing and validation procedures**

**See the comprehensive [`../extension-guide.md`](../extension-guide.md)**

### Quick Reference

1. **Create Control Class** in `src/controls/my_control.py`
2. **Create UI Renderer** in `src/ui/my_renderer.py`
3. **Register Components** in `src/app_factory.py`
4. **Test Integration** with existing generators

## Integration Points

Controls integrate with:

- **Generators** - Provide settings for artifact generation
- **UI Renderers** - Schema drives configuration forms
- **Validation** - Ensures configuration correctness
- **Metadata** - Provides user information and risk assessment

Each control is self-contained with its own validation rules and configuration schema, enabling easy extension and maintenance.
