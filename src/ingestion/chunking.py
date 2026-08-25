import re


def chunk_by_article(text: str) -> list[str]:
    partes = re.split(r'((?:Art\.|Artículo) \d+[°.]-)', text)
    return [partes[i] + partes[i + 1] for i in range(1, len(partes), 2)]


if __name__ == "__main__":
    with open("data/raw/ley_27551.txt", encoding="utf-8") as f:
        texto = f.read()

    chunks = chunk_by_article(texto)
    print(f"Total chunks: {len(chunks)}")
    for chunk in chunks:
        print("---")
        print(chunk)