# Sending shenanigans
import requests

# Custom module!
import discord_message_gen

# base 64 conversions
from base64 import b64encode, b64decode

# To prevent spam, and possible bans and/or ratelimitting
from time import sleep

# Token will be constant.
with open("/home/penguin/Desktop/discord-password/SHENANIGANS!/token2", "r") as f:
    token = f.read().replace("\n", "")

# Verbosity will be constant.
quiet = False
if quiet:
    print = lambda *args: None

presence_choice = input("online/idle/dnd/preserve[blank]\n")


def acquire_presence(presence_choice):
    if not presence_choice:
        returned_settings = repr(
            b64decode(
                requests.get(
                    "https://discord.com/api/v9/users/@me/settings-proto/1",
                    headers={"Authorization": token},
                ).json()["settings"]
            )
        )

        if r"\x06online\x12" in returned_settings:
            return "online"
        elif r"\x04idle\x12" in returned_settings:
            return "idle"
        elif r"\x03dnd\x12" in returned_settings:
            return "dnd"
    else:
        return presence_choice


while True:
    # re-read the file after going through the entire list.
    with open(
        "/home/penguin/Desktop/discord-password/SHENANIGANS!/donated-comments"
    ) as f:
        messages = [line.rstrip() for line in f]

    with open("/home/penguin/Desktop/discord-password/SHENANIGANS!/donated-emoji") as f:
        emojis = [line.strip("\n") for line in f]

    for message, emoji in zip(messages, emojis):
        headers = {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en-US",
            "authorization": token,
            "content-type": "application/json",
            "x-discord-locale": "en-US",
        }

        output = discord_message_gen.message_generate(
            message, emoji, acquire_presence(presence_choice)
        )

        json_data = {
            "settings": output,
        }

        response = requests.patch(
            "https://discord.com/api/v9/users/@me/settings-proto/1",
            headers=headers,
            json=json_data,
        )

        # Did it fail?
        failed = "retry_after" in response.json().keys()
        # It failed!
        while failed:
            failed = "retry_after" in response.json().keys()
            # It failed!
            if failed:
                # Wait the amount of time needed (plus 1 second to be safe)
                retry_after = int(response.json()["retry_after"])
                print(
                    "%s Waiting %d seconds! %s %s"
                    % (
                        "We are being ratelimitted. Retrying! ",
                        retry_after + 1,
                        response,
                        output,
                    )
                )
                sleep(1 + retry_after)

            # succeeded. Move on!
            else:
                break
            response = requests.patch(
                "https://discord.com/api/v9/users/@me/settings-proto/1",
                headers=headers,
                json=json_data,
            )
        else:
            print(response, output)
        sleep(8)
