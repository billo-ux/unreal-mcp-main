# Unreal MCP Tools Refactor & Validation

This document tracks the progress and validation of the Unreal MCP Python tool suite refactor and feature implementation.

# Task Overview: Unreal MCP Toolchain

A concise, logically grouped checklist for the refactor, validation, and expansion of the Unreal MCP tool suite. Tasks are grouped by major area for clarity and deduplication.

---

## 1. Asset Tools

### Completed
- [x] Grouped all asset tools into super group modules (basic, advanced, batch, reference, validation)
- [x] Refactored basic asset tools (CRUD for Blueprints, Levels, Materials, Niagara, Static Meshes)
- [x] Refactored advanced asset tools (Animation, Physics, AI, Data, Cinematics, Game Modes)
- [x] Batch operations for asset creation, deletion, renaming, and property setting (basic & advanced)
- [x] Asset selection tools (select_actors, deselect_actors, get_selected_actors)
- [x] Asset inventory: Enhanced `list_assets` to return metadata
- [x] Designed and implemented `get_asset_metadata`
- [x] Example extraction tool: Designed and implemented `extract_asset_examples`
- [x] Asset reference search: Stub and partial implementation for `find_asset_references`
- [x] Ensured Cursor rules compliance (type safety, no Any/Optional, robust docstrings, error handling)
- [x] Merged and deduplicated overlapping tools

### In Progress
- [ ] Complete and validate asset reference search for all asset types
- [ ] Document usage and add example runs for asset metadata, example extraction, and reference search
- [ ] Add support for configuring asset properties after creation
- [ ] Add diagnostics tools for asset management errors
- [ ] Add support for new Unreal asset types (Verse, Control Rig, Data Layers, World Partition, etc.)

### Future
- [ ] Batch import/export/list operations
- [ ] Advanced asset property configuration on creation (e.g., material parameters, animation curves)
- [ ] Asset/Blueprint validation tools
- [ ] Advanced asset reference search

---

## 2. UI & Editor Tools

### Completed
- [x] Refactored UI tools (UMG/widget creation, UI binding, viewport management)
- [x] Expanded UMG/widget tools (add_text_block_to_widget, add_button_to_widget, add_widget_to_viewport)
- [x] Refactored editor tools (actor/level management, undo/redo, world/editor settings, commands)
- [x] Selection tools for actors/assets in the editor

### In Progress
- [ ] Widget hierarchy management tools (reorder_widget, remove_widget_from_parent, get_widget_hierarchy) [Blocked: backend required]
- [ ] Expand dynamic widget creation (images, sliders, progress bars, etc.)
- [ ] Document usage and add example runs for new widget types and hierarchy tools
- [ ] Fix and enable the focus viewport tool (needs validation)
- [ ] Add tools for sending notifications/dialogs to the editor UI

### Future
- [ ] Tools for Editor Utility Widgets (Blutilities)
- [ ] Tools for managing widget hierarchy and dynamic parenting
- [ ] Tools for querying and reporting Unreal logs and diagnostics
- [ ] Tools for error reporting and diagnostics across all tool groups

---

## 3. Orchestration & Automation

### Completed
- [x] Orchestrator/agent script scaffold (orchestrator.py)
- [x] Capture and log outputs/errors for each tool call

### In Progress
- [ ] Implement context querying, planning, and step execution logic in orchestrator
- [ ] Implement retry logic for failed steps
- [ ] Optionally prompt user/LLM for ambiguous steps
- [ ] Document feedback loop and error handling best practices

### Future
- [ ] Expand orchestration for multi-agent/LLM workflows
- [ ] Add analytics/telemetry for tool usage and errors
- [ ] Integrate with CI/CD for automated tool validation

---

## 4. Testing & Diagnostics

### Completed
- [x] query_editor_logs tool implemented

### In Progress
- [ ] Implement automation test running (run_automation_test)
- [ ] Implement automation test result reporting (report_automation_test_results)
- [ ] Document usage and add example runs for diagnostics tools

### Future
- [ ] Integrate testing, debugging, and QA best practices
- [ ] Add performance profiling and optimization guides

---

## 5. Source Control & Localization

### In Progress
- [ ] Implement source control integration (run_source_control_command)
- [ ] Implement localization asset management (manage_localization_asset)

### Future
- [ ] Tools for project build/packaging automation and reporting
- [ ] Tools for automation/CI workflows and test reporting

---

## 6. Documentation & Example Gallery

### In Progress
- [ ] Systematically document all tools and add example runs to the gallery
- [ ] Add LLM prompt templates and docstring examples for all tools
- [ ] Centralize documentation and create an example gallery
- [ ] Automate documentation/gen scripts for new tools
- [ ] Add a "Best Practices" section to documentation

---

## 7. General Refactor & Validation

### Completed
- [x] Refactored all tools to be atomic, modular, and composable
- [x] Moved and grouped tools into super group files with registration functions
- [x] Deduplicated and merged similar tools (total tool count under 40)
- [x] Ensured robust error handling and docstrings for all tools
- [x] Audited all tools for strict type safety and Cursor rules compliance

### In Progress
- [ ] Code review, documentation review, and user testing for each tool group
- [ ] Collect feedback and log issues for each tool group
- [ ] Update validation checklist with results
- [ ] Integrate and test tools in an actual Unreal Engine environment

