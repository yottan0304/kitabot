import datetime
from pprint import pprint
from notion_client import Client

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)

#Get page id
def get_page_id(notion, title, data_base_id):
    db = notion.databases.query(
        **{
            "database_id": data_base_id,
            "filter": {
                "property": "Name",
                "rich_text": {
                    "contains": title
                }
            },
        }
    )
    return db['results'][0]['id']

#create page in database
def create_page(notion, data_base_id, title, kinds):
    notion.pages.create(
        **{
            'parent': {
                'database_id': data_base_id
            },
            'properties': {
                'Name': {
                    'title': [
                        {
                            'text': {
                                'content': title,
                            }
                        }
                    ]
                },
                '種別': {
                    'multi_select': [
                        {
                            'name': kinds,
                        }]
                },
                '視聴・読破日': {
                    'date': {
                        'start': now.date().strftime('%Y-%m-%d')
                    }
                }
            },
        }
    )

    return

#ADD block(h2)
def add_h2(notion, page_id, text):
    notion.blocks.children.append(
    "6973673eda4a431a9464c5614c6490d6",
    children=[{
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": text,
                }
            }],
            "color": "default",
        },
    }]
)

#ADD block(callout)
def add_callout(notion, page_id, text, emoji):
    notion.blocks.children.append(
        page_id,
        children=[{
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": text,
                    },
                }],
                "icon": {
                    "emoji": emoji
                },
                "color": "gray_background",
            }
        }]
)

def add_h2(notion, page_id, text):
    notion.blocks.children.append(
        page_id,
        children=[{
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": text,
                    }
                }],
                "color": "default",
            },
        }]
)

def add_bookmark(notion, page_id, url):
    notion.blocks.children.append(
        page_id,
        children=[{
            "object": "block",
            "type": "bookmark",
            "bookmark": {
                "url": url
                }
        }]
    )