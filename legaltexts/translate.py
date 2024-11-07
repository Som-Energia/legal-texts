from yamlns import ns
from pathlib import Path
from importlib.resources import files as package_files

def build_translations():
    if hasattr(build_translations, "translations"):
        return build_translations.translations
    translations = ns()
    for translation_file in package_files('legaltexts.i18n').iterdir():
        if translation_file.suffix != '.yaml': continue
        lang = translation_file.stem
        translations[lang] = ns.loads(translation_file.read_text())
    build_translations.translations = translations
    return build_translations.translations

def tr(lang, text, *args, **kwds):
    translations = build_translations()
    return translations[lang][text].format(*args, **kwds)

