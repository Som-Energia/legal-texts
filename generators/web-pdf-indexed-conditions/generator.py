#!/usr/bin/env python

import typer

app = typer.Typer()

@app.command()
def generate(translation_yaml: Path):
    """Generates a set of deployable files"""
    # TODO: this should be generalized to generate each one of the documents
    import subprocess
    subprocess.run([
        'pandoc',
        str(translation_yaml),
        '--css', 'pagedlegaltext.css',
        '-t', 'html',
        '-o', 'lala.pdf',
        '--metadata', 'pagetitle="CHANGE ME"',
        '--variable', 'margin-left=25.4mm',
        '--variable', 'margin-top=25.4mm',
        '--variable', 'margin-right=25.4mm',
        '--variable', 'margin-bottom=25.4mm',
        '--variable', 'header-text="hola',
        '--pdf-engine=weasyprint',
        #'--pdf-engine-opt=--pdf-variant=pdf/ua-1',
    ])


if __name__ == "__main__":
    app()

