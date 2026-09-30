"""
OpenAI Agents SDK — Computer Use Agent (CUA) Demo
==================================================
Uses the openai-agents SDK's ComputerTool with a Playwright backend
to let the model control a headless browser.

⚠️  Requires openai>=3.0 (openai-agents dependency).
    Install via: pip install -r requirements-openai-agents.txt
    This CANNOT share a virtualenv with browser-use (pins openai==2.26).

Usage:
    export OPENAI_API_KEY=sk-...
    python scripts/agents_sdk_cua_demo.py
"""

import asyncio
import base64
import os
import sys

from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("OPENAI_API_KEY is not set. Export it or add it to .env.")
        sys.exit(1)

    try:
        from agents import Agent, ComputerTool, Runner
        from agents.computer import AsyncComputer
    except ImportError:
        print(
            "openai-agents is not installed in this virtualenv.\n"
            "Install it in a separate venv:\n"
            "  python -m venv .venv-agents && source .venv-agents/bin/activate\n"
            "  pip install -r requirements-openai-agents.txt"
        )
        sys.exit(1)

    from playwright.async_api import async_playwright

    WIDTH, HEIGHT = 1280, 720

    class PlaywrightComputer(AsyncComputer):
        environment = "browser"
        dimensions = (WIDTH, HEIGHT)

        def __init__(self, page):
            self._page = page

        async def screenshot(self) -> str:
            buf = await self._page.screenshot(type="png")
            return base64.standard_b64encode(buf).decode("ascii")

        async def click(self, x: int, y: int, button: str = "left") -> None:
            await self._page.mouse.click(x, y, button=button)

        async def double_click(self, x: int, y: int) -> None:
            await self._page.mouse.dblclick(x, y)

        async def scroll(self, x: int, y: int, scroll_x: int, scroll_y: int) -> None:
            await self._page.mouse.move(x, y)
            await self._page.mouse.wheel(scroll_x, scroll_y)

        async def type(self, text: str) -> None:
            await self._page.keyboard.type(text)

        async def wait(self) -> None:
            await asyncio.sleep(2)

        async def move(self, x: int, y: int) -> None:
            await self._page.mouse.move(x, y)

        async def keypress(self, keys: list[str]) -> None:
            for key in keys:
                await self._page.keyboard.press(key)

        async def drag(self, path: list[dict]) -> None:
            if not path:
                return
            start = path[0]
            await self._page.mouse.move(start["x"], start["y"])
            await self._page.mouse.down()
            for point in path[1:]:
                await self._page.mouse.move(point["x"], point["y"])
            await self._page.mouse.up()

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": WIDTH, "height": HEIGHT}
        )
        page = await context.new_page()
        await page.goto("https://news.ycombinator.com")
        await page.wait_for_load_state("networkidle")

        computer = PlaywrightComputer(page)

        agent = Agent(
            name="CUA Browser Agent",
            instructions=(
                "You are controlling a browser. "
                "Find the title and URL of the #1 story on Hacker News."
            ),
            tools=[ComputerTool(computer=computer)],
            model="gpt-5.6",
        )

        print("Running OpenAI Agents SDK CUA agent...")
        result = await Runner.run(
            agent,
            "What is the #1 story on Hacker News right now? Give me the title and URL.",
        )
        print("\n--- Agent Result ---")
        print(result.final_output)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
