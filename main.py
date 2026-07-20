import argparse
import os
import sys
from typing import cast

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionToolUnionParam

from call_function import available_functions, call_function
from config import MAX_ITERATIONS
from prompts import system_prompt


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable is not set.")

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    # limit agent looping to not burn tokens
    for _ in range(MAX_ITERATIONS):
        try:
            response = generate_content(client, messages)
            if response:
                print(f"Response:\n{response}")
                return
        except Exception as e:
            print(f"Error: {e}")

    # if max iterations reached before answer exit with instructions
    print(
        f"Maximum iterations ({MAX_ITERATIONS} reached. Consider adjusting in `config.py`)"
    )
    sys.exit(1)


def generate_content(client: OpenAI, messages: list) -> str | None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=cast(list[ChatCompletionToolUnionParam], available_functions),
    )

    if response.usage is None:
        raise RuntimeError(
            "Response has missing usage field. Indicates failed API request."
        )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        return message.content

    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        result_message = call_function(tool_call, args.verbose)

        if not result_message.get("content"):
            raise RuntimeError(
                f"No content after calling function {tool_call.function.name}"
            )
        if args.verbose:
            print(f"-> {result_message['content']}")
        messages.append(result_message)

    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chatbot")

    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main()
