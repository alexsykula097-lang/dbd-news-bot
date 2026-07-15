import requests
from bs4 import BeautifulSoup

API_URL = (
    "https://forums.bhvr.com/api/v2/articles"
    "?locale=en"
    "&limit=10"
    "&siteSectionID=subcommunities-section-1"
    "&sort=-articleID"
)


def pobierz_najnowszy_news():
    try:
        response = requests.get(API_URL, timeout=15)

        if response.status_code != 200:
            return None

        dane = response.json()

        if not dane:
            return None

        artykul = dane[0]

        tytul = artykul.get("name", "Brak tytułu")

        link = artykul.get("url", "")

        if link.startswith("/"):
            link = "https://forums.bhvr.com" + link

        opis = "Brak opisu"
        obrazek = None

        page = requests.get(link, timeout=15)

        if page.status_code == 200:

            soup = BeautifulSoup(page.text, "html.parser")

            meta_desc = soup.find("meta", attrs={"name": "description"})

            if meta_desc:
                opis = meta_desc.get("content", opis)

            print("=== WSZYSTKIE IMG ===")

            for img in soup.find_all("img"):
                src = img.get("src")

                if src:
                    print(src)

                    if obrazek is None:
                        obrazek = src

        print("TYTUŁ:", tytul)
        print("OBRAZEK:", obrazek)

        return {
            "tytul": tytul,
            "opis": opis,
            "link": link,
            "obrazek": obrazek,
            "typ": "news"
        }

    except Exception as e:
        print("Błąd:", e)
        return None