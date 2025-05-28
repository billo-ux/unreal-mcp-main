# unreal-mcp-main
Repository for the Unreal MCP project, matching the workspace directory name.

## Epic Games Learning Crawler & Guideline Ingest

### Setup

1. Install dependencies:
   ```sh
   pip install -r tools/requirements.txt
   ```
2. Set your OpenAI API key (required for extract_rules.py):
   - On Windows (cmd):
     ```cmd
     set OPENAI_API_KEY=sk-...
     ```
   - On Linux/macOS:
     ```sh
     export OPENAI_API_KEY=sk-...
     ```

### Usage

To run the full pipeline manually:
```sh
python tools/crawl_epic_learning.py
python tools/extract_rules.py
python tools/update_guidelines.py
```

Or use the orchestrator hook (see orchestrator.py):
```python
from tools.orchestrator_hooks import ingest_guidelines
ingest_guidelines()
```

The pipeline will only process new tutorials and append new rules to AI_GUIDELINES.md.
