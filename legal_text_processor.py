#!/usr/bin/env python

import typer
from yamlns import ns
from pathlib import Path
import re
import typer

help="""\
Extracts a monolingual translation yaml from a markdown of a legal text,
using clause numbers as base for the string ID's.
"""

def extract_id(block):
    if not block: return
    chapter_match = re.match(r"#+\s+([0-9][0-9.]+)\s", block[0])
    if chapter_match:
        return f"CHAPTER_{chapter_match.group(1).replace('.','_')}MARKDOWN"

    clause_match = re.match(r"([0-9][0-9.]+)\s", block[0])
    if clause_match:
        return f"CLAUSE_{clause_match.group(1).replace('.','_')}MARKDOWN"

def join_blocks(blocks):
    return '\n'.join((
        ''.join(phases)
        for phases in blocks
    ))


app = typer.Typer(
    help=help,
)

@app.command()
def extract(markdown_file: Path):
    print(f"extracting {markdown_file}")
    blocks = [[]]
    for line in markdown_file.open():
        print(f"> {line}")
        if not line.strip() :
            blocks.append([])
            continue
        blocks[-1].append(line)

    yaml = ns()
    active_id = "PRE"
    for block in blocks:
        active_id = extract_id(block) or active_id
        yaml.setdefault(active_id, [])
        yaml[active_id].append(block)


    result = ns((
        (id, join_blocks(content))
        for id, content in yaml.items()
    ))

    result.dump(markdown_file.with_suffix(".yaml"))


if __name__ == "__main__":
    app()






