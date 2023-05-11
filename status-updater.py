# Web Requests
import requests

# Disord message base64 module
import discord_message_gen

# To prevent spam, and handling ratelimitting
from time import sleep

# Constants

# Change your directory! This just happened to be where I put the file(s)!
directory = "/home/penguin/Desktop/discord-password/SHENANIGANS!/"

# Token
with open(directory + "token2", "r") as f:
    token = f.read().replace("\n", "")

# print() becomes silenced
quiet = False
if quiet:
    print = lambda *args: None

# Appear online, idle, or dnd.
presence_choice = input("online/idle/dnd/auto[blank]\n")


def acquire_presence():
    global presence_choice
    if presence_choice in ["", "auto"]:
        returned_settings = requests.get(
            "https://discord.com/api/v9/users/@me/settings",
            headers={"Authorization": token},
        ).json()["status"]
        return returned_settings
    else:
        print("Always appearing {}".format(presence_choice))
        return presence_choice


while True:
    # re-read the file after going through the entire list. To update if the file changed.

    # Place a file containing messages
    with open(directory + "donated-comments") as f:
        messages = [line.rstrip() for line in f]
    # Place a file containing emojis, or name of emojis.
    with open(directory + "/donated-emoji") as f:
        emojis = [line.strip("\n") for line in f]

    # Examples:
    # [["custom", [2]]] # 2 seconds from time of PATCH to expiry
    # [["custom" [2023, 05, 11, 03, 14, 15, 09]]] # expires at a specific time!
    # [["hour", None]] # will expire 1 hour from time of patch. Second item set to None.
    # [["four hours", None]] # four hours expiry
    time = [["four hours", None] for _ in range(len(messages))]

    for message, emoji, expiry in zip(messages, emojis, time):
        # Required headers
        headers = {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en-US",
            "authorization": token,
            "content-type": "application/json",
            "x-discord-locale": "en-US",
        }

        # Forming message body to send
        output = discord_message_gen.message_generate(
            message, emoji, acquire_presence(), *expiry
        )
        json_data = {"settings": output}

        # Make the request
        response = requests.patch(
            "https://discord.com/api/v9/users/@me/settings-proto/1",
            headers=headers,
            json=json_data,
        )

        # Check if failed due to ratelimit
        # If it failed, wait the amount of time needed (plus 1 second to be safe)
        if "retry_after" in response.json().keys():
            retry_after = int(response.json()["retry_after"])
            print(
                "We are being ratelimitted. Retrying! Waiting %d seconds! %s %s"
                % (
                    retry_after + 1,
                    response,
                    output,
                )
            )
            # Wait out the ratelimit.
            sleep(1 + retry_after)

            # Make a new response after waiting.
            response = requests.patch(
                "https://discord.com/api/v9/users/@me/settings-proto/1",
                headers=headers,
                json=json_data,
            )
            # Success
            print(response, output)
        else:
            print(response, output)

        # Change sleep() if you have a specific expiry and update (let's say you wanted a switch every hour.)
        # Ideas: You can have the hands of a clock change every hour or so.
        sleep(8)
