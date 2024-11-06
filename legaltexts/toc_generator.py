import re
from bs4 import BeautifulSoup


def add_links_to_toc(html, text, target="#toc"):
    """
    >>> add_links_to_toc('<h2>Titol</h2>', text='Torna a dalt')
    '<h2>Titol<a href="#toc">Torna a dalt</a></h2>'

    >>> add_links_to_toc('<h3>Titol</h3>', text='Torna a dalt')
    '<h3>Titol<a href="#toc">Torna a dalt</a></h3>'

    >>> add_links_to_toc('<h3>Titol</h3>', text='Go up')
    '<h3>Titol<a href="#toc">Go up</a></h3>'

    >>> add_links_to_toc('<h3>Titol</h3>', text='Torna a dalt', target="#target")
    '<h3>Titol<a href="#target">Torna a dalt</a></h3>'
    """
    soup = BeautifulSoup(html, features="html.parser")
    headers = sum((
        soup.find_all(f'h{l}')
        for l in range(2,7)
    ), [])
    for header in headers:
        uplink = BeautifulSoup("<span class='pujar'> - <a href='#toc' /></span>", features="html.parser")
        uplink.find('a').string = text
        header.append(uplink)
    return str(soup)

def generate_toc(markdown_text, top_level=None, bottom_level=None):
    """
    >>> md = (
    ...     "Ignored\\n"
    ...     "# 1. level 1\\n"
    ...     "## 1.1. level 2\\n"
    ...     "### 1.1.1. level 3\\n"
    ...     )

    >>> generate_toc(md)
    '- [1. level 1](#level-1)\\n  - [1.1. level 2](#level-2)\\n    - [1.1.1. level 3](#level-3)'

    >>> generate_toc(md, top_level=2)
    '- [1.1. level 2](#level-2)\\n  - [1.1.1. level 3](#level-3)'

    >>> generate_toc(md, bottom_level=2)
    '- [1. level 1](#level-1)\\n  - [1.1. level 2](#level-2)'

    """
    top_level = top_level or 1
    toc = []
    for linia in markdown_text.splitlines():
        header = re.match(r"^(#{1,6})\s+((?:\d+[.])+)\s+(.*)", linia)
        if not header: continue
        level = len(header.group(1))  # Determina el nivell de la capçalera
        if top_level and level<top_level: continue
        if bottom_level and level>bottom_level: continue
        numbers = header.group(2)
        title = header.group(3).strip()

        # Crea el link del titol
        link = title.lower().replace(" ", "-").replace(".", "").replace(",", "")
        toc.append(f"{'  ' * (level - top_level)}- [{numbers} {title}](#{link})")
    return "\n".join(toc)

def main():
    # Lee el archivo Markdown
    with open("es_tmp.md", "r", encoding="utf-8") as file:
        content = file.read()

    # Genera la tabla de content
    toc = generate_toc(content)

    # Inserta la tabla de content al inicio del archivo
    content_toc = f"# TABLA DE CONTENIDOS\n\n{toc}\n\n"
    mod_content = content.replace("[TABLE]", content_toc)

    # Guarda el nuevo archivo con la TOC agregada
    with open("es.md", "w", encoding="utf-8") as file:
        file.write(mod_content)

if __name__ == "__main__":
    main()