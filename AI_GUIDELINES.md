# AI Blueprint & Asset Creation Guidelines

This guide defines best practices and implicit expectations for AI-driven asset and Blueprint creation in Unreal Engine projects.

## General Principles

- **Visibility:** Always place new actors/assets in the level at a location visible to the player, ideally in front of the default camera and above the ground (e.g., for a 100-unit cube, place at Z=50).
- **Correct Logic:** Connect Blueprint nodes with proper execution flow. Avoid duplicate or conflicting connections (e.g., only one Tick event chain).
- **Frame-Rate Independence:** Use `DeltaSeconds` for any time-based logic (e.g., movement, rotation) to ensure consistent behavior regardless of frame rate.
- **Variable Exposure:** Expose key variables (e.g., RotationSpeed) for easy adjustment in the editor.
- **Default Values:** Set sensible default values for variables and properties so the asset behaves as expected immediately after creation.
- **Error Handling:** If a node or property is unsupported or already connected, handle gracefully and avoid breaking the Blueprint.
- **Placement:** Place actors at a height appropriate for their mesh (e.g., half the mesh height above ground) and at a location visible to the player.
- **No Manual Fixes Required:** Ensure the result is ready to use and does not require the user to manually fix connections, placements, or logic.

## Example: Rotating Cube Blueprint

When asked to create a rotating cube:
- Create a Blueprint Actor with a StaticMeshComponent set to a cube mesh.
- Add a `RotationSpeed` variable (exposed, with a sensible default).
- In the Event Tick, multiply `DeltaSeconds` by `RotationSpeed` and apply to all axes in a `K2_AddActorLocalRotation` node.
- Connect the Tick event to the rotation logic (no duplicate connections).
- Place the actor at `[0, 0, 50]` (for a 100-unit cube) or in front of the camera.
- Compile and ensure the Blueprint is error-free and ready to use.

## How to Update

- Add new edge cases and best practices as you encounter them.
- Use this guide to inform all future AI-driven asset/Blueprint creation and placement tasks. 
