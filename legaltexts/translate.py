import yaml
from pathlib import Path

def build_translations():
    if hasattr(build_translations, "translations"):
        return build_translations.translations
    translations = {}
    pathlist = Path('legaltexts').glob('**/*.yaml')
    print(pathlist)
    for translation_file_name in pathlist:
        if translation_file_name.suffix != '.yaml': continue
        lang = translation_file_name.stem
        translations[lang] = yaml.safe_load(open(translation_file_name, 'r'))
    build_translations.translations = translations
    return build_translations.translations

def tr(lang, text, *args, **kwds):
    translations = build_translations()
    return translations[lang][text].format(*args, **kwds)

