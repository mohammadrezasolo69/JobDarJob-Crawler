import re

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


def extract_number(value):
    match = re.search(r'\d+', value)
    if match:
        return int(match.group())
    return 0


# def extract_number(value):
#     match = re.search(r'\d+', value)
#     if match:
#         return 60 - int(match.group())
#     return 0


# -------------------------------- quera ------------------------------------
def convert_work_experience(value: str):
    ...


def cover_complete(value: str) -> str:
    main_url = 'https://quera.org/'
    return main_url + value


def convert_publish_date(text):
    convert = {
        'یک': 1,
        'دو': 2,
    }
    for key, value in convert.items():
        text = text.replace(key, str(value))

    match = re.search(r'(\d+)\s+(روز|ماه)', text)
    if match:
        number = int(match.group(1))
        unit = match.group(2)
        if unit == 'ماه':
            return int(number) * 30
        else:
            return number
    else:
        return None
