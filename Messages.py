import pickle

Messages_en = {
    "Join_first": "The bot has connected to __channel_name__ in __server_name__",
    "Join_overlap": "The bot already in this channel, __channel_name__",
    "Join_move": "The bot has moved to __channel_name__ in __server_name__",
    "Leave_normal": "The bot has disconnected to channel, __channel_name__ in server, __server_name__",
    "Leave_abnormal": "The bot is not in any voice channel in server, __server_name__"
}

for i, j in Messages_en.items():
    print(i,':',j)
