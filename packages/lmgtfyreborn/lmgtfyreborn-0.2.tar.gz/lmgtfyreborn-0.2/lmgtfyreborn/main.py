# Copyright Diego Magdaleno 2020
# License: MIT
from typing import List


class Lmgtfy:
    def __init__(self, search_terms: List) -> None:
        self.search_terms = search_terms

    def __term_format(self, terms: List) -> str:
        self.formatted_terms = '+'.join(word.replace(" ", "+")
                                        for word in terms)
        return self.formatted_terms

    def get_url(self) -> str:
        terms = self.__term_format(self.search_terms)
        return 'http://lmgtfy.com/?q={}'.format(terms)
