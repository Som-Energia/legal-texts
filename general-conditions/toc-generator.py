import re

def generate_toc(markdown_text):
    toc = []
    for linia in markdown_text.splitlines():
        header = re.match(r"^(#{1,6})\s+(.*)", linia)
        if header:
            level = len(header.group(1))  # Determina el nivell de la capçalera
            title = header.group(2).strip()
            # Crea el link del titol
            link = title.lower().replace(" ", "-").replace(".", "").replace(",", "")
            toc.append(f"{'  ' * (level - 1)}- [{title}](#{link})")
    return "\n".join(toc)

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