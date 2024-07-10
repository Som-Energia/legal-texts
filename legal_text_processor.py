#!/usr/bin/env python

import typer
from yamlns import ns
from pathlib import Path
import re
import typer
import itertools
from consolemsg import warn, step, error
import difflib

help="""\
This CLI tool automates legaltext workflow
from the master version in a single language,
through translations and to generate deployable
versions in proper format.

master.docx -> import -> mydocument/es.md

mydocument/es.md -> extract -> mydocument/es.yaml

mydocument/es.md -> template -> mydocument/template.md

mydocument/es.yaml -> weblate  ->  mydocument/XX.yaml

mydocument/XX.yaml -> reintegrate  ->  mydocument/XX.md

mydocument/XX.yaml -> generate -> output/mydocument.XX.pdf/html/...

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

def extract_block_ids(blocks: list[list[str]]):
    block_ids = ['PRE']
    for block in blocks:
        new_id = extract_id(block)
        if not new_id: continue
        active_id = unrepeated_id(block_ids, new_id)
        block_ids.append(active_id)
    return block_ids

def diff(template_file: Path, content: list[str]):
    oldcontent = []
    if template_file.exists():
        with template_file.open() as f:
            oldcontent = f.readlines()
    difflines = difflib.unified_diff(
        oldcontent,
        content,
        fromfile=str(template_file),
        tofile='new',
    )
    return ''.join(difflines)

app = typer.Typer(
    help=help,
)

@app.command()
def extract(markdown_file: list[Path]):
    """
    Extracts a monolingual translation yaml from each markdown of a legal text.

    Clause numbers are used as base for the string ID's.
    """
    for md_file in markdown_file:
        print(f"Extracting {md_file}")
        ensure_extension(md_file, '.md')
        blocks = analyze_blocks(md_file.open())
        result = extract_translations(blocks)
        result.dump(md_file.with_suffix(".yaml"))

@app.command()
def template(markdown_file: list[Path]):
    """
    Extracts a template used to reintegrate back the translation files into markdown
    """
    for md_file in markdown_file:
        step(f"Extracting template from {md_file}")
        ensure_extension(md_file, '.md')
        template_file = md_file.parent / 'template.md'

        blocks = analyze_blocks(md_file.open())
        block_ids = extract_block_ids(blocks)
        content = [
            f"{{{id}}}\n" for id in block_ids
        ]
        content_diff = diff(template_file, content)
        if content_diff: warn(content_diff)
        step(f"Writing {template_file}...")
        template_file.write_text(''.join(content))

@app.command()
def reintegrate(translation_yaml: list[Path]):
    """Reconstructs markdown files from translation yamls."""
    for yaml_file in translation_yaml:
        ensure_extension(yaml_file, '.yaml')
        markdown_file = yaml_file.with_suffix('.md')
        template_file = yaml_file.parent/'template.md'
        step(f"Generating {markdown_file} from {yaml_file} and {template_file}")
        translation = ns.load(yaml_file)
        template = (yaml_file.parent/'template.md').read_text()
        content = template.format(**translation)
        markdown_file.write_text(content)

if __name__ == "__main__":
    app()






