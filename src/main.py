import discord
import os
import json
import boto3

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

# メッセージが出力された
# @client.event
# async def on_message(message):
#     # Bot自身へのメッセージの場合無視
#     if message.author == client.user:
#         return
#     # メッセージに$helloが入っている場合にHelloと返す
#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

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

#Lexインスタンス作成
lex_client = boto3.client(
    'lexv2-runtime',
    region_name = GetConf.get_region_name(),
    aws_access_key_id = GetConf.get_aws_access_key_id(),
    aws_secret_access_key = GetConf.get_aws_secret_access_key()
)

#Discord bot作成
client.run(token = GetConf.get_token())