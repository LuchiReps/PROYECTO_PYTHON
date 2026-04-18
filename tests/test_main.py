import os
from main import analyze_sentiment, fetch_news


def test_sentiment_positive():
    # Test unitario: ¿La IA reconoce palabras positivas?
    title = "This is an amazing and great breakthrough in AI"
    result = analyze_sentiment(title)
    assert result == "Positivo"


def test_sentiment_negative():
    # Test unitario: ¿La IA reconoce palabras negativas?
    title = "This is a terrible and bad error"
    result = analyze_sentiment(title)
    assert result == "Negativo/Neutro"


def test_fetch_news_fallback():
    if "NEWSAPI_KEY" in os.environ:
        del os.environ["NEWSAPI_KEY"]

    result = fetch_news("AI")
    assert isinstance(result, list)
    assert result, "Se espera que la función devuelva datos de ejemplo si no hay NEWSAPI_KEY"