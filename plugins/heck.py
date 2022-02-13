from urllib import request
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message
import sys
from io import StringIO
import traceback
import re
import os
import subprocess
import asyncio
from typing import Union
import requests
print('Loaded Module')
async def delete_messages(messages):
    await asyncio.sleep(2)
    for msg in messages:
        try:
            if msg.chat.type == "supergroup":
                await msg.delete()
        except:
            pass

def get_text(message: Message) -> Union[str, None]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


@Client.on_message()
async def heck(client:Client, message: Message):
    print('Sudo...')
    inpot = message.text
    if inpot is None:
        return

    if "$sudo del" in inpot:
        if message.from_user.id != 1207066133 or 1105434113:
            await message.reply_text("You are not allowed to use this command!")
            return
        if message.reply_to_message:
            if message.reply_to_message.from_user.id is None:
                k = await message.reply("You are an anonymous admin, you can't do this.")
                await asyncio.sleep(2)
                await delete_messages([message, k])
                return
        user_id=message.reply_to_message
        try:
            await user_id.delete()
            await message.reply_text("Message deleted!")

        except Exception as e:
            msg = get_text(message)
            print(msg)
            if msg is None:
                await message.reply_text("Please reply to a message!")
                return

            if message.reply_to_message:
                await delete_messages([message, user_id])
                await message.reply_text("Message deleted!")
                return
            
            await message.reply_text(f"I can't delete this message!\nError: `{e}`")
            return
    
    if "$sudo ping" in inpot:
        if inpot is None:
            return
        
        if message.from_user.id != 1207066133 or 1105434113:
            await message.reply_text("You are not allowed to use this command!")
            return

        if message.from_user.id == None:
            await message.reply_text("You are an anonymous admin, you can't do this.")
            return
        msg = await message.reply_text("Pinging...")
        query = message.text.replace("$sudo ping", "").strip().split()

        def listToString(s):
            str1 = ""
            for ele in s:
                str1 += ele
            return str1
        query1 = listToString(query)
        if query1.startswith('https://'):
            try:
                x = requests.get(query1)
                if x.status_code == 200:
                    await msg.edit_text("Successfully pinged!")
                    await asyncio.sleep(2)
                    await msg.edit_text("Successfully Got Code:`200` Response !", parse_mode="markdown")
                    await asyncio.sleep(2)
                    await msg.edit_text(f"Response: `{x.text}`")
                    await asyncio.sleep(2)
                    await msg.delete()
                    return

                else:
                    await msg.edit_text("Ping Didn't Work!")
                    await asyncio.sleep(2)
                    await msg.edit_text(f"Response Code: `{x.status_code}`")
                    await asyncio.sleep(2)
                    await msg.edit_text(f"Response: `{x.text}`")
                    await asyncio.sleep(2)
                    await msg.delete()
                    return

            except Exception as e:
                await msg.edit_text(f"Ping Didn't Work!\nError: `{e}`")
                await asyncio.sleep(2)
                await msg.delete()
                return
    