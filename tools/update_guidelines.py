import json, re
from pathlib import Path
from markdown_it import MarkdownIt

RULES_FILE = Path('cache/rules.json')
GUIDELINES_FILE = Path('AI_GUIDELINES.md')
CATEGORY_MAP = {
    'Blueprint': 'Blueprint Craftsmanship',
    'Geometry': 'Geometry & Modeling Tools',
    'Materials': 'Materials & Textures',
    'Performance': 'Performance & Tick Budget',
    'Testing': 'Testing & Validation',
    'SourceControl': 'Source-Control & Review',
}

with open(RULES_FILE, 'r', encoding='utf-8') as f:
    rules = [r for r in json.load(f) if r]

with open(GUIDELINES_FILE, 'r', encoding='utf-8') as f:
    md = f.read()

md_lines = md.splitlines()
md_new = []
inserted = set()

for i, line in enumerate(md_lines):
    md_new.append(line)
    for cat, heading in CATEGORY_MAP.items():
        if re.match(rf'^#+\s*{re.escape(heading)}', line):
            # Insert rules for this category after heading
            for rule in rules:
                if rule.startswith(cat) and rule not in md:
                    md_new.append(f"- {rule}  *(EDC auto)*")
                    inserted.add(rule)

with open(GUIDELINES_FILE.with_suffix('.md.tmp'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_new) + '\n')
Path(GUIDELINES_FILE.with_suffix('.md.tmp')).replace(GUIDELINES_FILE) 