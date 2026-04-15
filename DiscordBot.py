import discord
from discord.ext import tasks
import yfinance as yf
import datetime as dt

TOKEN = 'MTQ5MzMzMDU2NjU4ODY2NTg2Ng.GVdSUo.kf4ExYE8J0IHLGuxpdVYS1TsH_5UYXR5qFj0Zo'
CHANNEL_ID = 1493336961136595014
UPDATE_INTERVAL_MINUTES = 60

class EuroBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prev_price = None

    async def setup_hook(self):
        self.check_exchange_rate.start()

    async def on_ready(self):
        print(f'A Bot elindult: {self.user.name}')

    @tasks.loop(minutes=UPDATE_INTERVAL_MINUTES)
    async def check_exchange_rate(self):
        channel = self.get_channel(CHANNEL_ID)
        try:
            ticker = yf.Ticker("EURHUF=X")
            data = ticker.fast_info

            time = dt.datetime.now()
            TimeFormat = time.strftime("%Y.%m.%d %H:%M:%S")
            current_price = round(data.last_price, 2)

            color = discord.Color.blue()
            change_text = "Nincs adat az előző mérés óta."

            if self.prev_price is not None:
                diff = current_price - self.prev_price
                if diff > 0:
                    color = discord.Color.red()
                    change_text = f"Emelkedett: +{round(diff, 2)} Ft"
                elif diff < 0:
                    color = discord.Color.green()
                    change_text = f"Csökkent: {round(diff, 2)} Ft"
                else:
                    change_text = "Nem változott."

            embed = discord.Embed(title="Euro/Forint Árfolyam", color=color)
            embed.add_field(name="Jelenlegi ár", value=f"**{current_price} HUF**", inline=False)
            embed.add_field(name="Változás", value=change_text, inline=False)
            embed.set_footer(text=f"{TimeFormat}")

            await channel.send(embed=embed)
            
            self.prev_price = current_price

        except Exception as e:
            print(f"Hiba történt: {e}")

intents = discord.Intents.default()
client = EuroBot(intents=intents)
client.run(TOKEN)