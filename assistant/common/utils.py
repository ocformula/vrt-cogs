import asyncio
import json
import logging
import math
import re
from typing import Any, Dict, List, Optional, Tuple, Union

import discord
import openai
import tiktoken
from aiocache import cached
from openai.error import APIConnectionError, APIError, RateLimitError, Timeout
from openai.version import VERSION
from redbot.core import commands
from redbot.core.utils.chat_formatting import box
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_delay,
    wait_random_exponential,
)

log = logging.getLogger("red.vrt.assistant.utils")
encoding = tiktoken.get_encoding("cl100k_base")


def get_attachments(message: discord.Message) -> List[discord.Attachment]:
    """Get all attachments from context"""
    attachments = []
    if message.attachments:
        direct_attachments = [a for a in message.attachments]
        attachments.extend(direct_attachments)
    if hasattr(message, "reference"):
        try:
            referenced_attachments = [a for a in message.reference.resolved.attachments]
            attachments.extend(referenced_attachments)
        except AttributeError:
            pass
    return attachments


async def wait_message(ctx: commands.Context) -> Optional[discord.Message]:
    def check(message: discord.Message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        message = await ctx.bot.wait_for("message", timeout=600, check=check)
        if message.content == "cancel":
            await ctx.send("Canceled")
            return None
        return message
    except asyncio.TimeoutError:
        return None


async def can_use(message: discord.Message, blacklist: list, respond: bool = True) -> bool:
    allowed = True
    if message.author.id in blacklist:
        if respond:
            await message.channel.send("You have been blacklisted from using this command!")
        allowed = False
    elif any(role.id in blacklist for role in message.author.roles):
        if respond:
            await message.channel.send("You have a blacklisted role and cannot use this command!")
        allowed = False
    elif message.channel.id in blacklist:
        if respond:
            await message.channel.send("You cannot use that command in this channel!")
        allowed = False
    elif message.channel.category_id in blacklist:
        if respond:
            await message.channel.send(
                "You cannot use that command in any channels under this category"
            )
        allowed = False
    return allowed


def extract_code_blocks(content: str) -> List[str]:
    code_blocks = re.findall(r"```(?:\w+)(.*?)```", content, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r"```(.*?)```", content, re.DOTALL)
    return [block.strip() for block in code_blocks]


def extract_code_blocks_with_lang(content: str) -> List[Tuple[str, str]]:
    code_blocks = re.findall(r"```(\w+)(.*?)```", content, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r"```(.*?)```", content, re.DOTALL)
        return [("", block.strip()) for block in code_blocks]
    return [(block[0], block[1].strip()) for block in code_blocks]


def remove_code_blocks(content: str) -> str:
    content = re.sub(r"```(?:\w+)(.*?)```", "[Code Removed]", content, flags=re.DOTALL).strip()
    return re.sub(r"```(.*?)```", "[Code Removed]", content, flags=re.DOTALL).strip()


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    if not string:
        return 0
    num_tokens = len(encoding.encode(string))
    return num_tokens


def token_pagify(text: str, max_tokens: int = 2000):
    """Pagify a long string by tokens rather than characters"""
    token_chunks = []
    tokens = encoding.encode(text)
    current_chunk = []

    for token in tokens:
        current_chunk.append(token)
        if len(current_chunk) == max_tokens:
            token_chunks.append(current_chunk)
            current_chunk = []

    if current_chunk:
        token_chunks.append(current_chunk)

    text_chunks = []
    for chunk in token_chunks:
        text_chunk = encoding.decode(chunk)
        text_chunks.append(text_chunk)

    return text_chunks


def token_cut(message: str, max_tokens: int):
    cut_tokens = encoding.encode(message)[:max_tokens]
    return encoding.decode(cut_tokens)


def compile_messages(messages: List[dict]) -> str:
    """Compile messages list into a single string"""
    text = ""
    for message in messages:
        role = message["role"]
        content = message["content"]
        text += f"{role}: {content}\n"
    text += "\n"
    return text


def function_embeds(functions: Dict[str, Any], owner: bool) -> List[discord.Embed]:
    embeds = []
    pages = math.ceil(len(functions))
    for index, function_name in enumerate(list(functions)):
        function = functions[function_name]
        embed = discord.Embed(
            title="Custom Functions", description=function_name, color=discord.Color.blue()
        )

        if owner:
            schema = json.dumps(function.jsonschema, indent=2)
            if len(schema) > 1000:
                schema = f"{schema[:1000]}..."
            embed.add_field(name="Schema", value=box(schema, "json"), inline=False)
            code = box(function.code, "py")
            if len(function.code) > 1000:
                code = f"{box(function.code[:1000], 'py')}..."
            embed.add_field(name="Code", value=code, inline=False)
        else:
            embed.add_field(
                name="Schema", value=box(function.jsonschema["description"], "json"), inline=False
            )
            embed.add_field(name="Code", value=box("Hidden..."), inline=False)
        embed.set_footer(text=f"Page {index + 1}/{pages}")
        embeds.append(embed)
    if not embeds:
        embeds.append(
            discord.Embed(
                description="No custom code has been added yet!", color=discord.Color.purple()
            )
        )
    return embeds


def embedding_embeds(embeddings: Dict[str, Any], place: int) -> List[discord.Embed]:
    embeddings = sorted(embeddings.items(), key=lambda x: x[0])
    embeds = []
    pages = math.ceil(len(embeddings) / 5)
    start = 0
    stop = 5
    for page in range(pages):
        stop = min(stop, len(embeddings))
        embed = discord.Embed(title="Embeddings", color=discord.Color.blue())
        embed.set_footer(text=f"Page {page + 1}/{pages}")
        num = 0
        for i in range(start, stop):
            em = embeddings[i]
            text = em[1].text
            token_length = num_tokens_from_string(text)
            val = f"`Tokens: `{token_length}\n```\n{text[:30]}...\n```"
            embed.add_field(
                name=f"➣ {em[0]}" if place == num else em[0],
                value=val,
                inline=False,
            )
            num += 1
        embeds.append(embed)
        start += 5
        stop += 5
    if not embeds:
        embeds.append(
            discord.Embed(
                description="No embeddings have been added!", color=discord.Color.purple()
            )
        )
    return embeds


@retry(
    retry=retry_if_exception_type(Union[Timeout, APIConnectionError, RateLimitError]),
    wait=wait_random_exponential(min=1, max=5),
    stop=stop_after_delay(120),
    reraise=True,
)
@cached(ttl=1800)
async def request_embedding(text: str, api_key: str) -> List[float]:
    response = await openai.Embedding.acreate(
        input=text, model="text-embedding-ada-002", api_key=api_key, timeout=30
    )
    return response["data"][0]["embedding"]


@retry(
    retry=retry_if_exception_type(Union[Timeout, APIConnectionError, RateLimitError, APIError]),
    wait=wait_random_exponential(min=1, max=5),
    stop=stop_after_delay(120),
    reraise=True,
)
async def request_chat_response(
    model: str,
    messages: List[dict],
    api_key: str,
    temperature: float,
    functions: Optional[List[dict]] = [],
) -> dict:
    # response = await asyncio.to_thread(_chat, model, messages, api_key, temperature, functions)
    if VERSION >= "0.27.6" and model in ["gpt-3.5-turbo-0613", "gpt-4-32k-0613"]:
        response = await openai.ChatCompletion.acreate(
            model=model,
            messages=messages,
            temperature=temperature,
            api_key=api_key,
            timeout=60,
            functions=functions,
            function_call="auto" if functions else "none",
        )
    else:
        response = await openai.ChatCompletion.acreate(
            model=model, messages=messages, temperature=temperature, api_key=api_key, timeout=60
        )
    return response["choices"][0]["message"]


def _chat(
    model: str,
    messages: List[dict],
    api_key: str,
    temperature: float,
    functions: Optional[List[dict]] = [],
):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        api_key=api_key,
        timeout=60,
        functions=functions,
        function_call="auto" if functions else "none",
    )
    return response["choices"][0]["message"]


