# AI Models Reference - Wallos Refactor Project

**Version:** 1.0
**Last Updated:** 2025-01-XX
**Project:** Wallos PHP → Python + React Migration

---

## Executive Summary

### Available Resources
- **5 AI Platforms** with valid licenses
- **15+ Models** available for use
- **Estimated Cost:** $10 total (DeepInfra only)
- **Existing Subscriptions:** $50/month (already paid)

### Optimization Strategy
- **90% of tasks:** Free tier models (GPT-4o via Copilot)
- **5% complex tasks:** Claude Sonnet 4.5 (via Claude Code)
- **3% validation:** Gemini 2.5 Pro (1M context!)
- **2% algorithms:** GPT-4 Turbo (ChatGPT Plus)
- **<1% batch:** DeepInfra ($10 budget)

---

## Table of Contents

1. [License Overview](#license-overview)
2. [Model Specifications](#model-specifications)
3. [Task Assignment Matrix](#task-assignment-matrix)
4. [Phase-by-Phase Cost Analysis](#phase-by-phase-cost-analysis)
5. [DeepInfra Budget Optimization](#deepinfra-budget-optimization)
6. [Usage Limits & Fallback Strategy](#usage-limits--fallback-strategy)
7. [Model Selection Decision Tree](#model-selection-decision-tree)

---

## License Overview

| License | Provider | Monthly Cost | Status | Primary Model | Context | Daily Limit |
|---------|----------|--------------|--------|---------------|---------|-------------|
| **Claude Pro** | Anthropic | $20 | ✅ PAID | Claude Sonnet 4.5 | 200k | ~500 msg |
| **Copilot Pro** | GitHub | $10 | ✅ PAID | GPT-4o + 11 others | 128k | Unlimited (0x), ~50 (1x) |
| **ChatGPT Plus** | OpenAI | $20 | ✅ PAID | GPT-4 Turbo | 128k | ~40-80 msg/3h |
| **Google AI Pro** | Google | $0 | ✅ FREE | Gemini 2.5 Pro | **1M** | 1000/day |
| **DeepInfra** | DeepInfra | Pay-per-use | ✅ API | Qwen 2.5 Coder 32B | 32k | None (budget only) |
| **TOTAL** | - | **$50/month** | - | - | - | - |

**Additional Project Cost:** $10 (DeepInfra batch processing)

---

## Model Specifications

### 1. Claude Code (License: Claude Pro)

**Access Method:** VS Code native extension (this interface)

| Specification | Value |
|---------------|-------|
| **Model** | Claude Sonnet 4.5 |
| **Context Window** | 200,000 tokens (~600 pages) |
| **Cost per Request** | $0 (included in subscription) |
| **Daily Limit** | ~500 messages |
| **Hourly Limit** | ~45 messages per 3-hour window |
| **Rate Limit** | Rolling window, soft limits |
| **Best For** | Complex reasoning, architecture decisions, multi-file refactoring |

**Strengths:**
- ✅ Excellent code understanding
- ✅ Multi-file context awareness
- ✅ Strong reasoning for business logic
- ✅ Good at translating between languages (PHP → Python)
- ✅ Native VS Code integration

**Weaknesses:**
- ⚠️ Limited daily quota (~500 messages)
- ⚠️ Can be slow for simple tasks
- ⚠️ Overkill for boilerplate code

**Use Cases for This Project:**
1. PHP → Python service layer translation (complex business logic)
2. Architecture decisions (API design, service patterns)
3. Complex React components (state management, hooks)
4. Multi-file refactoring
5. Code review and validation
6. Debugging complex issues

**Estimated Usage:** 30-40% of tasks (~150-200 messages for entire project)

---

### 2. GitHub Copilot (License: Copilot Pro)

**Access Method:** VS Code extension + Copilot Chat

#### Tier 0x: Free/Unlimited Models

##### 2a. GPT-4o (PRIMARY WORKHORSE)

| Specification | Value |
|---------------|-------|
| **Model** | GPT-4o (OpenAI) |
| **Context Window** | 128,000 tokens (~400 pages) |
| **Cost per Request** | $0 (unlimited in Copilot Pro) |
| **Daily Limit** | Unlimited |
| **Rate Limit** | None |
| **Best For** | Code generation, boilerplate, tests, completions |

**Strengths:**
- ✅ Very fast response time
- ✅ Unlimited usage
- ✅ Excellent for repetitive patterns
- ✅ Great at test generation
- ✅ Strong code completion
- ✅ Multimodal (can understand images if needed)

**Weaknesses:**
- ⚠️ May lose context in very long sessions
- ⚠️ Less sophisticated reasoning than Claude
- ⚠️ Can hallucinate on complex business logic

**Use Cases for This Project:**
1. SQLAlchemy models (8 files, repetitive structure)
2. Pydantic schemas (10 files, validation patterns)
3. FastAPI routes (boilerplate CRUD)
4. Unit tests (pytest, vitest)
5. React components (simple, MUI patterns)
6. Code completions (inline)
7. Forms (React Hook Form)

**Estimated Usage:** 50-60% of tasks (~300-400 requests)

---

##### 2b. GPT-4.1

| Specification | Value |
|---------------|-------|
| **Model** | GPT-4.1 (OpenAI) |
| **Context Window** | 128,000 tokens |
| **Cost per Request** | $0 (unlimited) |
| **Daily Limit** | Unlimited |
| **Best For** | Refactoring, improved reasoning over GPT-4o |

**Use Cases:** Fallback when GPT-4o struggles with logic

**Estimated Usage:** 5-10% of tasks

---

##### 2c. GPT-5 mini

| Specification | Value |
|---------------|-------|
| **Model** | GPT-5 mini (OpenAI) |
| **Context Window** | 128,000 tokens |
| **Cost per Request** | $0 (unlimited) |
| **Daily Limit** | Unlimited |
| **Best For** | Quick fixes, simple tasks |

**Use Cases:** Fast iterations, simple code changes

**Estimated Usage:** <5% of tasks

---

##### 2d. Grok Code Fast 1 (Preview)

| Specification | Value |
|---------------|-------|
| **Model** | Grok Code Fast 1 (xAI) |
| **Context Window** | Unknown |
| **Cost per Request** | $0 (unlimited) |
| **Daily Limit** | Unlimited |
| **Status** | Preview (may be unstable) |
| **Best For** | Very fast code completion |

**Use Cases:** Experimental, not primary

**Estimated Usage:** <1% of tasks

---

#### Tier 0.33x: Limited Models (Cheaper)

##### 2e. o3-mini

| Specification | Value |
|---------------|-------|
| **Model** | o3-mini (OpenAI reasoning) |
| **Context Window** | 128,000 tokens |
| **Cost per Request** | 0.33x (cheaper than 1x tier) |
| **Daily Limit** | ~100 requests |
| **Best For** | Complex reasoning, edge cases |

**Use Cases:** Complex algorithms, edge case analysis

**Estimated Usage:** <5% of tasks

---

##### 2f. o4-mini (Preview)

| Specification | Value |
|---------------|-------|
| **Model** | o4-mini (OpenAI reasoning) |
| **Status** | Preview |
| **Cost per Request** | 0.33x |
| **Daily Limit** | ~100 requests |

**Use Cases:** Alternative to o3-mini

**Estimated Usage:** <1% of tasks

---

#### Tier 1x: Limited Models (Premium)

##### 2g. Claude Sonnet 3.5, 3.7, 4 (via Copilot)

| Specification | Value |
|---------------|-------|
| **Models** | Claude Sonnet 3.5, 3.7, 4 |
| **Context Window** | 200,000 tokens |
| **Cost per Request** | 1x (premium tier) |
| **Daily Limit** | ~50 requests |
| **Best For** | Complex logic (alternative to Claude Code) |

**Use Cases:** When Claude Code quota exhausted

**Estimated Usage:** <5% of tasks (as fallback)

---

##### 2h. Gemini 2.5 Pro (via Copilot)

| Specification | Value |
|---------------|-------|
| **Model** | Gemini 2.5 Pro |
| **Context Window** | 1,000,000 tokens |
| **Cost per Request** | 1x (premium tier) |
| **Daily Limit** | ~30 requests via Copilot |
| **Best For** | Long context analysis |

**Use Cases:** Prefer direct Gemini Code Assist (higher limits)

**Estimated Usage:** <1% of tasks (use Gemini Code Assist instead)

---

##### 2i. GPT-5

| Specification | Value |
|---------------|-------|
| **Model** | GPT-5 (OpenAI latest) |
| **Context Window** | 128,000 tokens (estimated) |
| **Cost per Request** | 1x (premium tier) |
| **Daily Limit** | ~50 requests |
| **Best For** | Latest capabilities |

**Use Cases:** Experimental, when GPT-4o insufficient

**Estimated Usage:** <5% of tasks

---

### 3. ChatGPT Plus / Codex (License: ChatGPT Plus)

**Access Method:** ChatGPT web interface or API

| Specification | Value |
|---------------|-------|
| **Model** | GPT-4 Turbo (with code interpreter) |
| **Context Window** | 128,000 tokens |
| **Cost per Request** | $0 (included in subscription) |
| **Hourly Limit** | ~40 messages/3h (GPT-4), ~80 messages/3h (GPT-4o) |
| **Daily Limit** | ~250-300 messages |
| **Best For** | Algorithms, debugging, Python execution |

**Strengths:**
- ✅ Can execute Python code (code interpreter)
- ✅ Strong mathematical/algorithmic reasoning
- ✅ Good for debugging complex logic
- ✅ Can analyze data, run calculations

**Weaknesses:**
- ⚠️ Hourly limits (40-80 msg/3h)
- ⚠️ Not integrated into VS Code workflow
- ⚠️ Requires copy-paste of code

**Use Cases for This Project:**
1. Currency conversion algorithms (complex calculations)
2. Statistical calculations (stats service)
3. next_payment date calculation logic (edge cases)
4. Debugging algorithm issues
5. Edge case analysis

**Estimated Usage:** 2-5% of tasks (~20-30 messages)

---

### 4. Gemini Code Assist (License: Google AI Pro - FREE)

**Access Method:** VS Code extension

| Specification | Value |
|---------------|-------|
| **Model** | Gemini 2.5 Pro |
| **Context Window** | **1,000,000 tokens** (~3,000 pages!) |
| **Cost per Request** | $0 (free tier) |
| **Rate Limit** | 50 requests/minute |
| **Daily Limit** | 1,000 requests/day |
| **Monthly Limit** | Free tier limits |
| **Best For** | **Long context analysis**, code review, validation |

**Strengths:**
- ✅ **MASSIVE context window** (1M tokens = entire codebase!)
- ✅ Excellent code review capabilities
- ✅ Can analyze entire project at once
- ✅ Strong validation and error detection
- ✅ Good at suggesting alternatives
- ✅ FREE (Google AI Pro free tier)

**Weaknesses:**
- ⚠️ Slower than GPT-4o
- ⚠️ Less specialized in code generation
- ⚠️ Free tier has monthly token limits

**Use Cases for This Project:**
1. **Code review** (validate entire phase against USER_STORIES.md)
2. **Long context validation** (check consistency across 50+ files)
3. **Refactoring suggestions** (with full project context)
4. **Alternative implementations** (when primary AI stuck)
5. **Final quality check** before phase completion
6. **Context preservation** (can hold entire project in memory)

**Estimated Usage:** 5-10% of tasks (~30-50 requests) - **CRITICAL for validation**

---

### 5. DeepInfra (License: API Key, Budget: $10)

**Access Method:** HTTP API (httpx/requests)

#### 5a. Qwen 2.5 Coder 32B (PRIMARY for batch)

| Specification | Value |
|---------------|-------|
| **Model** | Qwen 2.5 Coder 32B |
| **Context Window** | 32,768 tokens |
| **Cost per 1M Tokens** | **$0.27** (input + output combined) |
| **Daily Limit** | None (budget only) |
| **Rate Limit** | 100 requests/minute |
| **Best For** | **Batch code generation**, cost-effective processing |

**Budget Calculation:**
- $10 budget ÷ $0.27 per 1M tokens = **~37M tokens available**

**Strengths:**
- ✅ **Very cost-effective** ($0.27/1M tokens)
- ✅ Specialized for code (Qwen Coder)
- ✅ Good quality for batch operations
- ✅ No daily limits (only budget)
- ✅ Fast API response

**Weaknesses:**
- ⚠️ Smaller context (32k tokens)
- ⚠️ Requires API integration
- ⚠️ Not integrated into VS Code

**Use Cases for This Project:**
1. **Batch i18n conversion** (25 JS files → 2 JSON files)
2. **Batch Pydantic schema generation** (10 schemas at once)
3. **Batch test generation** (all backend tests)
4. **PHP → Python service layer** (bulk conversion)
5. **React components batch** (generate 20 components)

**Estimated Token Usage:**
- i18n: ~1.5M tokens = $0.40
- Schemas: ~5M tokens = $1.35
- Tests: ~7M tokens = $1.89
- Services: ~11M tokens = $2.97
- React: ~7M tokens = $1.89
- **Total: ~31.5M tokens = $8.50** (leaving $1.50 buffer)

**Estimated Usage:** <1% of tasks (by count), ~20% by volume

---

#### 5b. DeepSeek Coder 33B (ALTERNATIVE)

| Specification | Value |
|---------------|-------|
| **Model** | DeepSeek Coder 33B |
| **Context Window** | 16,384 tokens |
| **Cost per 1M Tokens** | $0.27 |
| **Best For** | Refactoring, code translation |

**Use Cases:** Alternative to Qwen if quality issues

**Estimated Usage:** Backup only

---

#### 5c. Llama 3.3 70B

| Specification | Value |
|---------------|-------|
| **Model** | Meta Llama 3.3 70B |
| **Context Window** | 128,000 tokens |
| **Cost per 1M Tokens** | $0.59 |
| **Best For** | Complex tasks requiring larger model |

**Budget:** $10 ÷ $0.59 = ~17M tokens

**Use Cases:** If Qwen insufficient for complex batch tasks

**Estimated Usage:** Backup only

---

#### 5d. Mistral Large

| Specification | Value |
|---------------|-------|
| **Model** | Mistral Large |
| **Context Window** | 128,000 tokens |
| **Cost per 1M Tokens** | $2.00 |
| **Best For** | General purpose, highest quality |

**Budget:** $10 ÷ $2 = ~5M tokens

**Use Cases:** Last resort for critical batch tasks

**Estimated Usage:** Unlikely to use (too expensive for our needs)

---

## Task Assignment Matrix

### By Task Type

| Task Type | Primary Model | Fallback | Cost | Reason |
|-----------|---------------|----------|------|--------|
| **Database Models** | GPT-4o (Copilot) | Claude Sonnet 4.5 | $0 | Repetitive structure, patterns |
| **Pydantic Schemas** | GPT-4o (Copilot) | - | $0 | Validation patterns |
| **API Routes (simple)** | GPT-4o (Copilot) | - | $0 | Boilerplate FastAPI |
| **API Routes (complex)** | Claude Sonnet 4.5 | GPT-4.1 | $0 | Multi-param queries |
| **Service Layer (simple)** | GPT-4o (Copilot) | - | $0 | CRUD operations |
| **Service Layer (complex)** | Claude Sonnet 4.5 | o3-mini | $0 | **PHP business logic translation** |
| **Algorithms** | GPT-4 Turbo (ChatGPT) | Claude Sonnet 4.5 | $0 | Mathematical reasoning |
| **Unit Tests** | GPT-4o (Copilot) | - | $0 | Test generation specialty |
| **Integration Tests** | Claude Sonnet 4.5 | GPT-4o | $0 | Complex scenarios |
| **React Components (simple)** | GPT-4o (Copilot) | - | $0 | MUI patterns |
| **React Components (complex)** | Claude Sonnet 4.5 | GPT-4.1 | $0 | State management, hooks |
| **Forms** | GPT-4o (Copilot) | - | $0 | React Hook Form patterns |
| **Code Review** | Gemini 2.5 Pro | Claude Sonnet 4.5 | $0 | **1M context window** |
| **Validation** | Gemini 2.5 Pro | - | $0 | Long context analysis |
| **Batch i18n** | Qwen 2.5 (DeepInfra) | - | **$0.50** | Cost-effective bulk |
| **Batch Schemas** | Qwen 2.5 (DeepInfra) | - | **$1.50** | Bulk generation |
| **Batch Tests** | Qwen 2.5 (DeepInfra) | - | **$2.00** | Bulk generation |
| **Batch Services** | Qwen 2.5 (DeepInfra) | - | **$3.00** | PHP→Python bulk |
| **Batch Components** | Qwen 2.5 (DeepInfra) | - | **$2.00** | React bulk |

---

### By Complexity Level

| Complexity | Primary Model | Rationale |
|------------|---------------|-----------|
| **Simple/Boilerplate** | GPT-4o (Copilot) | Fast, unlimited, good enough |
| **Medium** | GPT-4o or Claude Code | Based on task (data vs logic) |
| **Complex Logic** | Claude Sonnet 4.5 | Best reasoning, code understanding |
| **Algorithms** | GPT-4 Turbo | Mathematical reasoning |
| **Validation** | Gemini 2.5 Pro | Massive context |
| **Bulk Operations** | Qwen 2.5 (DeepInfra) | Cost-effective |

---

## Phase-by-Phase Cost Analysis

### PREPARATION Phase (1-2 days)

| Task | Model | License | Requests | Cost |
|------|-------|---------|----------|------|
| Database schema analysis | Claude Code | Claude Pro | 5 | $0 |
| Generate analysis docs | Claude Code | Claude Pro | 3 | $0 |
| **TOTAL** | - | - | **8** | **$0** |

---

### PHASE 1: Backend Foundation (4-5 days)

| Task | Model | License | Requests | Cost |
|------|-------|---------|----------|------|
| SQLAlchemy Models (8 files) | GPT-4o | Copilot Pro | 8-12 | $0 |
| Models validation | Gemini 2.5 Pro | Google AI Pro | 1 | $0 |
| Pydantic Schemas (10 files) | GPT-4o | Copilot Pro | 10-15 | $0 |
| Schemas validation | Claude Code | Claude Pro | 5 | $0 |
| API Routes (simple) | GPT-4o | Copilot Pro | 30-40 | $0 |
| API Routes (complex) | Claude Code | Claude Pro | 10-15 | $0 |
| Service Layer (simple) | GPT-4o | Copilot Pro | 15-20 | $0 |
| Service Layer (complex) | Claude Code | Claude Pro | 15-20 | $0 |
| Algorithms | GPT-4 Turbo | ChatGPT Plus | 5-10 | $0 |
| Unit Tests | GPT-4o | Copilot Pro | 20-30 | $0 |
| **TOTAL** | - | - | **119-167** | **$0** |

---

### PHASE 2: Backend Advanced (5-6 days)

| Task | Model | License | Requests | Cost |
|------|-------|---------|----------|------|
| Currency Service (Fixer API) | Claude Code | Claude Pro | 10 | $0 |
| Currency calculations | GPT-4 Turbo | ChatGPT Plus | 3 | $0 |
| Notification Service | GPT-4o | Copilot Pro | 5 | $0 |
| Logo Service (Pillow) | Claude Code | Claude Pro | 8 | $0 |
| Stats Service | GPT-4 Turbo | ChatGPT Plus | 8 | $0 |
| Stats aggregations | Claude Code | Claude Pro | 5 | $0 |
| Tests (all services) | GPT-4o | Copilot Pro | 15-20 | $0 |
| Validation review | Gemini 2.5 Pro | Google AI Pro | 3 | $0 |
| **TOTAL** | - | - | **57-62** | **$0** |

---

### PHASE 3: Backend Infrastructure (3-4 days)

| Task | Model | License | Requests | Cost |
|------|-------|---------|----------|------|
| Celery Tasks | Claude Code | Claude Pro | 10 | $0 |
| OpenAPI Examples | GPT-4o | Copilot Pro | 5 | $0 |
| Admin Endpoints | GPT-4o | Copilot Pro | 8 | $0 |
| Integration Tests | Claude Code | Claude Pro | 10 | $0 |
| **TOTAL** | - | - | **33** | **$0** |

---

### PHASE 4: Frontend Foundation (1.5-2 weeks)

| Task | Model | License | Tokens/Requests | Cost |
|------|-------|---------|-----------------|------|
| MUI Theme Setup | GPT-4o | Copilot Pro | 3 | $0 |
| **i18n Conversion (batch)** | **Qwen 2.5** | **DeepInfra** | **~1.5M tokens** | **$0.40** |
| Routing Setup | GPT-4o | Copilot Pro | 3 | $0 |
| API Client (Axios) | GPT-4o | Copilot Pro | 5 | $0 |
| **TOTAL** | - | - | **11 req + 1.5M tok** | **$0.40** |

---

### PHASE 5: Frontend Core (2-3 weeks)

| Task | Model | License | Requests | Cost |
|------|-------|---------|----------|------|
| Dashboard (simple) | GPT-4o | Copilot Pro | 5 | $0 |
| SubscriptionList | Claude Code | Claude Pro | 10 | $0 |
| SubscriptionForm | Claude Code | Claude Pro | 12 | $0 |
| SubscriptionCard | GPT-4o | Copilot Pro | 3 | $0 |
| Settings Pages (7 files) | GPT-4o | Copilot Pro | 15 | $0 |
| CategorySettings (drag-drop) | Claude Code | Claude Pro | 8 | $0 |
| Forms (React Hook Form) | GPT-4o | Copilot Pro | 10 | $0 |
| Component Tests | GPT-4o | Copilot Pro | 20 | $0 |
| **TOTAL** | - | - | **83** | **$0** |

---

### PHASE 6: Frontend Advanced (1.5-2 weeks)

| Task | Model | License | Requests | Cost |
|------|-------|---------|----------|------|
| Statistics Page | Claude Code | Claude Pro | 12 | $0 |
| Charts (Recharts) | GPT-4o | Copilot Pro | 8 | $0 |
| Admin Panel | GPT-4o | Copilot Pro | 10 | $0 |
| Logo Upload (drag-drop) | Claude Code | Claude Pro | 8 | $0 |
| Export Buttons | GPT-4o | Copilot Pro | 3 | $0 |
| E2E Tests (optional) | Claude Code | Claude Pro | 8 | $0 |
| **TOTAL** | - | - | **49** | **$0** |

---

### BATCH Operations (DeepInfra - Optional Optimization)

| Task | Model | Tokens (estimated) | Cost |
|------|-------|-------------------|------|
| i18n conversion (PL+EN) | Qwen 2.5 | ~1.5M | **$0.40** |
| Batch Pydantic schemas (10) | Qwen 2.5 | ~5M | **$1.35** |
| Batch backend tests | Qwen 2.5 | ~7M | **$1.89** |
| PHP→Python services (bulk) | Qwen 2.5 | ~11M | **$2.97** |
| React components (batch 20) | Qwen 2.5 | ~7M | **$1.89** |
| **Buffer** | - | - | **$1.50** |
| **TOTAL** | - | **~31.5M tokens** | **$10.00** |

---

### PROJECT TOTAL

| Phase | Requests (est.) | DeepInfra Cost | Total Cost |
|-------|----------------|----------------|------------|
| PREPARATION | 8 | $0 | $0 |
| PHASE 1 | 119-167 | $0 | $0 |
| PHASE 2 | 57-62 | $0 | $0 |
| PHASE 3 | 33 | $0 | $0 |
| PHASE 4 | 11 | $0.40 | $0.40 |
| PHASE 5 | 83 | $0 | $0 |
| PHASE 6 | 49 | $0 | $0 |
| BATCH (optional) | - | $9.60 | $9.60 |
| **TOTAL** | **~360-410** | **$10.00** | **$10.00** |

**AI Requests Breakdown:**
- Claude Code: ~120-150 (within ~500/day limit)
- GPT-4o (Copilot): ~200-250 (unlimited)
- Gemini 2.5 Pro: ~5-10 (within 1000/day limit)
- GPT-4 Turbo: ~15-20 (within ~250/day limit)
- DeepInfra: API calls (budget-limited)

**All within limits! ✅**

---

## DeepInfra Budget Optimization

### Strategy: Batch Processing for Maximum ROI

**Budget:** $10
**Primary Model:** Qwen 2.5 Coder 32B ($0.27/1M tokens)
**Available Tokens:** ~37M

### Allocation Breakdown

#### 1. i18n Conversion ($0.40-0.50)

**Task:** Convert PHP language files to React JSON
- **Input:** `scripts/i18n/{pl,en}.js` (2 files, ~50k tokens)
- **Output:** `public/locales/{pl,en}/translation.json` (~25k tokens)
- **Total:** ~1.5M tokens
- **Cost:** $0.40
- **Savings:** 2-3 hours manual work

**Prompt Template:**
```
Convert JavaScript i18n file to JSON format for react-i18next.

Input: scripts/i18n/pl.js (PHP format)
Output: public/locales/pl/translation.json

Requirements:
- Flat structure (no nested objects)
- Key-value pairs
- Preserve all translations
- Remove JS export syntax
```

---

#### 2. Batch Pydantic Schemas ($1.35-1.50)

**Task:** Generate all 10 Pydantic schemas in one batch
- **Input:** SQLAlchemy models + requirements (~2M tokens)
- **Output:** 10 schema files (~3M tokens)
- **Total:** ~5M tokens
- **Cost:** $1.35
- **Savings:** 4-6 hours manual work

**Prompt Template:**
```
Generate all Pydantic schemas for the following models:
[Include all 8 SQLAlchemy model files]

For each model, create:
1. {Model}Base - shared fields
2. {Model}Create - for POST
3. {Model}Update - for PATCH
4. {Model}Response - for GET
5. {Model}InDB - with timestamps

Requirements:
- Pydantic v2 syntax
- Full validation (Field, validators)
- Type hints
- Docstrings

Output: 10 separate Python files
```

---

#### 3. Batch Backend Tests ($1.89-2.00)

**Task:** Generate all pytest tests for services
- **Input:** All service files + schemas (~3M tokens)
- **Output:** All test files (~4M tokens)
- **Total:** ~7M tokens
- **Cost:** $1.89
- **Savings:** 1-2 days manual work

**Prompt Template:**
```
Generate pytest tests for all services:

Services:
[Include all 9 service files]

For each service, test:
- All public methods
- Happy path
- Edge cases
- Error handling
- Mocked dependencies

Requirements:
- pytest-asyncio
- >80% coverage
- Fixtures in conftest.py
```

---

#### 4. PHP→Python Services ($2.97-3.00)

**Task:** Bulk convert PHP service logic to Python
- **Input:** All PHP endpoints (~5M tokens)
- **Output:** Python services (~6M tokens)
- **Total:** ~11M tokens
- **Cost:** $2.97
- **Savings:** 3-4 days manual work

**Prompt Template:**
```
Convert PHP endpoints to Python FastAPI services.

PHP files:
[Include all endpoints/subscription/*.php, endpoints/currency/*.php, etc.]

For each PHP file, generate:
1. Python service method
2. Async/await syntax
3. SQLAlchemy queries
4. Error handling
5. Type hints

Preserve all business logic exactly.
```

---

#### 5. React Components Batch ($1.89-2.00)

**Task:** Generate ~20 React components in batch
- **Input:** Component specs + API schemas (~3M tokens)
- **Output:** React components (~4M tokens)
- **Total:** ~7M tokens
- **Cost:** $1.89
- **Savings:** 1 week manual work

**Prompt Template:**
```
Generate React components for all pages:

Components needed:
1. SubscriptionList (with filters, sort, pagination)
2. SubscriptionForm (React Hook Form + Zod)
3. SubscriptionCard
4. CategorySettings
5. CurrencySettings
... (15 more)

Requirements:
- Material-UI v5
- TypeScript
- React Query
- React Hook Form + Zod
- Responsive
```

---

### ROI Analysis

| Batch Task | Cost | Time Saved | Hourly Rate Equiv. | ROI |
|-----------|------|------------|-------------------|-----|
| i18n | $0.40 | 2-3 hours | ~$0.15/hour | 🔴 Low (but necessary) |
| Schemas | $1.35 | 4-6 hours | ~$0.25/hour | 🔴 Low (better with Copilot) |
| Tests | $1.89 | 1-2 days | ~$0.10/hour | ⚠️ Consider Copilot instead |
| Services | $2.97 | 3-4 days | ~$0.12/hour | ✅ Good (complex logic) |
| Components | $1.89 | 1 week | ~$0.05/hour | ✅ Excellent (high volume) |

**Recommendation:**
- ✅ **DO use DeepInfra** for: i18n (necessary), Services (complex), Components (high volume)
- ⚠️ **CONSIDER** for: Tests (Copilot might be better/free)
- ❌ **SKIP** for: Schemas (Copilot free tier sufficient)

**Optimized Allocation:**
1. i18n conversion: $0.40 ✅
2. ~~Schemas: $1.35~~ → Use GPT-4o instead (free)
3. ~~Tests: $1.89~~ → Use GPT-4o instead (free)
4. Services: $3.00 ✅
5. Components: $2.00 ✅
6. **New total: $5.40** (saves $4.60 for emergencies!)

---

## Usage Limits & Fallback Strategy

### Daily Limit Tracking

| Model | Daily Limit | Estimated Daily Usage | Buffer |
|-------|-------------|----------------------|--------|
| Claude Code | ~500 msg | ~30-40 msg | ✅ Safe |
| GPT-4o (Copilot) | Unlimited | ~50-80 msg | ✅ Safe |
| Gemini 2.5 Pro | 1000 req | ~2-5 req | ✅ Safe |
| GPT-4 Turbo | ~250 msg | ~3-5 msg | ✅ Safe |
| Claude Sonnet 4 (Copilot) | ~50 req | 0 (only as fallback) | ✅ Safe |

**Conclusion:** All limits comfortably within usage patterns

---

### Fallback Chain

```
Task: Generate Service Layer (complex)

PRIMARY:   Claude Code (Sonnet 4.5)
           ↓ (if quota exceeded)
FALLBACK1: Claude Sonnet 4 (via Copilot, limited tier)
           ↓ (if quota exceeded)
FALLBACK2: o3-mini (Copilot, limited tier)
           ↓ (if quota exceeded)
FALLBACK3: GPT-4.1 (Copilot, free tier)
           ↓ (if still insufficient)
MANUAL:    Human review + manual coding
```

**Likelihood of needing fallback:** <5% (limits are generous)

---

## Model Selection Decision Tree

```
START: Classify Task
│
├─ Is it simple boilerplate?
│  ├─ YES → GPT-4o (Copilot) [FAST, FREE, UNLIMITED]
│  └─ NO → Continue
│
├─ Does it require complex reasoning?
│  ├─ YES →
│  │  ├─ Is it business logic from PHP?
│  │  │  ├─ YES → Claude Code (Sonnet 4.5) [BEST FOR PHP→PY]
│  │  │  └─ NO →
│  │  │     ├─ Is it mathematical/algorithmic?
│  │  │     │  ├─ YES → GPT-4 Turbo (ChatGPT) [BEST FOR MATH]
│  │  │     │  └─ NO → Claude Code [DEFAULT FOR COMPLEX]
│  │  └─ NO → Continue
│  │
├─ Is it validation/review?
│  ├─ YES →
│  │  ├─ Does it need >100k context?
│  │  │  ├─ YES → Gemini 2.5 Pro [1M CONTEXT]
│  │  │  └─ NO → Claude Code [GOOD REASONING]
│  │  └─ NO → Continue
│  │
├─ Is it batch/bulk operation?
│  ├─ YES →
│  │  ├─ Is cost-effectiveness critical?
│  │  │  ├─ YES → Qwen 2.5 (DeepInfra) [$0.27/1M]
│  │  │  └─ NO → GPT-4o (Copilot) [FREE]
│  │  └─ NO → Continue
│  │
└─ DEFAULT → GPT-4o (Copilot) [SAFE DEFAULT]
```

---

## Summary & Recommendations

### Optimal Strategy for Wallos Refactor

1. **Primary Workhorse:** GPT-4o (Copilot) - 60% of tasks
   - All boilerplate, tests, simple components
   - Free, unlimited, fast

2. **Complex Tasks:** Claude Code (Sonnet 4.5) - 30% of tasks
   - PHP→Python business logic
   - Architecture decisions
   - Complex React components

3. **Validation:** Gemini 2.5 Pro - 5% of tasks
   - End-of-phase reviews
   - Long context checks
   - Alternative solutions

4. **Algorithms:** GPT-4 Turbo - 3% of tasks
   - Currency calculations
   - Statistical formulas
   - Edge case debugging

5. **Batch Operations:** Qwen 2.5 (DeepInfra) - <2% of tasks
   - i18n conversion: $0.40
   - PHP→Python services: $3.00
   - React components: $2.00
   - **Total: ~$5.50** (save $4.50 for buffer)

### Expected Outcomes

- **Total Project Cost:** $5.50 (vs $10 budget)
- **Time Savings:** 5-6 weeks (vs 11-15 weeks manual)
- **AI-Assisted:** 60-70% automation
- **Quality:** >80% test coverage, type-safe, production-ready

### Risk Mitigation

1. **Quota exhaustion:** Multi-tier fallback chain
2. **Quality issues:** Gemini 2.5 Pro validation after each phase
3. **Cost overrun:** $4.50 buffer + can use free tier fallbacks
4. **Context loss:** `context/_CORE_CONTEXT.md` always injected

---

**END OF REFERENCE DOCUMENT**
