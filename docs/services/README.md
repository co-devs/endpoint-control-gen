# Services Module
<!-- markdownlint-disable MD024 -->

Business logic services that coordinate between UI, controls, and generators to provide high-level application functionality.

## Service Components

### Artifact Service (`artifact_service.py`)

**Purpose**: Orchestrates artifact generation and packaging for security controls.

#### Core Responsibilities

- **Artifact Generation**: Coordinate multiple generators for a single control
- **Compatibility Filtering**: Select appropriate generators based on settings
- **Package Creation**: Bundle artifacts into downloadable ZIP packages
- **Documentation**: Generate comprehensive README files

#### Key Methods

##### `generate_all_artifacts(control_name, settings)`

**Purpose**: Generate all compatible artifacts for a security control.

**Process**:

1. Query generator registry for compatible generators
2. Execute each compatible generator with control settings
3. Collect generated artifacts in dictionary format
4. Return artifacts mapped by type

**Example**:

```python
artifacts = service.generate_all_artifacts("File_Association", {
    "file_associations": {".scr": "notepad.exe"}
})
# Returns: {"gpo": "xml_content", "powershell": "ps1_content", ...}
```

##### `create_download_package(control_name, artifacts)`

**Purpose**: Package multiple artifacts into a single ZIP download.

**Features**:

- **Standardized Naming**: Consistent file naming across artifact types
- **README Generation**: Comprehensive documentation included
- **Implementation Guide**: Step-by-step deployment instructions
- **Security Warnings**: Important safety reminders

**Package Contents**:

- `{control_name}_GPO.xml` - Group Policy Object export
- `{control_name}_Script.ps1` - PowerShell implementation script  
- `{control_name}_Registry.reg` - Registry file for manual import
- `{control_name}_Deploy.bat` - Batch script for deployment
- `README.txt` - Implementation instructions and warnings

#### README Generation

The service automatically generates comprehensive documentation:

```text
Windows Security Control Package
=================================

Control Name: File_Association_Security
Generated: 2024-12-06 14:30:00

Files Included:
- File_Association_Security_GPO.xml: Group Policy Object export
- File_Association_Security_Script.ps1: PowerShell implementation script
- File_Association_Security_Registry.reg: Registry file for manual import
- File_Association_Security_Deploy.bat: Batch script for deployment

IMPORTANT: Always test these configurations in a non-production environment first!

Implementation Notes:
1. Run scripts with Administrator privileges
2. Backup your system before applying changes
3. Test thoroughly before deploying to production
4. Consider the impact on user workflows
```

### UI Service (`ui_service.py`)

**Purpose**: Manage common UI elements, styling, and user interface coordination.

#### Core Responsibilities

- **Page Configuration**: Streamlit application setup and styling
- **Common UI Elements**: Headers, sidebars, and navigation
- **Artifact Display**: Consistent presentation of generated content
- **Download Management**: File download interface coordination

#### Key Methods

##### `setup_page_config()`

**Purpose**: Configure Streamlit application settings.

**Configuration**:

- **Title**: "Windows Security Controls Generator"
- **Icon**: 🛡️ (shield emoji)
- **Layout**: Wide (optimal for configuration forms)
- **Sidebar**: Expanded by default

##### `setup_custom_css()`

**Purpose**: Apply application-wide styling and theme.

**Styling Features**:

- **Control Cards**: Professional card-based layout
- **Risk Level Colors**:
  - High Risk: Red (`#dc3545`)
  - Medium Risk: Orange (`#fd7e14`)  
  - Low Risk: Green (`#28a745`)
- **Typography**: Consistent fonts and spacing

##### `render_sidebar()`

**Purpose**: Generate control selection sidebar with security notices.

**Components**:

- **Control Selection**: Dropdown with all available controls
- **Security Warnings**: Prominent testing reminders
- **Documentation Links**: Implementation guidance
- **Professional Branding**: Security-focused messaging

**Returns**: Selected control type string

##### `render_control_info(control)`

**Purpose**: Display security control metadata and information.

**Features**:

- **Control Header**: Name and description
- **Expandable Details**: Risk level, purpose, and targets
- **Risk Assessment**: Color-coded risk level display
- **Professional Formatting**: Consistent information layout

##### `render_artifacts_display(artifacts, control_name)`

**Purpose**: Present generated artifacts in organized, accessible format.

**Features**:

- **Tabbed Interface**: Separate tabs for each artifact type
- **Syntax Highlighting**: Language-appropriate code formatting
- **Individual Downloads**: Download button for each artifact
- **Preview Capability**: Full content display before download

**Supported Formats**:

- **PowerShell**: `.ps1` files with PowerShell syntax highlighting
- **XML**: `.xml` files with XML formatting
- **Registry**: `.reg` files with plain text display
- **Batch**: `.bat` files with batch syntax

##### `render_package_download(package_data, control_name)`

**Purpose**: Provide complete package download interface.

**Features**:

- **ZIP Download**: Single download for all artifacts
- **Professional Naming**: Consistent package naming convention
- **Complete Documentation**: Includes implementation guide
- **One-Click Deployment**: Everything needed in one package

## Service Integration

### Application Flow

```plaintext
User Input → UIService → ControlRegistry → SecurityControl
                   ↓
           ArtifactService → GeneratorRegistry → Multiple Generators
                   ↓
           Generated Artifacts → Package Creation → Download
```

### Dependency Management

Services coordinate multiple system components:

- **UIService Dependencies**:
  - ControlRegistry (for available controls)
  - SecurityControls (for metadata display)
  
- **ArtifactService Dependencies**:
  - GeneratorRegistry (for artifact generation)
  - Individual Generators (for content creation)

### Error Handling

Services provide robust error handling:

- **Input Validation**: Settings validation before processing
- **Generation Errors**: Graceful handling of generator failures
- **User Feedback**: Clear error messages and recovery guidance
- **Logging**: Comprehensive error tracking and debugging

## Service Benefits

### Separation of Concerns

- **UI Logic**: Isolated in UIService
- **Business Logic**: Centralized in ArtifactService
- **Domain Logic**: Contained in individual controls and generators

### Testability

- **Unit Testing**: Services can be tested independently
- **Mock Dependencies**: Easy to mock registries and components
- **Integration Testing**: Clear service boundaries enable comprehensive testing

### Maintainability

- **Single Responsibility**: Each service has focused responsibilities
- **Loose Coupling**: Services communicate through well-defined interfaces
- **Easy Extension**: New functionality can be added without affecting existing services

### User Experience

- **Consistent Interface**: UIService ensures uniform presentation
- **Professional Output**: ArtifactService provides polished, documented packages
- **Error Recovery**: Services provide clear feedback and recovery options

The services module provides the coordination layer that transforms individual components into a cohesive, professional security control generation system.
