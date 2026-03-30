import httpx
from selectolax.parser import HTMLParser
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "/Users/user/Downloads/events-491811-34c69e9eed3c.json"
SPREADSHEET_ID = "1exHaoBp4rYQzf_3fK9bNElSnoBk5EvYrqJ0h0wXjESk"
def get_sheet():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID).sheet1

def scrape():
    rows = []
    url = "https://www.eventbrite.com/d/nigeria--lagos/business--events/?page=1"
    headers = {'Authorization': 'Bearer NJ7LKGNHP64J6C7NJD6W'}
    response = httpx.get(url, headers=headers)
    html= HTMLParser(response.text)
    events = html.css('ul.SearchResultPanelContentEventCardList-module__eventList___2wk-D li')

    for event in events:
        title = event.css_first("h3")
        time = event.css_first("p.Typography_root__487rx")
        if title and time:
            rows.append([title.text(), time.text().strip()])

    return rows

def add_to_sheet():
    sheet = get_sheet()
    rows = scrape()
    for row in rows:
        sheet.append_row(row)

if __name__ == "__main__":
    add_to_sheet()