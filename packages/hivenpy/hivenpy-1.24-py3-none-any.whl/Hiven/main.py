from Hiven.client import Bot, events

TOKEN = "This is for testing purposes. Please ignore this file."

bot = Bot(TOKEN, debug=False, output=True)


@events.event
def on_house_join(ctx):
    print(ctx.house.join_time.strftime("%H"))



bot.login()
