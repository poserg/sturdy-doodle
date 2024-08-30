import requests
import json
import logging
from portfolio.clients.smart_lab import Bond

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)


class DohodClient:
    '''
    Example:
    curl -X 'POST' \
        'https://www.dohod.ru/assets/components/dohodbonds/connectorweb.php?action=info' \
         -d "customFilters%5Bsearch_string%5D=RU000A103HT3"
    ''' # noqa

    def __init__(self):
        self.url = 'https://www.dohod.ru/assets/components/dohodbonds/connectorweb.php?action=getbondinfo' # noqa

    def get_last_quote(self, isin):
        quote = self._get(isin)
        return Bond(
            isin,
            quote['mdShortName'],
            quote['price'],
            quote['addInfo']["nkd"])

    def _get(self, isin):
        logger.debug(f'ISIN: {isin}')
        r = requests.get(
            self.url,
            params={'isin': isin})
        logger.debug(f'response = {r.text}')
        return json.loads(r.text)
