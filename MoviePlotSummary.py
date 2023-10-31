import requests
from bs4 import BeautifulSoup
from googlesearch import search

while True:
    q = input("Search: ")

    query_plot = q + " imdb plot"
    query_rating = q + "imdb"

    search_res = []

    try:
        for res in search(query_plot, stop=20, pause = 0.001):
            print(res)
            if "plotsummary" in res:
                plot = res
                break
                
        plot_li = plot.split("/")

        for res in search(query_rating, num = 2, stop=20, pause = 0.001):
            print(res)
            if plot_li[-3] in res:
                rating = res
                break

    except:
        print("Error\n")
    else:
        print()
        
        try:
            
            session_plot = requests.Session()
            sessp = session_plot.get(plot, headers={"User-Agent": "Chrome"})

            session_rating = requests.Session()
            sessr = session_rating.get(rating, headers={"User-Agent": "Chrome"})

            soupp = BeautifulSoup(sessp.content, "html.parser")
            soupr = BeautifulSoup(sessr.content, "html.parser")

            sr = soupr.find("div", class_="sc-bde20123-0 gtEgaf")

            contentr = sr.find_all("span", class_="sc-bde20123-1 iZlgcd")
            num = sr.find_all("div", class_="sc-bde20123-3 bjjENQ")

            title = soupp.title

            title_li = [t.text for t in title][0].split("-")
            
            title_fin = ""

            for tl in title_li:
                if tl == " Plot ":
                    break
                title_fin += tl + "-"
                
            print(title_fin[:-1])
                
            print(
                f"Rating: {[cr.text for cr in contentr][0]} ({[n.text for n in num][0]})\n"
            )

            sp = soupp.find("div", class_="sc-f65f65be-0 fVkLRr")

            contentp = sp.find_all("li", role="presentation")

            sums = []

            for cp in contentp:
                sums.append(cp.text)

            print(max(sums, key=len) + "\n")
        
        except:
            print("Error\n")
        else:
            pass
