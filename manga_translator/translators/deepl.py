import deepl

from .common import CommonTranslator, MissingAPIKeyException
from .keys import DEEPL_AUTH_KEY

class DeeplTranslator(CommonTranslator):
    _LANGUAGE_CODE_MAP = {
        'CHS': 'ZH-HANS',
        'CHT': 'ZH-HANT',
        'JPN': 'JA',
        'ENG': 'EN-US',
        'CSY': 'CS',
        'NLD': 'NL',
        'FRA': 'FR',
        'DEU': 'DE',
        'HUN': 'HU',
        'ITA': 'IT',
        'POL': 'PL',
        'PTB': 'PT-BR',
        'ROM': 'RO',
        'RUS': 'RU',
        'ESP': 'ES',
        'IND': 'ID',
        'ARA': 'AR',
        'BGR': 'BG',
        'BUL': 'BG',
        'DAN': 'DA',
        'ELL': 'EL',
        'EST': 'ET',
        'FIN': 'FI',
        'KOR': 'KO',
        'LTH': 'LT',
        'LIT': 'LT',
        'LAV': 'LV',
        'NOB': 'NB',
        'SVK': 'SK',
        'SLO': 'SK',
        'SLV': 'SL',
        'SWE': 'SV',
        'TRK': 'TR',
        'TUR': 'TR',
        'UKR': 'UK'
    }

    def __init__(self):
        super().__init__()
        if not DEEPL_AUTH_KEY:
            raise MissingAPIKeyException('Please set the DEEPL_AUTH_KEY environment variable before using the deepl translator.')
        self.translator = deepl.Translator(DEEPL_AUTH_KEY)

    async def _translate(self, from_lang, to_lang, queries):
        return self.translator.translate_text('\n'.join(queries), target_lang = to_lang).text.split('\n')
