#!/usr/bin/env python3
"""
DeepInfra Batch Processing Script
Uses Qwen 2.5 Coder 32B for batch operations.

Budget: MAX $10 (target: $5-7)

Use ONLY when:
- Batch >10 similar files (ROI > parallel Copilot)
- Simple, repetitive tasks
- Copilot limit exceeded (unlikely)
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from openai import OpenAI  # DeepInfra is OpenAI-compatible
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()

# DeepInfra configuration
DEEPINFRA_API_KEY = os.environ.get("DEEPINFRA_API_KEY")
DEEPINFRA_BASE_URL = "https://api.deepinfra.com/v1/openai"
MODEL = "Qwen/Qwen2.5-Coder-32B-Instruct"
COST_PER_MILLION_TOKENS = 0.27  # $0.27 per 1M tokens

# Budget tracking
MAX_BUDGET = 10.0
BUDGET_FILE = Path(".deepinfra_budget.json")


class BudgetTracker:
    """Track DeepInfra spending."""

    def __init__(self):
        self.spent = 0.0
        self.tasks = []
        self.load()

    def load(self):
        """Load budget from file."""
        if BUDGET_FILE.exists():
            with open(BUDGET_FILE) as f:
                data = json.load(f)
                self.spent = data.get("spent", 0.0)
                self.tasks = data.get("tasks", [])

    def save(self):
        """Save budget to file."""
        with open(BUDGET_FILE, "w") as f:
            json.dump(
                {"spent": self.spent, "tasks": self.tasks, "remaining": MAX_BUDGET - self.spent},
                f,
                indent=2,
            )

    def log_request(self, task: str, tokens: int):
        """Log request and update spending."""
        cost = (tokens / 1_000_000) * COST_PER_MILLION_TOKENS
        self.spent += cost
        self.tasks.append({"task": task, "tokens": tokens, "cost": cost})
        self.save()
        return cost

    def check_budget(self, estimated_tokens: int) -> bool:
        """Check if we have budget for request."""
        estimated_cost = (estimated_tokens / 1_000_000) * COST_PER_MILLION_TOKENS
        return (self.spent + estimated_cost) <= MAX_BUDGET

    def get_summary(self) -> str:
        """Get spending summary."""
        table = Table(title="DeepInfra Budget Summary")
        table.add_column("Task", style="cyan")
        table.add_column("Tokens", justify="right", style="yellow")
        table.add_column("Cost", justify="right", style="green")

        for task in self.tasks:
            table.add_row(task["task"], f"{task['tokens']:,}", f"${task['cost']:.3f}")

        table.add_row("", "", "", style="bold")
        table.add_row("TOTAL", "", f"${self.spent:.2f}", style="bold green")
        table.add_row("REMAINING", "", f"${MAX_BUDGET - self.spent:.2f}", style="bold blue")

        return table


class DeepInfraBatchProcessor:
    """Process batch tasks via DeepInfra."""

    def __init__(self):
        if not DEEPINFRA_API_KEY:
            console.print("[red]ERROR: DEEPINFRA_API_KEY not set![/red]")
            console.print("Export it: export DEEPINFRA_API_KEY='your-key'")
            sys.exit(1)

        self.client = OpenAI(api_key=DEEPINFRA_API_KEY, base_url=DEEPINFRA_BASE_URL)
        self.budget = BudgetTracker()
        self.project_root = Path(__file__).parent.parent.parent

    def generate(
        self,
        task_name: str,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> Optional[str]:
        """Generate code via DeepInfra.

        Args:
            task_name: Task identifier for budget tracking
            system_prompt: System message
            user_prompt: User message
            max_tokens: Max completion tokens

        Returns:
            Generated code or None if budget exceeded
        """
        # Estimate tokens (rough: 1 token ≈ 4 chars)
        estimated_input_tokens = (len(system_prompt) + len(user_prompt)) // 4
        estimated_total_tokens = estimated_input_tokens + max_tokens

        # Check budget
        if not self.budget.check_budget(estimated_total_tokens):
            console.print(f"[red]Budget exceeded! Spent: ${self.budget.spent:.2f}[/red]")
            return None

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description=f"Generating {task_name}...", total=None)

                response = self.client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    max_tokens=max_tokens,
                    temperature=0.2,  # Lower = more deterministic
                )

            # Track usage
            tokens = response.usage.total_tokens
            cost = self.budget.log_request(task_name, tokens)

            console.print(
                f"[green]✓[/green] {task_name} generated "
                f"({tokens:,} tokens, ${cost:.3f}, "
                f"total: ${self.budget.spent:.2f})"
            )

            return response.choices[0].message.content

        except Exception as e:
            console.print(f"[red]✗ Error generating {task_name}: {e}[/red]")
            return None

    def batch_i18n_conversion(self):
        """Convert i18n files from 25 languages to 2 (pl, en).

        Estimated cost: $0.40
        """
        console.print("[bold]i18n Conversion: 25 languages → 2 (pl, en)[/bold]\n")

        # Read core context
        core_context_file = self.project_root / "context" / "_CORE_CONTEXT.md"
        if core_context_file.exists():
            core_context = core_context_file.read_text()
        else:
            core_context = ""

        # Read example language file (English)
        i18n_dir = self.project_root / "scripts" / "i18n"
        en_file = i18n_dir / "en.js"

        if not en_file.exists():
            console.print(f"[red]Error: {en_file} not found[/red]")
            return

        en_content = en_file.read_text()

        # System prompt
        system_prompt = f"""You are a translation expert specializing in i18n for web applications.

