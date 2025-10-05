# AI Strategy - Automated Refactoring with API Integration

**Project:** Wallos PHP → Python FastAPI + React
**Automation Goal:** 70-80% automated code generation
**Total Budget:** $10 (DeepInfra only, all others via existing licenses)

---

## Executive Summary

**5 AI Platforms Strategy:**
- 90% tasks: **GitHub Copilot API** (GPT-4o, unlimited via license)
- 5% tasks: **Claude API** (Sonnet 4.5, complex logic)
- 3% tasks: **Gemini API** (2.5 Pro, validation, 1M context)
- 2% tasks: **ChatGPT Plus API** (GPT-4 Turbo, algorithms)
- <1% tasks: **DeepInfra API** (Qwen 2.5 Coder, batch, max $10)

**Key Benefits:**
- ✅ Full automation via Python orchestrator
- ✅ Parallel execution (process 8 files simultaneously)
- ✅ All via existing licenses (API access included)
- ✅ Only DeepInfra costs money ($5-7 target, $10 max)
- ✅ No manual VS Code window management

---

## Available AI Resources

### 1. GitHub Copilot Pro - PRIMARY (90% of tasks)

**License:** $10/month (PAID)
**API Access:** Included in Copilot Pro license
**Authentication:** GitHub OAuth token
**Endpoint:** OpenAI-compatible API via GitHub

**Primary Model: GPT-4o**
- Context: 128k tokens
- Daily limit: **UNLIMITED** (0x pricing tier)
- Cost per request: $0
- Speed: Fast
- Best for: Boilerplate, CRUD, schemas, tests

**Alternative Models (via same API):**
- GPT-4.1 (0x tier - unlimited)
- GPT-4o-mini (0x tier - faster)
- GPT-5 mini (0x tier)
- Claude Sonnet 4 (1x tier - limited to ~50/day)
- Gemini 2.5 Pro (1x tier - limited to ~50/day)

**Usage Strategy:**
- Use GPT-4o (unlimited) for 90% of simple/medium tasks
- Avoid limited tier models (save for emergencies)
- Parallel execution: Process up to 8 files simultaneously
- No rate limiting concerns

**Tasks:**
- SQLAlchemy models (8 files parallel)
- Pydantic schemas (10 files parallel)
- API routes simple (12 files parallel)
- Backend tests (9 files parallel)
- React components simple (15 files parallel)

---

### 2. Claude Pro - COMPLEX LOGIC (5% of tasks)

**License:** $20/month (PAID)
**API Access:** Included in Claude Pro subscription
**Authentication:** Anthropic API key (from account)
**Endpoint:** https://api.anthropic.com/v1/messages

**Model: Claude Sonnet 4.5**
- Context: 200k tokens
- Daily limit: ~500 messages (~100 complex tasks)
- Cost per request: $0 (via license)
- Speed: Slower than GPT-4o (deeper reasoning)
- Best for: Complex business logic, architecture

**Usage Strategy:**
- Use ONLY for complex tasks requiring deep reasoning
- Sequential execution (not parallel)
- ~500 msg/day limit is generous for 5% usage

**Tasks:**
- Service layer complex (SubscriptionService, CurrencyService, StatsService)
- API routes complex (subscriptions with 9 endpoints)
- Architecture decisions
- Multi-file refactoring
- PHP → Python complex logic migration

---

### 3. Google AI Pro - VALIDATION (3% of tasks)

**License:** FREE tier
**API Access:** Free (1M tokens/day!)
**Authentication:** Google API key
**Endpoint:** https://generativelanguage.googleapis.com/v1beta/models

**Model: Gemini 2.5 Pro**
- Context: **1M tokens** (MASSIVE - entire codebase!)
- Daily limit: 1000 requests, 1M tokens/day
- Cost per request: $0
- Speed: Medium
- Best for: Code review, validation, large context analysis

**Usage Strategy:**
- Use for validation of entire phases
- Can analyze backend/app/ + frontend/src/ simultaneously
- Security audit, constraint checking
- Final review before commits

