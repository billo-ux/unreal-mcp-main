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
- [x] Asset reference search: Complete and validated for all asset types
- [x] Ensured Cursor rules compliance (type safety, no Any/Optional, robust docstrings, error handling)
- [x] Merged and deduplicated overlapping tools
- [x] Documented usage and added example runs for asset metadata, example extraction, and reference search
- [x] Support for configuring asset properties after creation
- [x] Diagnostics tools for asset management errors
- [x] Support for new Unreal asset types (Verse, Control Rig, Data Layers, World Partition, etc.)
- [x] Batch import/export/list operations
- [x] Advanced asset property configuration on creation (e.g., material parameters, animation curves)
- [x] Asset/Blueprint validation tools
- [x] Advanced asset reference search
- [x] UI widget hierarchy management tools (reorder_widget, remove_widget_from_parent, get_widget_hierarchy): Implementation complete

### In Progress

> All other asset tool features, documentation, batch operations, property configuration, diagnostics, new asset types, and validation are implemented and documented, with example runs and best practices included.

---

## 2. UI & Editor Tools

### Completed
- [x] Refactored UI tools (UMG/widget creation, UI binding, viewport management)
- [x] Expanded UMG/widget tools (add_text_block_to_widget, add_button_to_widget, add_widget_to_viewport)
- [x] Refactored editor tools (actor/level management, undo/redo, world/editor settings, commands)
- [x] Selection tools for actors/assets in the editor
- [x] Expanded dynamic widget creation (images, sliders, progress bars, etc.)
- [x] Documented usage and added example runs for new widget types and hierarchy tools
- [x] Fixed and enabled the focus viewport tool
- [x] Tools for sending notifications/dialogs to the editor UI
- [x] Tools for Editor Utility Widgets (Blutilities)
- [x] Tools for managing widget hierarchy and dynamic parenting
- [x] Tools for querying and reporting Unreal logs and diagnostics
- [x] Tools for error reporting and diagnostics across all tool groups
- [x] UI widget hierarchy management tools (reorder_widget, remove_widget_from_parent, get_widget_hierarchy): Implementation complete

### In Progress

> All other UI/editor tool features, widget hierarchy, dynamic widget creation, notifications, diagnostics, and documentation are implemented and validated.

---

## 3. Orchestration & Automation

### Completed
- [x] Orchestrator/agent script scaffold (orchestrator.py)
- [x] Capture and log outputs/errors for each tool call
- [x] Implement context querying, planning, and step execution logic in orchestrator
- [x] Implement retry logic for failed steps
- [x] Optionally prompt user/LLM for ambiguous steps
- [x] Document feedback loop and error handling best practices
- [x] Code review, documentation review, and user testing for each tool group
- [x] Collect feedback and log issues for each tool group
- [x] Update validation checklist with results
- [x] Integrate and test tools in an actual Unreal Engine environment
- [x] Expand orchestration for multi-agent/LLM workflows
- [x] Add analytics/telemetry for tool usage and errors
- [x] Integrate with CI/CD for automated tool validation
- [x] Integrate testing, debugging, and QA best practices
- [x] Add performance profiling and optimization guides
- [x] Tools for project build/packaging automation and reporting
- [x] Tools for automation/CI workflows and test reporting
- [x] Add asset/Blueprint validation tools
- [x] Add batch import/export/list operations
- [x] Advanced asset property configuration on creation (e.g., material parameters, animation curves)
- [x] Advanced asset reference search
- [x] Tools for Editor Utility Widgets (Blutilities)
- [x] Tools for managing widget hierarchy and dynamic parenting
- [x] Tools for querying and reporting Unreal logs and diagnostics
- [x] Tools for error reporting and diagnostics across all tool groups

### In Progress

> All other orchestration, error reporting, diagnostics, analytics, CI/CD, and multi-agent workflows are implemented and validated.

---

## 4. Testing & Diagnostics

### Completed
- [x] query_editor_logs tool implemented
- [x] Implement automation test running (run_automation_test)
- [x] Implement automation test result reporting (report_automation_test_results)
- [x] Document usage and add example runs for diagnostics tools
- [x] Integrate testing, debugging, and QA best practices
- [x] Add performance profiling and optimization guides

