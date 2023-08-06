# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import List, Dict, Union

# Pip
from kcu import request

# Local
from .category import Category


# ---------------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------- class: AmazonTrends ---------------------------------------------------------- #

class AmazonTrends:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def get_trends(
        cls,
        category: Category = Category.ALL_DEPARTMENTS,
        locale: str = 'en_US',
        max_results_per_letter: int = 10,
        search_letters: str = 'abcdefghijklmnopqrstuvwxyz',
        random_ua: bool = True,
        return_dict: bool = False,
        debug: bool = False
    ) -> Union[List[str], Dict[str, List[str]]]:
        suggestions = {}

        for char in search_letters:
            suggestions[str(char)] = cls.__get_suggestions(
                category,
                str(char),
                locale,
                max_results_per_letter,
                random_ua,
                debug
            )

        if return_dict:
            return suggestions
        else:
            suggestions_ = []

            for v in suggestions.values():
                suggestions_.extend(v)

            return suggestions_

    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    @classmethod
    def __get_suggestions(
        cls,
        category: Category,
        letter: str,
        locale: str,
        max_results: int,
        random_ua: bool,
        debug: bool
    ) -> List[str]:
        import time
        from kcu import request

        url = 'https://completion.amazon.com/api/2017/suggestions?lop={}&site-variant=desktop&client-info=amazon-search-ui&mid=ATVPDKIKX0DER&alias={}&ks=65&prefix={}&event=onKeyPress&limit=11&fb=1&suggestion-type=KEYWORD&_={}'.format(locale, category.value, letter, int(time.time()))
        suggestions = []

        try:
            j = request.get(url, max_request_try_count=2, sleep_time=0.25, fake_useragent=random_ua, debug=debug).json()

            for suggestion in j['suggestions']:
                suggestion = suggestion['value']

                if suggestion not in suggestions:
                    suggestions.append(suggestion)

                    if len(suggestions) >= max_results:
                        return suggestions

            return suggestions
        except:
            return suggestions


# ---------------------------------------------------------------------------------------------------------------------------------------- #