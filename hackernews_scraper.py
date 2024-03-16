import requests
from bs4 import BeautifulSoup
import re
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

rank = 0

with open('hackernews_top.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Rank', 'Title', 'URL', 'Website'])
    
    for page_num in range(1, 10):
        # url = f"https://news.ycombinator.com/?p={page_num}"
        url = f"https://news.ycombinator.com/front?day=2024-03-16&p={page_num}"
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        all_html_line = soup.findAll("span", class_='titleline')
            
        for html_line in all_html_line:
            html_line = str(html_line)
            rank += 1
            
            title_pattern = r'<a[^>]*>(.*?)</a>'
            title_match = re.search(title_pattern, html_line)
            title = title_match.group(1) if title_match else None
            
            # url_pattern = r'href="([^"]+)"'
            # url_match = re.search(url_pattern, html_line)
            # url = url_match.group(1) if url_match else None
            
            url_pattern = r'href="([^"]+)"'
            url_match = re.search(url_pattern, html_line)
            url = url_match.group(1) if url_match and url_match.group(1).startswith('http') else None
            
            website_pattern = r'sitestr">([^<]+)</span>'
            website_match = re.search(website_pattern, html_line)
            website = website_match.group(1) if website_match else None
            
            csvwriter.writerow([rank, title, url, website])
            print("Rank:", rank)
            # print("Title:", title)
            # print("Title:", title.encode('utf-8', 'ignore').decode('utf-8'))
            print("Title:", title.encode('ascii', 'ignore').decode('ascii'))
            print("URL:", url)
            print("Website:", website)
            print("")

print("CSV file created successfully!")
