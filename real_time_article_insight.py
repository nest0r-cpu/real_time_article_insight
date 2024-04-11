import requests
from bs4 import BeautifulSoup
import spacy
import re

# Function to scrape webpage and extract articles
def scrape_webpage(url):
    """
    Scrapes the specified webpage and extracts articles based on the provided CSS selector.
    
    Parameters:
        url (str): The URL of the webpage to scrape.
        
    Returns:
        list: A list of article elements found on the webpage.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', class_='vevent')  # Adjust this selector based on the actual HTML structure
    return articles

# Function to clean text by removing hyperlinks and special characters
def clean_text(text):
    """
    Cleans the text by removing hyperlinks and special characters.
    
    Parameters:
        text (str): The text to be cleaned.
        
    Returns:
        str: The cleaned text.
    """
    # Remove hyperlinks
    text = re.sub(r'\[\d+\]', '', text)
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

# Function to summarize article using spaCy
def summarize_article(article_text):
    """
    Summarizes the article text by extracting the first three sentences.
    
    Parameters:
        article_text (str): The text of the article.
        
    Returns:
        str: The summarized text.
    """
    cleaned_text = clean_text(article_text)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(cleaned_text)
    sentences = [sent.text for sent in doc.sents]
    summary = ' '.join(sentences[:3])  # Extracting the first three sentences as summary
    return summary

# Main function
def main():
    url = 'https://en.wikipedia.org/wiki/Portal:Current_events'
    articles = scrape_webpage(url)
    
    print("Number of articles found:", len(articles))
    
    for idx, article in enumerate(articles, start=1):
        article_text = article.get_text()  # Assuming the article text is directly in the article element
        print(f"Article {idx} content:")
        print(article_text)
        summary = summarize_article(article_text)
        print("Article Summary:")
        print(summary)
        print("\n")

if __name__ == "__main__":
    main()
