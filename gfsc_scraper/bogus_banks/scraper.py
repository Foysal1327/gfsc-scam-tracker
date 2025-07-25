import requests
from bs4 import BeautifulSoup
import re

def fetch_items():
    url = "https://www.gfsc.gg/consumers/scams-and-bogus-financial-institutions/bogus-banks-and-other-financial-institutions"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    gfsc_table = soup.find('table')
    
    table_headers = gfsc_table.find_all('th')
    table_titels = [title.text.strip() for title in table_headers]
    
    column_data = gfsc_table.find_all('tr')
    items = []

    for row in column_data[1:]:
        row_data = row.find_all('td')
        row_data = [data.text.strip() for data in row_data]
        # print(row_data[0], '|',  row_data[1])
        items.append({
                'name': row_data[0],
                'domain_name_note': row_data[1].strip(),
            })
        
    # Clean the items
    cleaned_items = clean_items(items)
    
    return cleaned_items

def clean_items(items):
    cleaned_items = []
    
    for item in items:
        # Cleaned the name
        name = item['name']
        name = name.replace('\xa0', ' ').replace('\n', ' ').replace('\t', ' ')
        name = re.sub(r'\s+', ' ', name).strip()
        domain_note = item['domain_name_note']
        
        cleaned_text = domain_note.replace('\u200b', '').replace('\n', ' ').replace('\t', ' ')
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        
        # Extracted domains using regex
        domain_pattern = r'(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'
        domains = re.findall(domain_pattern, cleaned_text)
        
        # Cleaned domains (removed protocols and paths)
        clean_domains = []
        for domain in domains:
            domain = re.sub(r'^https?://', '', domain)
            domain = domain.split('/')[0]
            if domain and domain not in clean_domains:
                clean_domains.append(domain)
        
        # Extracted notes
        notes = cleaned_text
        for domain in domains:
            notes = notes.replace(domain, '')

        # Cleaned up notes
        notes = re.sub(r'\s+', ' ', notes).strip()
        notes = re.sub(r'^[|\-\s]+|[|\-\s]+$', '', notes)
        
        cleaned_items.append({
            'name': name,
            'domains': clean_domains,
            'notes': notes if notes else ''
        })
    
    return cleaned_items