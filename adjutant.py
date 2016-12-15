# Required modules for bot to run
from random import randint
import discord
import asyncio
import logging
from discord.ext import commands
import re
import string

# Sets up writing to a local log file.
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='!')

# Notifies the channel when the bot is ready to receive commands.
@bot.event
async def on_ready():
    await bot.send_message(discord.Object(id='252701845187854339'), 'Adjutant online. Awaiting orders, commander.')

#Allows dice rolling functionality.
@bot.command(pass_context=True)
async def roll(ctx, roll : str):
    """Rolls a dice using #d# format.
    e.g !roll 3d6"""
    
    resultTotal = 0
    resultString = ''
    try:
        try: 
            numDice = roll.split('d')[0]
            diceVal = roll.split('d')[1]
        except Exception as e:
            print(e)
            await bot.say("Format has to be in #d# %s." % ctx.message.author.name)
            return

        if int(numDice) > 500:
            await bot.say("I can\'t roll that many dice, %s." % ctx.message.author.name)
            return
        
        bot.type()
        await bot.say("Rolling %s d%s for %s" % (numDice, diceVal, ctx.message.author.name))
        rolls, limit = map(int, roll.split('d'))

        for r in range(rolls):
            number = randint(1, limit)
            resultTotal = resultTotal + number
            
            if resultString == '':
                resultString += str(number)
            else:
                resultString += ', ' + str(number)
        
        if numDice == '1':
            await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString)
        else:
            await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString + "\n**Total:** " + str(resultTotal))

    except Exception as e:
        print(e)
        return

# Checks if the roll result meets a set threshold.
@bot.command(pass_context=True)
async def rollt(ctx, roll : str):
    """Rolls dice using #d#s# format with a set success threshold, Where s is the thresold type (< = >).
    e.g !rollt 3d10<55"""

    resultTotal = 0
    resultString = ''
    
    try: 
        valueList = re.split("(\d+)", roll)
        valueList = list(filter(None, valueList))

        diceCount = int(valueList[0])
        diceValue = int(valueList[2])
        thresholdSign = valueList[3]
        successThreshold = int(valueList[4])

    except Exception as e:
        print(e)
        await bot.say("Format has to be in #d#t# %s." % ctx.message.author.name)
        return
    
    if int(diceCount) > 500:
        await bot.say("I can\'t roll that many dice, %s." % ctx.message.author.name)
        return

    bot.type()
    await bot.say("Rolling %s d%s for %s with a success threshold of %s %s" % (diceCount, diceValue, ctx.message.author.name, thresholdSign, successThreshold))

    try:
        for r in range(0, diceCount):

            number = randint(1, diceValue)
            isRollSuccess = False
            resultTotal += number
            
            if thresholdSign == '<':
                if resultTotal < successThreshold:
                    isRollSuccess = True

            elif thresholdSign == '=':
                if resultTotal == successThreshold:
                    isRollSuccess = True

            elif thresholdSign == '>':
                if resultTotal > successThreshold:
                    isRollSuccess = True

            if resultString == '':
                resultString += str(number)
            else:
                resultString += ', ' + str(number)

        if isRollSuccess == True:
            await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString + "\n**Total: **" + str(resultTotal) + "  **Success!**" )
        else:
            await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString + "\n**Total: **" + str(resultTotal) + "  **Failure!**" )
        
    except Exception as e:
        print(e)
        return

# Rolls a set number of d6s and counts the number of hits according to Shadowrun rules. Includes glitch detection.
@bot.command(pass_context=True)
async def srroll(ctx, roll : str):

    numberSuccesses = 0
    numberGlitches = 0
    resultString = ''

    try:
        diceCount = int(roll)

    except Exception as e:
        print(e)
        await bot.say("Dice value must be an integer, %s." % ctx.message.author.name)
        return

    if int(diceCount) > 500:
        await bot.say("I can't roll that many dice, %s." % ctx.message.author.name)
        return

    bot.type()
    await bot.say("Rolling %s d6 for %s." % (diceCount, ctx.message.author.name))

    try:
        for r in range(0, diceCount):
            number = randint(1, 6)
            isRollSuccess = False
            isRollGlitch = False

            if number >= 5:
                numberSuccesses += 1
                isRollSuccess = True
            elif number == 1:
                numberGlitches += 1
                isRollGlitch = True

            if resultString == '':
                if isRollSuccess:
                    resultString += '**' + str(number) + '**'
                elif isRollGlitch:
                    resultString += '*' + str(number) + '*'
                else: resultString += str(number)
            else:
                if isRollSuccess:
                    resultString += ', ' + '**' + str(number) + '**'
                elif isRollGlitch:
                    resultString += ', ' + '*' + str(number) + '*'
                else:
                    resultString += ', ' + str(number)

            isRollSuccess = False
            isRollGlitch = False

        if numberGlitches > (diceCount / 2):
            if numberSuccesses == 0:
                await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString + "\n***CRITICAL GLITCH!***")
            else:
                await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString + "\n**Hits: **" + str(numberSuccesses) + "  **Glitch!**")
        else:
            await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString + "\n**Hits: **" + str(numberSuccesses))
        

    except Exception as e:
        print(e)
        return

#Logs the bot in to Discord.
bot.run('bot-token')
