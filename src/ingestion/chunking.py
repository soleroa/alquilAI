import re


def chunk_by_article(text: str) -> list[str]:
    matches = re.findall(r'((?:Art\.|Artículo) \d+[°.]-)', text)
    return [match for match in matches]