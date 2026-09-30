"""
Browser-Use Agent Demo
======================
Launches a headless browser agent that navigates to Hacker News,
finds the top story, and returns the result.

Usage:
    export OPENAI_API_KEY=sk-...
    python scripts/browser_agent_demo.py

Requires: browser-use, playwright (installed via requirements.txt)
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    from browser_use import Agent, Browser, ChatOpenAI

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print(
            "OPENAI_API_KEY is not set. "
            "Export it or add it to .env to run the full agent.\n"
            "Running a minimal Playwright-only smoke test instead...\n"
        )
        await _playwright_smoke_test()
        return

    llm = ChatOpenAI(model="gpt-4o-mini")
    browser = Browser(headless=True)

    agent = Agent(
        task="Go to https://news.ycombinator.com and return the title and URL of the #1 story.",
        llm=llm,
        browser=browser,
    )

    result = await agent.run()
    print("\n--- Agent Result ---")
    print(result)


async def _playwright_smoke_test() -> None:
    """Verify Playwright + Chromium work without an LLM key."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://news.ycombinator.com")
        title = await page.title()
        top_item = await page.text_content(".titleline > a")
        await browser.close()

    print(f"Page title : {title}")
    print(f"Top story  : {top_item}")
    print("\nPlaywright smoke test passed.")


if __name__ == "__main__":
    asyncio.run(main())
