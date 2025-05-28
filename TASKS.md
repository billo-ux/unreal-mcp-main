# Unreal MCP Tools Refactor & Validation

This document tracks the progress and validation of the Unreal MCP Python tool suite refactor and feature implementation.

## Completed Tasks

- [x] Grouped all tools into super group modules (basic, advanced, node/graph, editor, UI, project, asset management)
- [x] Refactored basic asset tools (CRUD for Blueprints, Levels, Materials, Niagara, Static Meshes)
- [x] Refactored advanced asset tools (Animation, Physics, AI, Data, Cinematics, Game Modes)
- [x] Refactored node & graph tools (node creation, connection, variable management, property access)
- [x] Refactored editor tools (actor/level management, undo/redo, world/editor settings, commands)
- [x] Refactored UI tools (UMG/widget creation, UI binding, viewport management)
- [x] Refactored project tools (input mappings, project settings, plugin management)
- [x] Refactored asset management tools (import/export/list assets)
- [x] Ensured all tools comply with Cursor rules (no Optional/Any, robust docstrings, error handling)
- [x] Added/updated registration for all tool groups
- [x] Merged and deduplicated overlapping tools

## In Progress Tasks

- [ ] Deepen validation for each tool group (code review, doc review, user testing)
- [ ] Add more specific asset types and subcategories as needed (e.g., Material Instance, Niagara Emitter, Sound Cue)
- [ ] Enhance error handling and validation for edge cases
- [ ] Add support for configuring asset properties after creation
- [ ] Update documentation and usage examples for all tools
- [ ] Integrate and test tools in an actual Unreal Engine environment
- [ ] Implement selection tools for actors/assets in the editor
- [ ] Implement batch operations (create, delete, rename, set-property) for assets and actors
- [ ] Add asset reference search tools (find where an asset is used)
- [ ] Add tools for creating and running Editor Utility Widgets (Blutilities)
- [ ] Fix and enable the focus viewport tool
- [ ] Add tools for sending notifications or dialogs to the editor UI
- [ ] Add tools for querying logs, errors, and diagnostics from Unreal
- [ ] Expand UMG/widget tools for images, sliders, progress bars, and custom widgets
- [ ] Add tools for managing widget hierarchy and dynamic parenting
- [ ] Add tools for building, cooking, and packaging projects
- [ ] Add tools for interacting with source control (Git, Perforce)
- [ ] Add tools for managing localization assets
- [ ] Add tools for running and reporting automation tests
- [ ] Audit all tools for strict type safety and Cursor rules compliance
- [ ] Expand docstrings with usage examples and add a "Best Practices" section

## Future Tasks

- [ ] Add advanced automation features (batch operations, AI-driven asset generation)
- [ ] Expand UI tools for more complex UMG workflows
- [ ] Add analytics/telemetry for tool usage and errors
- [ ] Integrate with CI/CD for automated tool validation
- [ ] Add support for new Unreal Engine versions and features
- [ ] Add tools for batch import/export/list operations in asset management
- [ ] Add diagnostics tools for asset management errors
- [ ] Add support for very new Unreal features (Verse, Control Rig Graphs, Data Layers, World Partition, etc.)
- [ ] Add tools for asset property configuration on creation (e.g., material parameters, animation curves)
- [ ] Add tools for advanced asset reference search
- [ ] Add tools for widget/UMG expansion and hierarchy management
- [ ] Add tools for error reporting and diagnostics across all tool groups
- [ ] Add tools for localization and translation workflows
- [ ] Add tools for project build/packaging automation and reporting
- [ ] Add tools for source control operations and integration
- [ ] Add tools for querying and reporting Unreal logs and diagnostics
- [ ] Add tools for automation/CI workflows and test reporting

## Implementation Plan

### Refactor & Grouping
- Move and refactor all tools into their respective super group files
- Ensure each file has a `register_<group>_tools(mcp)` function
- Deduplicate and merge similar tools, keeping total tool count under 40
- Use clear, consistent function and parameter names
- Ensure robust error handling and docstrings for all tools
- Audit all tools for strict type safety, no Any/Optional, and Cursor rules compliance
- Expand docstrings with usage examples and add a "Best Practices" section

### Validation Approach
- Code review for completeness and correctness
- Documentation of expected behavior and usage
- User testing in an active Unreal Engine instance
- Deepen validation for each tool group (code review, doc review, user testing)
- Integrate and test tools in an actual Unreal Engine environment

### Validation Checklist (from Asset Creation Tools Validation)
- [x] Animation: Animation Blueprint, Composite, Montage, Aim Offset, Blend Space, Pose Asset
- [x] AI: Behavior Tree, Blackboard
- [x] Blueprint: Blueprint Class
- [x] Cinematics: Level Sequence
- [x] Material: Material, Material Instance
- [x] Physics: Physics Asset
- [x] UI: Widget Blueprint
- [x] Niagara: Niagara System, Niagara Emitter
- [x] Level: Level
- [x] Texture: Render Target
- [x] Gameplay: Game Mode, Game State, Player Controller

