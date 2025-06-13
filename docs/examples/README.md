# Examples Module

Complete examples demonstrating how to extend the application with new security controls and artifact generators.

## Example Files

### New Control Example (`new_control_example.py`)

**Purpose**: Demonstrates creating a new "Registry Hardening" security control with its UI renderer.

#### Registry Hardening Control Features

- **Risk Level**: High (due to registry modification impact)
- **Category**: Registry Security
- **Target Areas**: System policies and service configurations

**Key Components**:

##### Control Implementation

```python
class RegistryHardeningControl(BaseSecurityControl):
    def __init__(self):
        metadata = SecurityControlMetadata(
            name="Registry Hardening",
            description="Apply registry modifications to harden Windows security",
            risk_level=RiskLevel.HIGH,
            purpose="Apply critical registry modifications to improve Windows security posture",
            common_targets=[
                "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies",
                "HKLM\\System\\CurrentControlSet\\Services",
            ],
            category="Registry Security"
        )
        super().__init__(metadata)
```

##### Settings Validation

- **Structure**: List of registry modification dictionaries
- **Required Fields**: `key`, `value_name`, `value_data`, `value_type`
- **Validation**: Ensures all modifications have complete information

##### Configuration Schema

**Common Modifications**:

- **Enable UAC**: User Account Control enforcement
- **Disable Autorun**: Prevent automatic execution from removable media
- **Disable Remote Desktop**: Block Terminal Server connections

**Supported Value Types**: `DWORD`, `REG_SZ`, `REG_MULTI_SZ`, `REG_BINARY`

##### UI Renderer Implementation

```python
class RegistryHardeningRenderer(BaseUIRenderer):
    def render_configuration(self, control) -> Optional[Dict[str, Any]]:
        # Common modifications checkboxes
        # Custom modification inputs
        # Real-time configuration building
```

**UI Features**:

- **Checkbox Selection**: Quick selection of common hardening modifications
- **Custom Modifications**: User-defined registry entries
- **Two-Column Layout**: Organized input fields
- **Dynamic Configuration**: Real-time settings compilation

#### Integration Steps

1. **Import Dependencies**: Core interfaces and base classes
2. **Implement Control**: Extend `BaseSecurityControl`
3. **Create UI Renderer**: Extend `BaseUIRenderer`
4. **Register Components**: Add to `AppFactory`

**For complete step-by-step instructions, see [`../extension-guide.md`](../extension-guide.md)**

### New Generator Example (`new_generator_example.py`)

**Purpose**: Demonstrates creating new artifact generators for cross-platform deployment.

#### Ansible Playbook Generator

**Purpose**: Generate Ansible playbooks for Linux/Unix security configuration.

**Features**:

- **Cross-Platform Translation**: Windows concepts to Linux equivalents
- **YAML Format**: Standard Ansible playbook structure
- **Task Organization**: Logical grouping of security tasks

**Supported Settings**:

- **File Associations** → MIME type configurations
- **Firewall Rules** → UFW (Uncomplicated Firewall) rules
- **Registry Modifications** → System configuration files

**Example Output**:

```yaml
---
# Ansible Playbook for Registry_Hardening
# Generated: 2024-12-06 14:30:00

- name: Apply security control
  hosts: all
  become: yes
  tasks:
    
    # File association security (Linux equivalent - MIME types)
    - name: Set default application for .scr files
      command: xdg-mime default notepad.exe application/x-scr
      become_user: "{{ item }}"
      with_items: "{{ ansible_user_list }}"
```

#### Terraform Generator

**Purpose**: Generate Terraform configurations for cloud infrastructure security.

**Features**:

- **Infrastructure as Code**: Declarative security configurations
- **AWS Provider**: Security group and resource definitions
- **Version Pinning**: Stable provider versions

**Supported Settings**:

- **Firewall Rules** → AWS Security Group rules
- **Network Policies** → VPC and subnet configurations

**Example Output**:

```hcl
# Terraform configuration for Network_Security
# Generated: 2024-12-06 14:30:00

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_security_group" "security_control" {
  name_prefix = "security-control-"
  description = "Security group for hardened instances"
  
  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Block malicious traffic"
  }
}
```

## Implementation Patterns

### Control Development Pattern

1. **Define Metadata**: Name, description, risk level, purpose
2. **Implement Validation**: Input validation logic
3. **Create Schema**: Configuration structure definition
4. **Build UI Renderer**: User interface for configuration
5. **Register Components**: Integration with application

### Generator Development Pattern

1. **Extend Base Generator**: Implement required interface methods
2. **Define Support Matrix**: Which settings the generator can process
3. **Implement Generation Logic**: Transform settings to target format
4. **Handle Edge Cases**: Robust error handling and validation
5. **Register Generator**: Integration with generator registry

### Cross-Platform Translation

Examples demonstrate translating Windows-specific concepts to other platforms:

- **Registry → Configuration Files**: Windows registry to Linux config files
- **Group Policy → Ansible Tasks**: GPO policies to automation tasks
- **Windows Firewall → UFW/iptables**: Firewall rule translation
- **Batch Scripts → Shell Scripts**: Command sequence translation

## Extension Guidelines

### Adding New Controls

1. **Identify Security Domain**: File system, network, registry, etc.
2. **Define Risk Assessment**: Appropriate risk level for changes
3. **Create Validation Rules**: Ensure configuration correctness
4. **Design UI Schema**: User-friendly configuration interface
5. **Test Integration**: Verify compatibility with existing generators

### Adding New Generators

1. **Choose Target Platform**: Windows, Linux, cloud, etc.
2. **Define Format**: Output format and structure
3. **Map Settings**: How control settings translate to target format
4. **Implement Generation**: Core transformation logic
5. **Test Compatibility**: Verify with all supported controls

### Best Practices

- **Consistent Interfaces**: Follow established patterns
- **Comprehensive Validation**: Validate inputs thoroughly  
- **Error Handling**: Provide clear error messages
- **Documentation**: Include inline comments and examples
- **Testing**: Unit tests for validation and generation logic

## Usage Instructions

### Running Examples

1. **Copy Example Code**: Use as template for new components
2. **Modify for Needs**: Adapt to specific security requirements
3. **Test Thoroughly**: Validate in development environment
4. **Register Components**: Add to AppFactory configuration
5. **Deploy Incrementally**: Add components one at a time

### Integration Checklist

- [ ] Control implements all required interface methods
- [ ] UI renderer provides complete configuration interface
- [ ] Generator supports relevant control settings
- [ ] Components registered in AppFactory
- [ ] Error handling implemented
- [ ] Validation logic tested
- [ ] Documentation updated

## Complete Implementation Guide

**For detailed step-by-step instructions on implementing and registering new controls and generators, including:**

- **File creation and placement**
- **Code templates with full examples**
- **Registration in AppFactory**
- **Testing procedures**
- **Troubleshooting common issues**

**See the comprehensive [`../extension-guide.md`](../extension-guide.md)**

These examples provide complete, working implementations that can be used as templates for extending the application with new security controls and deployment targets.
