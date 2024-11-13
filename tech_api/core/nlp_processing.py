# core/nlp_processing.py

from textblob import TextBlob
import re

def preprocess_text(text):
    """
    Preprocess the input text by removing special characters and converting to lowercase.
    
    Args:
        text (str): The input text to preprocess.

    Returns:
        str: The preprocessed text.
    """
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    return text.strip()

def analyze_sentiment(text):
    """
    Analyze the sentiment of the input text using TextBlob.
    
    Args:
        text (str): The input text to analyze.

    Returns:
        dict: A dictionary containing the polarity and subjectivity of the text.
    """
    blob = TextBlob(text)
    return {
        'polarity': blob.sentiment.polarity,  # Ranges from -1 (negative) to 1 (positive)
        'subjectivity': blob.sentiment.subjectivity  # Ranges from 0 (objective) to 1 (subjective)
    }

def extract_keywords(text, num_keywords=5):
    """
    Extract keywords from the input text using simple frequency analysis.
    
    Args:
        text (str): The input text from which to extract keywords.
        num_keywords (int): The number of keywords to extract.

    Returns:
        list: A list of extracted keywords.
    """
    words = preprocess_text(text).split()
    frequency = {}
    
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    
    # Sort keywords by frequency and return the top n keywords
    sorted_keywords = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    return [keyword[0] for keyword in sorted_keywords[:num_keywords]]

# Example usage
if __name__ == "__main__":
    sample_text = "I love programming in Python. Python is great for data science!"
    preprocessed = preprocess_text(sample_text)
    sentiment = analyze_sentiment(sample_text)
    keywords = extract_keywords(sample_text)

    print("Preprocessed Text:", preprocessed)
    print("Sentiment Analysis:", sentiment)
    print("Extracted Keywords:", keywords)
