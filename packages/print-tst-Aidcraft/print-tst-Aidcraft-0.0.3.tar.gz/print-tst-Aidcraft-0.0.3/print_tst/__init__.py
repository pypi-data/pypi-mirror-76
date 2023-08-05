import discord

def message(channel_id, message, token):
  client = commands.Bot(command_prefix="ac.", owner_ids=[609522313150332962, 369686253769195520, 486844421120327681])
  @client.event
  async def on_ready():
    await client.get_channel(channel_id).send(message)
    await client.close()
  client.run(token)
    
  