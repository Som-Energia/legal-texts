from yamlns import ns
from pathlib import Path

def build_translations():
    if hasattr(build_translations, "translations"):
        return build_translations.translations
    translations = ns()
    for translation_file in (Path(__file__).parent/'i18n').glob('*.yaml'):
        lang = translation_file.stem
        translations[lang] = ns.load(translation_file)
    build_translations.translations = translations
    return build_translations.translations

def tr(lang, text, *args, **kwds):
    translations = build_translations()
    return translations[lang][text].format(*args, **kwds)

