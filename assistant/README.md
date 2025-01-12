# Assistant Help

Advanced Chat GPT integration, with all the tools needed to configure a knowledgable Q&A or chat bot!

# chat

- Usage: `[p]chat <question> `
- Aliases: `ask`
- Cooldown: `1 per 6.0 seconds`
- Checks: `server_only`

Chat with [botname]!<br/><br/>Conversations are _Per_ user _Per_ channel, meaning a conversation you have in one channel will be kept in memory separately from another conversation in a separate channel<br/><br/>**Optional Arguments**<br/>--outputfile <filename> - uploads a file with the reply instead (no spaces)<br/>--extract - extracts code blocks from the reply<br/><br/>**Example**<br/>[p]chat write a python script that prints "Hello World!"<br/>- Including --outputfile hello.py will output a file containing the whole response.<br/>- Including --outputfile hello.py --extract will output a file containing just the code blocks and send the rest as text.<br/>- Including --extract will send the code separately from the reply

# convostats

- Usage: `[p]convostats [user] `
- Checks: `server_only`

Check the token and message count of yourself or another user's conversation for this channel<br/><br/>Conversations are _Per_ user _Per_ channel, meaning a conversation you have in one channel will be kept in memory separately from another conversation in a separate channel<br/><br/>Conversations are only stored in memory until the bot restarts or the cog reloads

# clearconvo

- Usage: `[p]clearconvo `
- Checks: `server_only`

Reset your conversation<br/><br/>This will clear all message history between you and the bot for this channel

# assistant

- Usage: `[p]assistant `
- Restricted to: `ADMIN`
- Aliases: `ass`
- Checks: `server_only`

Setup the assistant<br/><br/>You will need an api key to use the assistant. https://platform.openai.com/account/api-keys

## assistant embedmethod

- Usage: `[p]assistant embedmethod `

Cycle between embedding methods<br/><br/>**Dynamic** embeddings mean that the embeddings pulled are dynamically appended to the initial prompt for each individual question.<br/>When each time the user asks a question, the previous embedding is replaced with embeddings pulled from the current question, this reduces token usage significantly<br/><br/>**Static** embeddings are applied in front of each user message and get stored with the conversation instead of being replaced with each question.<br/><br/>**Hybrid** embeddings are a combination, with the first embedding being stored in the conversation and the rest being dynamic, this saves a bit on token usage<br/><br/>Dynamic embeddings are helpful for Q&A, but not so much for chat when you need to retain the context pulled from the embeddings. The hybrid method is a good middle ground

## assistant maxretention

- Usage: `[p]assistant maxretention <max_retention> `

Set the max messages for a conversation<br/><br/>Conversation retention is cached and gets reset when the bot restarts or the cog reloads.<br/><br/>Regardless of this number, the initial prompt and internal system message are always included,<br/>this only applies to any conversation between the user and bot after that.<br/><br/>Set to 0 to disable conversation retention

## assistant model

- Usage: `[p]assistant model [model=None] `

Set the GPT model to use<br/><br/>Valid models and their context info:<br/>- Model-Name: MaxTokens, ModelType<br/>- gpt-3.5-turbo: 4096, chat<br/>- gpt-3.5-turbo-16k: 16384, chat<br/>- gpt-4: 8192, chat<br/>- gpt-4-32k: 32768, chat<br/>- code-davinci-002: 8001, chat<br/>- text-davinci-003: 4097, completion<br/>- text-davinci-002: 4097, completion<br/>- text-curie-001: 2049, completion<br/>- text-babbage-001: 2049, completion<br/>- text-ada-001: 2049, completion<br/><br/>Other sub-models are also included

## assistant regexblacklist

- Usage: `[p]assistant regexblacklist <regex> `

Remove certain words/phrases in the bot's responses

## assistant exportjson

- Usage: `[p]assistant exportjson `

Export embeddings to a json file

## assistant maxtime

- Usage: `[p]assistant maxtime <retention_time> `

Set the conversation expiration time<br/><br/>Regardless of this number, the initial prompt and internal system message are always included,<br/>this only applies to any conversation between the user and bot after that.<br/><br/>Set to 0 to store conversations indefinitely or until the bot restarts or cog is reloaded

