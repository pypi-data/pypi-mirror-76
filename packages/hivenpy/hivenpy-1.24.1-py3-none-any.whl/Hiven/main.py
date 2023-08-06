from Hiven.client import Bot, events

TOKEN = "o2U0IGVEeW5WILjHPxyjfkWEFuLZEw8pqNxcrb8JUYynPboVe0mZBg8Mn3GRUExj2tJRMA3ChDFLbEUQTn90YBnUhDYS0dIZgzxVON53hT47YYCxOer8g17WodOrUxgL"

bot = Bot(TOKEN, debug=False, output=True)


@events.event
def on_ready():
    bot.send("hey\nhows it going?", 140475951728292090)



bot.login()
