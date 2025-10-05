#!/usr/bin/env python3
"""
API Connection Tester
=====================

Tests connectivity to all 5 AI APIs:
- OpenAI (GPT-4o) - substitute for Copilot
- Claude (Sonnet 4.5)
- Gemini (2.5 Pro)
- OpenAI (GPT-4 Turbo) - Codex
- DeepInfra (Qwen 2.5 Coder)

Usage:
    python scripts/automation/test_apis.py

Expected output:
    ✓ OpenAI API (GPT-4o): OK [substitute for Copilot]
    ✓ Claude API (Sonnet 4.5): OK
    ✓ Gemini API (2.5 Pro): OK
    ✓ DeepInfra API (Qwen 2.5): OK

    All APIs ready! 🎉
    Total cost this session: $0.00
"""

import asyncio
import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class APITester:
    """Test all AI APIs."""

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.results = []

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()

    async def test_openai_gpt4o(self) -> bool:
        """Test OpenAI GPT-4o (Copilot substitute)."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("✗ OpenAI API (GPT-4o): OPENAI_API_KEY not set")
            return False

        try:
            response = await self.client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o",
                    "messages": [{"role": "user", "content": "Hello"}],
                    "max_tokens": 10,
                },
            )
            response.raise_for_status()
            print("✓ OpenAI API (GPT-4o): OK [substitute for Copilot]")
            return True
        except Exception as e:
            print(f"✗ OpenAI API (GPT-4o): Failed - {e}")
            return False

    async def test_openai_gpt4_turbo(self) -> bool:
        """Test OpenAI GPT-4 Turbo (Codex)."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("✗ OpenAI API (GPT-4 Turbo): OPENAI_API_KEY not set")
            return False

        try:
            response = await self.client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4-turbo",
                    "messages": [{"role": "user", "content": "Hello"}],
                    "max_tokens": 10,
                },
            )
            response.raise_for_status()
            print("✓ OpenAI API (GPT-4 Turbo): OK [Codex/ChatGPT Plus]")
            return True
        except Exception as e:
            print(f"✗ OpenAI API (GPT-4 Turbo): Failed - {e}")
            return False

    async def test_claude(self) -> bool:
        """Test Anthropic Claude API."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("✗ Claude API (Sonnet 4.5): ANTHROPIC_API_KEY not set")
            return False

        try:
            response = await self.client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 10,
                    "messages": [{"role": "user", "content": "Hello"}],
                },
            )
            response.raise_for_status()
            print("✓ Claude API (Sonnet 4.5): OK")
            return True
        except Exception as e:
            print(f"✗ Claude API (Sonnet 4.5): Failed - {e}")
            return False

    async def test_gemini(self) -> bool:
        """Test Google Gemini API."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("✗ Gemini API (2.5 Pro): GOOGLE_API_KEY not set")
            return False

        try:
            response = await self.client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": "Hello"}]}],
                },
            )
            response.raise_for_status()
            print("✓ Gemini API (2.5 Pro): OK")
            return True
        except Exception as e:
            print(f"✗ Gemini API (2.5 Pro): Failed - {e}")
            return False

    async def test_deepinfra(self) -> bool:
        """Test DeepInfra API."""
        api_key = os.getenv("DEEPINFRA_API_KEY")
        if not api_key:
            print("✗ DeepInfra API (Qwen 2.5): DEEPINFRA_API_KEY not set")
            return False

        try:
            response = await self.client.post(
                "https://api.deepinfra.com/v1/openai/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
                    "messages": [{"role": "user", "content": "Hello"}],
                    "max_tokens": 10,
                },
            )
            response.raise_for_status()
            data = response.json()
            tokens = data["usage"]["total_tokens"]
            cost = (tokens / 1_000_000) * 0.27
            print(f"✓ DeepInfra API (Qwen 2.5): OK (cost: ${cost:.4f})")
            return True
        except Exception as e:
            print(f"✗ DeepInfra API (Qwen 2.5): Failed - {e}")
            return False

    async def test_all(self):
        """Test all APIs."""
        print("Testing API connections...\n")

        results = await asyncio.gather(
            self.test_openai_gpt4o(),
            self.test_openai_gpt4_turbo(),
            self.test_claude(),
            self.test_gemini(),
            self.test_deepinfra(),
        )

        success_count = sum(results)
        total_count = len(results)

        print(f"\n{'='*60}")
        if success_count == total_count:
            print(f"✨ All APIs ready! {success_count}/{total_count} passed 🎉")
            print("\nYou can now run:")
            print("  python scripts/automation/orchestrator.py --all")
        else:
            print(f"⚠️  {success_count}/{total_count} APIs working")
            print("\nPlease check:")
            print("  1. Environment variables are set correctly")
            print("  2. API keys are valid")
            print("  3. See API_KEYS_SETUP.md for detailed guide")
        print(f"{'='*60}\n")

        return success_count == total_count


async def main():
    """Main entry point."""
    tester = APITester()
    try:
        success = await tester.test_all()
        sys.exit(0 if success else 1)
    finally:
        await tester.close()


if __name__ == "__main__":
    asyncio.run(main())
