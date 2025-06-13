# System Architecture

## Overview

The Windows Security Controls Generator follows a modular, registry-based architecture that promotes extensibility and maintainability.

## Core Architecture Principles

### 1. Interface-Driven Design

All major components implement well-defined interfaces:

- `ISecurityControl` - Security control contract
- `IArtifactGenerator` - Artifact generation contract  
- `IUIRenderer` - User interface rendering contract
- `IControlRegistry` - Control management contract
- `IGeneratorRegistry` - Generator management contract

### 2. Registry Pattern

Central registries manage component discovery and instantiation:

- **ControlRegistry** - Maps control types to implementations and UI renderers
- **GeneratorRegistry** - Maps generator types to implementations

### 3. Factory Pattern

`AppFactory` provides centralized component creation and wiring.

## Component Flow

```plaintext
User Request → UIService → ControlRegistry → SecurityControl
                     ↓
             ArtifactService → GeneratorRegistry → Generators
                     ↓
                Generated Artifacts → Download Package
```

## Key Components

### Main Application (`main.py`)

- Entry point coordinating all components
- Handles both standard and custom control workflows
- Error handling and user feedback

### App Factory (`app_factory.py`)

- Central factory for component creation
- Registers all controls, generators, and UI renderers
- Provides dependency injection

### Core Layer

- **Interfaces** (`core/interfaces.py`) - Abstract contracts for all major components
- **Base Classes** (`core/base_control.py`) - Common functionality for security controls
- **Registries** (`core/registries.py`) - Component discovery and management

### Controls Layer

Security control implementations with validation logic and metadata:

- File Association Control
- Network Traffic Control  
- WinX Menu Control
- Custom Control (user-defined)

### Generators Layer

Artifact generation engines:

- **GPO Generator** - Group Policy Object XML
- **PowerShell Generator** - PowerShell scripts
- **Registry Generator** - Windows Registry files
- **Batch Generator** - Batch deployment scripts

### UI Layer

Streamlit-based user interface components:

- Control-specific configuration forms
- Dynamic UI generation based on control schemas
- Artifact display and download interfaces

### Services Layer

Business logic coordination:

- **ArtifactService** - Orchestrates artifact generation and packaging
- **UIService** - Manages common UI elements and styling

## Data Flow

1. **Initialization**: AppFactory creates and wires all components
2. **Control Selection**: User selects control type via UIService
3. **Configuration**: Control-specific UI renderer collects settings
4. **Validation**: Control validates settings against its schema
5. **Generation**: ArtifactService coordinates generators to create artifacts
6. **Packaging**: Multiple artifacts bundled into downloadable package
7. **Delivery**: User downloads complete package with documentation

## Extensibility Points

### Adding New Controls

1. Implement `ISecurityControl` interface
2. Create corresponding `IUIRenderer`
3. Register in `AppFactory.create_control_registry()`

### Adding New Generators

1. Implement `IArtifactGenerator` interface
2. Register in `AppFactory.create_generator_registry()`

### Adding New UI Components

1. Extend `BaseUIRenderer`
2. Implement control-specific configuration logic
3. Register with corresponding control

This architecture ensures loose coupling, high cohesion, and easy extensibility for future security controls and artifact types.
