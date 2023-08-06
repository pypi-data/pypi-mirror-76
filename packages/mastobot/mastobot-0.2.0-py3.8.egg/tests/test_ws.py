from mastobot import Bot, Favourite
from os import environ

instance = environ.get("INSTANCE")
token = environ.get("ACCESS_TOKEN")

bot = Bot(instance, token, websocket_mode=True)


@bot.on_home_update(":(cis|trans|ultra)?cate:", validation="regex")
def cated(status):
    return Favourite

bot.run()
