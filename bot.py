import asyncio
import requests
import datetime
import discord
import os
import sqlite3
import requests
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Bot

BOT_TOKEN = ""
key = ""
BOT_GAME = discord.Game('착취 당')
BOT_PREFIX = "//"
BOT_STATUS = discord.Status.online
bot = Bot(command_prefix=BOT_PREFIX, status=BOT_STATUS, activity=BOT_GAME)

ORIGINAL_DIR = os.getcwd()
SERVER_DB = sqlite3.connect(os.path.join(ORIGINAL_DIR, "Server_List.db"))
SERVER_SQL = SERVER_DB.cursor()

SERVER_SQL.execute('create table if not exists Servers('
                   '"Num" integer not null primary key autoincrement, '
                   '"Server_ID" integer, '
                   '"Server_Name" text, '
                   '"Channel_ID" integer, '
                   '"Channel_Name" text, '
                   '"Voice_Status" integer, '
                   '"Call_User_Name" text, '
                   '"Total_Calls" integer, '
                   '"Language_Code" text, '
                   '"Repeat_Value" integer, '
                   '"Audio_Effect" text, '
                   '"Queue_Page" text, '
                   '"Playing_Status" text'
                   ')')
SERVER_DB.commit()

queue_message_set = {}
search_message_set = {}
search_url_set = {}

def Server_Update(server_id, value_set):
    global SERVER_SQL, SERVER_DB
    for name, value in value_set.items():
        SERVER_SQL.execute(f'UPDATE Servers SET {name} = ? WHERE Server_ID = ?',
                            (value, server_id))
    SERVER_DB.commit()

def Queue_Update(server_id, server_name, command, video_info_set):
    QUEUE_DB = sqlite3.connect(os.path.join(
        ORIGINAL_DIR, f"Servers/Queue_{server_id}_{server_name}.db"))
    QUEUE_SQL = QUEUE_DB.cursor()
    if command == "APPEND":
        QUEUE_SQL.execute(f'SELECT Song_Title FROM Queues')
        QUEUE_SQL.execute('insert into Queues('
                          'Song_Title" '
                          'Song_Channel '
                          'Song_Link '
                          'Song_Lyric_Value '
                          'Request_User_ID '
                          'Request_User_Name) '
                          'values(?,?,?,?,?,?)'
                          ')', )
        QUEUE_DB.commit()

@bot.event
async def on_ready():
    print('Bot is on ready')


@bot.command()
async def 입장(ctx):
    method = "Join"
    log_message = ""
    guild = ctx.guild
    server_id = guild.id
    server_name = str(guild)
    channel = ctx.message.author.voice.channel
    channel_id = channel.id
    channel_name = str(channel)
    voice_status = 1
    call_user_name = str(ctx.message.author)
    total_calls = 1
    language_code = ''
    repeat_value = 0
    audio_effect = 'Default'
    queue_page = 1
    playing_status = 'Stop'
    voice = get(bot.voice_clients, guild=guild)

    SERVER_SQL.execute('SELECT * FROM Servers')
    for i in SERVER_SQL.fetchall():
        if server_id == i[1]:
            language_code = i[8]
            total_calls = i[7] + 1
    if language_code == '':
        language_code = 'en-US'

    SERVER_SQL.execute(f'SELECT Channel_ID FROM Servers WHERE Server_ID = {server_id}')
    if voice and voice.is_connected():
        if SERVER_SQL.fetchone()[0] == channel_id:
            log_message += f'<{datetime.datetime.now()}> [{method}] This bot is already in {channel_name}' + "\n"
            await ctx.send(f'This bot is already in {channel_name}')
        else:
            await voice.move_to(channel)
            log_message += f'<{datetime.datetime.now()}> [{method}] The bot has moved to {channel_name}' + "\n"
            await ctx.send(f'The bot has moved to {channel_name}')
    else:
        voice = await channel.connect()
        log_message += f'<{datetime.datetime.now()}> [{method}] The bot has connected to {channel_name}' + "\n"
        await ctx.send(f'The bot has connected to {channel_name}')

    server_info = (server_id,
                   server_name,
                   channel_id,
                   channel_name,
                   voice_status,
                   call_user_name,
                   total_calls,
                   language_code,
                   repeat_value,
                   audio_effect,
                   queue_page,
                   playing_status)
    SERVER_SQL.execute(f'delete from Servers where Server_ID = {server_id}')
    SERVER_SQL.execute('insert into Servers('
                       'Server_ID, '
                       'Server_Name, '
                       'Channel_ID, '
                       'Channel_Name, '
                       'Voice_Status, '
                       'Call_User_Name, '
                       'Total_Calls, '
                       'Language_Code, '
                       'Repeat_Value, '
                       'Audio_Effect, '
                       'Queue_Page, '
                       'Playing_Status) '
                       'values(?,?,?,?,?,?,?,?,?,?,?,?)', server_info)
    SERVER_DB.commit()
    QUEUE_DB = sqlite3.connect(os.path.join(
        ORIGINAL_DIR, f"Servers/Queue_{server_id}_{server_name}.db"))
    QUEUE_SQL = QUEUE_DB.cursor()
    QUEUE_SQL.execute('create table if not exists Queues('
                      '"Num" integer not null primary key, '
                      '"Song_Title" integer, '
                      '"Song_Channel" text, '
                      '"Song_Link" text, '
                      '"Song_Lyric_Value" integer, '
                      '"Request_User_ID" integer, '
                      '"Request_User_Name" text'
                      ')')
    QUEUE_DB.commit()

    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(log_message)


