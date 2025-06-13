# Getting Started

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Streamlit (`pip install streamlit`)
- Required dependencies (see requirements if available)

### Running the Application

```bash
# Navigate to project directory
cd /path/to/streamlit-dev-container

# Run the application
streamlit run src/main.py
```

The application will open in your default web browser at `http://localhost:8501`.

## First Steps

### 1. Select a Security Control

From the sidebar, choose from available security controls:

- **File Association Security** - Prevent malicious file execution
- **Network Traffic Control** - Configure firewall rules
- **WinX Menu Control** - Customize Windows X menu
- **Custom Control** - Define your own security policy

### 2. Configure Settings

Each control provides a tailored configuration interface:

- **Checkboxes** for common options
- **Dropdowns** for predefined choices
- **Text inputs** for custom values
- **Real-time validation** and feedback

### 3. Review Risk Assessment

Pay attention to the risk level indicators:

- 🟢 **Low Risk** - Minimal system impact
- 🟠 **Medium Risk** - Moderate impact, test recommended
- 🔴 **High Risk** - Significant impact, thorough testing required

### 4. Generate Artifacts

The system automatically generates compatible artifacts:

- **PowerShell Script** - Direct system configuration
- **GPO XML** - Group Policy Object for AD deployment
- **Registry File** - Manual registry modifications
- **Batch Script** - Automated deployment script

### 5. Download Package

Get a complete package including:

- All generated artifacts
- Implementation instructions
- Security warnings and best practices
- Deployment guidance

## Example Walkthrough

### File Association Security Control

1. **Select Control**: Choose "File Association Security" from sidebar
2. **Configure Extensions**:
   - Check `.scr` (Screen saver files)
   - Check `.pif` (Program Information Files)
   - Select "notepad.exe" as safe application
3. **Add Custom Extension**:
   - Enter `.xyz` in custom extension field
   - Enter `wordpad.exe` as custom application
4. **Review Configuration**:

   ```json
   {
     "file_associations": {
       ".scr": "notepad.exe",
       ".pif": "notepad.exe", 
       ".xyz": "wordpad.exe"
     }
   }
   ```

5. **View Generated Artifacts**:
   - **PowerShell**: Script with admin checks and error handling
   - **GPO XML**: Group Policy export with registry entries
   - **Registry**: `.reg` file for manual import
   - **Batch**: Deployment automation script
6. **Download Package**: Complete ZIP with all artifacts and documentation

## Understanding Generated Artifacts

### PowerShell Script Features

- **Administrative Privilege Check**: Ensures proper execution context
- **Backup Creation**: Automatic registry backup before changes
- **Error Handling**: Comprehensive error detection and reporting
- **Logging**: Detailed operation logging
- **Verification**: Post-change verification and rollback capability

### GPO XML Structure

- **Proper Formatting**: Valid XML structure for Group Policy import
- **Domain Integration**: Ready for Active Directory deployment
- **Computer Configuration**: Machine-level policy settings
- **Registry Extensions**: Direct registry modifications

### Registry File Format

- **Standard Format**: Compatible with Windows Registry Editor
- **Version Header**: Proper registry file format specification
- **Key Paths**: Correct HKEY structure and paths
- **Documentation**: Inline comments explaining modifications

### Batch Script Capabilities

- **Admin Checks**: Privilege verification before execution
- **Registry Import**: Automated `.reg` file import
- **PowerShell Execution**: Cross-script coordination
- **Error Handling**: Exit codes and error reporting

## Security Best Practices

### ⚠️ Critical Reminders

1. **Always Test First**: Test all configurations in non-production environments
2. **Create Backups**: Backup systems before applying changes
3. **Understand Impact**: Review risk levels and affected systems
4. **Incremental Deployment**: Apply changes gradually across infrastructure
5. **Monitor Results**: Verify changes work as expected

### Testing Strategy

#### Development Environment

1. **Isolated Testing**: Use dedicated test machines
2. **Snapshot Creation**: VM snapshots before changes
3. **Functionality Verification**: Ensure changes work as intended
4. **Impact Assessment**: Monitor for unexpected side effects

#### Production Deployment

1. **Pilot Group**: Deploy to small subset of systems first
2. **Monitoring**: Watch for issues during initial deployment
3. **Rollback Plan**: Prepare rollback procedures
4. **Documentation**: Document changes and any issues encountered

### Risk Management

#### High Risk Controls

- **Extra Testing**: Extended testing period
- **Management Approval**: Explicit approval for high-risk changes
- **Rollback Preparation**: Immediate rollback capability
- **Communication**: Notify affected users of changes

#### Medium Risk Controls

- **Standard Testing**: Normal testing procedures
- **Documentation**: Record changes and expected impact
- **Monitoring**: Watch for issues post-deployment

#### Low Risk Controls

- **Basic Testing**: Verify functionality
- **Standard Deployment**: Normal deployment procedures

## Troubleshooting

### Common Issues

#### Configuration Not Saved

- **Cause**: Validation failed for entered settings
- **Solution**: Check for required fields and valid formats
- **Check**: Error messages in the interface

#### No Artifacts Generated

- **Cause**: Settings incompatible with available generators
- **Solution**: Verify settings format matches control requirements
- **Check**: Review control documentation for required fields

#### PowerShell Script Fails

- **Cause**: Insufficient privileges or system restrictions
- **Solution**: Run PowerShell as Administrator
- **Check**: Execution policy settings (`Get-ExecutionPolicy`)

#### Registry Import Fails

- **Cause**: Invalid registry format or access restrictions
- **Solution**: Verify file format and run as Administrator
- **Check**: Registry file syntax and key permissions

### Getting Help

1. **Review Documentation**: Check module-specific documentation
2. **Validate Settings**: Ensure configuration matches schema requirements
3. **Check Logs**: Review PowerShell script output for specific errors
4. **Test Incrementally**: Apply changes step by step to isolate issues

## Next Steps

### Explore Advanced Features

- **Custom Controls**: Create user-defined security policies
- **Multiple Formats**: Use different deployment methods
- **Batch Operations**: Apply settings across multiple systems

### Extend the Application

- **New Controls**: Add security controls for specific needs
- **Custom Generators**: Create generators for additional platforms
- **UI Enhancements**: Customize interface for organizational needs

### Integration

- **CI/CD Pipelines**: Integrate with deployment automation
- **Configuration Management**: Use with existing CM tools
- **Monitoring**: Integrate with security monitoring systems

This application provides a professional foundation for Windows security configuration management. Start with simple controls and gradually expand to more complex policies as you become familiar with the system.