CRITICAL CONSTRAINTS (from project):
{core_context[:2000]}

Task: Convert JavaScript i18n format to JSON format for react-i18next.
Output: Clean JSON only (no code blocks, no explanations).
"""

        # Generate Polish translation
        console.print("\n1. Generating Polish (pl.json)...")
        pl_prompt = f"""Convert this i18n file to Polish (Poland locale).

Source (English):
```javascript
{en_content}
```

Requirements:
1. Output valid JSON for react-i18next
2. Translate all values to Polish
3. Keep all keys in English (e.g., "login", "subscription_name")
4. Use formal Polish ("Pan/Pani")
5. Currency format: "123 456,78 zł" (space as thousand separator)

Output ONLY the JSON, no markdown code blocks.
"""

        pl_json = self.generate("i18n_pl", system_prompt, pl_prompt, max_tokens=8192)

        if pl_json:
            # Save Polish
            output_dir = self.project_root / "frontend" / "src" / "locales"
            output_dir.mkdir(parents=True, exist_ok=True)
            (output_dir / "pl.json").write_text(pl_json)
            console.print(f"[green]✓[/green] Saved to frontend/src/locales/pl.json")

        # Generate English translation (convert from .js to .json)
        console.print("\n2. Generating English (en.json)...")
        en_prompt = f"""Convert this i18n file to clean JSON for react-i18next.

Source:
```javascript
{en_content}
```

Requirements:
1. Output valid JSON
2. Keep all English text
3. Remove JavaScript syntax (const, export, etc.)

Output ONLY the JSON, no markdown code blocks.
"""

        en_json = self.generate("i18n_en", system_prompt, en_prompt, max_tokens=8192)

        if en_json:
            (output_dir / "en.json").write_text(en_json)
            console.print(f"[green]✓[/green] Saved to frontend/src/locales/en.json")

        # Summary
        console.print(f"\n[bold green]i18n conversion complete![/bold green]")
        console.print(self.budget.get_summary())

    def batch_react_components(self, component_names: List[str]):
        """Generate simple React components in batch.

        Args:
            component_names: List of component names to generate

        Estimated cost: ~$1.50-2.00 for 15-20 components
        """
        console.print(f"[bold]React Components Batch ({len(component_names)} files)[/bold]\n")

        # Read core context
        core_context_file = self.project_root / "context" / "_CORE_CONTEXT.md"
        core_context = core_context_file.read_text() if core_context_file.exists() else ""

        system_prompt = f"""You are a React + TypeScript + Material-UI expert.

CRITICAL CONSTRAINTS:
{core_context[:2000]}

Generate clean, production-ready React components.
Output: TypeScript code only (no explanations).
"""

        for component_name in component_names:
            console.print(f"\nGenerating {component_name}...")

            user_prompt = f"""Generate {component_name} React component.

Requirements:
1. TypeScript with strict types (NO any)
2. Material-UI components ONLY
3. React Hook Form + Zod for forms (if applicable)
4. Proper props interface
5. Google-style JSDoc comments

Component: {component_name}

Output ONLY the TypeScript code, no markdown.
"""

            code = self.generate(
                f"component_{component_name}", system_prompt, user_prompt, max_tokens=4096
            )

            if code:
                # Save component
                output_file = (
                    self.project_root / "frontend" / "src" / "components" / f"{component_name}.tsx"
                )
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(code)
                console.print(f"[green]✓[/green] Saved to {output_file}")

        # Summary
        console.print(f"\n[bold green]React components generated![/bold green]")
        console.print(self.budget.get_summary())


def main():
    parser = argparse.ArgumentParser(description="DeepInfra Batch Processing")
    parser.add_argument(
        "--task",
        choices=["i18n", "components", "budget"],
        required=True,
        help="Task to run",
    )
    parser.add_argument(
        "--components",
        nargs="+",
        help="Component names for batch generation",
    )

    args = parser.parse_args()

    processor = DeepInfraBatchProcessor()

    if args.task == "budget":
        # Show budget summary
        console.print(processor.budget.get_summary())

    elif args.task == "i18n":
        processor.batch_i18n_conversion()

    elif args.task == "components":
        if not args.components:
            console.print("[red]Error: --components required[/red]")
            sys.exit(1)
        processor.batch_react_components(args.components)


if __name__ == "__main__":
    main()
