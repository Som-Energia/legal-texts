#!/usr/bin/env python

import typer
from yamlns import ns
from pathlib import Path
import re
import typer
import itertools
from consolemsg import warn, step

help="""\
Extracts a monolingual translation yaml from a markdown of a legal text,
using clause numbers as base for the string ID's.
"""

def extract_id(block):
    if not block: return
    chapter_match = re.match(r"#+\s+([0-9][0-9.]+)\s", block[0])
    if chapter_match:
        chapter_number = chapter_match.group(1).replace('.','_').strip('_')
        return f"CHAPTER_{chapter_number}_MARKDOWN"

    clause_match = re.match(r"((\d[0-9.]+)\d\.?)\s", block[0])
    if clause_match:
        clause_number = clause_match.group(1).replace('.','_').strip('_')
        return f"CLAUSE_{clause_number}_MARKDOWN"

def join_blocks(blocks):
    return '\n'.join((
        ''.join(phases)
        for phases in blocks
    ))

def unrepeated_id(existing, base):
    if base not in existing: return base
    warn(f"Dupped id {base}")
    for count in itertools.count(2):
        candidate = f"{base}__{count}"
        if candidate not in existing:
            return candidate
    error(f"Unable to find a suitable id alternative to {base}")



app = typer.Typer(
    help=help,
)

@app.command()
def extract(markdown_file: Path):
    print(f"extracting {markdown_file}")
    blocks = [[]]
    for line in markdown_file.open():
        if not line.strip() :
            blocks.append([])
            continue
        blocks[-1].append(line)

    yaml = ns()
    active_id = "PRE"
    for block in blocks:
        new_id = extract_id(block)
        if new_id:
            step(new_id)
            active_id = unrepeated_id(yaml, new_id)
        yaml.setdefault(active_id, [])
        yaml[active_id].append(block)


    result = ns((
        (id, join_blocks(content))
        for id, content in yaml.items()
    ))

    result.dump(markdown_file.with_suffix(".yaml"))


if __name__ == "__main__":
    app()






