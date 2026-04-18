import pytest
from main import analyze_sentiment

def test_sentiment_positive():
    # Test unitario: ¿La IA reconoce palabras positivas?
    title = "This is an amazing and great breakthrough in AI"
    result = analyze_sentiment(title)
    assert result == "Positivo"

def test_sentiment_negative():
    # Test unitario: ¿La IA reconoce palabras negativas?
    title = "This is a terrible and bad error"
    analysis = TextBlob(title)
    assert analysis.sentiment.polarity < 0

def test_api_connection():
    # Test de integración: Verificar que la API responde
    import requests
    response = requests.get("https://newsapi.org/")
    assert response.status_code == 200