**Tasks:**
- Validate all 10 schemas against USER_STORIES.md
- Review all 60 API endpoints
- Full codebase security audit
- Check constraints (no PostgreSQL, no Chakra UI, etc.)

---

### 4. ChatGPT Plus - ALGORITHMS (2% of tasks)

**License:** $20/month (PAID)
**API Access:** Included in ChatGPT Plus (GPT-4 API)
**Authentication:** OpenAI API key
**Endpoint:** https://api.openai.com/v1/chat/completions

**Model: GPT-4 Turbo**
- Context: 128k tokens
- Daily limit: ~80 messages per 3 hours
- Cost per request: $0 (via license)
- Speed: Medium
- Best for: Algorithms, math, edge cases

**Usage Strategy:**
- Use for hardest algorithmic problems
- Math calculations (payment dates, currency conversion)
- Edge case handling (Feb 29, leap years, etc.)
- Debugging complex logic

**Tasks:**
- Payment calculation logic (next_payment_date with relativedelta)
- Currency conversion algorithms (Fixer API integration)
- Date edge cases (month boundaries, leap years)
- Complex validation rules

**Plugin Name:** "Codex" (in config/scripts)
**License Name:** "ChatGPT Plus" (in documentation)

---

### 5. DeepInfra - BATCH PROCESSING (<1% of tasks)

**License:** Pay-per-use
**API Access:** Requires DEEPINFRA_API_KEY
**Authentication:** API key (export DEEPINFRA_API_KEY='...')
**Endpoint:** https://api.deepinfra.com/v1/openai

**Model: Qwen 2.5 Coder 32B**
- Context: 32k tokens
- Cost: $0.27 per 1M tokens
- Daily limit: None (budget only)
- Speed: Fast
- Best for: Batch processing simple repetitive tasks

