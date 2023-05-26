# HTTP client to switch of requests
import http.client

# JSON read
from json import loads

# Disord message base64 module
import discord_message_gen

# To prevent spam, and handling ratelimitting
from time import sleep

# argparse for front-end
import argparse

# pathlib for file paths
import pathlib


# Argparse and arguments
# Formatting
class CustomFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        self._max_help_position = 50
        if not action.option_strings:
            (metavar,) = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            parts = []
            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                parts.extend(action.option_strings)

            # if the Optional takes a value, format is:
            #    -s ARGS, --long ARGS
            # change to
            #    -s, --long ARGS
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    # parts.append('%s %s' % (option_string, args_string))
                    parts.append("%s" % option_string)
                parts[-1] += " %s" % args_string
            return ", ".join(parts)


parser = argparse.ArgumentParser(
    prog="Discord Status Updater",
    description="This simple-to-use program will update your Discord Custom Status.",
    formatter_class=CustomFormatter,
)

# Arguments
parser.add_argument(
    "-t",
    "--token",
    metavar="TOKEN PATH",
    required=True,
    help="Path to token file.",
    type=pathlib.Path,
)
parser.add_argument(
    "-c",
    "--comments",
    metavar="COMMENTS PATH",
    required=True,
    help="Path to comments file.",
    type=pathlib.Path,
)
parser.add_argument(
    "-e",
    "--emoji",
    metavar="EMOJI PATH",
    required=False,
    help="Path to emoji file. (Must have same number of lines as comments file).",
    type=pathlib.Path,
)
parser.add_argument(
    "-s",
    "--status",
    choices=["online", "o", "idle", "i", "dnd", "d", "auto", "a"],
    required=True,
    help="Status option [(o)nline/(i)dle/(d)nd/(a)uto]",
)
parser.add_argument(
    "-d",
    "--delay",
    required=False,
    help="Set a manual delay for updating.",
    type=int
)
parser.add_argument(
    "-a",
    "--api",
    required=True,
    choices=["proto", "p", "default", "d", "both", "b"],
    help="Choose api option [(p)roto/(d)efault/(b)oth]",
    type=str,
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    required=False,
    help="Enable verbose output.",
)

# Convert arguments to dictionary
args = parser.parse_args().__dict__

# print() becomes silenced
if not (args["verbose"]):
    print = lambda *args: None

# Read token file
with open(args["token"]) as f:
    token = f.read().replace("\n", "")

# Place a file containing messages
with open(args["comments"]) as f:
    messages = [line.rstrip() for line in f]

# Place a file containing emojis, or name of emojis.
if args["emoji"]:
    with open(args["emoji"]) as f:
        emojis = [line.strip("\n") for line in f]
        emojis += ["" for _ in range(len(messages) - len(emojis))]
    print("Using emojis.")
else:
    emojis = ["" for _ in range(len(messages))]
    print("Not using emojis.")

# Variables
# Argument handlers
args["api"] = args["api"][0]
args["status"] = args["status"][0]

# Constant
status = {"o": "online", "i": "idle", "d": "dnd", "a": "auto"}

api = {"p": "protobuf", "d": "default", "b": "both"}

# Connections
conn = http.client.HTTPSConnection("discord.com")
headers = {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en-US",
            "authorization": token,
            "content-type": "application/json",
            "x-discord-locale": "en-US",
        }

print(
    "Switching to {} status indefinitely\nUsing {} api".format(
        status[args["status"]], api[args["api"]]
    )
)

# Helper functions
# PAYLOAD
def generate_payload(api, true_status, message, emoji):
    if api == 'p':
        return """{"settings":"%s"}"""%(
            discord_message_gen.protobuf_message_generate(true_status, message, emoji)
        )
    else:
        # "custom_status": {"text": "Hello from the other siiiiiiiiiide", "expires_at": null, "emoji_id": null, "emoji_name": null}
        return discord_message_gen.message_generate(true_status, message, emoji)

# STATUS
def get_status():
    if args["status"] == "a":
        conn = http.client.HTTPSConnection("discord.com")
        conn.request(
            "GET",
            "/api/v9/users/@me/settings",
            headers=headers
        )
        res = conn.getresponse()
        data = res.read()
        return loads(data.decode("utf-8"))["status"][0]
    else:
        return args["status"]

delay = args["delay"] if args["delay"] and args["delay"] >= 1 else 1
print(f"Delay is {delay} seconds")
while True:
    for message, emoji in zip(messages, emojis):

        # If automatic, use protobuf (usually).
        if args["api"] == 'b':
            payload = generate_payload('p', get_status(), message, emoji)
        else:
            payload = generate_payload(args["api"], get_status(), message, emoji)
            print("Payload Generated.")

        # Make a http connection towards protobuf (if not forced to default.)
        conn.request("PATCH", "/api/v9/users/@me/settings%s"%("-proto/1" if args["api"] != 'd' else ''), payload, headers)
        print(f"Sent: {payload}", sep='')

        res = conn.getresponse()
        data = res.read()

        decoded_data = loads(data.decode("utf-8"))
        print(f"Received: {res.status}, {decoded_data}")

        sleep(delay)

        # Rate limitted
        if "retry_after" in decoded_data.keys():
            print("Rate-limitted: ", end='')
            wait_time = decoded_data["retry_after"]
            if args["api"] == 'p':
                print(f"Locked on protobuf. Waiting {wait_time}. Resending {payload}")
                sleep(wait_time)
                conn.request("PATCH", "/api/v9/users/@me/settings-proto/1", payload, headers)
                sleep(wait_time)
            elif args["api"] == 'd':
                print(f"Locked on default. Waiting {wait_time}. Resending {payload}"%wait_time)
                sleep(wait_time)
                conn.request("PATCH", "/api/v9/users/@me/settings", payload, headers)
            else:
                payload = generate_payload('d', get_status(), message, emoji)
                print(f"Protobuf is rate-limitted. Automatically switching to default api. Sending new payload: {payload}")
                conn.request("PATCH", "/api/v9/users/@me/settings", payload, headers)

            res = conn.getresponse()
            data = res.read()
            decoded_data = loads(data.decode("utf-8"))
            print(f"After rate-limit, received: {res.status}")


# print(args["token"], args["comments"], args["status"], args["api"])
