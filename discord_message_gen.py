# base 64 conversions
from base64 import b64encode

# For emoji support!
import emoji

# Timestamp generator
import time
from datetime import datetime, timedelta

# not supported (yet)
# timestamp = "21" + unix

# Check python version!
import sys

if sys.version_info[0:2] != (3, 11):
    raise Exception("This module requires python 3.11!")


def message_generate(message, emoji_symbol, presence_choice, expiry=False, custom_expiry=False):
    ## Useful sub-functions:

    # Converts a string to its hexadecimal representation, return str.
    convert_string_to_hex = lambda text: text.encode("utf-8").hex(" ")

    # adds a space every 2 chars.
    spacer = lambda s: " ".join(s[i : i + 2] for i in range(0, len(s), 2))

    # Takes a hex sequence (str). Finds number of bytes, and pads it (into hex).
    pad = lambda hex_sequence, offset=0: str(hex(len(hex_sequence.split()) + offset))[
        2:
    ].rjust(2, "0")

    ## Constants:

    # The presence table
    presence = {
        "online": "06 6f 6e 6c 69 6e 65 12",
        "idle": "04 69 64 6c 65 12",
        "dnd": "03 64 6e 64 12",
    }

    # emojis, constant offset, symbol handler, and utf8 -> hex formatter
    emoji_offset = 6 if emoji_symbol else 0
    emoji_symbol = (
        emoji_symbol
        if len(emoji_symbol) == 1
        else (emoji.emojize(emoji_symbol, language="alias"))
    )
    hex_emoji = convert_string_to_hex(emoji_symbol) if emoji_symbol else ""

    # Convert message to hex.
    hexified_text = convert_string_to_hex(message)

    # Generate timestamp
    now = datetime.now()
    HOUR = 3600

    # Time from now, returns datetime
    time_from_now = lambda sec: now+timedelta(seconds=sec)
    # Converts to unix with millisecond precision
    unix_time_converter = lambda t: int(time.mktime(t.timetuple())*1e3 + t.microsecond/1e3)
    # converts unix to hex with "prettifying".
    hex_time_converter = lambda t: spacer('0'+hex(t)[2:]).split()[::-1]

    # Puts all the functions together!
    all_time_control = lambda t: ' '.join(hex_time_converter(unix_time_converter(time_from_now(t))))
    specific_time_control = lambda y, mo, d, h, m, s, ms: ' '.join(hex_time_converter(unix_time_converter( datetime(y, mo, d, h, m, s, ms))))

    hour_from_now = all_time_control(HOUR)
    four_hours_from_now = all_time_control(4*HOUR)
    half_hour_from_now = all_time_control(0.5*HOUR)
    # midnight of next day

    midnight = (specific_time_control(now.year, now.month, now.day+1, 0, 0, 0, 0))
    expiry_table={
        "hour" : hour_from_now,
        "four hours" : four_hours_from_now,
        "half hour" : half_hour_from_now,
        "midnight" : midnight,
        "custom" : None if not custom_expiry else specific_time_control(*custom_expiry) if len(custom_expiry) != 1 else all_time_control(*custom_expiry)
    }

    # print(hour_from_now)

    # remaining byte numeric representations.
    n1 = pad(hexified_text, len(presence_choice) + 8 + emoji_offset + int(bool(expiry))*9)
    n2 = pad(hexified_text, 2 + emoji_offset + int(bool(expiry))*9)
    n3 = pad(hexified_text)

    return b64encode(
        bytes.fromhex(
            " ".join(
                [
                    "5a %s" % n1,  # message length
                    "0a 0%d" % (len(presence_choice) + 2),  # preesence length
                    "0a %s" % presence[presence_choice],  # presennce
                    n2,  # (remaining bits)
                    "0a %s" % n3,  # custom status length
                    hexified_text,  # custom status in hex.
                    "%s" % ("1a 04 " + hex_emoji if emoji_symbol else ""),
                    "%s" % ("21" + expiry_table[expiry] + "00 00" if expiry else ""),
                ]
            )
        )
    ).decode()


# DEBUG
# print(message_generate("Hello World!", ":penguin:", "dnd", "custom", [5]))
# WhEKBQoDZG5kEggKABoE8J+Qpw==
