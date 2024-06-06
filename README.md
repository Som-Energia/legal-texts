# Som Energia legal texts

This is still an experiment to have all the legal text centralized in a single repository.

Goals:

- Propagate changes from the legal team faster to the many uses of the texts.
- Have a clean format that can be easily diffable
- Being able to translate them in weblate
- Being able to export different required formats: html, pdf...

## Converting docx files into markdown

- Converting docx for all languages is expected to be done only the first time for each document.
- For next reviews of the document, we expect to import docx just the reference language and let the translators to work with weblate to update just the changed texts
- Use `import_docx.sh` passing all the docx files to import
- The script expects ES GL EU CA (uppercase) to be part of the name to deduce the language
- Sometimes GL is annotated GA, must be corrected in the input file
- This step generates a clean output just with basic formatting
- Even though it might clear too much
- Some formatting must be reviewed


## Review md files, first import

- Compare md for each language 


## Extracting 

