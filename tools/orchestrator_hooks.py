import subprocess, pathlib

def ingest_guidelines():
    root = pathlib.Path(__file__).parent.parent
    for cmd in [
        ["python","tools/crawl_epic_learning.py"],
        ["python","tools/extract_rules.py"],
        ["python","tools/update_guidelines.py"],
    ]:
        subprocess.run(cmd, cwd=root, check=True) 