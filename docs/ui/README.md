# UI Module

User interface components built with Streamlit for configuration, display, and interaction with security controls.

## Architecture

### Base Renderer (`base_renderer.py`)

Abstract base class defining the contract for all UI renderers:

- **`render_configuration()`** - Generate configuration form
- **`can_render()`** - Compatibility check with control types

### Control-Specific Renderers

#### File Association Renderer (`file_association_renderer.py`)

**Purpose**: Render configuration UI for Default App Associations control.

**Features**:

- **Extension Selection**: Checkbox interface for 19 dangerous extensions
- **Select All/None Buttons**: Quick selection controls using session state
- **Application Mapping**: Dropdown selection for safe applications
- **Custom Extensions**: Text input for additional extensions
- **Custom Applications**: Support for user-defined applications
- **Dynamic Column Layout**: 1-3 columns based on item count (currently 3 for 19 items)

**UI Components**:

- Extension checkboxes with descriptions
- Application selectboxes with predefined safe options
- Custom application text inputs
- Real-time configuration building

**Configuration Output**:

```python
{
    "file_associations": {
        ".scr": "notepad.exe",
        ".pif": "wordpad.exe",
        ".custom": "custom_app.exe"
    }
}
```

#### Network Traffic Renderer (`network_traffic_renderer.py`)

**Purpose**: Render configuration UI for LOLBIN Firewall Rules control.

**Features**:

- **Binary Selection**: Checkbox interface for 15 LOLBINs with tooltips
- **Select All/None Buttons**: Quick selection controls using session state
- **Architecture Support**: Automatically includes x86 and x64 paths
- **Custom Binary**: Text input for additional binaries
- **Dynamic Column Layout**: 1-3 columns based on item count (currently 3 for 15 items)
- **Help Tooltips**: Each binary shows description and path count on hover

#### WinX Menu Renderer (`winx_menu_renderer.py`)

**Purpose**: Render configuration UI for WinX Menu Hardening control.

**Features**:

- **Menu Item Selection**: Checkbox interface for 10 WinX menu items
- **Select All/None Buttons**: Quick selection controls using session state
- **Dynamic Column Layout**: 1-3 columns based on item count (currently 2 for 10 items)
- **System-wide Scope**: Changes apply to all users and default profile

#### Windows Hotkey Renderer (`windows_hotkey_renderer.py`)

**Purpose**: Render configuration UI for Windows Hotkey Control.

**Features**:

- **Option 1 - Disable All**: Checkbox to enable NoWinKeys policy (system-wide)
- **Option 2 - Disable Specific**: Checkbox interface for 12 individual hotkeys
- **Select All/None Buttons**: Quick selection controls using session state (disabled when Option 1 is checked)
- **Dynamic Column Layout**: 1-3 columns based on item count (currently 2 for 12 items)
- **Help Tooltips**: Each hotkey shows description and risk level on hover
- **Warning Message**: Displayed when "Disable All" is selected
- **Mutual Exclusion**: Specific hotkey checkboxes disabled when "Disable All" is active

#### Custom Renderer (`custom_renderer.py`)

**Purpose**: Render configuration UI for user-defined custom controls.

**Features**:

- **Dynamic Control Definition**: Text inputs for control name and description
- **Flexible Settings**: Text area for JSON-formatted settings
- **Real-time Validation**: Input validation and error feedback
- **Schema-Free Configuration**: No predefined structure requirements

**UI Flow**:

1. Control name and description input
2. Settings configuration (JSON format)
3. Validation and error display
4. Configuration compilation

## UI Service (`ui_service.py`)

Central service managing common UI elements and application-wide styling.

### Core Functions

#### Page Configuration

- **`setup_page_config()`** - Streamlit page configuration
  - Title: "Windows Security Controls Generator"
  - Icon: 🛡️
  - Layout: Wide
  - Sidebar: Expanded

#### Custom Styling

- **`setup_custom_css()`** - Application-wide CSS styling
  - Control card styling
  - Risk level color coding (High: Red, Medium: Orange, Low: Green)
  - Professional appearance

#### Main Interface

- **`render_main_header()`** - Application title and description
- **`render_sidebar_notices()`** - Security warnings and documentation links (used with st.navigation)
- **`render_control_info()`** - Control metadata display with expandable details

#### Artifact Display

- **`render_artifacts_display()`** - Tabbed interface for generated artifacts
  - Syntax-highlighted code display
  - Individual download buttons for each artifact
  - Support for PowerShell, XML, Registry, and Batch formats

- **`render_package_download()`** - Complete package download button
  - ZIP file generation
  - Comprehensive package with documentation

### UI Components

#### Control Information Display

```python
def render_control_info(self, control: ISecurityControl):
    metadata = control.get_metadata()
    st.header(f"{metadata.name}")
    
    with st.expander("ℹ️ About This Control"):
        # Risk level with color coding
        # Purpose and common targets
        # Security considerations
```

#### Artifact Tabs

- **PowerShell Script** - Syntax highlighted PowerShell code
- **GPO XML** - Formatted XML display
- **Registry File** - Registry format display
- **Batch Script** - Batch command display

#### Security Notices

- **Sidebar Warning** - Prominent testing reminder
- **Documentation Links** - Implementation guidance
- **Risk Assessment** - Color-coded risk levels

## Navigation and Rendering Process

### Streamlit Navigation

The application uses Streamlit's native `st.navigation()` for a clean, page-based interface:

- Each security control is rendered as a separate page
- Navigation menu automatically generated from registered controls
- URL routing for direct access to specific controls (e.g., `/default_app_associations`)
- Security notices persist in sidebar across all pages

### Rendering Flow

1. **Page Selection**: User navigates to control page via sidebar navigation
2. **Page Rendering**: Page function executes for selected control
3. **Renderer Lookup**: System finds appropriate UI renderer for the control
4. **Configuration Form**: Renderer generates control-specific form with session state
5. **User Interaction**: Select All/None buttons and checkboxes update session state
6. **Settings Collection**: Form inputs compiled into settings dictionary
7. **Validation**: Control validates settings
8. **Artifact Generation**: Compatible generators create artifacts
9. **Display**: Artifacts shown in tabbed interface with download options

## Adding New Renderers

**For complete step-by-step instructions on creating UI renderers for new controls, including:**

- **Full code templates with Streamlit examples**
- **Form element patterns and best practices**
- **Validation and error handling**
- **Registration with controls**
- **UI design principles**

**See the comprehensive [`../extension-guide.md`](../extension-guide.md)**

### Quick Reference

1. **Create Renderer Class** in `src/ui/my_renderer.py`
2. **Implement Required Methods** (`can_render`, `render_configuration`)
3. **Register with Control** in `src/app_factory.py`
4. **Test UI Integration** with configuration forms

## UI Design Principles

### User Experience

- **Progressive Disclosure** - Complex options in expandable sections
- **Clear Feedback** - Validation messages and success indicators
- **Consistent Layout** - Standardized component placement
- **Security Awareness** - Prominent warnings and risk indicators

### Accessibility

- **Color Coding** - Risk levels with consistent color scheme
- **Clear Labels** - Descriptive form labels and help text
- **Logical Flow** - Intuitive step-by-step configuration
- **Error Handling** - Clear error messages and recovery guidance

### Responsiveness

- **Wide Layout** - Optimized for desktop configuration tasks
- **Column Layout** - Organized form elements
- **Expandable Sections** - Efficient use of screen space
- **Tabbed Display** - Organized artifact presentation

The UI module ensures a consistent, professional user experience while maintaining flexibility for different control types and configurations.
