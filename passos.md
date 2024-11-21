# Passos que seguim amb pandoc

Primer de tot hem de tenir l'última versió vigent, en aquest cas utilitzem la versió **3.5.1**.

Per extreure l'índex del fitxer hem executat el següent, utilitzant el fitxer import_docx.sh ($1 és el fitxer):
```
pandoc -s "$1" -o $lang.md  -t markdown
```
El que passa és que la resta de text no es parseja correctament. AL fer-ho així no podem extreure les clàusules, només hem pogut obtenir els capítols.


Per defecte el que s'utilitza per parsejar els fitxers és la comanda ($1 és el fitxer):
```
pandoc "$1" -o $lang.md --columns 80000 -t gfm-raw_html
```
Això ens ha parsejat bé el fitxer però no ens extreu l'índex correctament, només ens mostra un tag de TAULA.


