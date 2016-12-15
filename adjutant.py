# Required modules for bot to run
from random import randint
import discord
import asyncio
import logging
from discord.ext import commands
import re
import string
from math import trunc
from credentials import token

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

# Quick rolling of 40KRPG tests.
@bot.command(pass_context=True)
async def dhroll(ctx, roll : str):
    """"Rolls a d100 using a # to set a success threshold.
    e.g !dhroll 50"""

    isRollSuccess = False
    resultTotal = 0
    resultString = ''
    
    try:
        try:
            successThreshold = int(roll)
        except Exception as e:
            print (e)
            await bot.say("Value must be an integer.")
            return

        if successThreshold < 1:
            await bot.say("Value must be greater than 1.")

        bot.type()
        await bot.say("Rolling 1d100 with a target number of %s for %s." % (successThreshold, ctx.message.author.name))

        number = randint(1, 100)
        if number < successThreshold:
            isRollSuccess = True
            resultTotal = (trunc(((successThreshold - number) / 10)) + 1)
            resultString += str(resultTotal)
        else:
            resultTotal = (trunc(((number - successThreshold) / 10)) + 1)
            resultString += str(resultTotal)

        if isRollSuccess:
            if resultTotal == 1:
                await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + str(number) + "\n**Succeeded by " + resultString + " degree.**")
            else:
                await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + str(number) + "\n**Succeeded by " + resultString + " degrees.**")
        else:
            if resultTotal == 1:
                await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + str(number) + "\n**Failed by " + resultString + " degree.**")
            else:
                await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + str(number) + "\n**Failed by " + resultString + " degrees.**")
                
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
        await bot.say("Format has to be in #d#t#,  %s." % ctx.message.author.name)
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
                await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString + "\n**Hits: " + str(numberSuccesses) + '**' + "  **Glitch!**")
        else:
            await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString + "\n**Hits: " + str(numberSuccesses) + '**')
        

    except Exception as e:
        print(e)
        return

# Allows rolling of a Chronicles of Darkness dice-pool, with exploding dice.
#Allows dice rolling functionality.
@bot.command(pass_context=True)
async def codroll(ctx, roll : str):
    """Rolls a dice using #d# format.
    e.g !roll 3d6"""
    
    resultTotal = 0
    resultString = ''
    numberSuccesses = 0

    try:
        try: 
            numDice = roll.split('d')[0]
            diceVal = 10
            explodeThreshold = roll.split('d')[1]
        except Exception as e:
            print(e)
            await bot.say("Format has to be in #d# %s." % ctx.message.author.name)
            return

        if int(numDice) > 500:
            await bot.say("I can\'t roll that many dice, %s." % ctx.message.author.name)
            return
        
        bot.type()
        await bot.say("Rolling %s d%s for %s" % (numDice, diceVal, ctx.message.author.name))
        rolls, explodeThreshold = map(int, roll.split('d'))

        for r in range(rolls):
            number = randint(1, diceVal)
            if number >= 7:
                numberSuccesses += 1

            if number >= explodeThreshold:
                number
            
            if resultString == '':
                resultString += str(number)
            else:
                resultString += ', ' + str(number)
        
        await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString)

    except Exception as e:
        print(e)
        return    
        

#Logs the bot in to Discord.
bot.run(token)
