
# Discord-Custom-Status-auto-updater

This is a project that will update your Discord Custom status automatically. It is nearly fully customizeable! You can change the text, emojis, time, and presence (online/idle/dnd).




## Features

- Control custom status!
- Set a delay or expiry!
- Control presence (online/idle/dnd/auto)!
    - Can appear online/idle/dnd indefinitely or auto-update based on current presence
- Emoji support!
- Low-maintenance code!


## Usage/Examples
To use the `discord_message_gen.py` module, just import it. It will generate a base64 string that you can send to the Discord [__`settings-proto`__]("https://discord.com/api/v9/users/@me/settings-proto/1") API endpoint.

Here is the simplest example of generating some `base64` code.
```py
from discord_message_gen import *

message = "I love Penguins!!"
emoji = ":penguin:"
presence = "dnd"
expiry = [None, None]
message_generate(message, emoji, presence,*expiry)
```

Expiry is a (teeny) bit more complicated. There are some default configurations such as midnight, thirty minutes, an hour, and four hours. If you would like to customize the time (down to the millisecond)! You have to change the expiry parameters of the `message_generate()` function. Here are some examples:

```py
message_generate(message, emoji, presence, *["custom", [1]])
```
In this example, it will write the custom_status, and expire in one second.

Here are a few more examples of valid expiry lists:
```py
expiry = [["custom" [2023, 05, 11, 03, 14, 15, 09]]]
```
This will expire at a very specific time. 5/11/2023 03:14:15.009

```py
expiry = [["hour", None]]
```
This will expire 1 hour from time of patch. Second element in the list must be set to `None`.

```py
[["four hours", None]]
```
This will expire 4 hours from time of patch. Because you are using a default configuration, you must set the second parameter to `None`.

When expiring to midnight, it will expire on midnight of the next day.

## Installation

You can git clone this directory.

```
git clone https://github.com/Mr-FuzzyPenguin/Discord-Custom-Status-auto-updater.git
```
Then, make sure that you have python 3.11 or higher. 

You can use `status-updater.py` as a sample, or you can make your own code. If you are using `status-updater.py` be sure to change the `directory` variable appropriately. Be sure to also place the following files in the same directory: `donated-comments`, `donated-emojis`, `token`. You can change the name of the files as well. 
## Contributing
This is the exact file that I run on my discord account. You may be wondering why there are some `donated-file`s. This is because I made this project so people could donate their own interesting witty comments, and I would set that as my custom status (since I'm not creative enough to think of any witty statuses). If you would like to donate your own witty comment, please do so [here](https://forms.gle/MEC4ZDRdkSATmgM1A)!

I am not accepting any merge requests. This was mainly intended as a showcase of this ~~very im~~practical project. If you would like to help me discover how the Nitro emojis would react with the protobuf encoding, please friend request [my discord account. I change my discord name often!](https://discordlookup.com/user/499285426369069079) So, that is why I didn't attach a tag, but you can still lookup my username! This is furthered by the upcoming username-switch implementation that Discord is coming up with soon.
## Roadmap

- (soon) Better Terminal UI for better quality of life [4/5]
- (soon) Arg parse so you can pass files for greater customizability [3/5]
- (soon) support for one-time change custom-status [2/5]
- (soon) Switching off `requests` [?/5]

#### Potential future ideas:
- Nitro support (but only if someone contributes, since I have no Nitro)
    - GIF and custom emoji support!


## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>

