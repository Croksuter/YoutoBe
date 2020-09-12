import asyncio
import discord
import os
import sqlite3
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Bot

BOT_TOKEN = "NzQ2MDA0Mjg3NTIzNjUxNzQ0.Xz6Aog.WRMKU4a3PcLYwHCabobM5itI07k"
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

def Get_server_values(ctx):
    server_id = ctx.guild.id
    SERVER_SQL.execute('SELECT * FROM Servers WHERE Server_ID = ?',
                       (server_id,))
    for i in SERVER_SQL.fetchall():
        if server_id == i[1]:
            return i



@bot.event
async def on_ready():
    print('Bot is on ready')


@bot.command(pass_context=True)
async def 입장(ctx):
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
    queue_message = 'OFF'
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

    SERVER_SQL.execute(f'SELECT Channel_ID FROM Servers WHERE Server_ID = {server_id}')
    if voice and voice.is_connected():
        if SERVER_SQL.fetchone()[0] == channel_id:
            print(f'[Join] This bot is already in {channel_name}')
            await ctx.send(f'This bot is already in {channel_name}')
        else:
            await voice.move_to(channel)
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

            print(f'The bot has moved to {channel_name} in {server_name}')
            await ctx.send(f'The bot has moved to {channel_name} in {server_name}')
    else:
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

        QUEUE_DB = sqlite3.connect(os.path.join(ORIGINAL_DIR, f"Servers/Queue_{server_id}_{server_name}.db"))
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

        voice = await channel.connect()
        print(f'The bot has connected to {channel_name} in {server_name}')
        await ctx.send(f'The bot has connected to {channel_name} in {server_name}')


@bot.command(pass_context=True)
async def 퇴장(ctx):
    guild = ctx.guild
    server_id = guild.id
    server_name = str(guild)
    channel = ctx.message.author.voice.channel
    channel_name = str(channel)
    voice = get(bot.voice_clients, guild=guild)
    if str(server_id) in queue_message_set.keys():
        del queue_message_set[f'{server_id}']
    if voice and voice.is_connected():
        await voice.disconnect()
        SERVER_SQL.execute('UPDATE Servers SET Voice_Status = ? WHERE Server_ID = ?',
                           (0, server_id))
        SERVER_DB.commit()
        print(f'The bot has disconnected to {channel_name} in {server_name}')
        await ctx.send(f'The bot has disconnected to {channel_name} in {server_name}')
    else:
        print(f'The bot is not in any voice channel in {server_name}')
        await ctx.send(f'The bot is not in any voice channel in {server_name}')


@bot.command()
async def 큐(ctx, *args):
    guild = ctx.guild
    server_id = guild.id
    server_name = str(guild)
    SERVER_SQL.execute(f"SELECT Queue_Page FROM Servers WHERE Server_ID = {server_id}")
    data = SERVER_SQL.fetchall()[0]
    now_page = int(data[0])
    QUEUE_DB = sqlite3.connect(os.path.join(
        ORIGINAL_DIR, f"Servers/Queue_{server_id}_{server_name}.db"))
    QUEUE_SQL = QUEUE_DB.cursor()
    QUEUE_SQL.execute('SELECT Song_Title FROM Queues')
    queue = QUEUE_SQL.fetchall()
    print(queue)
    if queue == []:
        embed = discord.Embed(
            title="There is no music in Queue",
            color=0x00ff56
        )
        await ctx.send(embed=embed)
    else:
        str_num = ""
        str_songs = ""
        total_items = len(queue)
        total_pages = total_items // 10 + 1 if total_items % 10 != 0 else total_items // 10
        for i in range((now_page - 1) * 10, now_page * 10 if now_page != total_pages else (now_page - 1) * 10 + total_items % 10):
            str_num += str(i + 1) + "\n"
            song_name = queue[i][0][:32] + '...' if len(queue[i][0]) > 35 else queue[i][0]
            str_songs += song_name + "\n"

        if str(server_id) not in queue_message_set.keys():
            print('server_id not in queueset')
            embed = discord.Embed(
                title=f"Queue Page[{now_page}/{total_pages}]  Total: {total_items}",
                color=0x00ff56
            )
            embed.add_field(name="번호", value=str_num, inline=True)
            embed.add_field(name="제목", value=str_songs, inline=True)
            queue_message_set[f"{server_id}"] = await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"Queue Page[{now_page}/{total_pages}]  Total: {total_items}",
                color=0x00ff56
            )
            embed.add_field(name="번호", value=str_num, inline=True)
            embed.add_field(name="제목", value=str_songs, inline=True)
            await queue_message_set[f"{server_id}"].delete()
            queue_message_set[f"{server_id}"] = await ctx.send(embed=embed)
        print(queue_message_set)


@bot.command()
async def 테스트(ctx):
    await 입장(ctx)
    await 큐(ctx)
    await 큐(ctx)
    await 퇴장(ctx)



bot.run(BOT_TOKEN)

