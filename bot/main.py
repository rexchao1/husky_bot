import os
from discord.ext import commands
import discord
import random
import time


TOKEN = os.getenv("DISCORD_TOKEN")


# client = discord.Client()
bot = commands.Bot(command_prefix='!')


memes = []
path1 = os.getcwd() + '/bot/Memes'
listing = os.listdir(path1)
for file in listing:
  path = path1 + '/' + file
  memes.append(path)

good_huskies = []
path2 = os.getcwd() + '/bot/good_images'
listing2 = os.listdir(path2)
for file in listing2:
  path = path2 + '/' + file
  good_huskies.append(path)

bad_huskies = []
path3 = os.getcwd() + '/bot/bad_images'
listing3 = os.listdir(path3)
for file in listing3:
  path = path3 + '/' + file
  bad_huskies.append(path)

normal_huskies = []
path4 = os.getcwd() + '/bot/normal_images'
listing4 = os.listdir(path4)
for file in listing4:
  path = path4 + '/' + file
  normal_huskies.append(path)

jokes = {
  'What do you call a husky puppy who can’t stop eating?': 'A little husky',
  'How many Huskies does it take to change a light bulb?': 'My Husky: Light bulb?! I ate the light bulb. Oh, and the '
                                                           'lamp! …and the coffee table it sat on, and the carpet '
                                                           'under the coffee table and…',
  'What’s a corn farmer’s favorite type of dog?': 'A Husky (hint: corn grows on husks) (Sorry for being so corny :)',
  'What do you call a husky/pug mix?' : 'A Hug!',
  "I'm not saying my neighbor's dog is big" : "But she's more than a little husky.",
  'I used to have a border collie...' : "Then my parents fed him too much and he became husky.",
  "My wife slapped me when I told her I'm buying her a puppy for Christmas." : 'I thought she would be excited to hear that she is getting a little husky...',
  'There was a bamboo stalk and a corn stalk who lived in the same neighborhood. The bamboo sometimes said "Sup my HUSKY bro"': 'One day the corn turns around and yells at the bamboo, "STOP STALKING ME"'
}
joke_Keys = list(jokes.keys())


FunFacts = [
  'Siberian sled dogs were used by the U.S. Army during World War II for Arctic search and rescue of downed pilots and cargo',
  'Huskies gained fame in 1925 after Siberian Husky sled dogs heroically brought lifesaving serum to fight a diphtheria epidemic in Nome, Alaska',
  'Huskies are high-energy and extremely athletic, and they can be expert escape artists',
  'The husky is naturally clean, and the dense coat that protects him against cold weather does not require any clipping or trimming',
  'Huskies may be intimidating, they are very friendly',
  'A husky can have brown eyes, blue eyes, one of each, or even multi-colored eyes',
  'Huskys can touch a top speed of 50 mph',
  'There are 12 types of huskies'
]



@bot.command()
async def helpme(ctx):
  await ctx.send('The following commands can be used:')
  time.sleep(0.5)
  await ctx.send('!joke | !meme | !fact | !generate husky normal | !generate husky cursed | !lastseed')


@bot.command()
async def generate(ctx, *args):
  global seed
  if len(args) == 0:
    return
  if args[0].lower() == 'husky':
    if len(args) != 1:
      if args[1].lower() in ['normal','regular','good']:
        image = random.choice(good_huskies)
        await ctx.send(file=discord.File(image))
      elif args[1].lower() in ['cursed','bad','weird']:
        image = random.choice(bad_huskies)
        await ctx.send(file=discord.File(image))
      else:
        await ctx.send('Error: That argument does not work')
        return
    else:
      image = random.choice(normal_huskies)
      await ctx.send(file=discord.File(image))


@bot.command()
async def joke(ctx):
  question = random.choice(joke_Keys)
  punchline = jokes[question]
  await ctx.send(question)
  time.sleep(2)
  await ctx.send(punchline)

@bot.command()
async def lastseed(ctx):
  if seed == 'None':
    await ctx.send('Please use this function after a generate function.')
  await ctx.send(int(seed[0]))

@bot.command()
async def meme(ctx):
  meme = random.choice(memes)
  await ctx.send(file=discord.File(meme))

@bot.command()
async def fact(ctx):
  fact1 = random.choice(FunFacts)
  await ctx.send(fact1 + '!')

@bot.event
async def on_message(message):
  channel = message.channel
  user_message = message.content
  user = message.author.name
  if user == 'HuskyBot':
    return
  if user_message.lower() == 'hello':
    await channel.send('Hello, and good morning!')
  await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(TOKEN)