## assistant resetconversations

- Usage: `[p]assistant resetconversations <yes_or_no> `

Wipe saved conversations for the assistant in this server<br/><br/>This will delete any and all saved conversations for the assistant.

## assistant relatedness

- Usage: `[p]assistant relatedness <mimimum_relatedness> `

Set the minimum relatedness an embedding must be to include with the prompt<br/><br/>Relatedness threshold between 0 and 1 to include in embeddings during chat<br/><br/>Questions are converted to embeddings and compared against stored embeddings to pull the most relevant, this is the score that is derived from that comparison<br/><br/>**Hint**: The closer to 1 you get, the more deterministic and accurate the results may be, just don't be _too_ strict or there wont be any results.

## assistant timezone

- Usage: `[p]assistant timezone <timezone> `

Set the timezone used for prompt placeholders

## assistant importcsv

- Usage: `[p]assistant importcsv <overwrite> `

Import embeddings to use with the assistant<br/><br/>Args:<br/> overwrite (bool): overwrite embeddings with existing entry names<br/><br/>This will read excel files too

## assistant resetglobalembeddings

- Usage: `[p]assistant resetglobalembeddings <yes_or_no> `
- Restricted to: `BOT_OWNER`

Wipe saved embeddings for all servers<br/><br/>This will delete any and all saved embedding training data for the assistant.

## assistant toggle

- Usage: `[p]assistant toggle `

Toggle the assistant on or off

## assistant wipecog

- Usage: `[p]assistant wipecog <confirm> `
- Restricted to: `BOT_OWNER`

Wipe all settings and data for entire cog

## assistant channel

- Usage: `[p]assistant channel <channel> `

Set the channel for the assistant

## assistant mention

- Usage: `[p]assistant mention `

Toggle whether to ping the user on replies

## assistant maxtokens

- Usage: `[p]assistant maxtokens <max_tokens> `

Set the max tokens the model can use at once<br/><br/>For GPT3.5 use 4000 or less.<br/>For GPT4 user 8000 or less (if 8k version).<br/><br/>Using more than the model can handle will raise exceptions.

## assistant system

- Usage: `[p]assistant system [system_prompt] `
- Aliases: `sys`

Set the system prompt for GPT to use<br/><br/>**Placeholders**<br/>- **botname**: [botname]<br/>- **timestamp**: discord timestamp<br/>- **day**: Mon-Sun<br/>- **date**: MM-DD-YYYY<br/>- **time**: HH:MM AM/PM<br/>- **timetz**: HH:MM AM/PM Timezone<br/>- **members**: server member count<br/>- **username**: user's name<br/>- **displayname**: user's display name<br/>- **roles**: the names of the user's roles<br/>- **rolementions**: the mentions of the user's roles<br/>- **avatar**: the user's avatar url<br/>- **owner**: the owner of the server<br/>- **servercreated**: the create date/time of the server<br/>- **server**: the name of the server<br/>- **py**: python version<br/>- **dpy**: discord.py version<br/>- **red**: red version<br/>- **cogs**: list of currently loaded cogs<br/>- **channelname**: name of the channel the conversation is taking place in<br/>- **channelmention**: current channel mention<br/>- **topic**: topic of current channel (if not forum or thread)<br/>- **banktype**: whether the bank is global or not<br/>- **currency**: currency name<br/>- **bank**: bank name<br/>- **balance**: the user's current balance

## assistant resetglobalconversations

- Usage: `[p]assistant resetglobalconversations <yes_or_no> `
- Restricted to: `BOT_OWNER`

Wipe saved conversations for the assistant in all servers<br/><br/>This will delete any and all saved conversations for the assistant.

## assistant view

- Usage: `[p]assistant view [private=True] `

View current settings<br/><br/>To send in current channel, use [p]assistant view false

## assistant regexfailblock

- Usage: `[p]assistant regexfailblock `
- Restricted to: `BOT_OWNER`

