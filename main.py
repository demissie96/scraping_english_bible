from queue import Empty
import requests
from requests_file import FileAdapter
from bs4 import BeautifulSoup
import json
import re
import unicodedata

book_list = [
    ["GEN", 50, "1Móz", "1 Mózes"], 
    ["EXO", 40, "2Móz", "2 Mózes"], 
    ["LEV", 27, "3Móz", "3 Mózes"], 
    ["NUM", 36, "4Móz", "4 Mózes"], 
    ["DEU", 34, "5Móz", "5 Mózes"], 
    ["JOS", 24, "Józs", "Józsué"], 
    ["JDG", 21, "Bír", "Bírák"], 
    ["RUT", 4, "Ruth", "Ruth"], 
    ["1SA", 31, "1Sám", "1 Sámuel"], 
    ["2SA", 24, "2Sám", "2 Sámuel"], 
    ["1KI", 22, "1Kir", "1 Királyok"], 
    ["2KI", 25, "2Kir", "2 Királyok"], 
    ["1CH", 29, "1Krón", "1 Krónika"], 
    ["2CH", 36, "2Krón", "2 Krónika"], 
    ["EZR", 10, "Ezsd", "Ezsdrás"], 
    ["NEH", 13, "Neh", "Nehémiás"], 
    ["EST", 10, "Eszt", "Eszter"], 
    ["JOB", 42, "Jób", "Jób"], 
    ["PSA", 150, "Zsolt", "Zsoltárok"], 
    ["PRO", 31, "Péld", "Példabeszédek"], 
    ["ECC", 12, "Préd", "Prédikátor"], 
    ["SNG", 8, "Énekek", "Énekek Éneke"], 
    ["ISA", 66, "Ésa", "Ésaiás"], 
    ["JER", 52, "Jer", "Jeremiás"], 
    ["LAM", 5, "JSir", "Jeremiás Siralmai"], 
    ["EZK", 48, "Ez", "Ezékiel"], 
    ["DAN", 12, "Dán", "Dániel"], 
    ["HOS", 14, "Hós", "Hóseás"], 
    ["JOL", 3, "Jóel", "Jóel"], 
    ["AMO", 9, "Ám", "Ámós"], 
    ["OBA", 1, "Abd", "Abdiás"], 
    ["JON", 4, "Jón", "Jónás"], 
    ["MIC", 7, "Mik", "Mikeás"], 
    ["NAM", 3, "Náh", "Náhum"], 
    ["HAB", 3, "Hab", "Habakuk"], 
    ["ZEP", 3, "Sof", "Sofóniás"], 
    ["HAG", 2, "Agg", "Aggeus"], 
    ["ZEC", 14, "Zak", "Zakariás"], 
    ["MAL", 4, "Mal", "Malakiás"], 
    ["MAT", 28, "Mt", "Máté"], 
    ["MRK", 16, "Mk", "Márk"], 
    ["LUK", 24, "Lk", "Lukács"], 
    ["JHN", 21, "Jn", "János"], 
    ["ACT", 28, "ApCsel", "ApCsel"], 
    ["ROM", 16, "Róm", "Róma"], 
    ["1CO", 16, "1Kor", "1 Korinthus"], 
    ["2CO", 13, "2Kor", "2 Korinthus"], 
    ["GAL", 6, "Gal", "Galácia"], 
    ["EPH", 6, "Ef", "Efézus"], 
    ["PHP", 4, "Fil", "Filippi"], 
    ["COL", 4, "Kol", "Kolossé"], 
    ["1TH", 5, "1Thessz", "1 Thessalonika"], 
    ["2TH", 3, "2Thessz", "2 Thessalonika"], 
    ["1TI", 6, "1Tim", "1 Timótheus"], 
    ["2TI", 4, "2Tim", "2 Timótheus"], 
    ["TIT", 3, "Tit", "Titus"], 
    ["PHM", 1, "Filem", "Filemon"], 
    ["HEB", 13, "Zsid", "Zsidó"], 
    ["JAS", 5, "Jak", "Jakab"], 
    ["1PE", 5, "1Pt", "1 Péter"], 
    ["2PE", 3, "2Pt", "2 Péter"], 
    ["1JN", 5, "1Jn", "1 János"], 
    ["2JN", 1, "2Jn", "2 János"], 
    ["3JN", 1, "3Jn", "3 János"], 
    ["JUD", 1, "Júd", "Júdás"], 
    ["REV", 22, "Jel", "Jelenések"]]

def chapters_content(book, chapter):
    
    if book == "PSA":
        if chapter < 10:
            chapter_url = f'00{chapter}'
        elif chapter < 100:
            chapter_url = f'0{chapter}'
        else:
            chapter_url = chapter
    else:
        if chapter < 10:
            chapter_url = f'0{chapter}'
        else:
            chapter_url = chapter
        
    verse_list = []
    
    # For request local file
    s = requests.Session()
    s.mount('file://', FileAdapter())

    response = s.get(f'file:///home/demissiejohannes/Desktop/Portfolio%20Projects/scrape_english_bible/eng-web_html/{book}{chapter_url}.htm')
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    
    verse_span = soup.find_all("span", class_="verse")
    for span in verse_span:
        span.replace_with(span.text)
    
    notemarks = soup.find_all("a", class_="notemark")
    mt = soup.find_all("div", class_="mt")
    mt2 = soup.find_all("div", class_="mt2")
    mt3 = soup.find_all("div", class_="mt3")
    ms = soup.find_all("div", class_="ms")
    chapterlabel = soup.find_all("div", class_="chapterlabel")
    tnav = soup.find_all("div", class_="tnav")
    footnote = soup.find_all("div", class_="footnote")
    copyright = soup.find_all("div", class_="copyright")
    
    for x in notemarks:
        x.decompose()
    for x in mt:
        x.decompose()
    for x in mt2:
        x.decompose()
    for x in mt3:
        x.decompose()
    for x in ms:
        x.decompose()
    for x in chapterlabel:
        x.decompose()
    for x in tnav:
        x.decompose()
    for x in footnote:
        x.decompose()
    for x in copyright:
        x.decompose()
    
   

    chapter_body = soup.find("div", class_="main")
    
    all_verse_div = chapter_body.find_all("div")
    
    chapter_in_one_string = ""
    
    for verse_div in all_verse_div:
        chapter_in_one_string += verse_div.text

    # print(chapter_in_one_string)
    chapter_in_one_string = unicodedata.normalize('NFKD', chapter_in_one_string)
            
    verse_div_list = re.split(r'(\d+)', chapter_in_one_string.strip())    
    # print(verse_div_list)
    
    try:
        verse_div_list.remove('')
    except:
        pass
    
    text_en = ''
    num = ''
    index = 0
    
    for element in verse_div_list:
        index += 1
        if index % 2 == 0:
            text_en = str(element.strip())
            verse_list.append({"num": num, "text_en": text_en}) 
        else:
            num = element

    return verse_list   
    
    

a_whole_chapter = chapters_content("JOB", 42)
print(a_whole_chapter)