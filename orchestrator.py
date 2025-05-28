# ---------------------------------------------------------------------------
# Configuration & logging  (ADD log level + results path)
# ---------------------------------------------------------------------------

MAX_RETRIES  = int(_config.get("retries", 2))
RETRY_DELAY  = int(_config.get("retry_delay", 2))
LOG_LEVEL    = getattr(logging, _config.get("log_level", "INFO").upper(), logging.INFO)
RESULTS_DIR  = _config.get("results_path", "orchestration_results")

logging.basicConfig(
    format="%(levelname)s │ %(asctime)s │ %(message)s",
    level=LOG_LEVEL,
    handlers=[logging.StreamHandler(sys.stdout)],
)

# ---------------------------------------------------------------------------
# Dynamic tool-module discovery  (OPTIONAL)
# ---------------------------------------------------------------------------

for mod_path in _config.get("tool_modules", []):
    try:
        import_module(mod_path)
        logger.debug("Imported extra tool module %s", mod_path)
    except Exception as exc:                                       # noqa: BLE001
        logger.warning("Could not import %s: %s", mod_path, exc)

# ... existing code ...

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py \"<prompt>\"")
        sys.exit(1)

    prompt: str = sys.argv[1]
    logger.info("Prompt received: %s", prompt)

    context = query_project_context()
    steps = plan_steps(prompt, context)

    if not steps:
        logger.warning("Planner produced no steps – exiting.")
        sys.exit(0)

    logger.info("Planned %d step(s):\n%s", len(steps), "\n".join(f" • {s['tool']}" for s in steps))

    results = execute_steps(steps)
    failures = [r for r in results if r["error"] is not None]

    logger.info("Orchestration complete: %d success, %d failed", len(results) - len(failures), len(failures))

    # Non‑zero exit code if anything failed so CI can flag the run.
    # ---------------------------------------------------------------------------
    # At the very end of main(): write a JSON summary  ★ NEW ★
    # ---------------------------------------------------------------------------
    import json, pathlib
    summary_dir = pathlib.Path(__file__).parent / RESULTS_DIR
    summary_dir.mkdir(parents=True, exist_ok=True)
    outfile = summary_dir / f"run_{int(time.time())}.json"
    with outfile.open("w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    logger.info("Wrote run summary → %s", outfile)

    # Optional: Run guideline ingest pipeline
    try:
        from tools.orchestrator_hooks import ingest_guidelines
        ingest_guidelines()
    except ImportError:
        pass

    sys.exit(2 if failures else 0)

# ... existing code ... 