---

# Implementation Plan & Recommendations

1. **Unblock Widget Hierarchy Tools:** Implement new UnrealMCP backend commands for widget hierarchy management (reorder, remove, get hierarchy).
2. **Complete Orchestrator:** Implement context querying, planning, and step execution logic; add retry logic and error handling documentation.
3. **Testing & Diagnostics:** Implement automation test running and reporting; document and add example runs.
4. **Source Control & Localization:** Implement and document source control and localization tools.
5. **Documentation:** Systematically document all tools, add example runs, and create a best practices section.
6. **Validation:** Continue code review, user testing, and validation for all tool groups; update checklist with results.
7. **Expand Asset & UI Tools:** Add support for new asset types, batch operations, advanced property configuration, and UI/UMG expansion.
8. **Future:** Integrate analytics, CI/CD, advanced automation, and support for new Unreal Engine features as needed.

---

This list will be updated and deepened as the project progresses, with each tool group and feature tracked for completion, validation, and documentation.

## Implementation Plan

### Highest Priority: Context & Tool Checklist for Advanced UE Automation/PCG

#### Subtasks:
- [x] Enhance asset inventory & metadata tools (in progress)
    - Expand `list_assets` to include metadata
    - Add and document `get_asset_metadata`
- [x] Implement example extraction tool
    - Design and implement `extract_asset_examples`
- [x] Complete and validate asset reference search
    - Finalize and test `find_asset_references`
- [x] Refactor all tools to be atomic, modular, and composable
- [x] Implement batch operations and advanced asset creation tools
- [x] Expand UI automation tools for UMG/Slate and hierarchy management
- [ ] Develop orchestrator/agent script for prompt-to-plan and step sequencing
    - [ ] Implement context querying logic
    - [ ] Implement planning logic (LLM or rule-based)
    - [ ] Implement step execution logic
    - [ ] Document usage and add example run
- [ ] Add feedback loop for error/output capture and retry logic
    - [x] Capture and log outputs/errors for each tool call (present in most tools)
    - [ ] Implement retry logic for failed steps (not present)
    - [ ] Optionally prompt user/LLM for ambiguous steps
    - [ ] Document feedback loop and error handling best practices
- [ ] Add LLM prompt templates and docstring examples for all tools
- [ ] Create testing and diagnostics tools (logs, unit/integration tests)
    - [x] query_editor_logs tool implemented
    - [ ] Implement automation test running (run_automation_test is a stub)
    - [ ] Implement automation test result reporting (report_automation_test_results is a stub)
    - [ ] Document usage and add example runs for diagnostics tools
- [ ] Add asset/Blueprint validation tools
- [ ] Centralize documentation and create an example gallery
- [ ] Integrate source control, CI/CD, localization, and analytics tools
    - [ ] Implement source control integration (run_source_control_command is a stub)
    - [ ] Implement localization asset management (manage_localization_asset is a stub)
- [ ] Automate documentation and generation scripts for new tools
- [ ] Add an "example run" for each new tool/feature in the example gallery

### Ongoing: Refactor & Validate Existing Tools
- Continue validation, documentation, and user testing for all tool groups as previously outlined.

### Next Action: Deepen validation for each tool group

#### Subtasks:
- [ ] Code review for each tool group (basic, advanced, node/graph, editor, UI, project, asset management)
- [ ] Documentation review for each tool group
- [ ] User testing for each tool group in an active Unreal Engine instance
- [ ] Collect feedback and log issues for each tool group
- [ ] Update validation checklist with results

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
- Add retry logic and feedback loop for orchestrator and tool calls
- Add and document automation test running and reporting
- Expand widget hierarchy management tools from stubs to full implementations
- Document all new and updated tools with usage examples and best practices

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

## Blockers & Next Concrete Actions

- Widget hierarchy management tools (reorder_widget, remove_widget_from_parent, get_widget_hierarchy) are blocked: No backend/server-side implementation exists in UnrealMCP for these commands. Full implementation requires new UnrealMCP backend commands for widget reordering, removal, and hierarchy querying.
- Orchestrator/agent script (orchestrator.py) is scaffolded but lacks context querying, planning, and step execution logic. Needs full implementation and example runs.
- Feedback loop retry logic is not present; most tools log errors but do not retry or prompt for ambiguous steps. Needs retry logic and documentation.
- Testing & diagnostics: query_editor_logs is implemented, but automation test running and reporting are stubs. Needs implementation and documentation.
- Source control and localization tools are stubs (run_source_control_command, manage_localization_asset). Need full implementation.
- Documentation and example runs are missing for many new tools and features. Needs systematic documentation and gallery updates.
- Many advanced/future features (analytics, CI/CD, advanced PCG, etc.) are not started and require design and planning.

### Immediate Next Steps
- Implement new UnrealMCP backend commands for widget hierarchy management (reorder, remove, get hierarchy) to unblock UI automation tools.
- Complete orchestrator/agent script with planning and execution logic.
- Add retry logic to feedback loop and document error handling best practices.
- Implement automation test running and reporting tools.
- Implement source control and localization asset management tools.
- Systematically document all tools and add example runs to the gallery.
- Continue code review, user testing, and validation for all tool groups.