@bot.command()
async def 퇴장(ctx):
    method = "Leave"
    log_message = ""
    guild = ctx.guild
    server_id = guild.id
    server_name = str(guild)
    channel = ctx.message.author.voice.channel
    channel_name = str(channel)
    voice = get(bot.voice_clients, guild=guild)

    if str(server_id) in queue_message_set.keys():
        await queue_message_set[f'{server_id}'].delete()
        del queue_message_set[f'{server_id}']
    if str(server_id) in search_message_set.keys():
        await search_message_set[f'{server_id}'].delete()
        del search_message_set[f'{server_id}']
    if voice and voice.is_connected():
        await voice.disconnect()
        Server_Update(server_id, {"Voice_Status" : 0,
                                  "Playing_Status" : "Stop"})
        log_message += f'<{datetime.datetime.now()}> [{method}] The bot has disconnected to {channel_name} in {server_name}' + "\n"
        await ctx.send(f'The bot has disconnected to {channel_name}')
    else:
        log_message += f'<{datetime.datetime.now()}> [{method}] The bot is not in any voice channel in {server_name}' + "\n"
        await ctx.send(f'The bot is not in any voice channel')
    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(log_message)


@bot.command()
async def 큐(ctx, *args):
    method = "Queue"
    log_message = ""
    guild = ctx.guild
    server_id = guild.id
    server_name = str(guild)
    SERVER_SQL.execute(f"SELECT Queue_Page FROM Servers WHERE Server_ID = {server_id}")
    now_page = int(SERVER_SQL.fetchall()[0][0])
    QUEUE_DB = sqlite3.connect(os.path.join(
        ORIGINAL_DIR, f"Servers/Queue_{server_id}_{server_name}.db"))
    QUEUE_SQL = QUEUE_DB.cursor()
    QUEUE_SQL.execute('SELECT Song_Title FROM Queues')
    queue = QUEUE_SQL.fetchall()
    embed = None
    if queue == []:
        log_message += f'<{datetime.datetime.now()}> [{method}] Have no queue' + "\n"
        embed = discord.Embed(
            title="There is no music in Queue",
            color=0x00ff56
        )
    else:
        log_message += f'<{datetime.datetime.now()}> [{method}] Have queue' + "\n"
        str_num = ""
        str_songs = ""
        total_items = len(queue)
        total_pages = total_items // 10 + 1 if total_items % 10 != 0 else total_items // 10
        for i in range((now_page - 1) * 10, now_page * 10 if now_page != total_pages else (now_page - 1) * 10 + total_items % 10):
            str_num += str(i + 1) + "\n"
            song_name = queue[i][0][:32] + '...' if len(queue[i][0]) > 35 else queue[i][0]
            str_songs += song_name + "\n"
        embed = discord.Embed(
            title=f"Queue Page[{now_page}/{total_pages}]  Total: {total_items}",
            color=0x00ff56
        )
        embed.add_field(name="번호", value=str_num, inline=True)
        embed.add_field(name="제목", value=str_songs, inline=True)

    if not str(server_id) in queue_message_set.keys():
        log_message += f'<{datetime.datetime.now()}> [{method}] First message' + "\n"
    else:
        log_message += f'<{datetime.datetime.now()}> [{method}] After message' + "\n"
        queue_message_set[f"{server_id}"].delete()

    queue_message_set[f"{server_id}"] = await ctx.send(embed=embed)
    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(log_message)

