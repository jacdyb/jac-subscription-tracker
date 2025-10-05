# AUTOMATION PLAN - AI-Assisted Refactor

**Projekt:** Wallos PHP → Python + React
**Wersja:** 1.0
**Data:** 2025-01-XX

---

## Spis Treści

1. [Overview](#overview)
2. [AI Models & Licenses](#ai-models--licenses)
3. [Context Protection](#context-protection)
4. [AI Tools Setup](#ai-tools-setup)
5. [Automation Strategy](#automation-strategy)
6. [Phase-by-Phase Automation](#phase-by-phase-automation)
7. [Orchestration Scripts](#orchestration-scripts)
8. [Quality Gates](#quality-gates)
9. [Monitoring & Progress Tracking](#monitoring--progress-tracking)
10. [Prompt Library](#prompt-library)
11. [Troubleshooting](#troubleshooting)

---

## Overview

### Cel
Automatyzacja maksymalnie dużej części refactoru (60-70%) przy wykorzystaniu AI tools dostępnych w VS Code, zachowując wysoką jakość kodu i pełną kontrolę nad procesem.

### AI Tools Stack
- **Claude Code** (Claude Pro) - complex logic, multi-file operations, architecture
- **GitHub Copilot** (Copilot Pro) - boilerplate code, tests, quick completions
- **Gemini Code Assist** (Google AI Pro) - validation, code review (1M context!)
- **ChatGPT Plus** (GPT-4 Turbo) - algorithms, debugging, edge cases
- **DeepInfra** (Qwen 2.5 Coder) - batch processing (budget: $10)

### Kluczowe Zasady
1. **AI generuje → Human review → Commit** (nigdy na odwrót)
2. **Small iterations** - małe, atomiczne zmiany
3. **Test-driven** - testy przed/z kodem
4. **Version control** - commit po każdej fazie
5. **Quality gates** - automatyczna walidacja przed merge
6. **Model selection** - wybór optymalnego modelu do zadania (GPT-4o free tier dla 90% tasków)

### Estymowany Stopień Automatyzacji

| Kategoria | Automatyzacja | Czas manualny | Czas z AI |
|-----------|---------------|---------------|-----------|
| **Database Models** | 85% | 1 tydzień | 1-2 dni |
| **Pydantic Schemas** | 90% | 3 dni | 4-6 godzin |
| **API Endpoints** | 70% | 2 tygodnie | 5-6 dni |
| **Services (Business Logic)** | 60% | 2 tygodnie | 1 tydzień |
| **Tests (Backend)** | 80% | 1 tydzień | 2 dni |
| **React Components** | 75% | 3 tygodnie | 1 tydzień |
| **Tests (Frontend)** | 75% | 1 tydzień | 2-3 dni |
| **Documentation** | 90% | 3 dni | 4-6 godzin |
| **Overall** | **~65-70%** | **11-15 tyg** | **5-6 tyg** |

---

## AI Models & Licenses

### Pełna Specyfikacja

**Szczegółowa dokumentacja:** [AI_MODELS_REFERENCE.md](./AI_MODELS_REFERENCE.md)

### Podsumowanie Modeli

| License | Monthly Cost | Primary Model | Context | Daily Limit | Use Case |
|---------|--------------|---------------|---------|-------------|----------|
| **Claude Pro** | $20 | Claude Sonnet 4.5 | 200k | ~500 msg | Complex logic, architecture |
| **Copilot Pro** | $10 | GPT-4o (free tier) | 128k | Unlimited | Boilerplate (90% tasks) |
| **ChatGPT Plus** | $20 | GPT-4 Turbo | 128k | ~40-80/3h | Algorithms, debugging |
| **Google AI Pro** | $0 | Gemini 2.5 Pro | **1M** | 1000/day | Validation, review |
| **DeepInfra** | Pay-per-use | Qwen 2.5 Coder 32B | 32k | None | Batch ($10 total) |

### Model Selection Strategy (4 Pillars + Batch)

**Primary (90% tasks):** GPT-4o (Copilot Pro, free tier) - $0
**Complex logic (5%):** Claude Sonnet 4.5 (Claude Code) - $0
**Validation (3%):** Gemini 2.5 Pro (Google AI Pro) - $0
**Algorithms (2%):** GPT-4 Turbo (ChatGPT Plus) - $0
**Batch (<1%):** Qwen 2.5 Coder (DeepInfra) - $10 total

**TOTAL PROJECT COST:** $10 (DeepInfra tylko)

### DeepInfra Budget Allocation ($10)

1. i18n conversion (25 lang files → 2): **$0.40**
2. PHP→Python services (batch): **$3.00**
3. React components (batch): **$2.00**
4. Buffer: **$4.60**

---

## Context Protection

### Problem
AI conversations are subject to context compression after ~200k tokens. Critical project constraints (SQLite ONLY, MUI ONLY, 2 languages ONLY) MUST NOT be lost.

### 5-Mechanism Protection Strategy

#### Mechanism 1: Core Context Files

```
context/
├── _CORE_CONTEXT.md           # ALWAYS included in ALL prompts
├── _CURRENT_PHASE.md          # Phase tracking
├── _PREVIOUS_DECISIONS.md     # Decision log
└── phase1/
    ├── models_context.md
    ├── schemas_context.md
    └── ...
```

**`context/_CORE_CONTEXT.md`** - Always injected into prompts:
```markdown
# CORE PROJECT CONTEXT - DO NOT DEVIATE

## CRITICAL CONSTRAINTS (NEVER FORGET)

1. **Database:** SQLite ONLY - NO PostgreSQL
2. **UI Library:** Material-UI v5 ONLY - NO Chakra, NO Radix
3. **Languages:** Polish + English ONLY - NOT 25 languages
4. **Auth:** JWT + API Key ONLY - NO OIDC/OAuth
5. **Notifications:** Webhooks ONLY - NO email/discord/telegram
6. **Calendar:** OUT OF SCOPE
7. **AI Recommendations:** OUT OF SCOPE

## BUSINESS RULES (CRITICAL)

1. **Price:** MUST be > 0
2. **Frequency:** 1-365
3. **Cycle:** days|weeks|months|years ONLY
4. **Category ID=1:** CANNOT be deleted (default)
5. **User ownership:** ALWAYS check user_id
6. **Cascade deletes:** When user deleted → delete all related

## CODE STYLE REQUIREMENTS

### Backend (Python):
- Type hints EVERYWHERE (Python 3.11+)
- Docstrings: Google style
- Async/await for all DB operations
- Tests: >80% coverage REQUIRED

### Frontend (TypeScript):
- TypeScript strict mode
- NO `any` types
- Material-UI components ONLY
- React Hook Form + Zod for forms
```

#### Mechanism 2: Prompt Templates

**File:** `prompts/templates/base_template.txt`
```
{CORE_CONTEXT}

---

SESSION-ID: {session_id}
PHASE: {current_phase}
LAST COMPLETED: {last_completed_task}
CURRENTLY: {current_task}
NEXT: {next_task}

---

{TASK_SPECIFIC_PROMPT}

---

VALIDATION CHECKLIST (before responding):
- [ ] SQLite only (no PostgreSQL mentioned)
- [ ] Material-UI only (no Chakra/Radix)
- [ ] Polish + English only (not 25 languages)
- [ ] Type hints everywhere (Python)
- [ ] Strict TypeScript (no `any`)
```

#### Mechanism 3: Validation Checksums

**File:** `scripts/automation/context_validator.py`
```python
#!/usr/bin/env python3
"""
Validate AI output against core constraints.
"""
import re
from pathlib import Path
from typing import List, Tuple
from rich.console import Console

console = Console()

class ContextValidator:
    """Validate AI-generated code against project constraints."""

    VIOLATIONS = {
        'postgresql': r'(?i)(postgresql|postgres|psycopg2)',
        'chakra': r'(?i)(chakra[-\s]ui|@chakra-ui)',
        'radix': r'(?i)(radix[-\s]ui|@radix-ui)',
        'oidc': r'(?i)(oidc|oauth|auth0|keycloak)',
        'wrong_languages': r'(?i)(i18n.*(?:fr|de|es|it|nl|sv|da|fi|no|pt|ru|zh|ja|ko))',
        'email_notif': r'(?i)(nodemailer|sendgrid|smtp|email.*notif)',
        'discord_notif': r'(?i)(discord\.js|discord.*webhook)',
        'telegram_notif': r'(?i)(telegram.*bot|telebot)',
    }

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def validate_file(self, file_path: Path) -> List[Tuple[str, str]]:
        """Check single file for violations.

        Returns:
            List of (violation_type, line) tuples
        """
        violations = []

        if not file_path.exists():
            return violations

        content = file_path.read_text()

        for violation_name, pattern in self.VIOLATIONS.items():
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                line_no = content[:match.start()].count('\n') + 1
                line = content.split('\n')[line_no - 1]
                violations.append((violation_name, f"L{line_no}: {line.strip()}"))

        return violations

    def validate_directory(self, directory: Path) -> bool:
        """Validate all files in directory.

        Returns:
            True if no violations, False otherwise
        """
        console.print(f"[yellow]Validating {directory}...[/yellow]")

        all_violations = {}

        for file_path in directory.rglob('*.py'):
            violations = self.validate_file(file_path)
            if violations:
                all_violations[str(file_path)] = violations

        for file_path in directory.rglob('*.ts*'):
            violations = self.validate_file(file_path)
            if violations:
                all_violations[str(file_path)] = violations

        if all_violations:
            console.print("[bold red]✗ CONSTRAINT VIOLATIONS DETECTED![/bold red]\n")

            for file_path, violations in all_violations.items():
                console.print(f"[red]{file_path}:[/red]")
                for violation_type, line in violations:
                    console.print(f"  - {violation_type}: {line}")
                console.print()

            return False
        else:
            console.print("[green]✓ No constraint violations[/green]")
            return True

    def validate_type_hints(self, backend_dir: Path) -> bool:
        """Check if all Python files have type hints."""
        console.print("[yellow]Validating type hints...[/yellow]")

        import subprocess
        result = subprocess.run(
            ['mypy', str(backend_dir), '--strict'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            console.print("[green]✓ All type hints present[/green]")
            return True
        else:
            console.print("[red]✗ Type hint errors:[/red]")
            console.print(result.stdout)
            return False

if __name__ == '__main__':
    validator = ContextValidator(Path.cwd())

    backend_ok = validator.validate_directory(Path('backend'))
    frontend_ok = validator.validate_directory(Path('frontend'))
    types_ok = validator.validate_type_hints(Path('backend/app'))

    if backend_ok and frontend_ok and types_ok:
        console.print("[bold green]✓ All validations passed![/bold green]")
        exit(0)
    else:
        console.print("[bold red]✗ Validation failed - review AI output![/bold red]")
        exit(1)
```

**Usage:**
```bash
# After AI generates code
python scripts/automation/context_validator.py

# In git pre-commit hook
python scripts/automation/context_validator.py || exit 1
```

#### Mechanism 4: Session Continuity Markers

Every AI prompt includes:
```markdown
SESSION-ID: 2025-01-15-001
PHASE: Phase 1 - Backend Foundation
LAST COMPLETED: SQLAlchemy models (8/8)
CURRENTLY: Pydantic schemas (6/10)
NEXT: API routes

CONTEXT REMINDER:
- SQLite ONLY
- MUI v5 ONLY
- PL+EN ONLY
```

#### Mechanism 5: Model-Specific Context Strategies

**GPT-4o (short context):**
- Include only CORE_CONTEXT.md
- Current task details
- Minimal examples

**Gemini 2.5 Pro (1M context):**
- Include FULL context (all previous decisions, entire codebase)
- Complete validation
- Comprehensive review

**Claude Sonnet 4.5 (200k context):**
- Include CORE_CONTEXT.md
- Current phase context
- Related files only

### Recovery Instructions

**File:** `.context_checkpoint.md` (see root directory)

If context is lost:
1. READ `.context_checkpoint.md`
2. READ `context/_CORE_CONTEXT.md`
3. READ `AI_MODELS_REFERENCE.md`
4. CHECK `context/_CURRENT_PHASE.md`
5. RESUME from current task

---

## AI Tools Setup

### Prerequisites

#### 1. VS Code Extensions (już zainstalowane)
```bash
# Sprawdź installed extensions
code --list-extensions | grep -E 'github|copilot|claude|gemini'
```

Wymagane:
- ✅ GitHub Copilot (`GitHub.copilot`)
- ✅ GitHub Copilot Chat (`GitHub.copilot-chat`)
- ✅ Claude Code (native interface - ten, który używasz)
- ✅ Gemini Code Assist (jeśli masz dostęp)

#### 2. Brak potrzeby API Keys
**WAŻNE:** Wszystkie tools działają przez VS Code OAuth, nie potrzebujesz hardcoded API keys w skryptach.

#### 3. Python Environment (dla orchestration scripts)
```bash
# Setup virtual environment
cd /Users/jacekdybowski/projects/jac-subscription-tracker
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install click rich anthropic google-generativeai openai
```

#### 4. VS Code Settings
`.vscode/settings.json`:
```json
{
  "github.copilot.enable": {
    "*": true,
    "python": true,
    "typescript": true,
    "typescriptreact": true
  },
  "github.copilot.chat.codeGeneration.instructions": [
    "Always use type hints in Python (Python 3.11+)",
    "Use Material-UI components in React",
    "Follow SOLID principles",
    "Add docstrings to all functions"
  ],
  "editor.formatOnSave": true,
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "typescript.format.enable": true,
  "eslint.enable": true
}
```

---

## Automation Strategy

### 1. Delegation Model

```
┌─────────────────────────────────────────────────────────┐
│  YOU (Human)                                            │
│  - Define requirements (USER_STORIES.md)               │
│  - Review & approve AI output                          │
│  - Make critical decisions                             │
│  - Final quality check                                 │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  ORCHESTRATION LAYER (Python scripts)                   │
│  - Batch processing PHP → Python                        │
│  - Parallel AI execution                                │
│  - Quality validation                                   │
│  - Progress tracking                                    │
└─────────────────────────────────────────────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Claude Code     │  │  Copilot         │  │  Gemini          │
│  (Primary)       │  │  (Assistant)     │  │  (Validator)     │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│ - Complex logic  │  │ - Boilerplate    │  │ - Code review    │
│ - Multi-file ops │  │ - Tests          │  │ - Alternative    │
│ - Refactoring    │  │ - Completions    │  │   solutions      │
│ - Architecture   │  │ - Quick fixes    │  │ - Validation     │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

### 2. Task Assignment Matrix

| Task Type | Primary AI | Secondary AI | Cost | Human Role |
|-----------|-----------|--------------|------|------------|
| **DB Schema → SQLAlchemy** | GPT-4o (free) | Claude S4.5 (complex) | $0 | Review relationships |
| **Pydantic Schemas** | GPT-4o (free) | Gemini 2.5 Pro (validation) | $0 | Type safety check |
| **API Routes** | GPT-4o (free) | Claude S4.5 (complex endpoints) | $0 | Logic review |
| **Service Layer** | Claude S4.5 | Qwen 2.5 Coder (batch) | $0-3 | **Critical review** |
| **Unit Tests** | GPT-4o (free) | GPT-4 Turbo (edge cases) | $0 | Edge cases |
| **React Components** | GPT-4o (free) | Qwen 2.5 Coder (batch) | $0-2 | UX decisions |
| **React Hooks** | GPT-4o (free) | Claude S4.5 (complex) | $0 | Quick review |
| **Type Definitions** | Codegen (OpenAPI) | - | $0 | Review |
| **Documentation** | GPT-4o (free) | - | $0 | Final polish |
| **i18n Conversion** | Qwen 2.5 Coder (batch) | - | $0.40 | Verify translations |
| **Code Review** | Gemini 2.5 Pro (1M context) | - | $0 | Final approval |

### 3. Workflow Pattern

**Standard Iteration:**
```
1. Human defines requirement (from USER_STORIES.md)
   ↓
2. AI generates code (Claude Code primary)
   ↓
3. Automated validation (linters, type checkers)
   ↓
4. AI generates tests (Copilot)
   ↓
5. Run tests (pytest/vitest)
   ↓
6. Human review (code + tests)
   ↓
7. Commit if approved
   ↓
8. Move to next task
```

**Batch Processing (for repetitive tasks):**
```
1. Human defines pattern (e.g., "generate CRUD for categories")
   ↓
2. Orchestration script identifies all similar tasks
   ↓
3. Parallel AI execution (Claude + Copilot + Gemini)
   ↓
4. Automated validation + test generation
   ↓
5. Human reviews batch (not individual files)
   ↓
6. Bulk commit if approved
```

---

## Phase-by-Phase Automation

### PREPARATION Phase (1-2 days)

#### Task 1: Database Schema Extraction & Analysis

**Tool:** Claude Code + manual inspection

**Process:**
```bash
# 1. Extract schema
sqlite3 db/wallos.db .schema > analysis/schema.sql

# 2. Generate ER diagram (optional)
# Use dbdiagram.io or similar
```

**Claude Code Prompt:**
```
Analyze the SQLite schema in analysis/schema.sql.

For each table, document:
1. Table name
2. Columns (name, type, constraints)
3. Foreign keys (relationships)
4. Indexes
5. Business logic implications

Output: analysis/database_analysis.md

Format:
## Table: subscriptions
- **id**: INTEGER PRIMARY KEY
- **user_id**: INTEGER, FK → users.id
- **name**: TEXT NOT NULL
...
Relationships:
- MANY-TO-ONE: subscription → user
- MANY-TO-ONE: subscription → category
...
```

**Automation:** 90%
**Human Task:** Review relationships, validate constraints

---

#### Task 2: PHP Endpoint Inventory

**Tool:** Orchestration Script + Claude Code

**Script:** `scripts/automation/analyze_php_endpoints.py`

```python
#!/usr/bin/env python3
"""
Analyze all PHP endpoints and generate inventory.
"""
import os
from pathlib import Path
import json

def scan_php_files(directory):
    """Scan all PHP files in directory."""
    php_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.php'):
                path = os.path.join(root, file)
                php_files.append({
                    'path': path,
                    'relative': os.path.relpath(path, directory),
                    'size': os.path.getsize(path)
                })
    return php_files

def main():
    base_dir = '/Users/jacekdybowski/projects/jac-subscription-tracker'
    endpoints_dir = os.path.join(base_dir, 'endpoints')
    api_dir = os.path.join(base_dir, 'api')

    endpoints = scan_php_files(endpoints_dir)
    api_files = scan_php_files(api_dir)

    inventory = {
        'endpoints': endpoints,
        'api': api_files,
        'total_count': len(endpoints) + len(api_files)
    }

    # Save inventory
    with open('analysis/php_inventory.json', 'w') as f:
        json.dump(inventory, f, indent=2)

    print(f"✓ Found {inventory['total_count']} PHP files")
    print(f"  - Endpoints: {len(endpoints)}")
    print(f"  - API: {len(api_files)}")
    print(f"  - Saved to: analysis/php_inventory.json")

if __name__ == '__main__':
    main()
```

**Run:**
```bash
python scripts/automation/analyze_php_endpoints.py
```

**Claude Code Prompt (for each endpoint):**
```
Analyze PHP endpoint: {file_path}

Extract:
1. HTTP method (GET/POST/DELETE/etc.)
2. Route/URL pattern
3. Input parameters (GET/POST/FILES)
4. Database operations (SELECT/INSERT/UPDATE/DELETE)
5. Response format (JSON/redirect/file)
6. Business logic summary
7. Dependencies (other files, APIs)

Output: JSON format
{
  "method": "POST",
  "route": "/endpoints/subscription/add.php",
  "inputs": {...},
  "database": [...],
  "response_type": "json",
  "logic_summary": "Creates new subscription with logo upload",
  "dependencies": ["getsettings.php", "inputvalidation.php"]
}
```

**Automation:** 85%
**Human Task:** Validate business logic extraction

---

### PHASE 1: Backend Foundation (4-5 days with AI)

#### Task 1.1: Generate SQLAlchemy Models

**AI Model:** GPT-4o (Copilot Pro, free tier)
**Cost:** $0
**Fallback:** Claude Sonnet 4.5 (if complex relationships)

**Input:**
- `analysis/schema.sql`
- `analysis/database_analysis.md`

**Claude Code Prompt:**
```
Generate SQLAlchemy 2.0 models from database schema.

Requirements:
- One model per table
- Async support (AsyncSession)
- Full type hints (Python 3.11+)
- Relationships with backref
- __repr__ for debugging
- Docstrings (Google style)

Tables to generate:
1. User (users)
2. Subscription (subscriptions)
3. Category (categories)
4. Currency (currencies)
5. PaymentMethod (payment_methods)
6. HouseholdMember (household_members)
7. NotificationSettings (notification_settings)
8. Settings (settings)

Output files:
- backend/app/models/user.py
- backend/app/models/subscription.py
- ... (8 files total)

Follow this pattern for each model:
```python
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class Subscription(Base):
    \"\"\"Subscription model representing recurring payments.

    Attributes:
        id: Primary key
        user_id: Foreign key to users table
        name: Subscription name
        ...
    \"\"\"
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ...

    # Relationships
    user = relationship("User", back_populates="subscriptions")
    category = relationship("Category")
    ...

    def __repr__(self) -> str:
        return f"<Subscription(id={self.id}, name={self.name})>"
```
```

**Expected Output:** 8 Python files in `backend/app/models/`

**Validation (Automatic):**
```bash
# Type checking
mypy backend/app/models/

# Linting
ruff check backend/app/models/

# Import test
python -c "from app.models.user import User; print('✓ Models import successfully')"
```

**Automation:** 90%
**Human Task:** Review relationships (10-15 min)

---

#### Task 1.2: Generate Pydantic Schemas

**AI Model:** GPT-4o (Copilot Pro, free tier)
**Cost:** $0
**Validation:** Gemini 2.5 Pro (check validation rules)

**Claude Code Prompt:**
```
Generate Pydantic v2 schemas for all models.

For each model (e.g., Subscription), create:
1. SubscriptionBase - shared fields
2. SubscriptionCreate - for POST requests
3. SubscriptionUpdate - for PATCH requests
4. SubscriptionResponse - for GET responses
5. SubscriptionInDB - with id, created_at

Requirements:
- Pydantic v2 syntax
- Full validation (email, URL, positive numbers, etc.)
- Type hints
- Docstrings
- ConfigDict with from_attributes=True

Example for Subscription:

File: backend/app/schemas/subscription.py
```python
from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Optional
from datetime import date, datetime
from enum import Enum

class CycleType(str, Enum):
    \"\"\"Subscription cycle types.\"\"\"
    DAYS = "days"
    WEEKS = "weeks"
    MONTHS = "months"
    YEARS = "years"

class SubscriptionBase(BaseModel):
    \"\"\"Base subscription schema with shared fields.\"\"\"
    name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0)
    currency_id: int
    frequency: int = Field(..., ge=1, le=365)
    cycle: CycleType
    next_payment: date
    auto_renew: bool = True
    start_date: Optional[date] = None
    notes: Optional[str] = None
    url: Optional[HttpUrl] = None
    # ... other fields

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('price must be greater than 0')
        return v

class SubscriptionCreate(SubscriptionBase):
    \"\"\"Schema for creating subscription.\"\"\"
    logo: Optional[str] = None  # filename or URL

class SubscriptionUpdate(BaseModel):
    \"\"\"Schema for updating subscription (all fields optional).\"\"\"
    name: Optional[str] = None
    price: Optional[float] = None
    # ... all fields optional

class SubscriptionResponse(SubscriptionBase):
    \"\"\"Schema for subscription response.\"\"\"
    id: int
    user_id: int
    created_at: datetime

    # Include related data
    currency_code: Optional[str] = None
    category_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class SubscriptionInDB(SubscriptionResponse):
    \"\"\"Schema for subscription in database (includes sensitive fields if any).\"\"\"
    pass
```
```

Generate schemas for:
1. User (auth.py, user.py)
2. Subscription
3. Category
4. Currency
5. PaymentMethod
6. HouseholdMember
7. NotificationSettings
8. Settings
9. Common (pagination, error responses)

Output: backend/app/schemas/*.py (10 files)
```

**Validation:**
```bash
# Import test
python -c "from app.schemas.subscription import SubscriptionCreate; print('✓')"

# Validation test
python -c "
from app.schemas.subscription import SubscriptionCreate
from datetime import date

try:
    sub = SubscriptionCreate(
        name='Netflix',
        price=-10,  # Invalid
        currency_id=1,
        frequency=1,
        cycle='months',
        next_payment=date.today()
    )
except ValueError as e:
    print('✓ Validation works:', e)
"
```

**Automation:** 95%
**Human Task:** Review validation rules (5-10 min)

---

#### Task 1.3: Generate FastAPI Routes (CRUD)

**AI Model:** GPT-4o (Copilot Pro, free tier)
**Cost:** $0
**Complex endpoints:** Claude Sonnet 4.5 (subscriptions, stats)
**Validation:** Gemini 2.5 Pro (validate all endpoints match USER_STORIES.md)

**Strategy:** Batch generation for all CRUD endpoints

**Claude Code Prompt:**
```
Generate FastAPI routers for all resources with full CRUD.

For each resource (Subscription, Category, Currency, PaymentMethod, HouseholdMember):

1. Create router file: backend/app/api/v1/{resource_plural}.py
2. Implement all CRUD operations from USER_STORIES.md
3. Use dependency injection for auth + db
4. Add proper error handling
5. Add OpenAPI documentation (docstrings)

Example: backend/app/api/v1/subscriptions.py

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.subscription import Subscription
from app.schemas.subscription import (
    SubscriptionCreate,
    SubscriptionUpdate,
    SubscriptionResponse
)
from app.schemas.common import PaginatedResponse
from app.services.subscription_service import SubscriptionService

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[SubscriptionResponse])
async def list_subscriptions(
    category_id: Optional[int] = Query(None),
    inactive: Optional[bool] = Query(None),
    sort: str = Query("next_payment"),
    order: str = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    \"\"\"List all subscriptions with filters and pagination.

    Args:
        category_id: Filter by category
        inactive: Include inactive subscriptions
        sort: Field to sort by
        order: Sort order (asc/desc)
        page: Page number
        limit: Items per page

    Returns:
        Paginated list of subscriptions
    \"\"\"
    service = SubscriptionService(db)
    result = await service.list_subscriptions(
        user_id=current_user.id,
        category_id=category_id,
        inactive=inactive,
        sort=sort,
        order=order,
        page=page,
        limit=limit
    )
    return result

@router.post("/", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    subscription_in: SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    \"\"\"Create new subscription.

    Args:
        subscription_in: Subscription data

    Returns:
        Created subscription

    Raises:
        HTTPException: 400 if validation fails
    \"\"\"
    service = SubscriptionService(db)
    subscription = await service.create_subscription(
        user_id=current_user.id,
        subscription_in=subscription_in
    )
    return subscription

@router.get("/{subscription_id}", response_model=SubscriptionResponse)
async def get_subscription(
    subscription_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    \"\"\"Get single subscription by ID.\"\"\"
    service = SubscriptionService(db)
    subscription = await service.get_subscription(subscription_id, current_user.id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    return subscription

@router.patch("/{subscription_id}", response_model=SubscriptionResponse)
async def update_subscription(
    subscription_id: int,
    subscription_in: SubscriptionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    \"\"\"Update subscription.\"\"\"
    service = SubscriptionService(db)
    subscription = await service.update_subscription(
        subscription_id, current_user.id, subscription_in
    )
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    return subscription

@router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subscription(
    subscription_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    \"\"\"Delete subscription.\"\"\"
    service = SubscriptionService(db)
    deleted = await service.delete_subscription(subscription_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    return None

@router.post("/{subscription_id}/clone", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def clone_subscription(
    subscription_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    \"\"\"Clone existing subscription.\"\"\"
    service = SubscriptionService(db)
    cloned = await service.clone_subscription(subscription_id, current_user.id)
    if not cloned:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    return cloned

@router.post("/{subscription_id}/renew", response_model=SubscriptionResponse)
async def renew_subscription(
    subscription_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    \"\"\"Renew subscription (calculate next payment).\"\"\"
    service = SubscriptionService(db)
    renewed = await service.renew_subscription(subscription_id, current_user.id)
    if not renewed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    return renewed
```
```

Generate routers for:
1. subscriptions.py (9 endpoints)
2. categories.py (5 endpoints)
3. currencies.py (6 endpoints)
4. payment_methods.py (6 endpoints)
5. household.py (4 endpoints)
6. auth.py (4 endpoints)
7. users.py (8 endpoints)
8. notifications.py (3 endpoints)
9. stats.py (4 endpoints)
10. admin.py (5 endpoints)
11. logos.py (2 endpoints)
12. database.py (3 endpoints)

Total: ~60 endpoints

For each endpoint, reference USER_STORIES.md for exact requirements.
```

**Copilot Role:**
- Auto-complete import statements
- Generate docstrings
- Suggest error messages

**Validation:**
```bash
# Import test
python -c "from app.api.v1.subscriptions import router; print('✓')"

# Endpoint count
python -c "
from app.api.v1.subscriptions import router
print(f'Endpoints: {len(router.routes)}')
"
```

**Automation:** 70%
**Human Task:**
- Review error handling (30 min)
- Verify endpoint matches USER_STORIES.md (30 min)

---

#### Task 1.4: Generate Service Layer

**AI Model:** Claude Sonnet 4.5 (Claude Code) - complex business logic
**Cost:** $0
**Alternative:** Qwen 2.5 Coder (DeepInfra) for simple services (batch)
**Budget:** ~$3.00 (if using DeepInfra for batch)

**Claude Code Prompt:**
```
Generate service layer for Subscription management.

File: backend/app/services/subscription_service.py

Requirements:
- All business logic from PHP endpoints/subscription/*.php
- Async methods
- Type hints
- Error handling
- Docstrings

Key methods to implement:
1. list_subscriptions() - with filters, pagination, sorting
2. get_subscription() - single by ID
3. create_subscription() - with logo handling
4. update_subscription() - partial update
5. delete_subscription() - with cleanup
6. clone_subscription() - duplicate logic
7. renew_subscription() - calculate next_payment
8. calculate_next_payment_date() - helper method

Example:
```python
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from app.models.subscription import Subscription
from app.models.user import User
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate
from app.schemas.common import PaginatedResponse

class SubscriptionService:
    \"\"\"Service for subscription operations.\"\"\"

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_subscriptions(
        self,
        user_id: int,
        category_id: Optional[int] = None,
        inactive: Optional[bool] = None,
        sort: str = "next_payment",
        order: str = "asc",
        page: int = 1,
        limit: int = 50
    ) -> PaginatedResponse[Subscription]:
        \"\"\"List subscriptions with filters and pagination.

        Args:
            user_id: User ID to filter by
            category_id: Optional category filter
            inactive: Optional inactive filter
            sort: Field to sort by
            order: Sort order
            page: Page number
            limit: Items per page

        Returns:
            Paginated response with subscriptions
        \"\"\"
        # Build query
        query = select(Subscription).where(Subscription.user_id == user_id)

        if category_id is not None:
            query = query.where(Subscription.category_id == category_id)

        if inactive is not None:
            query = query.where(Subscription.inactive == inactive)

        # Sorting
        sort_field = getattr(Subscription, sort, Subscription.next_payment)
        if order == "desc":
            query = query.order_by(sort_field.desc())
        else:
            query = query.order_by(sort_field.asc())

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)

        # Pagination
        query = query.offset((page - 1) * limit).limit(limit)

        # Execute
        result = await self.db.execute(query)
        items = result.scalars().all()

        return PaginatedResponse(
            data=items,
            meta={
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        )

    async def create_subscription(
        self,
        user_id: int,
        subscription_in: SubscriptionCreate
    ) -> Subscription:
        \"\"\"Create new subscription.

        Args:
            user_id: User ID
            subscription_in: Subscription data

        Returns:
            Created subscription
        \"\"\"
        # Create model instance
        subscription = Subscription(
            user_id=user_id,
            **subscription_in.model_dump(exclude={'logo'})
        )

        # Handle logo if provided
        if subscription_in.logo:
            # Logo handling logic (download, resize, save)
            # This will be implemented in logo_service
            pass

        self.db.add(subscription)
        await self.db.commit()
        await self.db.refresh(subscription)

        return subscription

    async def renew_subscription(
        self,
        subscription_id: int,
        user_id: int
    ) -> Optional[Subscription]:
        \"\"\"Renew subscription by calculating next payment date.

        Args:
            subscription_id: Subscription ID
            user_id: User ID (for ownership check)

        Returns:
            Updated subscription or None if not found
        \"\"\"
        subscription = await self.get_subscription(subscription_id, user_id)
        if not subscription:
            return None

        if subscription.auto_renew:
            subscription.next_payment = self.calculate_next_payment_date(
                current_date=subscription.next_payment,
                frequency=subscription.frequency,
                cycle=subscription.cycle
            )
            await self.db.commit()
            await self.db.refresh(subscription)

        return subscription

    def calculate_next_payment_date(
        self,
        current_date: date,
        frequency: int,
        cycle: str
    ) -> date:
        \"\"\"Calculate next payment date based on frequency and cycle.

        Args:
            current_date: Current payment date
            frequency: Number of cycles
            cycle: Cycle type (days/weeks/months/years)

        Returns:
            Next payment date
        \"\"\"
        if cycle == "days":
            return current_date + timedelta(days=frequency)
        elif cycle == "weeks":
            return current_date + timedelta(weeks=frequency)
        elif cycle == "months":
            return current_date + relativedelta(months=frequency)
        elif cycle == "years":
            return current_date + relativedelta(years=frequency)
        else:
            raise ValueError(f"Invalid cycle: {cycle}")
```
```

Generate services for:
1. subscription_service.py (complex - ~400 lines)
2. category_service.py (simple - ~150 lines)
3. currency_service.py (medium - ~250 lines, Fixer API)
4. payment_method_service.py (simple - ~150 lines)
5. household_service.py (simple - ~150 lines)
6. notification_service.py (medium - ~200 lines, webhook)
7. logo_service.py (medium - ~250 lines, Pillow)
8. stats_service.py (medium - ~300 lines, calculations)
9. user_service.py (medium - ~200 lines)

Total: ~2050 lines (~60% AI-generated)
```

**Automation:** 60%
**Human Task:** **CRITICAL REVIEW** (2-3 hours)
- Business logic correctness
- Edge cases handling
- Performance considerations

---

#### Task 1.5: Generate Tests (Backend)

**AI Model:** GPT-4o (Copilot Pro, free tier) - primary
**Cost:** $0
**Complex scenarios:** Claude Sonnet 4.5
**Edge cases:** GPT-4 Turbo (ChatGPT Plus)

**Copilot Chat Prompt:**
```
Generate pytest tests for SubscriptionService.

Requirements:
- pytest-asyncio for async tests
- Fixtures for db, user, sample data
- Test all methods
- Test happy path + edge cases
- Mock external dependencies (Fixer API, logo download)
- >80% coverage

File: backend/tests/unit/test_subscription_service.py

Example:
```python
import pytest
from datetime import date, timedelta
from app.services.subscription_service import SubscriptionService
from app.schemas.subscription import SubscriptionCreate
from app.models.subscription import Subscription

@pytest.mark.asyncio
async def test_create_subscription_success(db_session, test_user):
    \"\"\"Test creating subscription successfully.\"\"\"
    service = SubscriptionService(db_session)

    subscription_data = SubscriptionCreate(
        name="Netflix",
        price=15.99,
        currency_id=1,
        frequency=1,
        cycle="months",
        next_payment=date.today()
    )

    result = await service.create_subscription(
        user_id=test_user.id,
        subscription_in=subscription_data
    )

    assert result.id is not None
    assert result.name == "Netflix"
    assert result.price == 15.99
    assert result.user_id == test_user.id

@pytest.mark.asyncio
async def test_create_subscription_invalid_price(db_session, test_user):
    \"\"\"Test creating subscription with invalid price fails.\"\"\"
    service = SubscriptionService(db_session)

    with pytest.raises(ValueError, match="price must be greater than 0"):
        subscription_data = SubscriptionCreate(
            name="Netflix",
            price=-10,  # Invalid
            currency_id=1,
            frequency=1,
            cycle="months",
            next_payment=date.today()
        )

@pytest.mark.asyncio
async def test_calculate_next_payment_date_monthly(subscription_service):
    \"\"\"Test monthly payment date calculation.\"\"\"
    current = date(2025, 1, 15)
    next_payment = subscription_service.calculate_next_payment_date(
        current_date=current,
        frequency=1,
        cycle="months"
    )

    assert next_payment == date(2025, 2, 15)

@pytest.mark.asyncio
async def test_calculate_next_payment_date_yearly(subscription_service):
    \"\"\"Test yearly payment date calculation.\"\"\"
    current = date(2025, 1, 15)
    next_payment = subscription_service.calculate_next_payment_date(
        current_date=current,
        frequency=1,
        cycle="years"
    )

    assert next_payment == date(2026, 1, 15)

@pytest.mark.asyncio
async def test_renew_subscription_auto_renew_true(db_session, test_user, sample_subscription):
    \"\"\"Test renewing subscription with auto_renew=True.\"\"\"
    service = SubscriptionService(db_session)

    sample_subscription.auto_renew = True
    sample_subscription.next_payment = date(2025, 1, 1)
    sample_subscription.frequency = 1
    sample_subscription.cycle = "months"

    result = await service.renew_subscription(
        subscription_id=sample_subscription.id,
        user_id=test_user.id
    )

    assert result.next_payment == date(2025, 2, 1)

@pytest.mark.asyncio
async def test_list_subscriptions_with_filters(db_session, test_user, sample_subscriptions):
    \"\"\"Test listing subscriptions with category filter.\"\"\"
    service = SubscriptionService(db_session)

    result = await service.list_subscriptions(
        user_id=test_user.id,
        category_id=1,
        page=1,
        limit=10
    )

    assert len(result.data) > 0
    assert all(sub.category_id == 1 for sub in result.data)
    assert result.meta['page'] == 1
```
```

Generate tests for all services (9 files × ~300 lines = ~2700 lines tests)
```

**Copilot excels at:**
- Test structure
- Fixtures
- Happy path tests
- Edge case generation

**Claude Code for:**
- Complex business logic tests
- Integration scenarios

**Validation:**
```bash
# Run tests
pytest backend/tests/unit/ -v --cov=app/services --cov-report=term-missing

# Expected: >80% coverage
```

**Automation:** 80%
**Human Task:** Add edge cases AI missed (1-2 hours)

---

### PHASE 2: Backend Advanced (5-6 days with AI)

#### Task 2.1: Currency Service (Fixer API Integration)

**AI Model:** Claude Sonnet 4.5 (complex API integration logic)
**Cost:** $0

**Claude Code Prompt:**
```
Implement CurrencyService with Fixer API integration.

File: backend/app/services/currency_service.py

Requirements:
- httpx async client
- Fixer API integration (GET /latest?base=USD)
- Rate caching (24 hours)
- Conversion calculations
- Error handling (API down, invalid response)

Reference PHP code: endpoints/currency/update_exchange.php

Key methods:
1. update_exchange_rates() - fetch from Fixer
2. convert_currency() - convert amount between currencies
3. get_currencies() - list all currencies
4. create_currency() - add custom currency
5. update_currency() - edit currency
6. delete_currency() - remove if not in use

Include:
- Retry logic (3 attempts)
- Timeout (5 seconds)
- Rate limiting awareness
- Logging

Example:
```python
import httpx
from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta

from app.models.currency import Currency
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class CurrencyService:
    \"\"\"Service for currency operations and Fixer API integration.\"\"\"

    FIXER_API_URL = "https://api.apilayer.com/fixer/latest"

    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = httpx.AsyncClient(timeout=5.0)

    async def update_exchange_rates(self) -> Dict[str, float]:
        \"\"\"Fetch latest exchange rates from Fixer API.

        Returns:
            Dictionary of currency codes to rates

        Raises:
            HTTPException: If API call fails after retries
        \"\"\"
        headers = {"apikey": settings.FIXER_API_KEY}
        params = {"base": "USD"}

        for attempt in range(3):
            try:
                response = await self.client.get(
                    self.FIXER_API_URL,
                    headers=headers,
                    params=params
                )
                response.raise_for_status()
                data = response.json()

                if not data.get("success"):
                    raise ValueError(f"Fixer API error: {data.get('error')}")

                rates = data.get("rates", {})

                # Update database
                await self._update_rates_in_db(rates)

                logger.info(f"Updated {len(rates)} exchange rates")
                return rates

            except httpx.HTTPError as e:
                logger.warning(f"Fixer API attempt {attempt + 1} failed: {e}")
                if attempt == 2:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

        return {}

    async def _update_rates_in_db(self, rates: Dict[str, float]) -> None:
        \"\"\"Update currency rates in database.\"\"\"
        for code, rate in rates.items():
            query = select(Currency).where(Currency.code == code)
            result = await self.db.execute(query)
            currency = result.scalar_one_or_none()

            if currency:
                currency.rate = rate
                currency.updated_at = datetime.utcnow()

        await self.db.commit()

    async def convert_currency(
        self,
        amount: float,
        from_code: str,
        to_code: str
    ) -> float:
        \"\"\"Convert amount from one currency to another.

        Args:
            amount: Amount to convert
            from_code: Source currency code (e.g., 'EUR')
            to_code: Target currency code (e.g., 'USD')

        Returns:
            Converted amount

        Raises:
            ValueError: If currencies not found
        \"\"\"
        # Get currencies
        from_currency = await self._get_currency_by_code(from_code)
        to_currency = await self._get_currency_by_code(to_code)

        if not from_currency or not to_currency:
            raise ValueError("Currency not found")

        # Convert: amount * (to_rate / from_rate)
        result = amount * (to_currency.rate / from_currency.rate)
        return round(result, 2)

    async def _get_currency_by_code(self, code: str) -> Optional[Currency]:
        \"\"\"Get currency by code.\"\"\"
        query = select(Currency).where(Currency.code == code)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
```
```

Also implement:
- Caching layer (Redis optional, in-memory dict for now)
- Rate limiting (max 1 request/minute to Fixer)
- Fallback to cached rates if API fails
```

**Automation:** 70%
**Human Task:** Test with real Fixer API (30 min)

---

#### Task 2.2: Notification Service (Webhooks)

**AI Model:** GPT-4o (Copilot Pro, free tier)
**Cost:** $0
**Review:** Claude Sonnet 4.5 (webhook retry logic)

**Similar pattern to Currency Service**

**Automation:** 75%

---

#### Task 2.3: Logo Service (Pillow + Search)

**AI Model:** GPT-4o (Copilot Pro, free tier)
**Cost:** $0
**Image processing:** Claude Sonnet 4.5 (Pillow logic review)

**Automation:** 70%

---

### PHASE 3: Backend Infrastructure (3-4 days with AI)

#### Task 3.1: Celery Tasks

**AI Model:** GPT-4o (Copilot Pro, free tier)
**Cost:** $0

**Automation:** 75%

---

#### Task 3.2: OpenAPI Documentation

**AI Model:** Automatic (FastAPI) + GPT-4o for examples
**Cost:** $0

**Automation:** 95%

---

### PHASE 4-6: Frontend (2-3 weeks with AI)

#### Task 4.1: MUI Theme Setup

**AI Model:** GPT-4o (Copilot Pro, free tier)
**Cost:** $0
**Review:** Claude Sonnet 4.5 (theme architecture)

**Claude Code Prompt:**
```
Create Material-UI theme configuration with 8 color variants and dark mode.

File: frontend/src/theme/index.ts

Requirements:
- 8 primary colors (blue, green, red, yellow, purple, pink, orange, gray)
- Dark/Light mode support
- Custom theme factory
- TypeScript types

```typescript
import { createTheme, ThemeOptions, PaletteMode } from '@mui/material/styles';

const colorPalettes = {
  blue: {
    main: '#2196F3',
    light: '#64B5F6',
    dark: '#1976D2',
  },
  green: {
    main: '#4CAF50',
    light: '#81C784',
    dark: '#388E3C',
  },
  red: {
    main: '#F44336',
    light: '#E57373',
    dark: '#D32F2F',
  },
  // ... other colors
};

export type ColorTheme = keyof typeof colorPalettes;

export const createAppTheme = (
  colorTheme: ColorTheme = 'blue',
  mode: PaletteMode = 'light'
) => {
  return createTheme({
    palette: {
      mode,
      primary: colorPalettes[colorTheme],
      // ... other palette config
    },
    typography: {
      // ... typography config
    },
    components: {
      // ... component overrides
    },
  });
};
```
```

**Automation:** 90%

---

#### Task 4.2: Generate React Components

**AI Model:** GPT-4o (Copilot Pro, free tier) - primary
**Cost:** $0
**Complex components:** Claude Sonnet 4.5 (SubscriptionList, Dashboard)
**Batch option:** Qwen 2.5 Coder (DeepInfra) for simple components
**Budget:** ~$2.00 (if using DeepInfra for batch)

**Claude Code Prompt (example):**
```
Generate SubscriptionList component with MUI.

File: frontend/src/components/subscriptions/SubscriptionList.tsx

Requirements:
- Material-UI DataGrid or custom list
- Filters (category, inactive, search)
- Sorting
- Pagination
- Actions (edit, delete, clone, renew)
- Loading states
- Error handling
- TypeScript
- React Query for data fetching

```typescript
import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Select,
  MenuItem,
  IconButton,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  ContentCopy as CloneIcon,
  Refresh as RenewIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';

import { subscriptionsApi } from '@/api/subscriptions';
import { Subscription } from '@/types/subscription';
import { SubscriptionCard } from './SubscriptionCard';

interface SubscriptionListProps {
  onEdit: (subscription: Subscription) => void;
}

export const SubscriptionList: React.FC<SubscriptionListProps> = ({ onEdit }) => {
  const { t } = useTranslation();
  const queryClient = useQueryClient();

  const [filters, setFilters] = useState({
    categoryId: null as number | null,
    inactive: false,
    search: '',
    sort: 'next_payment',
    order: 'asc' as 'asc' | 'desc',
    page: 1,
    limit: 50,
  });

  // Fetch subscriptions
  const { data, isLoading, error } = useQuery({
    queryKey: ['subscriptions', filters],
    queryFn: () => subscriptionsApi.list(filters),
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: (id: number) => subscriptionsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subscriptions'] });
    },
  });

  // Clone mutation
  const cloneMutation = useMutation({
    mutationFn: (id: number) => subscriptionsApi.clone(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subscriptions'] });
    },
  });

  // Renew mutation
  const renewMutation = useMutation({
    mutationFn: (id: number) => subscriptionsApi.renew(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subscriptions'] });
    },
  });

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{t('error.loading_subscriptions')}</Alert>;
  }

  return (
    <Box>
      {/* Filters */}
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Box display="flex" gap={2}>
            <TextField
              label={t('search')}
              value={filters.search}
              onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              size="small"
            />
            {/* More filters... */}
          </Box>
        </CardContent>
      </Card>

      {/* List */}
      <Box display="flex" flexDirection="column" gap={2}>
        {data?.data.map((subscription) => (
          <SubscriptionCard
            key={subscription.id}
            subscription={subscription}
            onEdit={() => onEdit(subscription)}
            onDelete={() => deleteMutation.mutate(subscription.id)}
            onClone={() => cloneMutation.mutate(subscription.id)}
            onRenew={() => renewMutation.mutate(subscription.id)}
          />
        ))}
      </Box>
    </Box>
  );
};
```
```

Generate components:
1. SubscriptionList
2. SubscriptionForm (React Hook Form + Zod)
3. SubscriptionCard
4. CategorySettings
5. CurrencySettings
6. PaymentMethodSettings
7. Dashboard (overview cards)
8. Statistics (charts with Recharts)
9. ... (~25 components total)
```

**Automation:** 75%
**Human Task:** UX refinement, accessibility (2-3 days)

---

## Orchestration Scripts

### Main Orchestration Script

**File:** `scripts/automation/orchestrator.py`

```python
#!/usr/bin/env python3
"""
Main orchestration script for AI-assisted refactoring.
"""
import click
from rich.console import Console
from rich.progress import Progress, TaskID
from pathlib import Path
import asyncio
from typing import List, Dict

console = Console()

class UsageTracker:
    """Track AI model usage and costs."""

    def __init__(self):
        self.usage = {
            "gpt-4o": {"requests": 0, "cost": 0.0},
            "claude-sonnet-4.5": {"requests": 0, "cost": 0.0},
            "gemini-2.5-pro": {"requests": 0, "cost": 0.0},
            "gpt-4-turbo": {"requests": 0, "cost": 0.0},
            "qwen-2.5-coder": {"requests": 0, "cost": 0.0},
        }
        self.deepinfra_budget = 10.0
        self.deepinfra_spent = 0.0

    def log_request(self, model: str, tokens: int = 0):
        """Log AI model request."""
        if model in self.usage:
            self.usage[model]["requests"] += 1

            # Track DeepInfra costs
            if model == "qwen-2.5-coder":
                cost = (tokens / 1_000_000) * 0.27  # $0.27 per 1M tokens
                self.usage[model]["cost"] += cost
                self.deepinfra_spent += cost

    def get_summary(self) -> str:
        """Get usage summary."""
        summary = "AI Model Usage Summary:\n"
        for model, data in self.usage.items():
            summary += f"  {model}: {data['requests']} requests, ${data['cost']:.2f}\n"
        summary += f"\nDeepInfra Budget: ${self.deepinfra_budget:.2f}\n"
        summary += f"DeepInfra Spent: ${self.deepinfra_spent:.2f}\n"
        summary += f"DeepInfra Remaining: ${self.deepinfra_budget - self.deepinfra_spent:.2f}\n"
        return summary

    def check_budget(self) -> bool:
        """Check if DeepInfra budget exceeded."""
        return self.deepinfra_spent < self.deepinfra_budget

class RefactorOrchestrator:
    """Main orchestrator for refactoring workflow."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.php_dir = project_root / "endpoints"
        self.backend_dir = project_root / "backend"
        self.frontend_dir = project_root / "frontend"
        self.model_config = self.load_model_config()
        self.usage_tracker = UsageTracker()

    def load_model_config(self) -> Dict:
        """Load AI model configuration."""
        config_file = self.project_root / "config" / "ai_models.yaml"
        if config_file.exists():
            import yaml
            with open(config_file) as f:
                return yaml.safe_load(f)
        return {}

    def select_model(self, task_type: str, complexity: str = "medium") -> str:
        """Select optimal AI model based on task type and complexity.

        Args:
            task_type: Type of task (e.g., 'models', 'schemas', 'routes')
            complexity: Complexity level ('simple', 'medium', 'complex')

        Returns:
            Model identifier (e.g., 'gpt-4o', 'claude-sonnet-4.5')
        """
        # Default strategy: GPT-4o for 90% of tasks
        if complexity == "simple":
            return "gpt-4o"  # Copilot Pro, free tier

        elif complexity == "complex":
            if task_type in ["service_layer", "business_logic"]:
                return "claude-sonnet-4.5"  # Claude Code
            elif task_type == "validation":
                return "gemini-2.5-pro"  # Google AI Pro, 1M context
            elif task_type == "algorithms":
                return "gpt-4-turbo"  # ChatGPT Plus

        else:  # medium
            return "gpt-4o"  # Default to free tier

        return "gpt-4o"  # Fallback

    async def run_phase(self, phase: str):
        """Run specific phase of refactoring."""
        console.print(f"[bold blue]Starting Phase: {phase}[/bold blue]")

        if phase == "models":
            await self.generate_models()
        elif phase == "schemas":
            await self.generate_schemas()
        elif phase == "routes":
            await self.generate_routes()
        # ... other phases

    async def generate_models(self):
        """Generate SQLAlchemy models from schema."""
        console.print("[yellow]Generating SQLAlchemy models...[/yellow]")

        # Read schema
        schema_file = self.project_root / "analysis" / "schema.sql"
        if not schema_file.exists():
            console.print("[red]Error: schema.sql not found[/red]")
            return

        # Call Claude Code via VS Code API
        # (simplified - actual implementation would use VS Code extension API)
        console.print("[green]✓ Models generated[/green]")

        # Run validation
        await self.validate_models()

    async def validate_models(self):
        """Validate generated models."""
        console.print("[yellow]Validating models...[/yellow]")

        # Run mypy
        import subprocess
        result = subprocess.run(
            ["mypy", "backend/app/models"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            console.print("[green]✓ Type checking passed[/green]")
        else:
            console.print(f"[red]✗ Type errors:\n{result.stdout}[/red]")

        # Run ruff
        result = subprocess.run(
            ["ruff", "check", "backend/app/models"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            console.print("[green]✓ Linting passed[/green]")
        else:
            console.print(f"[yellow]Warnings:\n{result.stdout}[/yellow]")

@click.group()
def cli():
    """AI-assisted refactoring orchestrator."""
    pass

@cli.command()
@click.option('--phase', required=True, help='Phase to run (models/schemas/routes/etc.)')
def run(phase: str):
    """Run specific refactoring phase."""
    project_root = Path.cwd()
    orchestrator = RefactorOrchestrator(project_root)
    asyncio.run(orchestrator.run_phase(phase))

@cli.command()
def status():
    """Show refactoring progress."""
    console.print("[bold]Refactoring Status:[/bold]")
    # Read progress from .automation_progress.json
    # Display completed tasks, pending tasks, etc.

if __name__ == '__main__':
    cli()
```

**Usage:**
```bash
# Generate models
python scripts/automation/orchestrator.py run --phase=models

# Generate schemas
python scripts/automation/orchestrator.py run --phase=schemas

# Check status
python scripts/automation/orchestrator.py status
```

---

## Quality Gates

### Automated Validation

**File:** `scripts/automation/quality_gate.py`

```python
#!/usr/bin/env python3
"""
Quality gate checks for AI-generated code.
"""
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from rich.console import Console

console = Console()

class QualityGate:
    """Run quality checks on generated code."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.backend_dir = project_root / "backend"
        self.frontend_dir = project_root / "frontend"

    def run_backend_checks(self) -> bool:
        """Run all backend quality checks."""
        console.print("[bold]Running Backend Quality Checks[/bold]")

        checks = [
            ("Type Checking (mypy)", self.check_mypy),
            ("Linting (ruff)", self.check_ruff),
            ("Tests (pytest)", self.check_pytest),
            ("Coverage (>80%)", self.check_coverage),
            ("Import Order", self.check_imports),
        ]

        all_passed = True
        for name, check_fn in checks:
            passed = check_fn()
            status = "[green]✓[/green]" if passed else "[red]✗[/red]"
            console.print(f"{status} {name}")
            all_passed = all_passed and passed

        return all_passed

    def check_mypy(self) -> bool:
        """Check types with mypy."""
        result = subprocess.run(
            ["mypy", "backend/app", "--strict"],
            capture_output=True,
            cwd=self.project_root
        )
        return result.returncode == 0

    def check_ruff(self) -> bool:
        """Check linting with ruff."""
        result = subprocess.run(
            ["ruff", "check", "backend/app"],
            capture_output=True,
            cwd=self.project_root
        )
        return result.returncode == 0

    def check_pytest(self) -> bool:
        """Run pytest."""
        result = subprocess.run(
            ["pytest", "backend/tests", "-v"],
            capture_output=True,
            cwd=self.project_root
        )
        return result.returncode == 0

    def check_coverage(self) -> bool:
        """Check test coverage >80%."""
        result = subprocess.run(
            ["pytest", "backend/tests", "--cov=app", "--cov-report=term-missing", "--cov-fail-under=80"],
            capture_output=True,
            cwd=self.project_root
        )
        return result.returncode == 0

    def check_imports(self) -> bool:
        """Check import order."""
        result = subprocess.run(
            ["ruff", "check", "--select=I", "backend/app"],
            capture_output=True,
            cwd=self.project_root
        )
        return result.returncode == 0

    def run_frontend_checks(self) -> bool:
        """Run frontend quality checks."""
        console.print("[bold]Running Frontend Quality Checks[/bold]")

        checks = [
            ("Type Checking (tsc)", self.check_tsc),
            ("Linting (eslint)", self.check_eslint),
            ("Tests (vitest)", self.check_vitest),
            ("Build", self.check_build),
        ]

        all_passed = True
        for name, check_fn in checks:
            passed = check_fn()
            status = "[green]✓[/green]" if passed else "[red]✗[/red]"
            console.print(f"{status} {name}")
            all_passed = all_passed and passed

        return all_passed

    def check_tsc(self) -> bool:
        """Check TypeScript types."""
        result = subprocess.run(
            ["npx", "tsc", "--noEmit"],
            capture_output=True,
            cwd=self.frontend_dir
        )
        return result.returncode == 0

    def check_eslint(self) -> bool:
        """Check ESLint."""
        result = subprocess.run(
            ["npx", "eslint", "src"],
            capture_output=True,
            cwd=self.frontend_dir
        )
        return result.returncode == 0

    def check_vitest(self) -> bool:
        """Run Vitest."""
        result = subprocess.run(
            ["npx", "vitest", "run"],
            capture_output=True,
            cwd=self.frontend_dir
        )
        return result.returncode == 0

    def check_build(self) -> bool:
        """Check if build succeeds."""
        result = subprocess.run(
            ["npm", "run", "build"],
            capture_output=True,
            cwd=self.frontend_dir
        )
        return result.returncode == 0

if __name__ == '__main__':
    gate = QualityGate(Path.cwd())

    backend_ok = gate.run_backend_checks()
    frontend_ok = gate.run_frontend_checks()

    if backend_ok and frontend_ok:
        console.print("[bold green]✓ All quality checks passed![/bold green]")
        exit(0)
    else:
        console.print("[bold red]✗ Quality checks failed[/bold red]")
        exit(1)
```

**Usage:**
```bash
# Run all quality checks
python scripts/automation/quality_gate.py

# In CI/CD pipeline
python scripts/automation/quality_gate.py || exit 1
```

---

## Monitoring & Progress Tracking

### Progress Dashboard

**File:** `scripts/automation/progress_tracker.py`

```python
#!/usr/bin/env python3
"""
Track and display refactoring progress.
"""
from dataclasses import dataclass
from typing import List, Dict
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
import json
from pathlib import Path

console = Console()

@dataclass
class Task:
    name: str
    phase: str
    status: str  # pending, in_progress, completed, failed
    automation_percent: int
    estimated_time: str
    actual_time: str = ""

class ProgressTracker:
    """Track refactoring progress."""

    def __init__(self, progress_file: Path):
        self.progress_file = progress_file
        self.tasks = self.load_tasks()

    def load_tasks(self) -> List[Task]:
        """Load tasks from JSON."""
        if not self.progress_file.exists():
            return self.initialize_tasks()

        with open(self.progress_file) as f:
            data = json.load(f)

        return [Task(**task) for task in data['tasks']]

    def initialize_tasks(self) -> List[Task]:
        """Initialize task list from REFACTOR_PLAN.md."""
        return [
            Task("Database Models", "Phase 1", "pending", 85, "1-2 days"),
            Task("Pydantic Schemas", "Phase 1", "pending", 90, "4-6 hours"),
            Task("API Routes", "Phase 1", "pending", 70, "2-3 days"),
            Task("Service Layer", "Phase 1", "pending", 60, "3-4 days"),
            Task("Backend Tests", "Phase 1", "pending", 80, "1-2 days"),
            # ... all tasks from REFACTOR_PLAN.md
        ]

    def save_tasks(self):
        """Save tasks to JSON."""
        data = {'tasks': [task.__dict__ for task in self.tasks]}
        with open(self.progress_file, 'w') as f:
            json.dump(data, f, indent=2)

    def update_task(self, task_name: str, status: str, actual_time: str = ""):
        """Update task status."""
        for task in self.tasks:
            if task.name == task_name:
                task.status = status
                if actual_time:
                    task.actual_time = actual_time
                break
        self.save_tasks()

    def display(self):
        """Display progress dashboard."""
        # Summary
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.status == "completed")
        in_progress = sum(1 for t in self.tasks if t.status == "in_progress")
        pending = sum(1 for t in self.tasks if t.status == "pending")

        console.print("\n[bold]Refactoring Progress Dashboard[/bold]\n")

        # Progress bar
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task(
                "Overall Progress",
                total=total,
                completed=completed
            )

        console.print(f"\n✓ Completed: {completed}/{total}")
        console.print(f"⚙ In Progress: {in_progress}/{total}")
        console.print(f"⏳ Pending: {pending}/{total}\n")

        # Task table
        table = Table(title="Tasks")
        table.add_column("Phase", style="cyan")
        table.add_column("Task", style="white")
        table.add_column("Status", style="yellow")
        table.add_column("Auto %", justify="right", style="magenta")
        table.add_column("Estimated", justify="right")
        table.add_column("Actual", justify="right", style="green")

        for task in self.tasks:
            status_emoji = {
                "completed": "✓",
                "in_progress": "⚙",
                "pending": "⏳",
                "failed": "✗"
            }[task.status]

            table.add_row(
                task.phase,
                task.name,
                f"{status_emoji} {task.status}",
                f"{task.automation_percent}%",
                task.estimated_time,
                task.actual_time or "-"
            )

        console.print(table)

if __name__ == '__main__':
    tracker = ProgressTracker(Path(".automation_progress.json"))
    tracker.display()
```

**Usage:**
```bash
# View progress
python scripts/automation/progress_tracker.py

# Update task status
python -c "
from progress_tracker import ProgressTracker
from pathlib import Path

tracker = ProgressTracker(Path('.automation_progress.json'))
tracker.update_task('Database Models', 'completed', '1.5 days')
tracker.display()
"
```

---

## Prompt Library

### Templates for Common Tasks

**File:** `prompts/` directory

**Example: `prompts/generate_crud_endpoint.txt`**
```
Generate full CRUD REST API endpoint for {resource_name}.

Reference:
- USER_STORIES.md: {user_story_ids}
- Model: backend/app/models/{resource_name}.py
- Schema: backend/app/schemas/{resource_name}.py

Requirements:
- FastAPI router in backend/app/api/v1/{resource_plural}.py
- All CRUD operations: GET (list + single), POST, PATCH, DELETE
- Additional endpoints: {additional_endpoints}
- Dependency injection: get_db, get_current_user
- Error handling: 400, 401, 404, 500
- OpenAPI docs: docstrings for all endpoints
- Pagination for list endpoint (page, limit)
- Filters: {filter_fields}
- Sorting: {sort_fields}

Follow pattern from backend/app/api/v1/subscriptions.py

Output file: backend/app/api/v1/{resource_plural}.py
```

---

## Troubleshooting

### Common Issues

#### Issue 1: AI generates incorrect business logic

**Solution:**
1. Review PHP code manually
2. Add explicit business rules to prompt
3. Generate unit tests first (test-driven)
4. Use multiple AI for validation (Claude + Gemini)

#### Issue 2: Type errors after generation

**Solution:**
```bash
# Run mypy with detailed output
mypy backend/app --show-error-codes --pretty

# Fix common issues:
# - Missing imports
# - Incorrect type hints
# - Optional vs required fields
```

#### Issue 3: Tests fail after AI generation

**Solution:**
1. Review test assertions (AI may have wrong expectations)
2. Check fixtures (sample data correctness)
3. Verify mocking (external dependencies)
4. Add debugging:
```python
@pytest.mark.asyncio
async def test_something(db_session):
    # Add debugging
    import pprint
    result = await service.method()
    pprint.pprint(result.__dict__)
    assert ...
```

---

## Summary

### Key Takeaways

1. **AI is powerful but not autonomous** - always review output
2. **Small iterations** - generate → validate → commit
3. **Test-driven** - tests help catch AI mistakes
4. **Multiple AI tools** - use each for their strengths
5. **Quality gates** - automated validation is critical
6. **Human expertise required** - especially for business logic

### Expected Results

- **60-70% automation** overall
- **5-6 weeks** instead of 11-15 weeks
- **High quality code** (>80% test coverage, type-safe)
- **Maintainable** (follows SOLID, well-documented)
- **Total cost:** $10 (DeepInfra only, using optimized batch processing)
- **Model distribution:** 90% GPT-4o (free), 5% Claude S4.5 (free), 3% Gemini (free), 2% others

### Next Steps

1. ✅ Review this AUTOMATION_PLAN.md
2. Setup orchestration scripts (`scripts/automation/`)
3. Configure VS Code settings (`.vscode/settings.json`)
4. Start with PREPARATION phase (database analysis)
5. Begin Phase 1 (Backend Foundation)
6. Track progress (`.automation_progress.json`)
7. Regular commits + reviews

---

**Ready to start? Begin with:**
```bash
# 1. Setup automation scripts
mkdir -p scripts/automation analysis

# 2. Extract database schema
sqlite3 db/wallos.db .schema > analysis/schema.sql

# 3. Run PHP endpoint inventory
python scripts/automation/analyze_php_endpoints.py

# 4. Start Phase 1 with Claude Code
# Open VS Code → Claude Code panel → use prompts from this doc
```

**Good luck! 🚀**
