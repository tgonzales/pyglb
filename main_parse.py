from xml.etree.ElementTree import Element, tostring, fromstring
from bs4 import BeautifulSoup
from xmljson import badgerfish as bf
from xmljson import BadgerFish
import json
import requests

def convert_only_int(val):
    return int(val) if val.isdigit() else val

def preper_description(data):
    soup = BeautifulSoup(data, "html.parser")
    description = [
            {
                'type': 'text_full',
                'content': ''.join([p.getText().replace("\"", "'") for p in soup.find_all('p')])
            },
            {
                'type': 'links',
                'content': [link['href'] for link in soup.select('a')]
            }
    ]
    for i in soup.find_all():
        if i.name == 'img':
            obj = {"type": "image", "content": i['src']}
            description.append(obj)
            #print(obj)

        if i.name == 'p' and i.getText().split():
            obj = {"type": "text", "content": ' '.join(i.getText().replace("\"", "'").split())}
            description.append(obj)
            #print(obj)

    return description


def main(limit=100):
    data = requests.get('http://revistaautoesporte.globo.com/rss/ultimas/feed.xml')
    bf_int = BadgerFish(xml_fromstring=convert_only_int)
    data_parse = json.dumps(bf_int.data(fromstring(data.text)))
    data_parse = json.loads(data_parse)
    feed = {'feed':{'item':data_parse['rss']['channel']['item']}}
    item = [{'title': i['title']['$'], 'link': i['link']['$'], 'description': preper_description(i['description']['$'])} for i in feed['feed']['item']]
    count = len(feed['feed']['item'])
    #print('LEN ', count)
    if limit >= count:
        item = item[0:count]
    else:
        item = item[0:limit]

    feed['feed']['item'] = item
    #print('ITEM ', len(feed['feed']['item']))
    return feed

if __name__ == '__main__':
    print('crawler run...')
    print(main())