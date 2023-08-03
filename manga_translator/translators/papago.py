
# -*- coding: utf-8 -*-
from functools import cached_property
import uuid
import hmac, base64
import aiohttp
import time
import requests
import re

from .common import CommonTranslator, InvalidServerResponse

class PapagoTranslator(CommonTranslator):
    _LANGUAGE_CODE_MAP = {
        'CHS': 'zh-CN',
        'CHT': 'zh-TW',
        'JPN': 'ja',
        'ENG': 'en',
        'KOR': 'ko',
        'VIN': 'vi',
        'FRA': 'fr',
        'DEU': 'de',
        'ITA': 'it',
        'PTB': 'pt',
        'RUS': 'ru',
        'ESP': 'es',
    }
    _API_URL = 'https://papago.naver.com/apis/n2mt/translate'

    async def _translate(self, from_lang, to_lang, queries):
        data = {
            'honorific': "false",
            'source': from_lang,
            'target': to_lang,
            'text': '\n'.join(queries),
        }
        result = await self._do_request(data, self._version_key)
        if "translatedText" not in result:
            raise InvalidServerResponse(f'Papago returned invalid response: {result}\nAre the API keys set correctly?')
        return [str.strip() for str in result["translatedText"].split("\n")]

    @cached_property
    def _version_key(self):
        script = requests.get('https://papago.naver.com')
        mainJs = re.search(r'\/(main.*\.js)', script.text)[1]
        papagoVerData = requests.get(f'https://papago.naver.com/{mainJs}')
        return re.search(r'"PPG .*,"(v[^"]*)', papagoVerData.text)[1]

    async def _do_request(self, data, version_key):
        guid = uuid.uuid4()
        timestamp = int(time.time() * 1000)
        key = version_key.encode("utf-8")
        code = f"{guid}\n{self._API_URL}\n{timestamp}".encode("utf-8")
        token = base64.b64encode(hmac.new(key, code, "MD5").digest()).decode("utf-8")
        headers = {
            "Authorization": f"PPG {guid}:{token}",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Timestamp": str(timestamp),
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self._API_URL, data=data, headers=headers) as resp:
                return await resp.json()
