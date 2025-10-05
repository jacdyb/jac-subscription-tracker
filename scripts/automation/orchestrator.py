#!/usr/bin/env python3
"""
AI Automation Orchestrator - Main Engine
==========================================

Fully automated refactoring orchestration using 5 AI APIs:
- OpenAI (GPT-4o) - 90% tasks, unlimited
- Claude (Sonnet 4.5) - 5% complex logic
- Gemini (2.5 Pro) - 3% validation
- OpenAI (GPT-4 Turbo) - 2% algorithms
- DeepInfra (Qwen 2.5) - <1% batch

Reference: AI_STRATEGY.md, config/ai_models.yaml
"""

import asyncio
import json
import os
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "ai_models.yaml"
CORE_CONTEXT_PATH = PROJECT_ROOT / "context" / "_CORE_CONTEXT.md"
BUDGET_FILE = PROJECT_ROOT / ".deepinfra_budget.json"
LOG_FILE = PROJECT_ROOT / ".ai_requests.log"


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class TaskResult:
    """Result of a task execution."""
    task_name: str
    status: TaskStatus
    output: Optional[str] = None
    error: Optional[str] = None
    cost: float = 0.0
    tokens: int = 0
    duration: float = 0.0


class BudgetTracker:
    """Track DeepInfra spending."""

    def __init__(self, max_budget: float = 10.0, target_budget: float = 7.0):
        self.max_budget = max_budget
        self.target_budget = target_budget
        self.spent = 0.0
        self.tasks: List[Dict[str, Any]] = []
        self.load()

    def load(self):
        """Load budget from file."""
        if BUDGET_FILE.exists():
            data = json.loads(BUDGET_FILE.read_text())
            self.spent = data.get("spent", 0.0)
            self.tasks = data.get("tasks", [])

    def save(self):
        """Save budget to file."""
        data = {
            "spent": self.spent,
            "max_budget": self.max_budget,
            "target_budget": self.target_budget,
            "tasks": self.tasks,
        }
        BUDGET_FILE.write_text(json.dumps(data, indent=2))

    def log_request(self, task: str, tokens: int, cost: float):
        """Log DeepInfra request."""
        self.spent += cost
        self.tasks.append({
            "task": task,
            "tokens": tokens,
            "cost": cost,
        })
        self.save()

        if self.spent >= self.max_budget:
            raise ValueError(f"❌ Budget exceeded! Spent: ${self.spent:.2f} / Max: ${self.max_budget:.2f}")
        if self.spent >= self.target_budget:
            print(f"⚠️  Warning: Approaching target budget! Spent: ${self.spent:.2f} / Target: ${self.target_budget:.2f}")

    def get_remaining(self) -> float:
        """Get remaining budget."""
        return self.max_budget - self.spent


