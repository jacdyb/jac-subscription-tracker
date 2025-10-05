# AI Automation Quick Start Guide

**Complete setup in 5 minutes** → Start automating your refactor!

---

## Prerequisites

✅ Python 3.11+
✅ Active subscriptions:
- OpenAI API access (via ChatGPT Plus or separate)
- Claude Pro subscription
- Google AI Pro (free tier)
- DeepInfra account

---

## Step 1: Install Dependencies (1 min)

```bash
# Install automation requirements
pip install -r requirements-automation.txt
```

**What this installs:**
- `httpx` - Async HTTP client for API calls
- `python-dotenv` - Environment variable management
- `PyYAML` - Config file parsing
- `litellm` - (Optional) Unified API proxy

---

## Step 2: Set Up API Keys (3 min)

### Quick Setup

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your preferred editor
```

### Get Your API Keys

**See [API_KEYS_SETUP.md](API_KEYS_SETUP.md) for detailed instructions!**

Quick reference:

| Service | URL | Env Var |
|---------|-----|---------|
| **OpenAI** | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) | `OPENAI_API_KEY` |
| **Claude** | [claude.ai/account/api-keys](https://claude.ai/account/api-keys) | `ANTHROPIC_API_KEY` |
| **Gemini** | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | `GOOGLE_API_KEY` |
| **DeepInfra** | [deepinfra.com/dash/api_keys](https://deepinfra.com/dash/api_keys) | `DEEPINFRA_API_KEY` |

### Example .env

```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEEPINFRA_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Step 3: Test API Connections (1 min)

```bash
# Verify all APIs are working
python scripts/automation/test_apis.py
```

**Expected output:**

```
Testing API connections...

✓ OpenAI API (GPT-4o): OK [substitute for Copilot]
✓ OpenAI API (GPT-4 Turbo): OK [Codex/ChatGPT Plus]
✓ Claude API (Sonnet 4.5): OK
✓ Gemini API (2.5 Pro): OK
✓ DeepInfra API (Qwen 2.5): OK (cost: $0.0001)

============================================================
✨ All APIs ready! 5/5 passed 🎉

You can now run:
  python scripts/automation/orchestrator.py --all
============================================================
```

**If any API fails:**
- Check your API keys in `.env`
- See [API_KEYS_SETUP.md](API_KEYS_SETUP.md) troubleshooting section
- Verify you have active subscriptions

---

## Step 4: Run Automation! 🚀

### Option A: Run All Tasks (Full Automation)

```bash
# Generate everything at once
python scripts/automation/orchestrator.py --all
```

**What this does:**
- Generates 8 SQLAlchemy models in parallel (~5 min)
- Creates 10 Pydantic schemas in parallel (~6 min)
- Builds all API routes (~15 min)
- Creates service layer (~30 min)
- Generates tests (~10 min)
- **Total: ~2-3 hours** (vs 12+ hours manual)

### Option B: Run Specific Phase

```bash
# Backend only
python scripts/automation/orchestrator.py --phase backend

# Frontend only
python scripts/automation/orchestrator.py --phase frontend

# Models only
python scripts/automation/orchestrator.py --phase models
```

### Example Output

```
🚀 Starting full automation
   Total tasks: 24

📦 Running batch 1 (8 tasks)...
  ▶ Running: db_models (copilot.gpt-4o)...
  ▶ Running: pydantic_schemas (copilot.gpt-4o)...
  ▶ Running: api_routes_simple (copilot.gpt-4o)...
  ...
  ✓ Completed: db_models (12,453 tokens, 4.2s)
  ✓ Completed: pydantic_schemas (15,321 tokens, 5.1s)
  ...

✨ Automation complete!
   ✓ Completed: 22
   ✗ Failed: 2
   📊 Total tokens: 245,123
   ⏱️  Total time: 124.5s
   💰 DeepInfra spent: $0.32
```

---

## Understanding the Automation

### How It Works

1. **Task Assignment**: Reads `config/ai_models.yaml`
2. **Model Selection**: Automatically picks best AI model for each task
3. **Context Injection**: Adds `context/_CORE_CONTEXT.md` to every prompt
4. **Parallel Execution**: Runs 8-12 tasks simultaneously
5. **Validation**: Checks output against project constraints
6. **Budget Tracking**: Monitors DeepInfra spending (max $10)