**Budget Allocation ($10 max, target $5-7):**
1. i18n conversion (25 files → 2): **$0.40**
2. PHP→Python simple services (batch): **$2.00-3.00**
3. React simple components (if >10 similar): **$1.50-2.00**
4. Buffer: **$2.00-3.00**
5. **Reserved:** $2.00-3.50 (don't spend immediately)

**Usage Strategy:**
- Use ONLY when batch >10 similar simple files
- ROI check: Is batch cheaper than parallel Copilot API?
- Track spending in `.deepinfra_budget.json`
- Stop at $8 (warn), hard limit $10

**Tasks:**
- i18n language files conversion (25 → 2 languages)
- Batch simple React components (if 15+ similar)
- Fallback when other APIs have issues

---

## Model Selection Decision Tree

```
┌─────────────────────────────────────────────┐
│ New Task                                    │
└─────────────┬───────────────────────────────┘
              │
              ▼
         ┌─────────┐
         │ Simple/ │  YES  ┌─────────────────────┐
         │ Medium? ├──────→│ Copilot API (GPT-4o)│
         └────┬────┘       │ Unlimited, Parallel │
              │            └─────────────────────┘
              NO
              │
              ▼
      ┌───────────────┐
      │ Complex logic/│  YES  ┌──────────────────┐
      │ Architecture? ├──────→│ Claude API (S4.5)│
      └───────┬───────┘       │ Sequential       │
              │               └──────────────────┘
              NO
              │
              ▼
      ┌──────────────┐
      │ Full codebase│  YES  ┌───────────────────┐
      │ review/valid?├──────→│ Gemini API (2.5Pro)│
      └──────┬───────┘       │ 1M context!       │
             │               └───────────────────┘
             NO
             │
             ▼
      ┌─────────────┐
      │ Algorithm/  │  YES  ┌──────────────────────┐
      │ Math heavy? ├──────→│ Codex API (GPT-4 Turbo)│
      └─────┬───────┘       │ ChatGPT Plus license │
            │               └──────────────────────┘
            NO
            │
            ▼
      ┌──────────────┐
      │ Batch >10    │  YES  ┌─────────────────────┐
      │ simple files?├──────→│ DeepInfra (Qwen 2.5)│
      └──────┬───────┘       │ $0.27/1M tokens     │
             │               └─────────────────────┘
             NO
             │
             ▼
        Use Copilot API
        (default fallback)
```

---

## API Configuration

### Setup Required (one-time)

```bash
# 1. GitHub Copilot API (via GitHub token)
export GITHUB_TOKEN="ghp_your_token_here"

# 2. Anthropic Claude API (from claude.ai/account/api-keys)
export ANTHROPIC_API_KEY="sk-ant-api03-your_key_here"

# 3. Google Gemini API (from console.cloud.google.com)
export GOOGLE_API_KEY="AIzaSy_your_key_here"

# 4. OpenAI API (from platform.openai.com/api-keys)
export OPENAI_API_KEY="sk-your_key_here"

# 5. DeepInfra API (from deepinfra.com/dash/api_keys)
export DEEPINFRA_API_KEY="your_deepinfra_key"

# Add to ~/.zshrc or ~/.bashrc to persist
```

**IMPORTANT:** All API keys above are included in your existing licenses except DeepInfra!
- Copilot Pro → GitHub API access
- Claude Pro → Anthropic API access
- Google AI Pro → Free tier API
- ChatGPT Plus → OpenAI API access with Plus rate limits

---

## Orchestration Strategy

### Automatic Parallel Execution

**Orchestrator:** `scripts/automation/orchestrator.py`

**Workflow:**
```python
# Example: Generate 8 SQLAlchemy models in parallel

orchestrator = RefactorOrchestrator()

# Automatically:
# 1. Reads task from config/ai_models.yaml
# 2. Selects: Copilot API (GPT-4o, unlimited)
# 3. Launches 8 parallel API calls
# 4. Generates all 8 models simultaneously
# 5. Validates with context_validator.py
# 6. Reports results

orchestrator.run_phase("models")
```

**No manual work:**
- ❌ No opening 8 VS Code windows
- ❌ No copy-pasting prompts
- ❌ No manual review between files
- ✅ Fully automated batch processing
- ✅ Automatic validation
- ✅ Human review only at end of phase

### Execution Speed Comparison

| Task | Manual | Semi-Auto (Native) | **Full Auto (API)** |
|------|--------|-------------------|---------------------|
| 8 SQLAlchemy models | 80 min | 32 min | **5 min** |
| 10 Pydantic schemas | 100 min | 40 min | **6 min** |
| 12 API routes | 120 min | 45 min | **7 min** |
| **Total Phase 1** | **12.8h** | **4h** | **2h** |

**Automation wins:** 84% time savings vs manual, 50% vs semi-auto!

---

## Cost Analysis

### Total Project Cost Breakdown

| Platform | Monthly License | API Calls Estimate | Cost via API | Notes |
|----------|----------------|-------------------|--------------|-------|
| **GitHub Copilot** | $10 | ~400 (90% tasks) | **$0** | Included in license |
| **Claude Pro** | $20 | ~20 (5% tasks) | **$0** | Included in license |
| **Google AI Pro** | $0 | ~15 (3% tasks) | **$0** | Free tier |
| **ChatGPT Plus** | $20 | ~10 (2% tasks) | **$0** | Included in license |
| **DeepInfra** | $0 | ~5 (<1% tasks) | **$5-7** | Pay-per-use only |
| **TOTAL** | $50/mo | ~450 calls | **$5-7** | Only DeepInfra costs! |

**You already pay $50/month for licenses** - API access is included!
**Additional cost for this project:** Only $5-7 (DeepInfra)

### DeepInfra Budget Tracking

**File:** `.deepinfra_budget.json`
```json
{
  "budget_max": 10.0,
  "budget_target": 7.0,
  "spent": 0.0,
  "remaining": 10.0,
  "tasks": []
}
```

**Auto-tracking:** Orchestrator updates this file after each DeepInfra call.

---

## Fallback Chains

When primary API fails or quota exceeded:

### Standard Chain (simple/medium tasks)
1. **Copilot API** (GPT-4o) - unlimited
2. Claude API (Sonnet 4.5) - if unlimited fails
3. Gemini API (2.5 Pro) - last resort

### Complex Chain (complex tasks)
1. **Claude API** (Sonnet 4.5) - primary
2. Codex API (GPT-4 Turbo) - if Claude quota exceeded
3. Gemini API (2.5 Pro) - last resort

### Validation Chain
1. **Gemini API** (2.5 Pro, 1M context) - primary
2. Claude API (Sonnet 4.5) - fallback

### Batch Chain
1. **Copilot API parallel** - free, fast
2. DeepInfra - only if >10 files AND budget available
3. Manual - if both fail

---

## Usage Limits & Warnings

```yaml
limits:
  copilot_api:
    daily: null  # UNLIMITED (0x tier)
    warn_at: null

  claude_api:
    daily: 500  # ~100 complex tasks
    warn_at: 400

  gemini_api:
    daily: 1000  # requests
    tokens_per_day: 1000000  # 1M tokens
    warn_at: 800

  codex_api:
    per_3_hours: 80  # ChatGPT Plus limit
    warn_at: 60

  deepinfra_api:
    budget_max: 10.0
    budget_target: 7.0
    warn_at: 8.0
```

---

## Task Assignments Reference

See: `config/ai_models.yaml` for full task-to-model mappings.

**Quick Reference:**

| Task Type | Primary API | Parallel? | Est. Time |
|-----------|-------------|-----------|-----------|
| SQLAlchemy models (8) | Copilot | ✅ 8× | 5 min |
| Pydantic schemas (10) | Copilot | ✅ 10× | 6 min |
| API routes simple (12) | Copilot | ✅ 12× | 7 min |
| API routes complex (3) | Claude | ❌ seq | 30 min |
| Service simple (6) | Copilot | ✅ 6× | 8 min |
| Service complex (3) | Claude | ❌ seq | 45 min |
| Tests backend (9) | Copilot | ✅ 9× | 10 min |
| React simple (15) | Copilot | ✅ 15× | 12 min |
| React complex (5) | Claude | ❌ seq | 40 min |
| i18n conversion | DeepInfra | ✅ batch | 3 min ($0.40) |
| Code review full | Gemini | ❌ 1× | 5 min |

**Total Phase 1 (Backend Foundation):** ~2 hours (vs 12.8h manual)

---

## Context Strategy

How much context to include in each API call:

### Copilot API (GPT-4o) - Minimal Context
- Core constraints only (`context/_CORE_CONTEXT.md` summary)
- Current file + related schema
- Target: <8k tokens input

### Claude API (Sonnet 4.5) - Moderate Context
- Core constraints
- Current phase files
- Related business logic
- Target: <50k tokens input

### Gemini API (2.5 Pro) - Full Context
- **Entire codebase** (1M context!)
- All constraints
- All user stories
- All generated code so far
- Target: <500k tokens input

### Codex API (GPT-4 Turbo) - Minimal Context
- Only algorithm problem
- Math formulas
- Edge cases
- Target: <5k tokens input

### DeepInfra API (Qwen 2.5) - Minimal Context
- Batch template
- Simple instructions
- Target: <3k tokens input per file

---

## Next Steps

1. **Setup API keys** (5 min):
   ```bash
   # Copy from respective platforms
   export GITHUB_TOKEN="..."
   export ANTHROPIC_API_KEY="..."
   export GOOGLE_API_KEY="..."
   export OPENAI_API_KEY="..."
   export DEEPINFRA_API_KEY="..."
   ```

2. **Test API access** (5 min):
   ```bash
   python scripts/automation/test_apis.py
   ```

3. **Run orchestrator** (automatic):
   ```bash
   python scripts/automation/orchestrator.py --phase=models
   ```

4. **Review & commit** (manual):
   ```bash
   git add backend/app/models/
   git commit -m "feat: generate SQLAlchemy models (automated)"
   ```

---

**See also:**
- `QUICK_START.md` - Step-by-step getting started guide
- `config/ai_models.yaml` - Full task-to-model configuration
- `context/_CORE_CONTEXT.md` - Constraints for AI prompts
