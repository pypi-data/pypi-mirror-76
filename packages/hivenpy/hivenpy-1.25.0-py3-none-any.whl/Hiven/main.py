from Hiven.client import Bot, events

TOKEN = "bruh, you tried."

bot = Bot(TOKEN, debug=False, output=True)


@events.event
async def on_message(ctx):
    message = ctx.message
    if message.content == "!pfp":
        await ctx.send(ctx.author.icon)



bot.login()
