# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import re
import sys
import time

import discord
from pubsub import pub
import meshtastic
import meshtastic.tcp_interface

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

with open("token.txt", "r") as f:
	token = f.read().strip()

# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
bot = discord.Client(intents=intents)

node_ip = "192.168.86.24"

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
	# CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
	guild_count = 0

	# LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
	for guild in bot.guilds:
		# PRINT THE SERVER'S ID AND NAME.
		print(f"- {guild.id} (name: {guild.name})")

		# INCREMENTS THE GUILD COUNTER.
		guild_count = guild_count + 1

	# PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
	print("Meshtastic Discord Bot is in " + str(guild_count) + " guilds.")

# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	# CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
	if bot.user.mentioned_in(message):
		msg_content = message.clean_content.replace("@Meshtastic Publisher", "").strip()
		msg = f"{message.author.display_name}@Discord: \"" + msg_content + "\""

		try:
			iface = meshtastic.tcp_interface.TCPInterface(hostname=node_ip)
		except Exception as ex:
			print(f"Error: Could not connect to {node_ip} {ex}")
			await message.channel.send(f"Failed to send message via SLAM node.")

		time.sleep(1)
		iface.sendText(msg)
		iface.close()

		discord_msg = f"Sent message \"{msg_content}\" over mesh via SLAM."
		print(discord_msg)
		await message.channel.send(discord_msg)

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(token)
