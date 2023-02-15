from pprint import pprint
import discord
import os
import json
import movie_info_scraping
import notion
import re

# Select os directory
os.chdir(os.path.join(os.path.dirname(__file__), "../"))
CONFIG_PATH = 'json/config.json'

# Make intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Start Bot
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Record Notion
    if "487572866267873290" == str(message.author.id):

        try:
            # Get info
            pprint("test1")
            info = movie_info_scraping.get_info(message.content)

            if None != info:
                pprint("test2")
                await message.channel.send(""f'{message.content}を見るんですね！')

                # Check Notion's database
                if "Match" != notion.check_record(GetConf.get_notion_api_key(), GetConf.get_notion_database_id(), message.content):
                    
                    # Send on Notion
                    pprint("test3")
                    notion.create_record(GetConf.get_notion_api_key(), GetConf.get_notion_database_id(), info)
                    await message.channel.send("Notion映画情報記録しました！観たら感想をぜひ書いてください！")

                else:
                    await message.channel.send("何度か見ている作品ですね")

        except:
            pprint("normal msessage")

        if "https://amzn.asia" in message.content:

            # Get movie name
            movie_name = movie_info_scraping.get_name(message.content, GetConf.get_amazon_login_id(), GetConf.get_amazon_login_password())
            await message.channel.send(""f'{movie_name}を見るんですね！')

            # Check Notion's database
            if "Match" != notion.check_record(GetConf.get_notion_api_key(), GetConf.get_notion_database_id(), movie_name):
                
                # Get info
                info = movie_info_scraping.get_info(movie_name)
                
                # Send on Notion
                notion.create_record(GetConf.get_notion_api_key(), GetConf.get_notion_database_id(), info)
                await message.channel.send("Notion映画情報記録しました！観たら感想をぜひ書いてください！")

            else:
                await message.channel.send("何度か見ている作品ですね")


# Get config
class GetConf:
    @classmethod
    def get_token(cls): 
        with open(CONFIG_PATH) as f:
            token = json.load(f).get('TOKEN')
        return token
    @classmethod
    def get_region_name(cls):
        with open(CONFIG_PATH) as f:
            region_name = json.load(f).get('REGION_NAME')
        return region_name
    @classmethod
    def get_aws_access_key_id(cls):
        with open(CONFIG_PATH) as f:
            aws_access_key_id = json.load(f).get('AWS_ACCESS_KEY_ID')
        return aws_access_key_id
    @classmethod
    def get_aws_secret_access_key(cls):
        with open(CONFIG_PATH) as f:
            aws_secret_access_key = json.load(f).get('AWA_SECRET_ACCESS_KEY')
        return aws_secret_access_key 
    @classmethod
    def get_amazon_login_id(cls):
        with open(CONFIG_PATH) as f:
            amazon_login_id = json.load(f).get('AMAZON_LOGIN_ID')
        return amazon_login_id 
    @classmethod
    def get_amazon_login_password(cls):
        with open(CONFIG_PATH) as f:
            amazon_login_password = json.load(f).get('AMAZON_LOGIN_PASSWORD')
        return amazon_login_password 

    @classmethod
    def get_notion_api_key(cls):
        with open(CONFIG_PATH) as f:
            notion_api_key = json.load(f).get('NOTION_API_KEY')
        return notion_api_key
    @classmethod
    def get_notion_database_id(cls):
        with open(CONFIG_PATH) as f:
            notion_database_id = json.load(f).get('NOTION_DATABASE_ID')
        return notion_database_id

# Make Discord instans
client.run(token = GetConf.get_token())