### Basic Asset Types (Unreal)
- [x] Blueprint Class (✔️ Low)
- [x] Level (✔️ Low)
- [x] Material (✔️ Low)
- [x] Material Instance (✔️ Low)
- [x] Static Mesh (✔️ Medium)
- [x] Niagara System (✔️ Medium)
- [x] Niagara Emitter (✔️ Medium)
- [x] Texture (✔️ Low)
- [x] Sound Cue (✔️ Medium)
- [x] Sound Wave (✔️ Medium)
- [x] Font (✔️ Low)
- [x] Curve (✔️ Medium)
- [x] Data Table (✔️ Medium)
- [x] Struct (✔️ Medium)
- [x] Enum (✔️ Medium)
- [x] Slate Brush (✔️ Medium)
- [x] Paper2D Sprite (✔️ Medium)
- [x] Paper2D Tile Map (✔️ High)

### Advanced Asset Types (Unreal)
- [x] Animation Blueprint (✔️ Medium)
- [x] Animation Composite (✔️ Medium)
- [x] Animation Montage (✔️ Medium)
- [x] Aim Offset (✔️ Medium)
- [x] Blend Space (✔️ Medium)
- [x] Pose Asset (✔️ Medium)
- [x] Physics Asset (✔️ Medium)
- [x] Behavior Tree (✔️ Medium)
- [x] Blackboard (✔️ Medium)
- [x] Level Sequence (✔️ Medium)
- [x] Data Asset (✔️ Medium)
- [x] Game Mode (✔️ Medium)
- [x] Game State (✔️ Medium)
- [x] Player Controller (✔️ Medium)
- [x] Animation Layer Interface (✔️ High)
- [x] Animation Sequence (✔️ Medium)
- [x] Control Rig (✔️ High)
- [x] MetaHuman (✔️ High)
- [x] Sound Mix (✔️ Medium)
- [x] Sound Class (✔️ Medium)
- [x] Media Player (✔️ Medium)
- [x] Media Texture (✔️ Medium)
- [x] Widget Animation (✔️ Medium)
- [x] Widget Style Asset (✔️ Medium)

