# Som Energia legal texts

[![CI Status](https://github.com/som-energia/legal-texts/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/Som-Energia/legal-texts/actions)

This repository contains the legal texts
to be used in our applications and the scripts
to generate any production format based on them.

Generated output: <https://som-energia.github.io/legal-texts/>


## Goals

- Propagate changes from the legal team faster to the many uses of the texts
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

**Note:** if your distro ships with pandoc<1.3.1,
try install deb package from [here](https://github.com/jgm/pandoc/releases/latest)


## Glossary

### Actors

- Legal team: Produces and maintains legal texts
- Translation team: Translates legal text to different languages
- Communication team: Decide how and where to present the documents to the users
- Integrators: IT crew that adapts and inject masters into the system
- Deployers: IT and Communication crew that use the documents in their platforms

### Artifacts

Master document
: A document produced and maintained by the legal team, usually in a single language, and better if it has few formatting or artifacts.
: In SomEnergia, master documents are doc files stored in a given GoogleDrive folder.

Deployed document
: An specific file derived from one or many master files, adapted by format, language, styling or utilities for the users to access it in an specific platform
: Example: The html page in the website, the html fragment to be embeded inside a web form, the pdf sent by email, the pdf to be signed by signaturit...

### Constituents of a document

Content
: The essential content stripped from any layout, style or utility.

Style
: Design options we can apply to document elements (color, font family, font size, decorations...)

Layout
: Distribution of the document elements in the available space.
: Although it is often included as part of the style, here we explicitly discriminate layout and style.

Utilities
: Functional elements of the document which are not parte of the content itself but help the user to read it
: Example: Table of content, back links, search widgets, buttons...

Format
: Type of digital support
: Example: HTML page, PDF document...
: Here we avoid using format o formatting to refer to layout or style.

Platform
: Technological system which makes a document available to the user
: Examples: Front website, back office, webforms, ERP...

### Systems

Version Control System
: A system that maintains, documents and integrates changes different people make to a set of files, usually plain text files.
: We are currently using `git` as VCS within the web platform `github`.

Markdown
: A richtext format wich reensembles plaintext, specialized to represent content, as opposed to layout or style, which can be converted to multiple formats (html, docx, pdf...)

Translation file
: A file containing text translations in a single language.
: Every text piece has a unique identifier to relate the same text piece in different languages.
: We are using YAML format for translation files and descriptive `UPPER_SNAKE_CASE` for identifiers.

Weblate
: Webapp to translate texts in git projects.
: Currently used in SomEnergia to translate any text of any application to the 4 official languages or more

## Pipeline

### Import docx files as markdown

**Master and translations:**
The normal workflow considers the version of a document in a single original language to be the master to be imported.
The rest of languages should be translated using Weblate.
Still having docx files for several languages to be imported has sense in the following cases:

- The first import, if translated docx files already exist
- The expected time lapse when the legal team is not adopting single master workflow yet.

Procedure:

- Obtain the master docx files
- Ensure the docx files have language markers in its name (CA, ES, EU or GL/GA, in uppercase)
- Create a folder in this project for the document, say: `my-document/`.
- Enter the folder and execute `import_docx.sh` passing the docx to be imported as parameters
- This will generate `my-document/<lang>.md`

About the output:

- This step generates a clean markdown output just with basic formatting
    - Even though it might clear too much
    - Some formatting must be reviewed
- Paragraphs are splitted by sentence.
    - This is convenient since this improves the diff effectivity but be aware of possible artifacts.
    - Some languages split or merge the sentences in a different way.

### Review md files after import

- Compare imported md files to identify real changes and formatting or import errors
    - Against previous version in git
    - Against same document in other languages
- TODO: List of usual import errors

### Extracting translation yaml files

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

### Extracting template for resynthesizing md's

The template is a file specifying how to compose translated texts to rebuild a translated markdown document.

```bash
# first time, all languages
legal-text-processor template mydocument/??.md
# successive, just the reference one
legal-text-processor template mydocument/es.md
```
- This generates `mydocument/template.md`.
- It will trigger colored messages if a previous `template.md` exists and any clause structure change is detected.
- This is useful when importing several languages, to spot structure differences among them.

### Resynthesizing md from translations

Once translators have translated the new sentences in weblate,
the following command:

```bash
legal-text-processor reintegrate my_output
```

It will regenerate markdowns back from the specified translations using the template.

### Generate output documents

TODO: This step is still under heavy development,
this documentation does not reflect reality
and reality will surely change.

```bash
legal-text-processor generate ....
```




