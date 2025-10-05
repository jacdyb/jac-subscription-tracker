# API Keys Setup Guide

**Complete guide to obtaining all API keys for automated refactoring**

⚠️ **IMPORTANT:** GitHub Copilot API nie ma publicznego API dostępu! Użyjemy **LiteLLM Proxy** jako workaround.

---

## Table of Contents

1. [LiteLLM Proxy Setup (Recommended)](#litellm-proxy-setup)
2. [Alternative: Direct API Keys](#alternative-direct-api-keys)
3. [API Keys for Each Provider](#api-keys-for-each-provider)
4. [Verification](#verification)

---

## LiteLLM Proxy Setup (Recommended)

### Dlaczego LiteLLM?

**Problem:** GitHub Copilot NIE ma publicznego API do automatyzacji
**Rozwiązanie:** LiteLLM Proxy - ujednolicone API dla wszystkich providerów

**Korzyści:**
- ✅ Jedno API dla wszystkich modeli (OpenAI format)
- ✅ Automatic load balancing
- ✅ Cost tracking
- ✅ Retry logic
- ✅ Rate limiting
- ✅ Copilot access via extension proxy

### Setup LiteLLM (10 minut)

#### 1. Install LiteLLM

```bash
pip install litellm[proxy]
```

#### 2. Create LiteLLM Config

**File:** `config/litellm_config.yaml`

```yaml
model_list:
  # Copilot (via GitHub Copilot API - requires extension workaround)
  - model_name: gpt-4o
    litellm_params:
      model: gpt-4o
      api_base: http://localhost:8000/copilot  # Local proxy
      api_key: ${GITHUB_TOKEN}

  # Claude (direct API)
  - model_name: claude-sonnet-4-5
    litellm_params:
      model: anthropic/claude-sonnet-4-20250514
      api_key: ${ANTHROPIC_API_KEY}

  # Gemini (direct API)
  - model_name: gemini-2-5-pro
    litellm_params:
      model: gemini/gemini-2.5-pro
      api_key: ${GOOGLE_API_KEY}

  # OpenAI / Codex (direct API)
  - model_name: gpt-4-turbo
    litellm_params:
      model: gpt-4-turbo
      api_key: ${OPENAI_API_KEY}

  # DeepInfra (direct API)
  - model_name: qwen-2-5-coder-32b
    litellm_params:
      model: deepinfra/Qwen/Qwen2.5-Coder-32B-Instruct
      api_key: ${DEEPINFRA_API_KEY}

# General settings
general_settings:
  master_key: ${LITELLM_MASTER_KEY}  # Generate: openssl rand -hex 32
  database_url: sqlite:///litellm.db  # Track usage

litellm_settings:
  drop_params: true  # Auto-remove unsupported params
  success_callback: ["langfuse"]  # Optional: tracking
  failure_callback: ["sentry"]  # Optional: error tracking
```

#### 3. Start LiteLLM Proxy

```bash
# Terminal 1: Start LiteLLM proxy
litellm --config config/litellm_config.yaml --port 4000

# Runs on: http://localhost:4000
```

#### 4. Test LiteLLM

```bash
curl http://localhost:4000/v1/models
```

---

## Alternative: Direct API Keys

Jeśli nie chcesz LiteLLM, użyj bezpośrednio API keys (ale Copilot będzie problemem).

---

## API Keys for Each Provider

### 1. ⚠️ GitHub Copilot (PROBLEM!)

**Problem:** GitHub Copilot **NIE MA** publicznego API!

**Opcje:**
1. **LiteLLM Proxy** (recommended) - see above
2. **Continue.dev** - open source, ma Copilot integration
3. **Aider** - może używać Copilot przez extension
4. **Fallback:** Użyj OpenAI API bezpośrednio (GPT-4o dostępne!)

**Rekomendacja:** Użyj **OpenAI API** bezpośrednio zamiast Copilot dla automatyzacji:
- Masz ChatGPT Plus → masz OpenAI API access
- GPT-4o dostępny przez OpenAI API
- Identyczny model jak w Copilot

### 2. Anthropic Claude API ✅

**Źródło:** https://claude.ai/account/api-keys

**Kroki:**
1. Zaloguj się na https://claude.ai
2. Przejdź do: Settings → API Keys
3. Kliknij: "Create API Key"
4. Nazwij: "Wallos Refactor Automation"
5. Skopiuj klucz: `sk-ant-api03-...`

**Format:**
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**Uprawnienia:** Full access (brak granularnych uprawnień)

**Limit:** ~500 requests/day (w ramach Claude Pro subscription)

**Weryfikacja:**
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

---

### 3. Google Gemini API ✅

**Źródło:** https://console.cloud.google.com/apis/credentials

**Kroki:**
1. Przejdź do: https://aistudio.google.com/apikey
2. Kliknij: "Create API Key"
3. Wybierz project (lub stwórz nowy)
4. Skopiuj klucz: `AIzaSy...`

**Format:**
```bash
export GOOGLE_API_KEY="AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**Uprawnienia:**
- "Generative Language API" musi być enabled
- Nie wymaga dodatkowych uprawnień

**Limit:**
- Free tier: 60 requests/minute, 1000 requests/day
- 1M tokens/day (!)

**Weryfikacja:**
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=$GOOGLE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "contents": [{"parts": [{"text": "Hello"}]}]
  }'
```

---

### 4. OpenAI API (ChatGPT Plus) ✅

**Źródło:** https://platform.openai.com/api-keys

**Kroki:**
1. Zaloguj się na: https://platform.openai.com
2. Przejdź do: API Keys
3. Kliknij: "Create new secret key"
4. Nazwij: "Wallos Refactor"
5. **Permissions:** All (or Project-specific)
6. Skopiuj klucz: `sk-proj-...` lub `sk-...`

**Format:**
```bash
export OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**Uprawnienia:**
- Wybierz: "All" lub
- Granular: "Model capabilities" → "Read & Write"

**Limit:**
- ChatGPT Plus subscribers: ~80 requests per 3 hours dla GPT-4
- GPT-4o: More generous limits

**Weryfikacja:**
```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4-turbo",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 100
  }'
```

**💡 TIP:** Użyj GPT-4o jako zamiennik dla Copilot!
```bash
# Copilot equivalent via OpenAI
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Generate SQLAlchemy model"}]
  }'
```

---

### 5. DeepInfra API ✅

**Źródło:** https://deepinfra.com/dash/api_keys

**Kroki:**
1. Zaloguj się na: https://deepinfra.com
2. Przejdź do: Dashboard → API Keys
3. Kliknij: "Create API Key"
4. Nazwij: "Wallos Refactor"
5. Skopiuj klucz: (format różny, np. `xxxx...`)

**Format:**
```bash
export DEEPINFRA_API_KEY="your_deepinfra_key_here"
```

**Uprawnienia:** Full access (brak opcji granularnych)

**Limit:** None (pay-per-use only)

**Pricing:** $0.27 per 1M tokens (Qwen 2.5 Coder 32B)

**Weryfikacja:**
```bash
curl https://api.deepinfra.com/v1/openai/chat/completions \
  -H "Authorization: Bearer $DEEPINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 100
  }'
```

---

## GitHub Token dla Copilot (⚠️ Ograniczenia)

### Problem z GitHub Copilot API

**GitHub Copilot NIE UDOSTĘPNIA publicznego API!**

Copilot działa tylko przez:
- VS Code extension (GUI only)
- GitHub CLI (limited)
- JetBrains plugin (GUI only)

**Nie ma:**
- REST API
- Python SDK
- Automation support

### Workaround 1: GitHub Token (Limited)

**Źródło:** https://github.com/settings/tokens

**Kroki:**
1. Przejdź do: Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Kliknij: "Generate new token (classic)"
3. Nazwij: "Wallos Refactor Automation"
4. Expiration: 90 days (max)
5. **Scopes (uprawnienia):**
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:org` (Read org and team membership)
   - ❌ **Brak scope dla Copilot API!** (nie istnieje)

**Format:**
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**⚠️ WAŻNE:** Ten token **NIE** daje dostępu do Copilot API, bo API nie istnieje!

### Workaround 2: Użyj OpenAI API zamiast Copilot

**Rekomendowane rozwiązanie:**

```yaml
# W config/ai_models.yaml zmień:

# Zamiast:
copilot:
  api_endpoint: "https://api.githubcopilot.com/v1"  # NIE ISTNIEJE!

# Użyj:
openai:
  name: "OpenAI API (GPT-4o substitute for Copilot)"
  api_endpoint: "https://api.openai.com/v1"
  auth_env_var: "OPENAI_API_KEY"
  models:
    gpt-4o:
      model_id: "gpt-4o"
      # Identical to Copilot's GPT-4o!
```

**Dlaczego to działa:**
- Copilot używa GPT-4o pod spodem
- OpenAI API daje bezpośredni dostęp do GPT-4o
- Identyczny model, identyczne wyniki
- Masz ChatGPT Plus → masz OpenAI API access

### Workaround 3: LiteLLM z Continue.dev Extension

**Jeśli NAPRAWDĘ chcesz Copilot:**

1. Install Continue.dev extension w VS Code
2. Continue ma Copilot integration
3. Continue expose local API endpoint
4. LiteLLM może się z nim połączyć

**Setup:**
```bash
# 1. Install Continue.dev extension
code --install-extension continue.continue

# 2. Configure Continue to use Copilot
# Edit: ~/.continue/config.json
{
  "models": [{
    "title": "GitHub Copilot",
    "provider": "github-copilot"
  }]
}

# 3. Continue starts local server on http://localhost:65432
# 4. LiteLLM proxy do tego endpoint
```

**Ale to skomplikowane!** Łatwiej użyć OpenAI API bezpośrednio.

---

## Recommended Setup (Simplest)

### Finalna Rekomendacja:

**ZAMIAST** walczyć z Copilot API (który nie istnieje):

```bash
# ~/.zshrc or ~/.bashrc

# 1. OpenAI (substitute for Copilot - GPT-4o)
export OPENAI_API_KEY="sk-proj-xxx"  # From platform.openai.com

# 2. Claude
export ANTHROPIC_API_KEY="sk-ant-api03-xxx"  # From claude.ai

# 3. Gemini
export GOOGLE_API_KEY="AIzaSyxxx"  # From aistudio.google.com

# 4. DeepInfra
export DEEPINFRA_API_KEY="xxx"  # From deepinfra.com

# Apply
source ~/.zshrc
```

**Update config/ai_models.yaml:**
```yaml
providers:
  # PRIMARY: OpenAI (GPT-4o) instead of Copilot
  openai:
    name: "OpenAI API (ChatGPT Plus)"
    api_endpoint: "https://api.openai.com/v1"
    auth_env_var: "OPENAI_API_KEY"
    models:
      gpt-4o:
        model_id: "gpt-4o"
        # Same as Copilot!

  # Keep others as-is
  claude: ...
  gemini: ...
  deepinfra: ...
```

---

## Verification Script

**Run after setup:**

```bash
python scripts/automation/test_apis.py
```

**Expected output:**
```
Testing API connections...

✓ OpenAI API (GPT-4o): OK [substitute for Copilot]
✓ Claude API (Sonnet 4.5): OK
✓ Gemini API (2.5 Pro): OK
✓ DeepInfra API (Qwen 2.5): OK

All APIs ready! 🎉
Total cost this session: $0.00
```

---

## Security Best Practices

### 1. Never Commit API Keys

```bash
# Add to .gitignore
echo "*.env" >> .gitignore
echo ".env.local" >> .gitignore
echo "config/api_keys.yaml" >> .gitignore
```

### 2. Use Environment Variables

```bash
# Store in shell profile (recommended)
~/.zshrc  # or ~/.bashrc

# Or use .env file (with python-dotenv)
cp .env.example .env
# Edit .env with your keys
```

### 3. Rotate Keys Regularly

- OpenAI: Rotate every 90 days
- Claude: Rotate every 90 days
- Gemini: Rotate every 180 days
- DeepInfra: Rotate when project done

### 4. Limit Scope

- GitHub: Only necessary repos
- OpenAI: Project-specific keys if possible
- Claude: (no scope options)
- Gemini: (no scope options)

---

## Troubleshooting

### Issue: "API key invalid"

```bash
# Test each key separately
curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"
curl https://api.anthropic.com/v1/messages -H "x-api-key: $ANTHROPIC_API_KEY" -d '{"model":"claude-sonnet-4-20250514","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'
```

### Issue: "Rate limit exceeded"

**OpenAI:**
```bash
# Check your quota
curl https://api.openai.com/dashboard/billing/usage \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

**Claude:** Limit to 500/day (check console.anthropic.com)

**Gemini:** Limit to 60/min, 1000/day (check console.cloud.google.com)

### Issue: "Copilot API not working"

**Solution:** Use OpenAI API (GPT-4o) instead!

Copilot API doesn't exist for automation. GPT-4o via OpenAI API is identical.

---

## Summary

### ✅ Working APIs (Use These):
1. **OpenAI API** (GPT-4o) - Substitute for Copilot ⭐
2. **Claude API** - Complex logic
3. **Gemini API** - Validation
4. **DeepInfra API** - Batch processing

### ❌ NOT Working:
- GitHub Copilot API - doesn't exist for automation!

### 💰 Cost:
- OpenAI + Claude + Gemini: **$0** (via existing licenses)
- DeepInfra: **$5-7** total

### ⏱️ Setup Time:
- Getting API keys: ~15 minutes
- Testing: ~5 minutes
- **Total: ~20 minutes**

---

**Next:** Run `python scripts/automation/test_apis.py` to verify!
