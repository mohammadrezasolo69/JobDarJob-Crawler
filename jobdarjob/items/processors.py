from bs4 import BeautifulSoup
from w3lib.html import remove_tags


def clean_result(value: str) -> str:
    return remove_tags(
        value.strip().replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').replace('\u200c', ' ')
    )


def clean_description(value: str) -> str:
    soup = BeautifulSoup(value, 'html.parser')
    text = soup.get_text(strip=True)
    return text.replace("'", "''")