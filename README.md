# Som Energia legal texts

This is still an experiment to have all the legal text centralized in a single repository.

Goals:

- Propagate changes from the legal team faster to the many uses of the texts.
- Have a clean format that can be easily diffable
- Being able to translate them in weblate
- Being able to export different required formats: html, pdf...

## Installation

```bash
sudo apt install pandoc weasyprint
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Converting docx files into markdown

- Converting docx for all languages is expected to be done only the first time for each document.
- For next reviews of the document, we expect to import docx just the reference language and let the translators to work with weblate to update just the changed texts
- Use `import_docx.sh` passing all the docx files to import
- The script expects ES GL EU CA (uppercase) to be part of the name to deduce the language
- Sometimes GL is annotated as GA, the script fixes that
- This step generates a clean output just with basic formatting
- Even though it might clear too much
- Some formatting must be reviewed
- Paragraphs are splitted by sentence.
  This is convenient since improves the diff effectivity but this might introduce artifacts.
  Besides some languages split or merge the sentences.

## Review md files, first import

- Compare md for each language 

## Extracting translation yamls

```bash
# first time, all languages
legal-text-processor extract mydocument/??.md
# successive, just the reference one
legal-text-processor extract mydocument/es.md
```

- Generates `mydocument/??.yaml` containing the translation
- This is done by identifying numbered titles and clauses
- Translation ID's are based on the title/clause numbering, not the content
- Some sentences start with something similar to a clause number generating an extra ID. This has to be corrected by hand.
- TODO: let the script check the numbering sequence and report inconsistencies

## Extracting template for resynthesizing md's

```bash
# first time, all languages
legal-text-processor template mydocument/??.md
# successive, just the reference one
legal-text-processor template mydocument/es.md
```
- This generates `mydocument/template.md`.
- If there is a previous `template.md` it will highlight differences.
- This is useful when providing all languages at once, to detect any missfit language.
- This is useful to acknoledge changes in the source.

## Resynthesizing md from translations

Once translators have translated the new sentences in weblate,
the following command:

```bash
legal-text-processor reintegrate my_output
```

will regenerate markdowns back from the specified translations.

## Output documents

TODO: This step is still under heavy development,
this documentation does not reflect reality
and reality will surely change.

legal-text-processor generate ....


