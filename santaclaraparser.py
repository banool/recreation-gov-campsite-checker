import requests
from html.parser import HTMLParser

cookies = {
    'ASPSESSIONIDCQDCTCAD': 'NGFPGHJCBECHJNEIAONNBEOO',
    'ASPSESSIONIDSSDDSCBB': 'PCBNDPCAIEDDMMCFJKJKIFHO',
    '__utma': '79996289.678760665.1592847762.1592847762.1592847762.1',
    '__utmc': '79996289',
    '__utmz': '79996289.1592847762.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    '__utmt': '1',
    '__utmb': '79996289.5.10.1592847762',
}

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    'Accept': 'text/html',
    'Referer': 'http://gooutsideandplay.org/reservations/SiteDetails.asp?SiteID=291&ArriveDate=12/17/2020&DepartDate=12/20/2020&TheDate=9/1/2020',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'text/html'
}


response = requests.get('http://gooutsideandplay.org/reservations/SiteDetails.asp?SiteID=291&ArriveDate=12/17/2020&DepartDate=12/20/2020&TheDate=8/1/2020', headers=headers, cookies=cookies, verify=False)

print(response.text)

HTMLParser.feed(response.text)
HTMLParser.close()