### Integration Steps
- Import and register all tool modules in `

## Potential Gaps & Opportunities for Improvement

- Missing Asset Types: Consider adding support for very new Unreal features (e.g., Verse, Control Rig Graphs, Data Layers, World Partition, etc.)
- Asset Property Configuration: Expand tools for setting up default properties/metadata on asset creation (e.g., material parameters, animation curves)
- Batch Operations: No batch asset creation, deletion, or property editing tools yet
- Asset Reference Tools: No tools for finding references to an asset (e.g., "where is this material used?")
- Selection Tools: No explicit tool for selecting actors/assets in the editor
- Editor Utility Widgets: No tools for creating or running Editor Utility Widgets (Blutilities)
- Viewport Camera Control: Focus viewport is present but commented out due to bugs—fixing this would be valuable
- Editor Notifications/Dialogs: No tools for sending notifications or dialogs to the editor UI
- Complex Widget Construction: Tools for adding images, sliders, progress bars, or custom widgets to UMG are not present
- Widget Hierarchy/Parenting: No tools for managing widget hierarchy or dynamic parenting
- Build/Packaging Tools: No tools for triggering project builds, cooking, or packaging
- Version Control Integration: No tools for interacting with source control (e.g., Git, Perforce)
- Localization: No tools for managing localization assets
- Error Reporting/Diagnostics: Tools for querying logs, errors, or diagnostics from Unreal
- Automation/CI: No tools for running automation tests or reporting results

## Cursor Rules Compliance

- Type Safety: Most tools are compliant, but a few (e.g., property_value in set_actor_property) are untyped. All parameters should have explicit types.
- No Optionals/Any: Some tools still use Any, Optional, or untyped parameters. These should be refactored for strict type safety.
- Docstrings: Most tools have docstrings, but not all provide usage examples. Add examples where type hints are missing or ambiguous.
- Error Handling: Generally robust, but some tools could provide more detailed error messages or recovery options.

## Recommendations

- Add/Expand Tools:
  - Selection Tools: Add tools for selecting/deselecting actors/assets in the editor.
  - Batch Operations: Add batch create/delete/rename/set-property tools.
  - Reference Search: Add tools to find all references to a given asset.
  - Editor Utility Widgets: Add tools for creating and running Editor Utility Widgets.
  - Viewport Camera: Fix and enable the focus viewport tool.
  - Widget/UMG Expansion: Add tools for more widget types and hierarchy management.
  - Build/Packaging: Add tools for building, cooking, and packaging projects.
  - Source Control: Add tools for basic source control operations.
  - Localization: Add tools for managing localization assets.
  - Diagnostics: Add tools for querying logs and errors.
  - Automation: Add tools for running and reporting automation tests.
- Refactor for Cursor Rules:
  - Audit all tools for type safety, no Any/Optional, and add docstring usage examples.
  - Refactor any tool with ambiguous or missing parameter types.
- Documentation:
  - Expand docstrings with usage examples, especially for tools with complex parameters.
  - Add a "Best Practices" section to your documentation for tool usage.

## Categorized Improvements & Recommendations

### Basic Asset Tools
- Batch Operations: Add batch create/delete/rename/set-property tools for basic assets.
- Asset Property Configuration: Expand tools for setting up default properties/metadata on asset creation (e.g., material parameters, animation curves).
- Asset Reference Tools: Add tools for finding references to a basic asset (e.g., "where is this material used?").

### Advanced Asset Tools
- Missing Asset Types: Consider adding support for very new Unreal features (e.g., Verse, Control Rig Graphs, Data Layers, World Partition, etc.).
- Batch Operations: Add batch create/delete/rename/set-property tools for advanced assets.
- Asset Reference Tools: Add tools for finding references to an advanced asset.

### Node & Graph Tools
- Widget Hierarchy/Parenting: Add tools for managing widget hierarchy or dynamic parenting in node/graph workflows.

### Editor Tools
- Selection Tools: Add tools for selecting/deselecting actors/assets in the editor.
- Editor Utility Widgets: Add tools for creating and running Editor Utility Widgets (Blutilities).
- Viewport Camera Control: Fix and enable the focus viewport tool.
- Editor Notifications/Dialogs: Add tools for sending notifications or dialogs to the editor UI.
- Error Reporting/Diagnostics: Add tools for querying logs, errors, or diagnostics from Unreal.

### UI Tools
- Complex Widget Construction: Add tools for adding images, sliders, progress bars, or custom widgets to UMG.
- Widget/UMG Expansion: Add tools for more widget types and hierarchy management.

### Project Tools
- Build/Packaging Tools: Add tools for triggering project builds, cooking, or packaging.
- Version Control Integration: Add tools for interacting with source control (e.g., Git, Perforce).
- Localization: Add tools for managing localization assets.
- Automation/CI: Add tools for running automation tests or reporting results.

### Asset Management Tools
- Batch Operations: Add batch import/export/list tools.
- Diagnostics: Add tools for querying logs and errors related to asset management.

### General/All Groups
- Refactor for Cursor Rules: Audit all tools for type safety, no Any/Optional, and add docstring usage examples. Refactor any tool with ambiguous or missing parameter types.
- Documentation: Expand docstrings with usage examples, especially for tools with complex parameters. Add a "Best Practices" section to your documentation for tool usage.

## Next Steps: Concrete Proposal for Selection Tool (Editor Tools)

### Purpose
Enable programmatic selection and deselection of actors and assets in the Unreal Editor, supporting workflows for batch operations, property editing, and automation.

### Proposed API

```python
@mcp.tool()
def select_actors(ctx: Context, names: List[str]) -> Dict[str, Any]:
    """
    Select actors in the current level by name.
    Args:
        names: List of actor names to select
    Returns:
        Dict with success status and list of selected actors
    Example:
        select_actors(ctx, ["Cube1", "Sphere2"])
    """
    ...

@mcp.tool()
def deselect_actors(ctx: Context, names: List[str]) -> Dict[str, Any]:
    """
    Deselect actors in the current level by name.
    Args:
        names: List of actor names to deselect
    Returns:
        Dict with success status and list of remaining selected actors
    Example:
        deselect_actors(ctx, ["Cube1"])
    """
    ...

@mcp.tool()
def get_selected_actors(ctx: Context) -> List[str]:
    """
    Get the list of currently selected actors in the editor.
    Returns:
        List of selected actor names
    Example:
        get_selected_actors(ctx)
    """
    ...
```

### Usage Example
```python
# Select two actors
select_actors(ctx, ["Cube1", "Sphere2"])
# Deselect one actor
deselect_actors(ctx, ["Cube1"])
# Get currently selected actors
selected = get_selected_actors(ctx)
```

### Implementation Notes
- These tools should interact with the Unreal Editor selection API.
- Should provide clear error messages if actors are not found or selection fails.
- Should be type-safe and follow Cursor rules (no Any/Optional, robust docstrings).

---

## Next Steps

1. Prioritize improvements from the above Recommendations and Gaps sections.
2. See a concrete proposal for a specific new tool (e.g., batch operations, selection, build/package).
3. Get a full audit of Cursor rules compliance for all tools.
4. Focus on bug fixes (e.g., focus viewport) or new features as needed