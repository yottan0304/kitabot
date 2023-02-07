from pprint import pprint
from notion_client import Client
from modules import notion_modules as module

def check_record(api_key, data_base_id, title):

    notion = Client(auth = api_key)

    # Pull database
    db = notion.databases.query(
        **{
            'database_id' : data_base_id
        }
    )

    # Check title
    for index in range(len(db['results'])):
        if title == db['results'][index]['properties']['Name']['title'][0]['text']['content']:
            return "Match"

    return

def create_record(api_key, data_base_id, info):
    
    notion = Client(auth = api_key)

    # create page
    if info[1] == "movies":
        module.create_page(notion, data_base_id, info[0], "映画")
    elif info[1] == "dramas":
        module.create_page(notion, data_base_id, info[0], "ドラマ")
    elif info[1] == "animes":
        module.create_page(notion, data_base_id, info[0], "アニメ")

    # get page id
    page_id = module.get_page_id(notion, info[0], data_base_id)

    # add Filmarks
    module.add_h2(notion, page_id, "■Filmarks")
    module.add_bookmark(notion, page_id, info[2])

    # add synopsis
    if "" != info[3]:
        module.add_h2(notion, page_id, "■あらすじ")
        module.add_callout(notion, page_id, info[3], "🎬")

    # add impression
    module.add_h2(notion, page_id, "■所感")