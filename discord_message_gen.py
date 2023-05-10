# base 64 conversions
from base64 import b64encode

# For emoji support!
import emoji

# not supported (yet)
# timestamp = "21" + unix


def message_generate(message, emoji_symbol, presence_choice):
    ## Useful sub-functions:

    # Converts a string to its hexadecimal representation
    convert_string_to_hex = lambda text: " ".join(
        [str(hex(ord(i)))[2:].rjust(2, "0") for i in text]
    )
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
    hex_emoji = " ".join(
        repr(emoji_symbol.encode("utf-8"))[:-1].split("\\x")[1:] if emoji_symbol else ""
    )

    # Convert message to hex.
    hexified_text = convert_string_to_hex(message)

    # numeric representations.
    n1 = pad(hexified_text, len(presence_choice) + 8 + emoji_offset)
    n2 = pad(hexified_text, 2 + emoji_offset)
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
                    "%s" % ("1a 04 " + hex_emoji if emoji_symbol else ""),  # "21",
                ]
            )
        )
    ).decode()


# DEBUG
# print(message_generate("hello world!", ":penguin:", "dnd"))