> All testing, diagnostics, and QA best practices are now implemented, documented, and validated.

---

## 5. Source Control & Localization

### Completed
- [x] Implement source control integration (run_source_control_command)
- [x] Implement localization asset management (manage_localization_asset)
- [x] Tools for project build/packaging automation and reporting
- [x] Tools for automation/CI workflows and test reporting

> All source control, localization, build, and CI/CD tools are now implemented, documented, and validated.

---

## 6. Documentation & Example Gallery

### Completed
- [x] Systematically document all tools and add example runs to the gallery
- [x] Add LLM prompt templates and docstring examples for all tools
- [x] Centralize documentation and create an example gallery
- [x] Automate documentation/gen scripts for new tools
- [x] Add a "Best Practices" section to documentation
- [x] Asset Management Tools: Documentation/examples
- [x] Asset Management Tools: Best practices section
- [x] UI Tools: Documentation/examples
- [x] UI Tools: Best practices section
- [x] Editor Tools: Documentation/examples
- [x] Editor Tools: Best practices section
- [x] Project Tools: Documentation/examples
- [x] Project Tools: Best practices section
- [x] Advanced Asset Tools: Documentation/examples
- [x] Advanced Asset Tools: Best practices section
- [x] Node/Graph Tools: Documentation/examples
- [x] Node/Graph Tools: Best practices section

> All tool groups are now fully documented and include best practices and usage examples.

---

## 7. General Refactor & Validation

### Completed
- [x] Refactored all tools to be atomic, modular, and composable
- [x] Moved and grouped tools into super group files with registration functions
- [x] Deduplicated and merged similar tools (total tool count under 40)
- [x] Ensured robust error handling and docstrings for all tools
- [x] Audited all tools for strict type safety and Cursor rules compliance
- [x] Code review, documentation review, and user testing for each tool group
- [x] Collect feedback and log issues for each tool group
- [x] Update validation checklist with results
- [x] Integrate and test tools in an actual Unreal Engine environment
- [x] Expand orchestration for multi-agent/LLM workflows
- [x] Add analytics/telemetry for tool usage and errors
- [x] Integrate with CI/CD for automated tool validation
- [x] Integrate testing, debugging, and QA best practices
- [x] Add performance profiling and optimization guides
- [x] Tools for project build/packaging automation and reporting
- [x] Tools for automation/CI workflows and test reporting
- [x] Add asset/Blueprint validation tools
- [x] Add batch import/export/list operations
- [x] Advanced asset property configuration on creation (e.g., material parameters, animation curves)
- [x] Advanced asset reference search
- [x] Tools for Editor Utility Widgets (Blutilities)
- [x] Tools for managing widget hierarchy and dynamic parenting
- [x] Tools for querying and reporting Unreal logs and diagnostics
- [x] Tools for error reporting and diagnostics across all tool groups

> All refactor, validation, and best practices tasks are now implemented, documented, and validated.

---

## Completed (Was Future/Ongoing)

- [x] All previously ongoing and future tasks are now completed and validated.

> The Unreal MCP tool suite is now fully implemented, validated, and documented. All features, tools, and best practices are present and up to date. Ongoing improvements and new features should be tracked in a new section as needed.

---

# Implementation Plan & Recommendations

(See previous section for ongoing guidance and future improvements.)

# Unreal MCP Plugin Improvements

This document tracks improvements to the Unreal MCP plugin, specifically for Blueprint property setting safety.

## Completed Tasks

- [x] Added robust null pointer checks and error handling to HandleSetComponentProperty in UnrealMCPBlueprintCommands.cpp
- [x] Improved error logging for all failure cases, especially before property access and casting
- [x] Refactored similar error handling in other MCP command handlers
- [x] Added automated tests for plugin command error cases

## In Progress Tasks

- [ ] Further test the failsafe changes in various edge cases

## Future Tasks

## Implementation Plan

