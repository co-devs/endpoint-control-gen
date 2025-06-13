# Generators Module

Artifact generation engines that convert security control settings into deployable Windows artifacts.

## Available Generators

### GPO Generator (`gpo_generator.py`)

**Purpose**: Generate Group Policy Object XML files for Active Directory deployment.

- **File Extension**: `.xml`
- **MIME Type**: `text/xml`
- **Output**: Well-formed GPO XML with proper structure and identifiers

**Features**:

- Automatic GUID generation with timestamp
- Support for registry-based policies
- Firewall rule integration
- Computer configuration scope
- Domain-ready structure

**Supported Settings**:

- `file_associations` - Registry entries for file associations
- `firewall_rules` - Windows Defender Firewall rules

**Example Output**:

```xml
<GroupPolicyObject>
  <Identifier>{12345678-1234-5678-9012-202412061430}</Identifier>
  <Domain>example.com</Domain>
  <Name>Control_Name</Name>
  <Computer>
    <Enabled>true</Enabled>
    <ExtensionData>
      <Registry>
        <Policy State="Enabled" Key="HKEY_CLASSES_ROOT\.scr" ValueName="" Value="notepad.exe"/>
      </Registry>
    </ExtensionData>
  </Computer>
</GroupPolicyObject>
```

### PowerShell Generator (`powershell_generator.py`)

**Purpose**: Generate PowerShell scripts for direct system configuration.

- **File Extension**: `.ps1`
- **MIME Type**: `text/plain`
- **Output**: PowerShell script with error handling and logging

**Features**:

- Administrative privilege checks
- Comprehensive error handling
- Backup creation before changes
- Detailed logging and feedback
- Rollback capabilities

**Script Structure**:

1. Header with metadata and requirements
2. Administrative privilege verification
3. Backup creation
4. Configuration implementation
5. Verification and reporting

### Registry Generator (`registry_generator.py`)

**Purpose**: Generate Windows Registry files for manual or automated import.

- **File Extension**: `.reg`
- **MIME Type**: `text/plain`
- **Output**: Standard Windows Registry format

**Features**:

- Registry version header
- Proper key path formatting
- Data type handling (string, DWORD, binary)
- Comment documentation
- Merge-ready format

**Example Output**:

```registry
Windows Registry Editor Version 5.00

; File Association Security Control
; Generated on 2024-12-06 14:30:00

[HKEY_CLASSES_ROOT\.scr]
@="notepad.exe"

[HKEY_CLASSES_ROOT\.pif]
@="notepad.exe"
```

### Batch Generator (`batch_generator.py`)

**Purpose**: Generate batch scripts for deployment automation.

- **File Extension**: `.bat`
- **MIME Type**: `text/plain`
- **Output**: Windows batch script with error handling

**Features**:

- Administrative privilege checks
- Registry import automation
- PowerShell script execution
- Error handling and logging
- System compatibility checks

## Generator Architecture

### Base Implementation

All generators extend `BaseArtifactGenerator` and implement:

1. **`generate()`** - Core generation logic
2. **`get_file_extension()`** - File extension for output
3. **`get_mime_type()`** - MIME type for downloads
4. **`supports_settings()`** - Compatibility check

### Settings Compatibility

Generators declare which settings they can process:

- File association settings
- Firewall rule settings
- Custom configuration properties
- Registry modifications

### Output Standards

- **Consistent formatting** - Professional, readable output
- **Error handling** - Robust error detection and reporting
- **Documentation** - Embedded comments and usage instructions
- **Validation** - Generated content follows platform standards

## Generation Process

1. **Compatibility Check**: Generator validates it can process settings
2. **Content Generation**: Settings transformed into platform-specific format
3. **Formatting**: Output formatted according to platform standards
4. **Validation**: Generated content verified for correctness

## Adding New Generators

**For complete step-by-step instructions on creating and integrating new artifact generators, including:**

- **Full code templates with examples**
- **File creation and placement**
- **Settings compatibility handling**
- **Registration in AppFactory**
- **Advanced generator patterns**
- **Testing procedures**

**See the comprehensive [`../extension-guide.md`](../extension-guide.md)**

### Quick Reference

1. **Create Generator Class** in `src/generators/my_generator.py`
2. **Implement Required Methods** (`generate`, `get_file_extension`, `get_mime_type`, `supports_settings`)
3. **Register Generator** in `src/app_factory.py`
4. **Test Compatibility** with existing controls

## Integration Points

Generators integrate with:

- **ArtifactService** - Orchestrates generation process
- **Settings Validation** - Ensures compatible input
- **Download Packaging** - Provides formatted output
- **UI Display** - Enables preview and download

Each generator is independent and can be developed, tested, and deployed separately while maintaining consistent interfaces and output quality.
