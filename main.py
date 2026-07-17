import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable is not set.")

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    messages = [{"role": "user", "content": args.user_prompt}]
    generate_content(client, messages)


def generate_content(client: OpenAI, messages: list) -> None:
    response = client.chat.completions.create(
        model="openrouter/free", messages=messages
    )

    if response.usage is None:
        raise RuntimeError(
            "Response has missing usage field. Indicates failed API request."
        )

    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")

    print(f"Response:\n{response.choices[0].message.content}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main()
