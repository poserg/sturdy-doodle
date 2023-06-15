import requests
import json
import logging
from portfolio.clients.smart_lab import Bond

logger = logging.getLogger(__name__)


class DohodClient:
    '''
    Example:
    curl -X 'POST' \
        'https://www.dohod.ru/assets/components/dohodbonds/connectorweb.php?action=info' \
         -d "customFilters%5Bsearch_string%5D=RU000A103HT3"
    ''' # noqa

    def __init__(self):
        self.url = 'https://www.dohod.ru/assets/components/dohodbonds/connectorweb.php?action=info' # noqa

    def get_last_quote(self, isin):
        quote = self._get(isin)[0]
        return Bond(
            quote['name'],
            quote['last'],
            quote['accruedint'])

    def _get(self, isin):
        r = requests.post(
            self.url,
            data={'customFilters[search_string]': isin})
        logger.debug(f'response = {r.text}')
        return json.loads(r.text)
