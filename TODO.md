## Deute tècnic

- [ ] El TOC del document del webforms no te titol (Taula de continguts)
- [ ] Target del TOC ha de ser també multi idioma (o insertem el target de toc a mà)
- [ ] Las listas del general conditions estan rotas la mayoria
- [ ] Provar el generat a webforms
- [ ] Links in a different window
- [ ] import general-conditions in different languages
- [ ] Create a weblate project for general-conditions
- [ ] Combined webform output for general-conditions and indexed


- [ ] Moure les operacions de gha a un makefile
- [ ] Integrar l'script d'importació (bash) a l'script python principal
- [ ] Generalitzar la reintegració (processar tots els masters que tenen un template.md)
- [ ] Generalitzar la generació per declarativament definir:
    - Nom de la sortida
    - Quins inputs pren
    - Quin conversor fa servir
    - Paràmetres
- [ ] En la extracció comprovar que la numeració és consecutiva

- [x] TOC strings (title and link text) as translatable
- [x] Reorganitzar per generate generic
- [x] Posar els assets a un subdirectori
- [x] Fer servir l'acció de notificacio al chat quan falla

## Pending unknowns

- [x] Com recomposar el document a partir de les cadenes traduides
- [x] Given a markdown how to properly format into pdf
- [ ] Given a markdown how to properly format into html selfcontained
- [ ] Given a markdown how to properly format into html embeded
- [ ] HTML: How to make links to open in a different windows in html
- [x] HTML: How to generate the TOC
- [x] HTML: Backlinks
- [x] PDF: CSS Styling
- [x] PDF: how to generate TOC metadata
- [x] PDF: Page header
- [x] PDF: Page footers refering pages and document title
- [x] Warn if document changes the existing template
- [ ] If no master provided, locate all documents to reintegrate by looking at template.md
- [ ] Declarative output definition

## Hand made changes to the generated md

- Titol principal només està a català
- Números de les primeres clauses en catala 1.1 a 2.3 estaven en negreta
- Treure negretes als titols de nivell 4
- Afegir lletres a) b) i c) als titols de nivell 4
- Negreta del titol 6 que trencava linia en ca
- eu negreta en titols 1. i 2.
- es i gl tenen comes i punts en negreta
- els subindexos es marquen amb `\_(contingut)` i ha de ser `~contingut~` o en LaTeX