### Model Selection Strategy

| Task Type | AI Model | Why |
|-----------|----------|-----|
| Simple CRUD | **GPT-4o** | Unlimited, fast, parallel |
| Complex logic | **Claude Sonnet 4.5** | Best reasoning |
| Validation | **Gemini 2.5 Pro** | 1M context window |
| Algorithms | **GPT-4 Turbo** | Math expert |
| Batch (10+) | **Qwen 2.5 Coder** | Cost-effective |

### Cost Breakdown

| Service | Model | Limit | Cost | Usage |
|---------|-------|-------|------|-------|
| OpenAI | GPT-4o | Unlimited | $0 | 90% |
| Claude | Sonnet 4.5 | 500/day | $0 | 5% |
| Gemini | 2.5 Pro | 1000/day | $0 | 3% |
| OpenAI | GPT-4 Turbo | 80/3h | $0 | 2% |
| DeepInfra | Qwen 2.5 | Budget | **$5-7** | <1% |

**Total project cost: $5-7** (only DeepInfra)

---

## Troubleshooting

### "OPENAI_API_KEY not set"

```bash
# Check .env file exists
ls -la .env

# Verify content
cat .env

# Make sure to load .env in your shell
export $(cat .env | xargs)
```

### "Rate limit exceeded"

**OpenAI (GPT-4o):** Shouldn't happen (unlimited)
**Claude:** 500/day limit - wait or use fallback
**Gemini:** 1000/day limit - wait or use fallback

### "Budget exceeded"

DeepInfra has hard limit of $10. Check spending:

```bash
cat .deepinfra_budget.json
```

Adjust in `config/ai_models.yaml`:

```yaml
limits:
  deepinfra.qwen-2-5-coder-32b:
    budget_max: 15.0  # Increase if needed
```

### API Connection Fails

1. **Check API key format**:
   - OpenAI: starts with `sk-proj-` or `sk-`
   - Claude: starts with `sk-ant-api03-`
   - Gemini: starts with `AIzaSy`
   - DeepInfra: varies

2. **Verify subscriptions**:
   - OpenAI: platform.openai.com → check billing
   - Claude: claude.ai → Settings → Subscription
   - Gemini: Free tier, no subscription needed
   - DeepInfra: deepinfra.com → add payment method

3. **Test each API individually** - see [API_KEYS_SETUP.md](API_KEYS_SETUP.md) verification section

---

## Optional: LiteLLM Proxy (Advanced)

**Why use LiteLLM?**
- Unified API interface (all models use OpenAI format)
- Automatic load balancing
- Cost tracking
- Retry logic

**Setup:**

```bash
# Create config
cp config/litellm_config.example.yaml config/litellm_config.yaml

# Start proxy
litellm --config config/litellm_config.yaml --port 4000

# Update .env to point to proxy
OPENAI_API_BASE=http://localhost:4000
```

See [API_KEYS_SETUP.md](API_KEYS_SETUP.md) for detailed LiteLLM setup.

---

## Next Steps

1. ✅ **APIs working?** → Run `--phase backend` to generate models
2. ✅ **Backend done?** → Run `--phase frontend` for React components
3. ✅ **All generated?** → Review code, run tests, commit!

**Full documentation:**
- [AI_STRATEGY.md](AI_STRATEGY.md) - Complete AI automation strategy
- [API_KEYS_SETUP.md](API_KEYS_SETUP.md) - Detailed API setup guide
- [REFACTOR_PLAN.md](REFACTOR_PLAN.md) - Overall refactor plan
- [config/ai_models.yaml](config/ai_models.yaml) - Task-to-model mappings

---

## Summary

✅ **Setup time:** 5 minutes
✅ **Total cost:** $5-7 (DeepInfra only)
✅ **Time savings:** 70% (15h vs 50h manual)
✅ **Automation:** Maximum (minimal intervention)

🚀 **Ready to automate? Run:**

```bash
python scripts/automation/test_apis.py    # Test first
python scripts/automation/orchestrator.py --all  # Then automate!
```

**Questions?** See [API_KEYS_SETUP.md](API_KEYS_SETUP.md) or check existing documentation.
