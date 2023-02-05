import discord
import os
import json
import boto3
import selenium_serach
import re
import notion
from pprint import pprint

# BASEディレクトリ指定
os.chdir(os.path.join(os.path.dirname(__file__), "../"))
CONFIG_PATH = 'json/config.json'

# Discordインスタンス作成
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Bot起動時の出力
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    #Record Notion
    if "487572866267873290" == str(message.author.id):

        if re.match(r'[https://amzn.asia]+', message.content):

            #Get movie name
            movie_name = selenium_serach.get_name(message.content, GetConf.get_amazon_login_id(), GetConf.get_amazon_login_password())
            await message.channel.send(""f'{movie_name}を見るんですね！')
            pprint("movie name OK")

            #Check Notion's database
            if "Match" != notion.check_record(GetConf.get_notion_api_key(), GetConf.get_notion_database_id(), movie_name):
                
                #Get info
                pprint("check OK")
                info = selenium_serach.get_info(movie_name)
                

                #Send on Notion
                pprint("befor send to notion")
                notion.create_record(GetConf.get_notion_api_key(), GetConf.get_notion_database_id(), info)
                await message.channel.send("Notion映画情報記録しました！観たら感想をぜひ書いてください！")

            else:
                await message.channel.send("何度か見ている作品ですね")


# JSONファイルからトークン情報を得る
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

#Lexインスタンス作成
# lex_client = boto3.client(
#     'lexv2-runtime',
#     region_name = GetConf.get_region_name(),
#     aws_access_key_id = GetConf.get_aws_access_key_id(),
#     aws_secret_access_key = GetConf.get_aws_secret_access_key()
# )

#Discord bot作成
client.run(token = GetConf.get_token())