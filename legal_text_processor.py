#!/usr/bin/env python

import typer
from yamlns import ns
from pathlib import Path
import re
import typer
import itertools
from consolemsg import warn, step, error

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

def analyze_blocks(f):
    blocks = [[]]
    for line in f:
        if not line.strip() :
            blocks.append([])
            continue
        blocks[-1].append(line)
    return blocks

def extract_translations(blocks):
    yaml = ns()
    active_id = "PRE"
    for block in blocks:
        new_id = extract_id(block)
        if new_id:
            step(new_id)
            active_id = unrepeated_id(yaml, new_id)
        yaml.setdefault(active_id, [])
        yaml[active_id].append(block)

    return ns((
        (id, join_blocks(content))
        for id, content in yaml.items()
    ))


def ensure_extension(path: Path, extension: str):
    if path.suffix == extension: return
    raise Exception(f"Expected {extension} extension")

app = typer.Typer(
    help=help,
)

@app.command()
def extract(markdown_file: Path):
    print(f"extracting {markdown_file}")
    ensure_extension(markdown_file, '.md')
    blocks = analyze_blocks(markdown_file.open())
    result = extract_translations(blocks)
    result.dump(markdown_file.with_suffix(".yaml"))

@app.command()
def template(markdown_file: Path):
    print(f"extracting {markdown_file}")
    ensure_extension(markdown_file, '.md')
    blocks = analyze_blocks(markdown_file.open())

    block_ids = ['PRE']
    for block in blocks:
        new_id = extract_id(block)
        if not new_id: continue
        step(new_id)
        active_id = unrepeated_id(block_ids, new_id)
        block_ids.append(active_id)

    template_file = markdown_file.parent / 'template.md'
    step(f"Writing {template_file}...")
    template_file.write_text('\n'.join((
        f"{{{id}}}" for id in block_ids
    )))

@app.command()
def generate(translation_yaml: Path):
    ensure_extension(translation_yaml, '.yaml')
    translation_yaml.with_suffix('.md').write_text(content)
    print(f"Generating {}")
    translation = ns.load(translation_yaml)
    template = (translation_yaml.parent/'template.md').read_text()
    content = template.format(**translation)
    translation_yaml.with_suffix('.md').write_text(content)

if __name__ == "__main__":
    app()