Toggle whether failed regex blocks the assistant's reply<br/><br/>Some regexes can cause [catastrophically backtracking](https://www.rexegg.com/regex-explosive-quantifiers.html)<br/>The bot can safely handle if this happens and will either continue on, or block the response.

## assistant temperature

- Usage: `[p]assistant temperature <temperature> `

Set the temperature for the model (0.0 - 1.0)<br/><br/>Closer to 0 is more concise and accurate while closer to 1 is more imaginative

## assistant importjson

- Usage: `[p]assistant importjson <overwrite> `

Import embeddings to use with the assistant<br/><br/>Args:<br/> overwrite (bool): overwrite embeddings with existing entry names

## assistant topn

- Usage: `[p]assistant topn <top_n> `

Set the embedding inclusion amout<br/><br/>Top N is the amount of embeddings to include with the initial prompt

## assistant maxrecursion

- Usage: `[p]assistant maxrecursion <recursion> `

Set the maximum function calls allowed in a row<br/><br/>This sets how many times the model can call functions in a row<br/><br/>Only the following models can call functions at the moment<br/>- gpt-3.5-turbo-0613<br/>- gpt-3.5-turbo-16k-0613<br/>- gpt-4-0613

## assistant minlength

- Usage: `[p]assistant minlength <min_question_length> `

set min character length for questions<br/><br/>Set to 0 to respond to anything

## assistant prompt

- Usage: `[p]assistant prompt [prompt] `
- Aliases: `pre`

Set the initial prompt for GPT to use<br/><br/>**Placeholders**<br/>- **botname**: [botname]<br/>- **timestamp**: discord timestamp<br/>- **day**: Mon-Sun<br/>- **date**: MM-DD-YYYY<br/>- **time**: HH:MM AM/PM<br/>- **timetz**: HH:MM AM/PM Timezone<br/>- **members**: server member count<br/>- **username**: user's name<br/>- **displayname**: user's display name<br/>- **roles**: the names of the user's roles<br/>- **rolementions**: the mentions of the user's roles<br/>- **avatar**: the user's avatar url<br/>- **owner**: the owner of the server<br/>- **servercreated**: the create date/time of the server<br/>- **server**: the name of the server<br/>- **py**: python version<br/>- **dpy**: discord.py version<br/>- **red**: red version<br/>- **cogs**: list of currently loaded cogs<br/>- **channelname**: name of the channel the conversation is taking place in<br/>- **channelmention**: current channel mention<br/>- **topic**: topic of current channel (if not forum or thread)<br/>- **banktype**: whether the bank is global or not<br/>- **currency**: currency name<br/>- **bank**: bank name<br/>- **balance**: the user's current balance

## assistant openaikey

- Usage: `[p]assistant openaikey `
- Aliases: `key`

Set your OpenAI key

## assistant persist

- Usage: `[p]assistant persist `
- Restricted to: `BOT_OWNER`

Toggle persistent conversations

## assistant exportcsv

- Usage: `[p]assistant exportcsv `

Export embeddings to a .csv file<br/><br/>**Note:** csv exports do not include the embedding values

## assistant embeddingtest

- Usage: `[p]assistant embeddingtest <question> `
- Aliases: `etest`

Fetch related embeddings according to the current settings along with their scores<br/><br/>You can use this to fine-tune the minimum relatedness for your assistant

## assistant blacklist

- Usage: `[p]assistant blacklist <channel_role_member> `

Add/Remove items from the blacklist<br/><br/>channel_role_member can be a member, role, channel, or category channel

## assistant questionmark

- Usage: `[p]assistant questionmark `

Toggle whether questions need to end with \***\*?\*\***

## assistant resetembeddings

- Usage: `[p]assistant resetembeddings <yes_or_no> `

Wipe saved embeddings for the assistant<br/><br/>This will delete any and all saved embedding training data for the assistant.

## assistant functioncalls

- Usage: `[p]assistant functioncalls `

Toggle whether GPT can call functions<br/><br/>Only the following models can call functions at the moment<br/>- gpt-3.5-turbo-0613<br/>- gpt-3.5-turbo-16k-0613<br/>- gpt-4-0613

