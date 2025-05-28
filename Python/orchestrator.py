"""
Orchestrator/Agent Script for Unreal MCP

This script accepts a natural language prompt, queries project/asset context, plans a sequence of tool calls, executes each step, and captures outputs/errors. It is the entry point for advanced automation, PCG, and multi-step workflows.

Usage Example:
    python orchestrator.py "Make a procedural dungeon level with random rooms and place 5 types of monsters, a player spawn, and exit."

Best Practices:
- Use atomic, modular tools for each step.
- Always query context (assets, metadata, examples) before planning.
- Capture and log all outputs and errors for each step.
- Implement retry logic for failed steps.
- If a step is ambiguous, prompt the user or LLM for clarification.
- Summarize results and provide links/paths to generated content.
"""

import sys
import logging
from typing import List, Dict, Any
import time
import importlib
from tools import asset_management_tools
from tools import ui_tools
from tools import project_tools

# Import tool APIs (assume FastMCP or direct tool calls)
# from tools.asset_management_tools import ...
# from tools.ui_tools import ...
# ... (import other tool modules as needed)

logger = logging.getLogger("Orchestrator")
logging.basicConfig(level=logging.INFO)

MAX_RETRIES = 2
RETRY_DELAY = 2  # seconds

def query_project_context() -> Dict[str, Any]:
    """Query project/asset context using inventory and metadata tools."""
    ctx = asset_management_tools.Context()
    assets = asset_management_tools.list_assets(ctx, with_metadata=True)
    # For brevity, get metadata for first 3 assets only
    asset_list = assets.get('assets', []) if assets.get('success') else []
    metadata = []
    for asset in asset_list[:3]:
        path = asset.get('path') if isinstance(asset, dict) else asset
        if path:
            meta = asset_management_tools.get_asset_metadata(ctx, path)
            metadata.append(meta)
    return {'assets': asset_list, 'metadata': metadata}

def extract_examples(asset_type: str, count: int = 3) -> List[Dict[str, Any]]:
    """Extract real asset/code/Blueprint/script examples for a given type."""
    ctx = asset_management_tools.Context()
    result = asset_management_tools.extract_asset_examples(ctx, asset_type, count)
    return result.get('examples', []) if result.get('success', True) else []

def plan_steps(prompt: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Plan a sequence of tool calls from the prompt and context."""
    # For now, use a simple rule-based plan for the dungeon prompt
    if 'dungeon' in prompt.lower():
        return [
            {'tool': 'create_level', 'args': {'level_name': 'ProceduralDungeon'}},
            {'tool': 'batch_create_assets', 'args': {'assets': [
                {'type': 'Blueprint', 'name': 'BP_Room', 'save_path': '/Game/Blueprints'},
                {'type': 'Blueprint', 'name': 'BP_Monster1', 'save_path': '/Game/Blueprints'},
                {'type': 'Blueprint', 'name': 'BP_Monster2', 'save_path': '/Game/Blueprints'},
                {'type': 'Blueprint', 'name': 'BP_Monster3', 'save_path': '/Game/Blueprints'},
                {'type': 'Blueprint', 'name': 'BP_Monster4', 'save_path': '/Game/Blueprints'},
                {'type': 'Blueprint', 'name': 'BP_Monster5', 'save_path': '/Game/Blueprints'},
                {'type': 'Blueprint', 'name': 'BP_PlayerSpawn', 'save_path': '/Game/Blueprints'},
                {'type': 'Blueprint', 'name': 'BP_Exit', 'save_path': '/Game/Blueprints'}
            ]}},
            # Add more steps as needed
        ]
    # Default: no plan
    return []

def prompt_for_ambiguity(step: Dict[str, Any]) -> Dict[str, Any]:
    logger.warning(f"Ambiguous step detected: {step}. Skipping for now.")
    return step

def execute_steps(steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Execute each planned step, capturing outputs and errors. Implements feedback loop and retry logic."""
    results = []
    ctx = asset_management_tools.Context()
    for step in steps:
        attempt = 0
        while attempt <= MAX_RETRIES:
            try:
                logger.info(f"Executing step: {step} (Attempt {attempt+1})")
                tool = step.get('tool')
                args = step.get('args', {})
                if tool == 'create_level':
                    output = ui_tools.create_umg_widget_blueprint(ctx, **args)  # Placeholder, replace with actual level creation
                elif tool == 'batch_create_assets':
                    output = asset_management_tools.batch_create_assets(ctx, **args)
                else:
                    output = {'success': False, 'message': f'Unknown tool: {tool}'}
                error = None if output.get('success') else output.get('message')
                if error:
                    raise Exception(error)
                results.append({"step": step, "output": output, "error": None})
                break
            except Exception as e:
                logger.error(f"Error executing step: {e}")
                if attempt < MAX_RETRIES:
                    logger.info(f"Retrying step after {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
                    attempt += 1
                else:
                    results.append({"step": step, "output": None, "error": str(e)})
                    break
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py \"<prompt>\"")
        sys.exit(1)
    prompt = sys.argv[1]
    logger.info(f"Received prompt: {prompt}")
    context = query_project_context()
    examples = extract_examples(asset_type="Blueprint")  # Example usage
    steps = plan_steps(prompt, context)
    results = execute_steps(steps)
    logger.info(f"Results: {results}")
    print("Orchestration complete. See logs for details.")

if __name__ == "__main__":
    main() 