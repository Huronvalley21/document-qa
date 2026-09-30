"""
CUA (Computer-Use Agent) Demo
==============================
Demonstrates OpenAI's computer-use-preview model controlling a
Playwright browser.  The model sees screenshots and emits actions
(click, type, scroll, keypress) which are executed in the browser.

Usage:
    export OPENAI_API_KEY=sk-...
    python scripts/cua_demo.py

Requires: openai, playwright (installed via requirements.txt)

NOTE: This uses the openai 2.x client directly — no openai-agents SDK
needed — so it works alongside browser-use in the same virtualenv.
"""

import asyncio
import base64
import os
import sys

from dotenv import load_dotenv

load_dotenv()

DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720
MODEL = "computer-use-preview"


async def take_screenshot(page) -> str:
    """Capture page screenshot and return base64-encoded PNG."""
    buf = await page.screenshot(type="png")
    return base64.standard_b64encode(buf).decode("ascii")


async def execute_action(page, action: dict) -> None:
    """Translate a CUA action dict into Playwright calls."""
    action_type = action.get("type")

    if action_type == "click":
        x, y = action["x"], action["y"]
        btn = action.get("button", "left")
        await page.mouse.click(x, y, button=btn)

    elif action_type == "double_click":
        x, y = action["x"], action["y"]
        await page.mouse.dblclick(x, y)

    elif action_type == "type":
        await page.keyboard.type(action["text"])

    elif action_type == "keypress":
        keys = action["keys"]
        for key in keys:
            await page.keyboard.press(key)

    elif action_type == "scroll":
        x, y = action["x"], action["y"]
        delta_x = action.get("scroll_x", 0)
        delta_y = action.get("scroll_y", 0)
        await page.mouse.move(x, y)
        await page.mouse.wheel(delta_x, delta_y)

    elif action_type == "wait":
        await asyncio.sleep(2)

    elif action_type == "screenshot":
        pass  # will be taken next loop iteration

    else:
        print(f"  [skip] unknown action type: {action_type}")


async def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print(
            "OPENAI_API_KEY is not set.\n"
            "Export it or add it to .env to run the CUA demo.\n"
            "The computer-use-preview model requires an OpenAI API key."
        )
        sys.exit(1)

    from openai import OpenAI
    from playwright.async_api import async_playwright

    client = OpenAI(api_key=api_key)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": DISPLAY_WIDTH, "height": DISPLAY_HEIGHT}
        )
        page = await context.new_page()
        await page.goto("https://news.ycombinator.com")
        await page.wait_for_load_state("networkidle")

        screenshot_b64 = await take_screenshot(page)

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "You are looking at Hacker News. "
                            "Find the title and URL of the #1 story on the page. "
                            "Once you have the answer, respond with the title and URL as text."
                        ),
                    },
                ],
            }
        ]

        tools = [
            {
                "type": "computer_use_preview",
                "display_width": DISPLAY_WIDTH,
                "display_height": DISPLAY_HEIGHT,
                "environment": "browser",
            }
        ]

        print("Starting CUA loop...")
        for step in range(1, 11):
            print(f"\n--- Step {step} ---")

            response = client.responses.create(
                model=MODEL,
                input=messages,
                tools=tools,
                truncation="auto",
            )

            computer_calls = [
                item for item in response.output if item.type == "computer_call"
            ]

            if not computer_calls:
                text_items = [
                    item for item in response.output if item.type == "message"
                ]
                for item in text_items:
                    for content in item.content:
                        if hasattr(content, "text"):
                            print(f"  Model says: {content.text}")
                print("\nCUA loop complete (model returned text, no more actions).")
                break

            for call in computer_calls:
                action = call.action
                action_dict = {
                    "type": action.type,
                }
                for attr in ("x", "y", "button", "text", "keys", "scroll_x", "scroll_y"):
                    if hasattr(action, attr):
                        action_dict[attr] = getattr(action, attr)

                print(f"  Action: {action_dict}")
                await execute_action(page, action_dict)
                await asyncio.sleep(0.5)

                screenshot_b64 = await take_screenshot(page)

                messages = response.output + [
                    {
                        "type": "computer_call_output",
                        "call_id": call.call_id,
                        "output": {
                            "type": "computer_screenshot",
                            "image_url": f"data:image/png;base64,{screenshot_b64}",
                        },
                    }
                ]
        else:
            print("\nReached max steps without a final text response.")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
