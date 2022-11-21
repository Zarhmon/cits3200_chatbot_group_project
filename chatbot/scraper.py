import webbrowser
import bs4
import requests

def callback(url):
    webbrowser.open_new_tab(url)

def google_search(query):
    url = 'https://google.com/search?q=' + "+".join(query.split())
    req = requests.get( url )
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    heading_object=soup.find_all( 'h3' )
    links = []
    for i, item in enumerate(soup.find_all( 'h3' )):
        if item.parent.get("href") is None: continue
        links.append({
            "title":item.getText(),
            "link":"https://google.com"+item.parent.get("href")
        })
    for info in heading_object:
        print(info.getText())
        print("--------------------------------------------------------------------------------------------")
    return links
    

def scholar_search(query):
    url = 'https://scholar.google.com.au/scholar?q=' + "+".join(query.split())
    req = requests.get( url )
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    links = []
    heading_object=soup.find_all( 'h3' )
    for i, item in enumerate(soup.find_all( 'h3' )):
        if item.a.get("href") is None: continue
        links.append({
            "title":item.getText(),
            "link":item.a.get("href")
        })
    for info in heading_object:
        print(info.getText())
        print("--------------------------------------------------------------------------------------------")
    return links

if __name__ == "__main__":
    q = input("Enter query: ")
    q = q.replace("search ", "")
    from pprint import pprint
    pprint(google_search(q))
    pprint(scholar_search(q))
    print("--------------------------------------------------------------------------------------------")
    