# VibeBot

*literally 1984*

This is a stupid-simple python service you can use to enforce ridiculous rules on chatters, i.e. Twitch chat.

Examples of some natural-language vibe rules:

- "do not allow any messages that speak poorly of the Shrek franchise"
- "only allow messages that are in cute nyaa tumblr speak :3 hehe~~"
- "do not allow messages related to the streamer's love life or lack thereof"
- "do not allow messages even slightly related to pineapples"
- "only allow messages that praise Joel; deny all other messages"

inspired by tweet `<screenshot>`

## Details

This does NOT integrate directly with Twitch or any chat service. It just exposes an http API on whatever port you want. You'll have to glue it to whatever Twitch automation you have (SAMMI, etc). Just send it HTTP messages with a json payload like this:


*url*: `http://localhost:8081/api`

```json
{ "chat_message": "<the message>" }
```

It will return with either

```json
{ "result": "pass" }
```

or

```json
{ "result": "fail" }
```

Now you can timeout the ones who fail your vibe check 😈


## Getting started

**Using uv** *recommeded*

1. install `uv` if you don't have it already: https://github.com/astral-sh/uv?tab=readme-ov-file#installation
1. in a command line, `cd` into this directory
1. run: `uv run --env-file .env main.py --port 8081` (or whatever port you like)
1. The service should run.

**Without using uv**
1. it's only python so just figure it out

## Configuration

### LLM
The LLM-related configuration lives in the file `.env`.

- `LLM_BASE_URL`: defaults to `https://openrouter.ai/api/v1` (openrouter mimics the OpenAI API, but lets you choose smaller, faster, cheaper (even free) models)
- `LLM_API_KEY`: paste your secret token from openrouter (or OpenAI or whatever) here
- `MODEL_NAME`: the model to use. Defaults to a very speedy and cheap model `MODEL_NAME=meta-llama/llama-3.2-3b-instruct:nitro`

The default model `meta-llama/llama-3.2-3b-instruct:nitro` is currently $0.08 per *million* tokens in, so if you load $10 onto your open router account, you should be good to go for a looooong time.

Using `:nitro` at the end of the name tells openrouter to pick the fastest llm provider. *Sometimes even the fastest providers are under heavy load and slow down, so if you're unlucky it might be too slow for chat.*

You can also select free versions of models, but these are slower and subject to throttling. Feel free to use these for testing though:

- `meta-llama/llama-3.2-3b-instruct:free`
- `meta-llama/llama-3.2-1b-instruct:free`
- `google/gemma-3-1b-it:free`
- `google/gemini-2.0-flash-exp:free`

(an API key is still needed for free models but you will not be charged)

### System Prompt
The system prompt lives in `config/system_prompt.txt`. You probably shouldn't have to touch this, but feel free to poke around.

### VibeRule
The vibe rule you want to be enforced lives in `config/vibe.txt`. You can update this live while the service is running and it should take effect within 5sec (the service reads it every 5sec).


## Notes on speed, rate limits and throttling

If your chat is extremely spammy you may need to put it on slow mode to get the full benefit.