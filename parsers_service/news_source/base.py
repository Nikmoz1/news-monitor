import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from fake_useragent import UserAgent


def requests_retry_session(retries: int = 7,
                           backoff_factor: float = 0.2,
                           status_forcelist: tuple = (400, 500, 502, 503, 504),
                           session: requests.Session = None) -> requests.Session:
    """  Метод додає функціональність для повторних спроб під час процесу скрапингу.
         Використовується як альтернатива request.get. Також перевизначені заголовки дозволяють
         імітувати поведінку браузера, що дозволяє надійніше виконувати потрібну роботу.
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    session.headers.update({
        "User-Agent": UserAgent().random,
        "Accept": "text/html,*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,mt;q=0.6,uk;q=0.5",
        "Content-Type": "application/json; charset=utf-8",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest",
    })
    return session


class BaseParser:
    base_url: str = None

    def __init__(self, session: requests.Session = None):
        self.session = requests_retry_session(session=session)

