import disnake

from disnake.ext import commands

import settings
import urllib
import requests
import base64
import hashlib
import secrets

from shared_flow import print_auth_url


bot = commands.Bot(command_prefix=settings.prefix, help_command=None, intents=disnake.Intents.all(), test_guilds=[854627292821979136])



@bot.event #отображает в консоли, что бот готов к работе
async def on_ready():
	print(f"Bot {bot.user.name} готов к работе") 
	

@bot.event #сообщает в канал, что человек ушел с сервера 
async def on_member_remove(member): 
	channel = bot.get_channel(settings.channelid)
	await channel.send(embed = disnake.Embed(description = f'`{member}` покинул сервер', colour = disnake.Colour.red()))


@bot.event #приветсвенный текст в канал при входе новго участника
async def on_member_join(member):

	role_rec = member.guild.get_role(settings.role_rec)
	channel = bot.get_channel(settings.channelhi)
	await channel.send(f'{member.mention} привет, ищешь компанию в ире? Чтобы к нам присоедениться нужно познакомиться с нашим {role_rec.mention} в голосовом чате. Линкуй {role_rec.mention} и договаривайтесь на удобное время!')

random = base64.urlsafe_b64encode(secrets.token_bytes(32)) #создали 32 случайных байта  
m = hashlib.sha256()
m.update(random)
d = m.digest()
code_challenge = base64.urlsafe_b64encode(d).decode().replace("=", "")
#-------------------------------------------------------------------------
client_id = '01f2b79e34aa44ddaa90b934ed351d88' #айди апликейшена у ссп

@bot.slash_command(description='выводит ссылку авторизации в API') #команда, выводящая ссылку для авторизации в апи
async def auth(ctx):

	url = print_auth_url(client_id, code_challenge=code_challenge)

	class Auth_link_button(disnake.ui.View):
		def __init__(self):
			super().__init__(timeout=None)
			self.add_item(disnake.ui.Button(label='Тык для авторизации', url=url))

	view = Auth_link_button()
	channel = bot.get_channel(settings.channelid)
	await ctx.send('Пройдите авторизацию, после чего вас перебросит на новую страницу. Откройте строку с ссылкой и скопируйте значение после code=<букафки и циферки> до знака "&" \n**ПРИМЕР** То, что вам нужно скопировать выделено жирным: https: //localhost/callback/?code=**91PtE1eGnEKXF69AobLzpQ**&state=qwery',  view=view)


@bot.slash_command(description='Чтобы вставить ваш код для подтверждения авторизации') 
async def code(ctx, code): 
	 
	await ctx.send(f'Я запомнил ваш код: {code}')
	
bot.run(settings.token)