@retry(
    retry=retry_if_exception_type(Union[Timeout, APIConnectionError, RateLimitError, APIError]),
    wait=wait_random_exponential(min=1, max=5),
    stop=stop_after_delay(120),
    reraise=True,
)
async def request_completion_response(
    model: str, message: str, api_key: str, temperature: float, max_tokens: int
) -> str:
    response = await openai.Completion.acreate(
        model=model,
        prompt=message,
        temperature=temperature,
        api_key=api_key,
        max_tokens=max_tokens,
    )
    return response["choices"][0]["text"]


@retry(
    retry=retry_if_exception_type(Union[Timeout, APIConnectionError, RateLimitError, APIError]),
    wait=wait_random_exponential(min=1, max=5),
    stop=stop_after_delay(120),
    reraise=True,
)
async def request_image_create(prompt: str, api_key: str, size: str, user_id: str) -> str:
    response = await openai.Image.acreate(api_key=api_key, prompt=prompt, size=size, user=user_id)
    return response["data"][0]["url"]


@retry(
    retry=retry_if_exception_type(Union[Timeout, APIConnectionError, RateLimitError, APIError]),
    wait=wait_random_exponential(min=1, max=5),
    stop=stop_after_delay(120),
    reraise=True,
)
async def request_image_edit(
    prompt: str, api_key: str, size: str, user_id: str, image: bytes, mask: Optional[bytes]
) -> str:
    response = await openai.Image.create_edit(
        api_key=api_key, prompt=prompt, size=size, user=user_id, image=image, mask=mask
    )
    return response["data"][0]["url"]


@retry(
    retry=retry_if_exception_type(Union[Timeout, APIConnectionError, RateLimitError, APIError]),
    wait=wait_random_exponential(min=1, max=5),
    stop=stop_after_delay(120),
    reraise=True,
)
async def request_image_variant(
    prompt: str, api_key: str, size: str, user_id: str, image: bytes
) -> str:
    response = await openai.Image.create_variation(
        api_key=api_key, prompt=prompt, size=size, user=user_id, image=image
    )
    return response["data"][0]["url"]
