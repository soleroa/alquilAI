import re


def chunk_by_article(text: str) -> list[str]:
    matches = re.findall(r'((?:Art\.|Artículo) \d+[°.]-)', text)
    return [match for match in matches]


if __name__ == "__main__":
    sample = "Art. 1°- Contenido... Artículo 2°- Otro contenido... Art. 10°- Más."
    print(chunk_by_article(sample))
