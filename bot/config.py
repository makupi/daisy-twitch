import json


with open("twitch.json") as config_file:
    twitch_config = json.load(config_file)

with open("channels.json") as channels_file:
    tmp = json.load(channels_file)
    channels = tmp.get("channels")

irc_token = twitch_config.get("irc_token", "")
api_token = twitch_config.get("api_token", "")
nick = twitch_config.get("nick", "")
prefix = twitch_config.get("prefix", ";")
nookipedia_key = twitch_config.get("nookipedia", "")

def save_channels():
    with open("channels.json", "w") as channels_file:
        json.dump({"channels": list(dict.fromkeys(channels))}, channels_file)