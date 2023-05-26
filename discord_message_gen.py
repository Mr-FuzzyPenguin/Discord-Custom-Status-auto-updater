# base 64 conversions
from base64 import b64encode

# Dict to JSON conversions
from json import dumps

# For emoji support!
import emoji

# Timestamp generator
import time
from datetime import datetime, timedelta

## Helpful constants:
# The presence table
status = {"o": "online", "i": "idle", "d": "dnd", "a": "auto"}

# For time
now = datetime.now()
HOUR = 3600

## Useful functions on hex-operations:
# adds a space every 2 chars.
spacer = lambda s: " ".join(s[i : i + 2] for i in range(0, len(s), 2))

# Converts a string to its hexadecimal representation, return str.
convert_string_to_hex = lambda text: spacer(str(text.encode("utf-8").hex()))

# Takes a hex sequence (str). Finds number of bytes, and pads it (into hex).
pad = lambda hex_sequence, offset=0: str(hex(len(hex_sequence.split()) + offset))[
    2:
].rjust(2, "0")

### Default
## Generating iso timestamp
def timestamp_generate(timestamp):
    # re-initialize time every time this function is run
    now = datetime.now()

    # Useful time sub-functions for iso-formatting:
    # Time from now, returns iso-formatted string
    time_from_now = lambda sec: (now + timedelta(seconds=sec)).isoformat()
    # millisecond precision with iso-format
    specific_time_control = lambda y, mo, d, h, m, s, ms: " ".join(
        datetime(y, mo, d, h, m, s, ms).isoformat()
    )

    # pre-made settings
    hour_from_now = time_from_now(HOUR)
    four_hours_from_now = time_from_now(4 * HOUR)
    half_hour_from_now = time_from_now(0.5 * HOUR)

    # midnight of next day
    midnight = specific_time_control(now.year, now.month, now.day + 1, 0, 0, 0, 0)

    # Expiry table for choosing expiry time.
    expiry_table = {
        "hour": hour_from_now,
        "four hours": four_hours_from_now,
        "half hour": half_hour_from_now,
        "midnight": midnight,
    }

    # check time expiry in expiry_table
    if type(timestamp) == str:
        return None if timestamp not in expiry_table.keys() else expiry_table[timestamp]
    elif type(timestamp) == list:
        return specific_time_control(*timestamp)
    elif type(timestamp) == int:
        return time_from_now(timestamp)
    else:
        return None


def message_generate(user_status, text, user_emoji='', expiry=None):
    user_emoji=emoji.emojize(user_emoji)

    altered_settings = {
        "custom_status": {
            "text": text,
            "expires_at": timestamp_generate(expiry),
            "emoji_id": None, # not supported, due to lack of testing with Nitro.
            "emoji_name": user_emoji
        }
    }

    # If not automatically adding status, don't change status.
    if user_status[0] != 'a':
        altered_settings["status"] = status[user_status[0]]

    # Will need to use json.dumps()
    return dumps(altered_settings)


### Protobuf
## Generating UNIX to hex timestamp.
def protobuf_timestamp_generate(timestamp):
    # re-initialize time every time this function is run
    now = datetime.now()
    # Useful time sub-functions for protobuf:
    # Time from now, returns datetime
    time_from_now = lambda sec: now + timedelta(seconds=sec)
    # Converts to unix with millisecond precision
    unix_time_converter = lambda t: int(
        time.mktime(t.timetuple()) * 1e3 + t.microsecond / 1e3
    )
    # converts unix to hex with "prettifying".
    hex_time_converter = lambda t: spacer("0" + hex(t)[2:]).split()[::-1]

    # Function merger:
    all_time_control = lambda t: " ".join(
        hex_time_converter(unix_time_converter(time_from_now(t)))
    )
    specific_time_control = lambda y, mo, d, h, m, s, ms: " ".join(
        hex_time_converter(unix_time_converter(datetime(y, mo, d, h, m, s, ms)))
    )

    # pre-made settings
    hour_from_now = all_time_control(HOUR)
    four_hours_from_now = all_time_control(4 * HOUR)
    half_hour_from_now = all_time_control(0.5 * HOUR)

    # midnight of next day
    midnight = specific_time_control(now.year, now.month, now.day + 1, 0, 0, 0, 0)

    # Expiry table for choosing expiry time.
    expiry_table = {
        "hour": hour_from_now,
        "four hours": four_hours_from_now,
        "half hour": half_hour_from_now,
        "midnight": midnight,
    }
    # check time expiry in expiry_table
    if type(timestamp) == str:
        return None if timestamp not in expiry_table.keys() else expiry_table[timestamp]
    elif type(timestamp) == list:
        return specific_time_control(*timestamp)
    elif type(timestamp) == int:
        return all_time_control(timestamp)
    else:
        return None

# Generate protobuf base64 encoding
def protobuf_message_generate(user_status, text, user_emoji='', expiry=False):
    # takes in field (hex value or bool), and hex string
    # returns:
    # field#, hex_string
    add_field = lambda field, hex_string: " ".join(
        ["" if not field else field, f"{len(hex_string.split()):0{2}x}", hex_string]
    )

    return b64encode(
        bytes.fromhex(
            add_field("5a",
                add_field("0a", add_field("0a", convert_string_to_hex(status[user_status])))
                + " 12 "
                + add_field(False,
                    add_field("0a", convert_string_to_hex(text))
                    + " "
                    + add_field("1a",
                        convert_string_to_hex(emoji.emojize(user_emoji, language="alias")),
                    ) * int(bool(user_emoji)),
                )
                + (f" 21 {protobuf_timestamp_generate(expiry)} 00 00") * int(bool(expiry)),
            )
        )
    ).decode()
