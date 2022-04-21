import os
import re
from typing import List, Optional
import dnnlib
import numpy as np
import PIL.Image
import torch
import legacy
from discord.ext import commands
import discord
import random
import time
from dotenv import load_dotenv
import bz2
import pickle
import _pickle as cPickle



#token
load_dotenv('.env')



#pkl decompression
def decompress_pickle(file):
 data = bz2.BZ2File(file, ‘rb’)
 data = cPickle.load(data)
 return data

def generate_images(network_pkl: str, seeds: Optional[List[int]], outdir: str) :
  print('Loading networks from "%s"...' % network_pkl)
  device = torch.device('cuda')
  with dnnlib.util.open_url(network_pkl,'rb') as f :
    G = legacy.load_network_pkl(f)['G_ema'].to(device)  # type: ignore

  os.makedirs(outdir, exist_ok=True)

  if seeds is None :
    print('Error: seeds argument is required')

  # Labels.
  label = torch.zeros([1, G.c_dim], device=device)

  # Generate images.
  for seed_idx, seed in enumerate(seeds) :
    print('Generating image for seed %d (%d/%d) ...' % (seed, seed_idx, len(seeds)))
    z = torch.from_numpy(np.random.RandomState(seed).randn(1, G.z_dim)).to(device)
    img = G(z, label)
    img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
    PIL.Image.fromarray(img[0].cpu().numpy(), 'RGB').save(f'{outdir}/seed{seed:04d}.png')



print('Starting bot...')

# client = discord.Client()
bot = commands.Bot(command_prefix='!')

cursed_seeds = [1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 15, 16, 18, 19, 26, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40,
                42, 43, 45, 46, 51, 52, 53, 54, 55, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 70, 71, 73, 75, 76, 77, 78,
                80, 81, 82, 84, 85, 86, 87, 89, 90, 91, 92, 93, 94, 96, 97, 98, 99, 100, 102, 103, 104, 105, 106, 108,
                109, 110, 112, 113, 114, 115, 118, 119, 120, 121, 122, 124, 125, 127, 128, 129, 130, 131, 132, 135, 137,
                138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158,
                159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179,
                180, 181, 182, 183, 184, 186, 187, 188, 189, 190, 191, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202,
                203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 216, 217, 218, 219, 220, 221, 222, 223, 224,
                225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 245, 246,
                247, 248, 249, 253, 254, 255, 256, 258, 259, 260, 262, 263, 264, 265, 267, 269, 270, 271, 272, 273, 275,
                276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296,
                297, 298, 299, 300, 301, 302, 304, 307, 309, 311, 312, 313, 314, 315, 316, 318, 319, 320, 321, 323, 324,
                325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 344, 346, 347,
                349, 350, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 370, 371, 373,
                374, 375, 376, 377, 378, 379, 381, 382, 383, 385, 386, 387, 388, 390, 391, 392, 393, 394, 396, 397, 398,
                399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419,
                420, 421, 422, 423, 424, 425, 426, 427, 428, 430, 431, 432, 433, 434, 436, 437, 438, 439, 440, 441, 442,
                443, 444, 445, 446, 447, 449, 450, 452, 454, 455, 456, 458, 459, 460, 462, 463, 464, 465, 466, 471, 472,
                473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 487, 488, 489, 490, 491, 492, 493, 494,
                495, 496, 497, 498, 499
                ]
good_seeds = [0,3,9,13,14,17,20,21,22,23,24,25,32,41,44,47,48,49,50,56,57,58,69,
72,74,79,83,88,95,101,107,111,116,117,123,126,133,134,136,185,192,215,244,
250,251,252,257,261,266,268,274,303,305,306,308,310,317,322,343,345,348,351,
368,369,372,380,384,389,395,429,435,448,451,453,457,461,467,468,469,470,486
              ]
seed = 'None'

memes = []

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

path1 = os.getcwd() + '/Memes'

listing = os.listdir(path1)
for file in listing:
  path = path1 + '\\' + file
  memes.append(path)


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

joke_Keys = list(jokes.keys())

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
        seed = [random.choice(good_seeds)]
      elif args[1].lower() in ['cursed','bad','weird']:
        seed = [random.choice(cursed_seeds)]
      elif args[1][0:5].lower() == 'seed=':
        seed = [int(args[1][5:])]
      else:
        await ctx.send('Error: That argument does not work')
        return
    else:
      seed = [random.randint(500, 1000)]
    await ctx.send("Generating image...")
    outdir = os.getcwd() + "/out"
    network_path = "https://drive.google.com/file/d/10Wuzo69P5Um-ZxePbCJByK0V3-N9YSIe/view?usp=sharing"
    # generating the image
    generate_images(network_pkl=network_path, seeds=seed, outdir=outdir)
    # get the path of your image
    image_path = f'{outdir}/seed{seed[0]:04d}.png'
    with open(image_path, 'rb') as f :
      picture = discord.File(f)
      await ctx.send(file=picture)

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


bot.run(os.getenv('HUSKY_BOT_TOKEN'))

