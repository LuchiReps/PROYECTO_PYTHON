import os
import requests
from textblob import TextBlob
from pydantic import BaseModel, ValidationError
from typing import List, Optional


class ArticleSchema(BaseModel):
    title: str
    description: Optional[str] = None
    url: str


def analyze_sentiment(text: str) -> str:
    """Analiza el sentimiento de un texto y devuelve una etiqueta simple."""
    analysis = TextBlob(text)
    return "Positivo" if analysis.sentiment.polarity > 0 else "Negativo/Neutro"


def fetch_news(topic: str) -> List[dict]:
    """Obtiene noticias de NewsAPI si hay clave, o devuelve datos de ejemplo."""
    api_key = os.getenv("NEWSAPI_KEY", "").strip()
    if not api_key:
        print("Advertencia: NEWSAPI_KEY no está configurada. Se usarán datos de ejemplo.")
        return [
            {
                "title": "AI mejora el diagnóstico médico",
                "description": "Ejemplo de artículo",
                "url": "https://example.com/article1"
            },
            {
                "title": "La IA enfrenta desafíos éticos",
                "description": "Ejemplo de artículo",
                "url": "https://example.com/article2"
            }
        ]

    params = {
        "q": topic,
        "apiKey": api_key,
        "pageSize": 5,
        "language": "es"
    }
    try:
        response = requests.get("https://newsapi.org/v2/everything", params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("articles", [])
    except requests.RequestException as exc:
        print(f"Error al consultar la API de noticias: {exc}")
        return []


def validate_and_analyze(articles: List[dict]) -> List[dict]:
    """Valida la lista de artículos y aplica análisis de sentimiento al título."""
    results: List[dict] = []
    for article in articles:
        try:
            valid_article = ArticleSchema(**article)
            sentiment = analyze_sentiment(valid_article.title)
            results.append({
                "title": valid_article.title,
                "sentiment": sentiment
            })
        except ValidationError as exc:
            print(f"Error de calidad en datos: {exc}")
    return results


def main() -> None:
    raw_data = fetch_news("Artificial Intelligence")
    processed_data = validate_and_analyze(raw_data[:5])
    for item in processed_data:
        print(f"[{item['sentiment']}] - {item['title']}")


if __name__ == "__main__":
    main()