class APIClient:
    """Universal API client for all providers."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.budget_tracker = BudgetTracker()
        self.client = httpx.AsyncClient(timeout=120.0)

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()

    async def call_openai(
        self, model: str, prompt: str, context: str = ""
    ) -> Tuple[str, int]:
        """Call OpenAI API (GPT-4o or GPT-4 Turbo)."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")

        messages = []
        if context:
            messages.append({"role": "system", "content": context})
        messages.append({"role": "user", "content": prompt})

        response = await self.client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": 0.3,
            },
        )
        response.raise_for_status()
        data = response.json()

        content = data["choices"][0]["message"]["content"]
        tokens = data["usage"]["total_tokens"]
        return content, tokens

    async def call_claude(self, prompt: str, context: str = "") -> Tuple[str, int]:
        """Call Anthropic Claude API."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")

        system_prompt = context if context else "You are an expert Python/React developer."

        response = await self.client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 8000,
                "system": system_prompt,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        response.raise_for_status()
        data = response.json()

        content = data["content"][0]["text"]
        tokens = data["usage"]["input_tokens"] + data["usage"]["output_tokens"]
        return content, tokens

    async def call_gemini(self, prompt: str, context: str = "") -> Tuple[str, int]:
        """Call Google Gemini API."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not set")

        full_prompt = f"{context}\n\n{prompt}" if context else prompt

        response = await self.client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": full_prompt}]}],
                "generationConfig": {"temperature": 0.3},
            },
        )
        response.raise_for_status()
        data = response.json()

        content = data["candidates"][0]["content"]["parts"][0]["text"]
        # Gemini doesn't return token count in response, estimate
        tokens = len(full_prompt.split()) * 2  # Rough estimate
        return content, tokens

    async def call_deepinfra(self, prompt: str, context: str = "") -> Tuple[str, int]:
        """Call DeepInfra API (Qwen 2.5 Coder)."""
        api_key = os.getenv("DEEPINFRA_API_KEY")
        if not api_key:
            raise ValueError("DEEPINFRA_API_KEY not set")

        messages = []
        if context:
            messages.append({"role": "system", "content": context})
        messages.append({"role": "user", "content": prompt})

        response = await self.client.post(
            "https://api.deepinfra.com/v1/openai/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
                "messages": messages,
                "temperature": 0.3,
            },
        )
        response.raise_for_status()
        data = response.json()

        content = data["choices"][0]["message"]["content"]
        tokens = data["usage"]["total_tokens"]
        cost = (tokens / 1_000_000) * 0.27  # $0.27/1M tokens

        # Track budget
        self.budget_tracker.log_request("deepinfra_request", tokens, cost)

        return content, tokens

    async def call_api(
        self, provider: str, model: str, prompt: str, context: str = ""
    ) -> Tuple[str, int]:
        """Call appropriate API based on provider.model."""
        if provider == "openai" or provider == "copilot":
            return await self.call_openai(model, prompt, context)
        elif provider == "claude":
            return await self.call_claude(prompt, context)
        elif provider == "gemini":
            return await self.call_gemini(prompt, context)
        elif provider == "deepinfra":
            return await self.call_deepinfra(prompt, context)
        elif provider == "codex":
            # Codex = OpenAI GPT-4 Turbo
            return await self.call_openai("gpt-4-turbo", prompt, context)
        else:
            raise ValueError(f"Unknown provider: {provider}")


