from dataclasses import dataclass
from urllib.request import urlopen, Request
from lxml import html


@dataclass
class ParseResult:
    word: str
    type: str
    translate: str
    description: str


class ParseWord:
    def __init__(self):
        self.path = f'https://dictionary.cambridge.org/dictionary/english-russian/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        self.xpath_word = '//*[@id="page-content"]/div[2]/div[4]/div/div/div[1]/div[3]/div[1]/div[2]/div/div[3]/span'
        self.xpath_type = '//*[@id="page-content"]/div[2]/div[4]/div/div/div[1]/div[2]/div[2]/span'
        self.xpath_description = '//*[@id="page-content"]/div[2]/div[4]/div/div/div[1]/div[3]/div[1]/div[2]/div/div[2]/div'

    def get(self, word):
        request = Request(self.path + word, headers=self.headers)
        response = urlopen(request)
        response_content = response.read()
        return response_content.decode('utf-8')

    def get_translate(self, tree) -> str:
        words = tree.xpath(self.xpath_word)
        for word in words:
            return word.text_content()

    def get_type(self, tree) -> str:
        types = tree.xpath(self.xpath_type)
        for part_of_speech in types:
            return part_of_speech.text_content()

    def get_description(self, tree) -> str:
        description_list = tree.xpath(self.xpath_description)
        return "".join([teg_a.text_content() for teg_a in description_list])

    def parse(self, word: str, html_str: str) -> ParseResult:
        tree = html.fromstring(html_str)
        return ParseResult(
            word=word,
            translate=self.get_translate(tree),
            type=self.get_type(tree),
            description=self.get_description(tree)
        )

    def __call__(self, word: str) -> ParseResult:
        return self.parse(word, self.get(word))


parse_word = ParseWord()


if __name__ == '__main__':
    print(parse_word("word"))
