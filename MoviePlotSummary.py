import requests
from bs4 import BeautifulSoup
from googlesearch import search

def get_plot_url(query):
    query_plot = query + " imdb plot"
    for res in search(query_plot, stop=20, pause=0.1):
        if "plotsummary" in res:
            return res
    return None

def get_rating_url(query, plot_url):
    query_rating = query + " imdb"
    plot_id = plot_url.split("/")[-3]
    for res in search(query_rating, num=2, stop=20, pause=0.1):
        if plot_id in res:
            return res
    return None

def fetch_and_parse(url):
    try:
        session = requests.Session()
        response = session.get(url, headers={"User-Agent": "Chrome"})
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def extract_rating(soup):
    try:
        rating_tag = soup.find("span", {"itemprop": "ratingValue"})
        rating = rating_tag.text if rating_tag else "N/A"
        
        review_count_tag = soup.find("span", {"itemprop": "ratingCount"})
        num_reviews = review_count_tag.text if review_count_tag else "N/A"
        
        return rating, num_reviews
    except (AttributeError, IndexError):
        return None, None

def extract_plot(soup):
    try:
        plot_tag = soup.find("div", {"id": "summary_text"})
        plot_summary = plot_tag.text.strip() if plot_tag else "Plot summary not found"
        return plot_summary
    except AttributeError:
        return None

def main():
    while True:
        query = input("Search: ")

        plot_url = get_plot_url(query)
        if not plot_url:
            print("Plot URL not found")
            continue

        rating_url = get_rating_url(query, plot_url)
        if not rating_url:
            print("Rating URL not found")
            continue

        plot_soup = fetch_and_parse(plot_url)
        rating_soup = fetch_and_parse(rating_url)

        if not plot_soup or not rating_soup:
            print("Failed to fetch and parse URLs")
            continue

        rating, num_reviews = extract_rating(rating_soup)
        plot_summary = extract_plot(plot_soup)

        if not rating or not num_reviews:
            print("Failed to extract rating information")
            continue

        if not plot_summary:
            print("Failed to extract plot summary")
            continue

        title = plot_soup.title.string.split(" - ")[0]
        print(f"\n{title}")
        print(f"Rating: {rating} ({num_reviews})")
        print(f"Plot Summary: {plot_summary}\n")

if __name__ == "__main__":
    main()
