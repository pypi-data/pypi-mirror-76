# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional

# Local
from .utils import get_text

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ----------------------------------------------------------- class: WikiImage ----------------------------------------------------------- #

class WikiImage:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        url: str,
        caption: Optional[str]
    ):
        self.url = url
        self.caption = caption


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def from_element(
        cls,
        element
    ) -> Optional:
        try:
            img = element.find('img')

            try:
                src = img['srcset'].split(', ')[-1].strip('/').split(' ')[0].strip(' ')
            except:
                try:
                    src = img['src'].strip('/')
                except:
                    return None

            return cls(src, get_text(element.find('div', class_='thumbcaption')))
        except:
            return None


# ---------------------------------------------------------------------------------------------------------------------------------------- #