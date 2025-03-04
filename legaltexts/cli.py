#!/usr/bin/env python

import typer
import yaml
from collections import OrderedDict
from pathlib import Path
import re
import itertools
from consolemsg import warn, step, error
import difflib
try:
    import translate
    import toc_generator
except ImportError:
    from . import translate
    from . import toc_generator

from typing_extensions import Annotated

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

mydocument/XX.md -> generate -> output/mydocument.XX.pdf/html/...

"""

def represent_dictionary_order(self, dict_data):
    return self.represent_mapping('tag:yaml.org,2002:map', dict_data.items())

def setup_yaml():
    yaml.add_representer(OrderedDict, represent_dictionary_order)

setup_yaml()

output_dir = Path(__file__).parent.parent/'output'
if output_dir.is_relative_to(Path.cwd()):
    output_dir = output_dir.relative_to(Path.cwd())

def extract_id(block):
    """
    Check if the block starts translatable string if so retunrs the id.
    It is detected as chapter when the block starts with a hashes and dotted number. 
    It is detected as clause when the block starts with dotted number.
    """
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
    """
    Given a base id, returns unique id by appending a sequence number.     
    """
    if base not in existing: return base
    warn(f"Dupped id {base}")
    for count in itertools.count(2):
        candidate = f"{base}__{count}"
        if candidate not in existing:
            return candidate
    error(f"Unable to find a suitable id alternative to {base}")

def analyze_blocks(f):
    """
    Returns an array of blocks (md paragraph),
    composed each by an array of lines. 
    """
    blocks = [[]]
    for line in f:
        if not line.strip() :
            blocks.append([])
            continue
        blocks[-1].append(line)
    return blocks

def extract_translations(blocks):
    """
    Organized list of blocks into translation dictionary
    """
    yaml = OrderedDict()
    active_id = "PRE"
    for block in blocks:
        new_id = extract_id(block)
        if new_id:
            step(new_id)
            active_id = unrepeated_id(yaml, new_id)
        yaml.setdefault(active_id, [])
        yaml[active_id].append(block)

    return OrderedDict((
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

def diff(old_file: Path, newcontent: list[str]):
    oldcontent = []
    if old_file.exists():
        with old_file.open() as f:
            oldcontent = f.readlines()
    difflines = difflib.unified_diff(
        oldcontent,
        newcontent,
        fromfile=str(old_file),
        tofile='new',
    )
    return ''.join(difflines)

def generate_pdf_file(markdown_file: Path, css_file: Path = "pagedlegaltext.css", output_pdf: Path = "output.pdf"):
    """
    Generates pdf from markdown file
    """
    # TODO: this should be generalized to generate each one of the documents
    import subprocess
    subprocess.run([
        'pandoc',
        str(markdown_file),
        '--css', css_file,
        '-t', 'html',
        '-o', output_pdf,
        '--metadata', 'pagetitle="CHANGE ME"',
        '--variable', 'margin-left=25.4mm',
        '--variable', 'margin-top=25.4mm',
        '--variable', 'margin-right=25.4mm',
        '--variable', 'margin-bottom=25.4mm',
        '--variable', 'header-text="hola',
        '--pdf-engine=weasyprint',
        #'--pdf-engine-opt=--pdf-variant=pdf/ua-1',
    ])

def md_to_html_fragment(markdown: str)->str:
    """
    Generates html fragmentf from markdown file
    """
    import subprocess
    from somutils.testutils import temp_path
    with temp_path() as tmp:
        markdown_file = tmp/f"input.md"
        output_html = tmp/'output.html'
        markdown_file.write_text(markdown)
        subprocess.run([
            'pandoc',
            str(markdown_file),
            '-t', 'html',
            '-o', output_html,
            '--wrap=preserve',
        ])
        return output_html.read_text()

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
        with open(md_file.with_suffix(".yaml"), 'w') as outputfile:
            yaml.dump(result, outputfile)

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
    for yaml_file_name in translation_yaml:
        ensure_extension(yaml_file_name, '.yaml')
        markdown_file = yaml_file_name.with_suffix('.md')
        template_file = yaml_file_name.parent/'template.md'
        step(f"Generating {markdown_file} from {yaml_file_name} and {template_file}")
        translation = yaml.safe_load(open(yaml_file_name, 'r'))
        template = (yaml_file_name.parent/'template.md').read_text()
        content = template.format(**translation)
        markdown_file.write_text(content)

@app.command()
def generate(
    input_dir: Annotated[str, typer.Argument(help="Input directory (name of weblate directory)")]='',
    output_prefix: Annotated[str, typer.Option(help='Optional prefix for output files')]='output',
    target_type: Annotated[str, typer.Option(help='html or pdf output')]='html',
    with_toc: Annotated[bool, typer.Option(help='With TOC')]=False
    ):
    if target_type=='pdf':
        generate_pdf(
            Path(input_dir),
            output_prefix
        )
    if target_type=='html':
        generate_html(
            Path(input_dir),
            output_prefix,
            with_toc
        )
    if not input_dir:
        print(f"Input directory should be especified")

def generate_pdf(master_path: Path, output_prefix: str):
    """Generates a pdf"""
    document = master_path.name
    output_dir.mkdir(exist_ok=True)
    for markdown_file in master_path.glob('??.md'):
        lang = markdown_file.stem
        output_template = f'{output_prefix}-{document}-{lang}.pdf'
        target = output_dir / output_template
        step(f"Generating {target}...")
        generate_pdf_file(markdown_file, 'pagedlegaltext.css', target)

def generate_html(master_path: Path, output_prefix: str, with_toc: bool = False):
    """Generates an html fragment"""
    document = master_path.name
    output_dir.mkdir(exist_ok=True)
    for markdown_file in master_path.glob('??.md'):
        lang = markdown_file.stem
        output_template = f'{output_prefix}-{document}-{lang}.html'
        target = output_dir / output_template
        step(f"Generating {target}")

        step(f"  Reading {markdown_file}...")
        markdown_content = markdown_file.read_text()

        if with_toc:
            step(f"  Generating TOC")
            markdown_with_toc = toc_generator.add_markdown_toc(
                markdown_content,
                place_holder='[TABLE]',
                title=translate.tr(lang, 'TOC_TITLE'),
                top_level=2,
            )
            step(f"  Generating html...")
            html = md_to_html_fragment(markdown_with_toc)
        else:
            step(f"  Generating html...")
            html = md_to_html_fragment(markdown_content)

        final_content = html
        if with_toc:
            step(f"  Adding up-links...")
            top=f"<span id={document}-top></span>\n\n"
            final_content = top+toc_generator.add_links_to_toc(
                html,
                text=f"{translate.tr(lang, 'TOC_GO_TO_TOC')} ↑",
                target=f"#{document}-top",
            )

        step(f"  Writing output")
        target.write_text(final_content)



if __name__ == "__main__":
    app()