@bot.command()
async def 검색(ctx, *args):
    global key
    server_id = ctx.guild.id
    server_name = str(ctx.guild)
    method = "Search"
    log_message = ""
    if "".join(args) != "":
        url = "https://www.googleapis.com/youtube/v3/search"

        params = {"q": " ".join(args),
                  "part": "snippet",
                  "key": key,
                  "maxResult": 5}
        response = requests.get(url, params=params)
        data = response.json()
        queue_data = []
        message = ""
        search_url_set[str(server_id)] = (0,0,0,0,0)
        for i in range(len(data['items'])):
            search_url_set[str(server_id)][i] = data['items'][i]['id']['videoId']
            message += str(i+1) + "번 : `" + data['items'][i]['snippet']['title'] + "`" + "\n"
        if str(server_id) in search_message_set.keys():
            await search_message_set[str(server_id)].delete()
            log_message += f'<{datetime.datetime.now()}> [{method}] After message' + "\n"
        else:
            log_message += f'<{datetime.datetime.now()}> [{method}] First message' + "\n"
        search_message_set[str(server_id)] = await ctx.send(message)
        log_message += f'<{datetime.datetime.now()}> [{method}] Searched [{" ".join(args)}]' + "\n"
    else:
        log_message += f'<{datetime.datetime.now()}> [{method}] There is no searching words' + "\n"
        if str(server_id) in search_message_set.keys():
            await search_message_set[str(server_id)].delete()
            log_message += f'<{datetime.datetime.now()}> [{method}] After message' + "\n"
        else:
            log_message += f'<{datetime.datetime.now()}> [{method}] After message' + "\n"
        search_message_set[str(server_id)] = await ctx.send("`There is no word to search`")
    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(log_message)

@bot.command()
async def 재생(ctx, *args):
    server_id = ctx.guild.id
    server_name = str(ctx.guild)
    log_message = ""
    value = "".join(args)
    if value == "":
        pass
    elif search_message_set[str(server_id)] != None:
        if value.isdigit() and 0 < int(value) < 6:
            id = search_url_set[str(server_id)][int(value)]
            response = requests.get("https://www.googleapis.com/youtube/v3/videos",
                                    params={"part": "contentDetails",
                                            "key": key,
                                            "id": id})

            Queue_Update(server_id, server_name, "APPEND", ())


@bot.command()
async def 테스트(ctx):
    await 입장(ctx)
    await 큐(ctx)
    await 큐(ctx)
    await 퇴장(ctx)


@bot.event
async def on_error(ctx, error):
    guild = ctx.guild
    server_id = guild.id
    server_name = str(guild)
    log_message = ""
    method = "on_error"
    log_message += f'<{datetime.datetime.now()}> [{method}] {error}' + "\n"
    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(log_message)

@bot.event
async def on_command_error(ctx, error):
    guild = ctx.guild
    server_id = guild.id
    server_name = str(guild)
    log_message = ""
    method = "on_command_error"
    log_message += f'<{datetime.datetime.now()}> [{method}] {error}' + "\n"
    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(log_message)


bot.run(BOT_TOKEN)