class Orchestrator:
    """Main orchestration engine."""

    def __init__(self, config_path: Path = CONFIG_PATH):
        self.config = yaml.safe_load(config_path.read_text())
        self.client = APIClient(self.config)
        self.core_context = self._load_core_context()
        self.results: List[TaskResult] = []

    def _load_core_context(self) -> str:
        """Load core context template."""
        if CORE_CONTEXT_PATH.exists():
            return CORE_CONTEXT_PATH.read_text()
        return ""

    def _parse_model_reference(self, model_ref: str) -> Tuple[str, str]:
        """Parse 'provider.model' reference."""
        parts = model_ref.split(".")
        if len(parts) != 2:
            raise ValueError(f"Invalid model reference: {model_ref}")
        return parts[0], parts[1]

    async def run_task(
        self, task_name: str, task_config: Dict[str, Any]
    ) -> TaskResult:
        """Run a single task."""
        import time

        start_time = time.time()

        try:
            # Parse primary model
            primary_ref = task_config.get("primary")
            if not primary_ref:
                return TaskResult(
                    task_name=task_name,
                    status=TaskStatus.FAILED,
                    error="No primary model specified",
                )

            provider, model = self._parse_model_reference(primary_ref)

            # Build prompt
            prompt = f"Task: {task_config.get('description', task_name)}\n\n"
            prompt += "Generate the required code following all constraints."

            # Call API
            print(f"  ▶ Running: {task_name} ({primary_ref})...")
            output, tokens = await self.client.call_api(
                provider, model, prompt, self.core_context
            )

            duration = time.time() - start_time

            result = TaskResult(
                task_name=task_name,
                status=TaskStatus.COMPLETED,
                output=output,
                tokens=tokens,
                duration=duration,
            )

            print(f"  ✓ Completed: {task_name} ({tokens} tokens, {duration:.1f}s)")
            return result

        except Exception as e:
            duration = time.time() - start_time
            result = TaskResult(
                task_name=task_name,
                status=TaskStatus.FAILED,
                error=str(e),
                duration=duration,
            )
            print(f"  ✗ Failed: {task_name} - {e}")
            return result

    async def run_parallel_tasks(
        self, task_configs: Dict[str, Dict[str, Any]], max_parallel: int = 8
    ) -> List[TaskResult]:
        """Run multiple tasks in parallel."""
        tasks = []
        for task_name, task_config in task_configs.items():
            parallel = task_config.get("parallel", False)
            if parallel:
                tasks.append(self.run_task(task_name, task_config))

        # Run in batches
        results = []
        for i in range(0, len(tasks), max_parallel):
            batch = tasks[i : i + max_parallel]
            print(f"\n📦 Running batch {i // max_parallel + 1} ({len(batch)} tasks)...")
            batch_results = await asyncio.gather(*batch)
            results.extend(batch_results)

        return results

    async def run_phase(self, phase_name: str):
        """Run a specific phase (e.g., 'backend', 'frontend')."""
        tasks_config = self.config.get("tasks", {})

        # Filter tasks for this phase (you can customize this logic)
        phase_tasks = {
            name: config
            for name, config in tasks_config.items()
            if phase_name.lower() in name.lower()
        }

        if not phase_tasks:
            print(f"⚠️  No tasks found for phase: {phase_name}")
            return

        print(f"\n🚀 Starting phase: {phase_name}")
        print(f"   Tasks: {len(phase_tasks)}")

        results = await self.run_parallel_tasks(phase_tasks)
        self.results.extend(results)

        # Summary
        completed = sum(1 for r in results if r.status == TaskStatus.COMPLETED)
        failed = sum(1 for r in results if r.status == TaskStatus.FAILED)
        total_tokens = sum(r.tokens for r in results)

        print(f"\n✨ Phase complete: {phase_name}")
        print(f"   ✓ Completed: {completed}")
        print(f"   ✗ Failed: {failed}")
        print(f"   📊 Total tokens: {total_tokens:,}")

    async def run_all(self):
        """Run all tasks."""
        tasks_config = self.config.get("tasks", {})

        print(f"\n🚀 Starting full automation")
        print(f"   Total tasks: {len(tasks_config)}")

        results = await self.run_parallel_tasks(tasks_config)
        self.results.extend(results)

        # Final summary
        completed = sum(1 for r in results if r.status == TaskStatus.COMPLETED)
        failed = sum(1 for r in results if r.status == TaskStatus.FAILED)
        total_tokens = sum(r.tokens for r in results)
        total_duration = sum(r.duration for r in results)

        print(f"\n✨ Automation complete!")
        print(f"   ✓ Completed: {completed}")
        print(f"   ✗ Failed: {failed}")
        print(f"   📊 Total tokens: {total_tokens:,}")
        print(f"   ⏱️  Total time: {total_duration:.1f}s")
        print(f"   💰 DeepInfra spent: ${self.client.budget_tracker.spent:.2f}")

    async def close(self):
        """Cleanup."""
        await self.client.close()


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="AI Automation Orchestrator")
    parser.add_argument(
        "--phase",
        type=str,
        help="Run specific phase (e.g., 'backend', 'frontend')",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all tasks",
    )
    args = parser.parse_args()

    orchestrator = Orchestrator()

    try:
        if args.all:
            await orchestrator.run_all()
        elif args.phase:
            await orchestrator.run_phase(args.phase)
        else:
            print("Usage:")
            print("  python orchestrator.py --all              # Run all tasks")
            print("  python orchestrator.py --phase backend    # Run backend phase")
            print("  python orchestrator.py --phase frontend   # Run frontend phase")
    finally:
        await orchestrator.close()


if __name__ == "__main__":
    asyncio.run(main())
