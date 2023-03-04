from bs4 import BeautifulSoup
import requests
import dateutil.parser

# Directory to save the file in
directory = "C:/PythonFiles/PST.AG"

def get_add_data(url, categories, title, reward_amount, assoc_org, loc, about, img_urls, dob_value):
    # Send a request to the URL and get the content
    response = requests.get(url)
    content = response.content

    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # Create a BeautifulSoup object
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the nth div with class "elementor-widget-container"

    # Extract the "Title" value
    divs = soup.find_all("div", class_="elementor-widget-container")
    if len(divs) >= 9:
        div = divs[8]  # 0-based indexing
        title = div.find_next("h2").get_text(strip=True)
    else:
        title = ""
    print(f"Fetching information for {title}.. .")    
    
    # Extract the "Date of Birth" value
    dob_h2 = soup.find("h2", text="Date of Birth:")
    if dob_h2:
        div = dob_h2.find_next("div", class_="elementor-widget-container")
        if div:
            dob_text = div.get_text(strip=True)
            try:
                dob_value = dateutil.parser.parse(dob_text).date().isoformat()
            except ValueError:
                dob_value = dob_text
        else:
            dob_value = ""
    else:
        dob_value = ""

    # Extract the "Reward Amount" value
    divs = soup.find_all("div", class_="elementor-widget-container")
    if len(divs) >= 12:
        div = divs[11]  # 0-based indexing
        reward_amount = div.find_next("h2").get_text(strip=True)
        if reward_amount == "Do your part": reward_amount=""
    else:
        reward_amount = ""

    # Find the "Associated Organizations" value
    org_h2 = soup.find("h2", text="Associated Organizations:")
    if org_h2:
        div = org_h2.find_next("div", class_="elementor-widget-container")
        if div:
            assoc_org = div.get_text(strip=True)
        else:
            assoc_org = ""
    else:
        org_h2 = soup.find_all("h2", class_="elementor-heading-title elementor-size-default")
        found = False
        for div in org_h2:
            if "Associated Organization" in div.get_text():
                found = True
                break
        if found:
            assoc_org = div.find_next("a").get_text(strip=True)
        else:
            assoc_org = ""

    # Find the "Known Locales" value
    loc_h2 = soup.find("h2", text="Known Locales:")
    if loc_h2:
        div = loc_h2.find_next("div", class_="elementor-widget-container")
        if div:
            loc = div.get_text(strip=True)
        else:
            loc = ""
    else:
        loc_h2 = soup.find_all("h2", class_="elementor-heading-title elementor-size-default")
        found = False
        for div in loc_h2:
            if "Associated Location(s):" in div.get_text():
                found = True
                break
        if found:
            loc = div.find_next("div", class_="elementor-widget-container")
            loc = loc.get_text(strip=True)
        else:
            loc = ""

    # Find the "About" value
    about_h2 = soup.find("h2", text="About")
    if about_h2:
        div = about_h2.find_next("div", class_="elementor-widget-container")
        if div:
            about = div.get_text(strip=True)
        else:
            about = ""
    else:
        about = ""

    # Find all .jpg links
    img_url = []
    for link in soup.find_all("a"):
        url_jpg = link.get("href")
        if url_jpg and url_jpg.endswith(".jpg"):
            img_url.append(url_jpg)
        img_urls = {n for n in img_url}if img_url else ""

    return url, categories, title, reward_amount, assoc_org, loc, about, img_urls, dob_value
