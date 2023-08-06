# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Union

# Pip
from kcu import request
from bs4 import BeautifulSoup as bs

# Local
from .models.wiki_text import WikiText
from .models.wiki_quote import WikiQuote
from .models.wiki_image import WikiImage

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: WikiArticle ---------------------------------------------------------- #

class WikiArticle:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        url: str,
        title: str,
        elements: List[Union[WikiText, WikiQuote, WikiImage]]
    ):
        self.url = url
        self.title = title
        self.elements = elements


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def get_article(
        cls,
        name: str,
        random_ua: bool = True,
        debug: bool = False
    ) -> Optional:
        try:
            url = 'https://en.wikipedia.org/wiki/{}'.format(name)

            soup = bs(
                request.get(
                    url, fake_useragent=random_ua, debug=debug
                ).content,
                'lxml'
            )

            title = soup.find('h1', {'id':'firstHeading'}).get_text()
            content = soup.find('div', {'id':'bodyContent'}).find('div', {'class':'mw-parser-output'})

            elements = []

            for child in content.find_all(['div', 'p', 'h1', 'h2', 'h3', 'blockquote'], recursive=False):
                span = child.find('span')

                if span and span.get('id') in ['Notes', 'References', 'External_links']:
                    break

                if child.name == 'div':
                    child = child.find('div', class_='thumbinner')

                    if child is None:
                        continue

                if child.name in ['p', 'h1', 'h2', 'h3']:
                    method = WikiText.from_element
                elif child.name == 'blockquote':
                    method = WikiQuote.from_element
                else:
                    method = WikiImage.from_element

                element = method(child)

                if element:
                    elements.append(element)

            return cls(url, title, elements)
        except:
            return None

# ---------------------------------------------------------------------------------------------------------------------------------------- #