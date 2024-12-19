import yaml
from pathlib import Path
from importlib.resources import files as package_files

def build_translations():
    if hasattr(build_translations, "translations"):
        return build_translations.translations
    translations = {}
    for translation_file_name in package_files('legaltexts.i18n').iterdir():
        if translation_file_name.suffix != '.yaml': continue
        lang = translation_file_name.stem
        translations[lang] = yaml.safe_load(open(translation_file_name, 'r'))
    build_translations.translations = translations
    return build_translations.translations

def tr(lang, text, *args, **kwds):
    translations = build_translations()
    return translations[lang][text].format(*args, **kwds)