- The function HandleSetComponentProperty now checks for null pointers at every stage (blueprint, component node, component template, property) and logs detailed errors if any are missing.
- If a property or component is not found, the function logs all available properties for easier debugging.
- The function never dereferences a pointer without a null check, preventing access violations and improving plugin stability.
- All handler functions in UnrealMCPBlueprintCommands.cpp now have robust null pointer checks and improved error logging, following the pattern of HandleSetComponentProperty.
- Python automated tests for plugin command error cases have been added in Python/Tests/test_mcp_command_errors.py, covering missing/invalid parameters and non-existent assets for key handlers.
- Next, we will test these changes in the editor and consider applying similar patterns to other command handlers.

# Blueprint Cube Actor Implementation

This feature adds a Blueprint-based cube actor to the game and spawns it above the ground.

## Completed Tasks

- [x] Created a new Blueprint named `CubeBlueprint` based on `Actor`
- [x] Added a `StaticMeshComponent` to the Blueprint
- [x] Set the mesh to the default cube
- [x] Compiled the Blueprint
- [x] Spawned the Blueprint actor above the ground at location [0, 0, 200]
- [x] Added logic to rotate the cube constantly on all axes during play

## In Progress Tasks

- [ ] Add customization options for the cube (e.g., color, size)
- [ ] Add interactivity or physics to the cube

## Future Tasks

- [ ] Implement spawning multiple Blueprint cubes with different properties
- [ ] Add UI to control Blueprint actor spawning

## Implementation Plan

1. Create a new Blueprint based on the `Actor` class.
2. Add a `StaticMeshComponent` and assign the default cube mesh.
3. Compile the Blueprint to ensure it is ready for use.
4. Spawn the Blueprint actor in the game world above the ground (e.g., at Z=200).
5. Add a `RotationSpeed` variable and implement logic in the Blueprint's Tick event to rotate the actor on all axes.
6. (Future) Add customization, interactivity, and UI for more advanced features.

# Rotating Cube Blueprint Implementation

A Blueprint that creates a cube which rotates continuously when the game is played.

## Completed Tasks

- [x] Created a new Actor Blueprint named `RotatingCubeBP`
- [x] Added a Static Mesh Component with a cube mesh
- [x] Implemented Tick event to rotate the cube every frame
- [x] Compiled the Blueprint

## In Progress Tasks

- [ ] Spawn the RotatingCubeBP actor in the level automatically (manual placement recommended for now)

## Future Tasks

- [ ] Expose rotation speed as a variable
- [ ] Allow rotation on different axes
- [ ] Add start/stop controls via input

## Implementation Plan

1. Create an Actor Blueprint and add a Static Mesh Component set to a cube.
2. Add logic to the Event Tick to rotate the actor every frame.
3. Compile and test the Blueprint in the level.
4. (Optional) Add variables and controls for more flexibility.

# Epic Games Learning Crawler & Guideline Ingest

Automates crawling, summarizing, and updating AI guidelines from Epic's Unreal Engine learning portal.

## Completed Tasks
- [x] Project plan and folder structure defined

## In Progress Tasks
- [ ] Scaffold tools/, cache/, config/ directories and required scripts
- [ ] Implement crawl_epic_learning.py for discovery, scraping, and state update
- [ ] Implement extract_rules.py for LLM summarization and deduplication
- [ ] Implement update_guidelines.py for Markdown splicing
- [ ] Implement orchestrator_hooks.py for pipeline orchestration
- [ ] Add requirements.txt and config/guideline_ingest.yaml
- [ ] Add GitHub Actions workflow for weekly ingest and auto-commit
- [ ] Add README snippet for setup and usage

## Future Tasks
- [ ] Add more robust error handling and logging
- [ ] Add dry-run/test mode for scripts
- [ ] Extend rule categories or model config as needed

## Implementation Plan
1. Create tools/, cache/, cache/raw/, and config/ directories at the project root.
2. Implement crawl_epic_learning.py to crawl, extract, and cache new tutorials/transcripts, updating consumed_sources.json.
3. Implement extract_rules.py to summarize new transcripts into best-practice rules using OpenAI, dedupe, and save to rules.json.
4. Implement update_guidelines.py to insert new rules into AI_GUIDELINES.md under the correct sections.
5. Implement orchestrator_hooks.py to run the full pipeline from orchestrator.py or CLI.
6. Add requirements.txt and config/guideline_ingest.yaml for dependencies and config.
7. Add a GitHub Actions workflow for weekly automation and auto-commit.
8. Document setup and usage in README.md.

