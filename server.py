from typing import Callable
from flask import Flask, request, jsonify
from pydantic import BaseModel
from pydantic_ai import Agent
import asyncio


class ApiRequest(BaseModel):
    chat_message: str


app = Flask(__name__)


def set_agent_provider(
    agent_provider: Callable[[], Agent],
):
    global _agent_provider
    _agent_provider = agent_provider


def get_agent_provider() -> Callable[[], Agent]:
    global _agent_provider
    if _agent_provider is None:
        raise ValueError("Agent provider is not set.")
    return _agent_provider


def set_user_message_builder(
    user_message_builder: Callable[[str], str],
):
    global _user_message_builder
    _user_message_builder = user_message_builder


def get_user_message_builder() -> Callable[[str], str]:
    global _user_message_builder
    if _user_message_builder is None:
        raise ValueError("User message builder is not set.")
    return _user_message_builder


@app.route("/api", methods=["POST"])
async def handle_request():
    data = ApiRequest(**request.get_json())

    async def do_once():
        response = await _get_agent_response(data.chat_message)

        # take only the first word:
        response = response.split()[0].lower()

        return jsonify({"result": response})

    try:
        return await do_once()
    except Exception as e:
        # try one more time...
        try:
            return await do_once()
        except Exception as e:
            # if it fails again, return the error
            return jsonify({"result": "error", "error": str(e)}), 400


async def _get_agent_response(chat_message: str, timeout_seconds: int = 4) -> str:
    agent = get_agent_provider()()

    user_message_builder = get_user_message_builder()
    message = user_message_builder(chat_message)

    async def run_agent():
        response = await agent.run(message)
        return response.data

    try:
        result = await asyncio.wait_for(run_agent(), timeout=timeout_seconds)
        return result
    except asyncio.TimeoutError:
        raise TimeoutError("Agent response timed out.")


def run_server(
    agent_provider: Callable[[], Agent],
    user_message_builder: Callable[[str], str],
    port: int,
):
    set_agent_provider(agent_provider)
    set_user_message_builder(user_message_builder)
    app.run(host="0.0.0.0", port=port, debug=False)
