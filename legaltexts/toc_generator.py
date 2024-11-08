import re
from bs4 import BeautifulSoup

def add_links_to_toc(html, text, target="#toc"):
    """
    >>> add_links_to_toc('<h2>Titol</h2>', text='Torna a dalt')
    '<h2>Titol<span class="pujar"> - <a href="#toc">Torna a dalt</a></span></h2>'

    >>> add_links_to_toc('<h3>Titol</h3>', text='Torna a dalt')
    '<h3>Titol<span class="pujar"> - <a href="#toc">Torna a dalt</a></span></h3>'

    >>> add_links_to_toc('<h3>Titol</h3>', text='Go up')
    '<h3>Titol<span class="pujar"> - <a href="#toc">Go up</a></span></h3>'

    >>> add_links_to_toc('<h3>Titol</h3>', text='Torna a dalt', target="#target")
    '<h3>Titol<span class="pujar"> - <a href="#target">Torna a dalt</a></span></h3>'
    """
    soup = BeautifulSoup(html, features="html.parser", preserve_whitespace_tags={'p', 'li'})
    headers = sum((
        soup.find_all(f'h{l}')
        for l in range(2,7)
    ), [])
    for header in headers:
        uplink = BeautifulSoup(f"<span class='pujar'> - <a href='{target}' /></span>", features="html.parser")
        uplink.find('a').string = text
        header.append(uplink)
    return soup.prettify(formatter=None)

def generate_toc(markdown_text, top_level=None, bottom_level=None, title=None):
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

    >>> generate_toc(md, title="Index")
    '# Index\\n\\n- [1. level 1](#level-1)\\n  - [1.1. level 2](#level-2)\\n    - [1.1.1. level 3](#level-3)'

    """
    top_level = top_level or 1
    toc_title = f"# {title}\n\n" if title else ''
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
    return toc_title + "\n".join(toc)

def add_markdown_toc(
    original_md: str,
    title: str|None=None,
    place_holder:str = '',
    top_level: int = 0,
):
    """
    >>> md = (
    ...     "[TOC]\\n"
    ...     "# 1. level 1\\n"
    ...     )

    >>> add_markdown_toc(md)
    '- [1. level 1](#level-1)\\n\\n[TOC]\\n# 1. level 1\\n'
    >>> add_markdown_toc(md, place_holder='[TOC]')
    '- [1. level 1](#level-1)\\n# 1. level 1\\n'
    >>> add_markdown_toc(md, place_holder='[BAD]')
    '- [1. level 1](#level-1)\\n\\n[TOC]\\n# 1. level 1\\n'
    """
    toc = generate_toc(original_md, top_level = top_level, title=title)
    if place_holder and place_holder in original_md:
        return original_md.replace(place_holder, toc)
    return '\n\n'.join([toc, original_md])


if __name__ == "__main__":
    main()
