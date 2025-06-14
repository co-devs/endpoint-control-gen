# Controls Module

Security control implementations that define policies, validation logic, and configuration schemas.

## Available Controls

### File Association Control (`file_association_control.py`)

**Purpose**: Prevent execution of malicious files by changing default applications for commonly abused extensions.

- **Risk Level**: Low
- **Category**: File System Security
- **Common Targets**: 30+ dangerous extensions including `.scr`, `.bat`, `.cmd`, `.vbs`, `.js`, `.jar`, `.appx`, `.ps1`

**Centralized Configuration**:

- **`DANGEROUS_EXTENSIONS`** dictionary at the top of the file contains all configurable extensions
- Each extension entry includes description and default safe application
- **To add new extensions**: Simply add entries to the `DANGEROUS_EXTENSIONS` dictionary

**Configuration Schema**:

- `file_associations` - Dictionary mapping file extensions to safe applications
- Automatically generated from `DANGEROUS_EXTENSIONS` dictionary
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

**Adding New Extensions**:

```python
# In file_association_control.py
DANGEROUS_EXTENSIONS = {
    ".new_ext": {"description": "Description of new extension", "default_app": "notepad.exe"},
    # ... existing extensions
}
```

### Network Traffic Control (`network_traffic_control.py`)

**Purpose**: Block network traffic from commonly abused Windows binaries to prevent data exfiltration and C2 communication.

- **Risk Level**: High
- **Category**: Network Security
- **Common Targets**: 8+ risky binaries including `powershell.exe`, `cmd.exe`, `wscript.exe`, `regsvr32.exe`

**Centralized Configuration**:

- **`RISKY_BINARIES`** dictionary at the top of the file contains all configurable binaries
- Each binary entry includes description and full system path
- **To add new binaries**: Simply add entries to the `RISKY_BINARIES` dictionary

**Configuration Schema**:

- `firewall_rules` - List of firewall rules automatically generated from `RISKY_BINARIES`
- Each rule blocks outbound traffic from specified programs
- Automatic rule naming: `Block_{binary}_Outbound`

**Adding New Binaries**:

```python
# In network_traffic_control.py
RISKY_BINARIES = {
    "new_binary.exe": {"description": "Description of binary", "path": "C:\\Path\\To\\new_binary.exe"},
    # ... existing binaries
}
```

### WinX Menu Control (`winx_menu_control.py`)

**Purpose**: Remove potentially dangerous entries from the Windows+X menu to limit user access to administrative tools.

- **Risk Level**: Low
- **Category**: User Interface Security
- **Common Targets**: 10+ menu items including Command Prompt, PowerShell, Computer Management, Event Viewer

**Centralized Configuration**:

- **`WINX_ITEMS`** dictionary at the top of the file contains all configurable menu items
- Each item entry includes description and actual menu name
- **To add new items**: Simply add entries to the `WINX_ITEMS` dictionary

**Configuration Schema**:

- `winx_removal` - List of menu items to remove from Windows+X menu
- Default removes administrative Command Prompt and PowerShell entries
- Schema automatically generated from `WINX_ITEMS` dictionary

**Adding New Menu Items**:

```python
# In winx_menu_control.py
WINX_ITEMS = {
    "New Item": {"description": "Description of menu item", "menu_name": "Actual Menu Name"},
    # ... existing items
}
```

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