# embeddings (Hybrid Command)

- Usage: `[p]embeddings [query] `
- Slash Usage: `/embeddings [query] `
- Restricted to: `ADMIN`
- Aliases: `emenu`
- Checks: `server_only`

Manage embeddings for training<br/><br/>Embeddings are used to optimize training of the assistant and minimize token usage.<br/><br/>By using this the bot can store vast amounts of contextual information without going over the token limit.<br/><br/>**Note**<br/>You can enter a search query with this command to bring up the menu and go directly to that embedding selection.

# customfunctions (Hybrid Command)

- Usage: `[p]customfunctions `
- Slash Usage: `/customfunctions `
- Restricted to: `GUILD_OWNER`
- Aliases: `customfunction and customfunc`
- Checks: `server_only`

Add custom function calls for Assistant to use<br/><br/>**READ**<br/>- [Function Call Docs](https://platform.openai.com/docs/guides/gpt/function-calling)<br/>- [OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb)<br/>- [JSON Schema Reference](https://json-schema.org/understanding-json-schema/)<br/><br/>Only these two models can use function calls as of now:<br/>- gpt-3.5-turbo-0613<br/>- gpt-4-0613<br/><br/>The following objects are passed by default as keyword arguments.<br/>- **user**: the user currently chatting with the bot (discord.Member)<br/>- **channel**: channel the user is chatting in (TextChannel|Thread|ForumChannel)<br/>- **server**: current server (discord.Guild)<br/>- **bot**: the bot object (Red)<br/>- **conf**: the config model for Assistant (GuildSettings)<br/>- All functions **MUST** include \*args, \*\*kwargs in the params and return a string<br/>

```python
# Can be either sync or async
async def func(*args, **kwargs) -> str:
```

<br/>Only bot owner can manage this, server owners can see descriptions but not code

## Function Example

```python
import discord
from redbot.core import bank
async def get_member_balance(guild: discord.Guild, name: str, *args, **kwargs) -> str:
    user = guild.get_member_named(name)
    if not user:
        return "Could not find that user"
    bal = await bank.get_balance(user)
    return f"{bal} VC"
```

## JSON Schema Example

```json
{
  "name": "get_member_balance",
  "description": "Get a member's VC balance by name",
  "parameters": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "description": "the name of the member"
      }
    },
    "required": ["name"]
  }
}
```

# 3rd Party Cog Support

3rd party cogs can register their own functions easily by using a custom listener.

The code below is used in my Fluent cog for example.

```python
    @commands.Cog.listener()
    async def on_assistant_cog_add(self, cog: commands.Cog):
        # This function could also be a string, and can be async OR sync
        async def get_translation(bot, message: str, to_language: str, *args, **kwargs) -> str:
            # If something needs to be imported to use a function, then do it inside the function
            # from some_package import some_class_or_method

            # All functions MUST take *args, **kwargs as params
            cog = bot.get_cog("Fluent")
            if not cog:
                return "Cog not loaded!"
            lang = await cog.converter(to_language)
            if not lang:
                return "Invalid target language"
            try:
                translation = await cog.translate(message, lang)
                return f"{translation.text}\n({translation.src} -> {lang})"
            except Exception as e:
                return f"Error: {e}"

        schema = {
            "name": "get_translation",
            "description": "Use this function to translate text",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "the text to translate"},
                    "to_language": {
                        "type": "string",
                        "description": "the target language to translate to",
                    },
                },
                "required": ["message", "to_language"],
            },
        }
        await cog.register_function(self, schema, get_translation)
```

When the assistant cog is loaded, the Fluent cog can now inject its custom function into the registry to be used by the chat model.
Additionally, if the Fluent cog was loaded _after_ the Assistant cog, it will detect if the cog has the `on_assistant_cog_add` listener and execute it.

- Assistant will automatically unregister cogs when they are unloaded
- If a cog tries to register a function whos name already exists, an error will be logged and the function will not register
- All functions **MUST** take `*args, **kwargs` as parameters
- When importing actual function objects in your cogs, make sure to import librries `inside` of the function
- The function name in your schema must match the function name itself exactly
