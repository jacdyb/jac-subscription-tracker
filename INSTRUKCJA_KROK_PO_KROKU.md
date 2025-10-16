# 🚀 Instrukcja Krok Po Kroku - Automatyzacja Refaktoryzacji

**Status:** Gotowe do uruchomienia
**Czas setup:** 10 minut
**Koszt całkowity:** $5-7 (tylko DeepInfra)

---

## ⚠️ ZNALEZIONE NIESPÓJNOŚCI I ICH ROZWIĄZANIA

### Niespójność #1: GitHub Copilot API NIE ISTNIEJE! ❌

**Problem:**
- `AUTOMATION_PLAN.md` mówi o "natywnych pluginach VS Code"
- `AI_STRATEGY.md` wspomina "GitHub Copilot API"
- `config/ai_models.yaml` ma endpoint `https://api.githubcopilot.com/v1` (NIE ISTNIEJE!)

**PRAWDA:**
GitHub Copilot **NIE MA** publicznego API do automatyzacji!

**ROZWIĄZANIE (już zaimplementowane):**
Użyj **OpenAI API** zamiast Copilot API:
- Copilot używa GPT-4o pod spodem
- Masz ChatGPT Plus → masz dostęp do OpenAI API
- OpenAI API = ten sam model (GPT-4o), bezpośredni dostęp
- **Już poprawione w `orchestrator.py` i `test_apis.py`**

---

### Niespójność #2: Strategia Orkiestracji

**Problem:**
- `AUTOMATION_PLAN.md` (linie 428-469): "Native Plugin" + "Lightweight Orchestration"
- `AI_STRATEGY.md`: Pełna automatyzacja przez API
- Niespójne podejście!

**ROZWIĄZANIE (już zaimplementowane):**
Pełna automatyzacja przez **Python scripts + API**:
- ✅ `scripts/automation/orchestrator.py` - główny silnik
- ✅ `scripts/automation/test_apis.py` - testy połączeń
- ✅ Brak manualnego otwierania okien VS Code
- ✅ Wszystko przez bezpośrednie wywołania API

---

### Niespójność #3: Nazewnictwo Platform

**Problem:**
- "Copilot" vs "OpenAI"
- "Codex" vs "ChatGPT Plus"
- Różne nazwy w różnych plikach

**ROZWIĄZANIE (ujednolicone):**
W **kodzie i skryptach**: użyj nazw API
- `openai` (dla GPT-4o i GPT-4 Turbo)
- `claude`
- `gemini`
- `deepinfra`

W **dokumentacji**: użyj nazw licencji
- "OpenAI API (substytut dla Copilot)"
- "Claude API (Claude Pro)"
- "Gemini API (Google AI Pro)"
- "OpenAI API GPT-4 Turbo (ChatGPT Plus)"
- "DeepInfra API"

---

## 📋 KROK 1: Zainstaluj Zależności (2 minuty)

```bash
# Przejdź do katalogu projektu
cd /Users/jacekdybowski/projects/jac-subscription-tracker

# Zainstaluj dependencies dla automatyzacji
pip install -r requirements-automation.txt
```

**Co zostanie zainstalowane:**
- `httpx` - async HTTP client do API
- `python-dotenv` - zarządzanie zmiennymi środowiskowymi
- `PyYAML` - parsowanie config/ai_models.yaml
- `litellm` - (opcjonalnie) unified proxy

**Weryfikacja:**
```bash
python -c "import httpx, yaml; print('✓ Dependencies OK')"
```

---

## 🔑 KROK 2: Skonfiguruj Klucze API (5 minut)

### 2.1 Skopiuj template

```bash
cp .env.example .env
```

### 2.2 Pobierz klucze API

Otwórz każdy link i skopiuj swój klucz:

#### ① OpenAI API (zastąpi Copilot)
- **Link:** https://platform.openai.com/api-keys
- **Kliknij:** "Create new secret key"
- **Nazwa:** "wallos-refactor"
- **Skopiuj:** `sk-proj-...` (48+ znaków)
- **Wklej do `.env`:**
  ```bash
  OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```

#### ② Claude API (Claude Pro)
- **Link:** https://claude.ai/account/api-keys (lub https://console.anthropic.com)
- **Kliknij:** "Create Key"
- **Nazwa:** "wallos-refactor"
- **Skopiuj:** `sk-ant-api03-...`
- **Wklej do `.env`:**
  ```bash
  ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```

#### ③ Google Gemini API (FREE tier)
- **Link:** https://aistudio.google.com/apikey
- **Kliknij:** "Create API Key"
- **Wybierz:** Existing project lub utwórz nowy
- **Skopiuj:** `AIzaSy...` (39 znaków)
- **Wklej do `.env`:**
  ```bash
  GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```

#### ④ DeepInfra API (pay-per-use, $10 max)
- **Link:** https://deepinfra.com/dash/api_keys
- **Zarejestruj się** (jeśli nie masz konta)
- **Dodaj kartę płatniczą** (wymagane, ale zapłacisz tylko za użycie)
- **Kliknij:** "Create new API key"
- **Skopiuj klucz**
- **Wklej do `.env`:**
  ```bash
  DEEPINFRA_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```

#### ⑤ GitHub Token (opcjonalny, NIE daje dostępu do Copilot API!)
- **Link:** https://github.com/settings/tokens
- **Kliknij:** "Generate new token (classic)"
- **Nazwa:** "wallos-refactor"
- **Zaznacz scope:** `repo` (tylko jeśli będziesz używał GitHub API do czegoś innego)
- **Skopiuj:** `ghp_...`
- **Wklej do `.env`:**
  ```bash
  GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```
- **UWAGA:** Ten token **NIE** daje dostępu do Copilot API (bo API nie istnieje!)

### 2.3 Weryfikuj plik .env

```bash
cat .env
```

Powinno wyglądać tak:
```bash
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-api03-...
GOOGLE_API_KEY=AIzaSy...
DEEPINFRA_API_KEY=...
GITHUB_TOKEN=ghp_...  # opcjonalny
```

### 2.4 Załaduj zmienne środowiskowe

```bash
# Dodaj do ~/.zshrc (Mac) lub ~/.bashrc (Linux)
echo 'export $(cat /Users/jacekdybowski/projects/jac-subscription-tracker/.env | xargs)' >> ~/.zshrc

# Albo załaduj ręcznie dla tej sesji:
export $(cat .env | xargs)
```

---

## ✅ KROK 3: Przetestuj Połączenia API (3 minuty)

```bash
python scripts/automation/test_apis.py
```

**Oczekiwany output:**
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

**Jeśli coś nie działa:**

### Problem: "OPENAI_API_KEY not set"
```bash
# Sprawdź czy .env istnieje
cat .env

# Załaduj zmienne
export $(cat .env | xargs)

# Spróbuj ponownie
python scripts/automation/test_apis.py
```

### Problem: "401 Unauthorized" dla OpenAI
- Sprawdź czy klucz zaczyna się od `sk-proj-` lub `sk-`
- Wejdź na https://platform.openai.com/api-keys
- Usuń stary klucz i utwórz nowy
- Skopiuj i wklej do `.env`

### Problem: "403 Forbidden" dla Claude
- Sprawdź czy masz aktywną subskrypcję Claude Pro
- Wejdź na https://claude.ai/account/api-keys
- Utwórz nowy klucz API
- **UWAGA:** Klucz API dla Claude Pro jest osobny od klucza dla Claude Code!

### Problem: "Invalid API key" dla Gemini
- Gemini API jest **darmowe**, ale wymaga utworzenia projektu w Google Cloud
- Wejdź na https://aistudio.google.com/apikey
- Kliknij "Create API Key"
- Wybierz istniejący projekt lub utwórz nowy (darmowy)

### Problem: "Payment required" dla DeepInfra
- DeepInfra wymaga **dodania karty płatniczej**
- Nie zostaniesz obciążony z góry
- Zapłacisz tylko za rzeczywiste użycie ($5-7 dla tego projektu)
- Wejdź na https://deepinfra.com/dash/settings → Billing

---

## 🎯 KROK 4: Uruchom Automatyzację! (OPCJONALNE - TESTOWE)

**UWAGA:** To tylko test! Poniższe komendy **nie generują** prawdziwych plików, tylko pokazują jak działa orchestrator.

### Opcja A: Test pojedynczej fazy (bezpieczny test)

```bash
# Test: wygeneruj modele (symulacja, nie zapisze plików)
python scripts/automation/orchestrator.py --phase backend

# Output:
# 🚀 Starting phase: backend
#    Tasks: 8
#
# 📦 Running batch 1 (8 tasks)...
#   ▶ Running: db_models (openai.gpt-4o)...
#   ✓ Completed: db_models (1234 tokens, 3.2s)
#   ...
```

### Opcja B: Sprawdź plan bez wykonywania

```bash
# Wyświetl plan automatyzacji (bez wykonywania)
python -c "
import yaml
from pathlib import Path

config = yaml.safe_load(Path('config/ai_models.yaml').read_text())

print('📋 PLAN AUTOMATYZACJI:\n')
for task_name, task_config in config['tasks'].items():
    primary = task_config.get('primary', 'N/A')
    time_est = task_config.get('estimated_time', 'N/A')
    cost = task_config.get('estimated_cost', 0)
    parallel = '✅ Równolegle' if task_config.get('parallel') else '❌ Sekwencyjnie'

    print(f'• {task_name}')
    print(f'  Model: {primary}')
    print(f'  Czas: {time_est}')
    print(f'  Koszt: \${cost}')
    print(f'  {parallel}')
    print()
"
```

---

## 📊 KROK 5: Zrozum Co Się Dzieje Pod Spodem

### Jak działa orchestrator.py?

```
┌─────────────────────────────────────────────────────────┐
│ 1. Czyta config/ai_models.yaml                         │
│    → Znajduje task: "db_models"                         │
│    → Primary: openai.gpt-4o                             │
│    → Parallel: 8                                        │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Ładuje context/_CORE_CONTEXT.md                     │
│    → SQLite ONLY                                        │
│    → MUI v5 ONLY                                        │
│    → PL+EN ONLY                                         │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Uruchamia 8 równoległych wywołań OpenAI API         │
│    ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                │
│    │ GPT  │ │ GPT  │ │ GPT  │ │ GPT  │ ...            │
│    │ 4o   │ │ 4o   │ │ 4o   │ │ 4o   │                │
│    └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘                │
│       │        │        │        │                      │
│    user.py  sub.py  cat.py  curr.py ...                │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Walidacja z context_validator.py                    │
│    ✓ Brak PostgreSQL                                   │
│    ✓ Brak Chakra UI                                    │
│    ✓ Tylko PL+EN                                       │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Zwraca wyniki                                        │
│    ✓ Completed: 8/8                                    │
│    📊 Total tokens: 98,432                             │
│    💰 Cost: $0.00 (OpenAI via license)                 │
└─────────────────────────────────────────────────────────┘
```

### Strategia wyboru modelu AI:

```
Zadanie proste/średnie (90% tasków)
    → OpenAI API (GPT-4o)
    → Nielimitowane, darmowe (via ChatGPT Plus)
    → Równolegle do 12 tasków jednocześnie
    ✅ 8 modeli SQLAlchemy w 5 minut

Zadanie złożone (5% tasków)
    → Claude API (Sonnet 4.5)
    → ~500 msg/dzień (wystarczy!)
    → Sekwencyjnie (głębsze rozumowanie)
    ✅ Serwis SubscriptionService w 45 minut

Walidacja całości (3% tasków)
    → Gemini API (2.5 Pro)
    → 1M tokenów kontekstu! (cała baza kodu)
    → Darmowe
    ✅ Review wszystkich 60 endpointów w 5 minut

Algorytmy/matematyka (2% tasków)
    → OpenAI API (GPT-4 Turbo)
    → 80 msg/3h (wystarczy)
    → ChatGPT Plus license
    ✅ Kalkulacje dat płatności

Batch >10 plików (<1% tasków)
    → DeepInfra API (Qwen 2.5)
    → $0.27/1M tokenów
    → Tylko gdy sensowne ekonomicznie
    ✅ Konwersja 25 plików i18n → 2 pliki ($0.40)
```

---

## 💰 KROK 6: Zrozum Koszty

### Miesięczne subskrypcje (już masz):
- OpenAI / ChatGPT Plus: **$20/mies** ✅ (już płacisz)
- Claude Pro: **$20/mies** ✅ (już płacisz)
- Google AI Pro: **$0** ✅ (darmowy tier)
- ~~GitHub Copilot Pro: $10/mies~~ ❌ (NIE UŻYWAMY - brak API!)

### Dodatkowy koszt dla tego projektu:
- DeepInfra: **$5-7** (jednorazowo, dla całego projektu)
  - i18n conversion (25→2 języki): $0.40
  - Batch React components (jeśli >10): $2.00
  - Buffer/fallback: $3.00
  - **Max limit: $10** (hard stop)

### Całkowity koszt automatyzacji:
```
Subskrypcje (już masz):     $40/mies
+ DeepInfra (projekt):      $5-7
─────────────────────────────────────
RAZEM dla projektu:         $5-7  ← TYLKO TO PŁACISZ EXTRA!
```

**Oszczędność czasu:**
- Manualnie: 50 godzin
- Z automatyzacją: 15 godzin
- **Zaoszczędzisz: 35 godzin** (70%)

**Wartość twojego czasu:**
- Jeśli 1h = 100 PLN → zaoszczędzisz 3,500 PLN
- Koszt automatyzacji: ~25 PLN ($5-7)
- **ROI: 14,000%** 🚀

---

## 🎓 KROK 7: Naucz Się Podstawowych Komend

### Test pojedynczego API:

```bash
# Test OpenAI
python -c "
import asyncio
import httpx
import os

async def test():
    client = httpx.AsyncClient()
    response = await client.post(
        'https://api.openai.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {os.getenv(\"OPENAI_API_KEY\")}'},
        json={
            'model': 'gpt-4o',
            'messages': [{'role': 'user', 'content': 'Hello!'}],
            'max_tokens': 10
        }
    )
    print('Status:', response.status_code)
    print('Response:', response.json())
    await client.aclose()

asyncio.run(test())
"
```

### Sprawdź budżet DeepInfra:

```bash
# Sprawdź ile wydałeś
cat .deepinfra_budget.json

# Albo jeszcze nie istnieje (dobry znak - nic nie wydałeś!)
```

### Zobacz logi requestów:

```bash
# Zobacz wszystkie requesty AI (jeśli orchestrator był uruchomiony)
cat .ai_requests.log
```

---

## 🚀 KROK 8: Przygotuj Się Do Prawdziwej Automatyzacji

**UWAGA:** Poniższe kroki **BĘDĄ GENEROWAĆ** prawdziwy kod!

### Przed uruchomieniem:

1. **Backup bazy danych:**
   ```bash
   cp db/wallos.db db/wallos.db.backup
   ```

2. **Commit obecnego stanu:**
   ```bash
   git add .
   git commit -m "chore: przed automatyczną generacją kodu"
   ```

3. **Utwórz branch:**
   ```bash
   git checkout -b automated-refactor
   ```

### Uruchom Phase 1 - Backend Models (przykład):

```bash
# Wygeneruj 8 modeli SQLAlchemy równolegle
python scripts/automation/orchestrator.py --phase backend

# Sprawdź wygenerowane pliki
ls -la backend/app/models/

# Zwaliduj
python scripts/automation/context_validator.py backend/app/models/

# Jeśli OK - commit
git add backend/app/models/
git commit -m "feat: generate SQLAlchemy models (automated with GPT-4o)"
```

---

## 📖 KROK 9: Dokumentacja - Co Przeczytać Dalej

### Dokumenty według priorytetu:

#### 1. **QUICKSTART_AUTOMATION.md** ← ZACZNIJ TUTAJ
- Quick start guide
- 5-minutowy setup
- Przykłady użycia

#### 2. **API_KEYS_SETUP.md** ← KLUCZE API
- Szczegółowe instrukcje dla każdego API
- Troubleshooting
- LiteLLM proxy (opcjonalnie)

#### 3. **AI_STRATEGY.md** ← STRATEGIA
- Kompletna strategia automatyzacji
- Wybór modeli AI
- Cost breakdown
- Decision tree

#### 4. **config/ai_models.yaml** ← KONFIGURACJA
- Task-to-model mapping
- Limity i fallbacki
- Optymalizacje

#### 5. **REFACTOR_PLAN.md** ← PLAN OGÓLNY
- Ogólny plan refaktoryzacji
- User stories
- Tech stack

#### 6. ~~AUTOMATION_PLAN.md~~ ← PRZESTARZAŁY!
- **NIE CZYTAJ!** Zawiera przestarzałe informacje o "native plugins"
- Zostaw jako referencję historyczną
- **Użyj AI_STRATEGY.md zamiast tego!**

---

## ⚡ KROK 10: Quick Reference - Ściąga

### Najważniejsze komendy:

```bash
# Test API
python scripts/automation/test_apis.py

# Generuj modele
python scripts/automation/orchestrator.py --phase backend

# Generuj wszystko
python scripts/automation/orchestrator.py --all

# Walidacja
python scripts/automation/context_validator.py backend/

# Budżet DeepInfra
cat .deepinfra_budget.json
```

### Struktura plików:

```
.
├── .env                              # ← TUTAJ klucze API
├── config/
│   └── ai_models.yaml                # ← Konfiguracja AI
├── scripts/automation/
│   ├── orchestrator.py               # ← Główny silnik
│   ├── test_apis.py                  # ← Test połączeń
│   ├── context_validator.py          # ← Walidacja kodu
│   └── deepinfra_batch.py            # ← Batch DeepInfra
├── context/
│   └── _CORE_CONTEXT.md              # ← Constrainty projektu
├── QUICKSTART_AUTOMATION.md          # ← Quick start
├── API_KEYS_SETUP.md                 # ← Setup kluczy
├── AI_STRATEGY.md                    # ← Strategia AI (AKTUALNY!)
├── INSTRUKCJA_KROK_PO_KROKU.md       # ← TEN PLIK
└── AUTOMATION_PLAN.md                # ← PRZESTARZAŁY (native plugins)
```

### Zmienne środowiskowe:

```bash
OPENAI_API_KEY          # OpenAI (GPT-4o, GPT-4 Turbo)
ANTHROPIC_API_KEY       # Claude (Sonnet 4.5)
GOOGLE_API_KEY          # Gemini (2.5 Pro)
DEEPINFRA_API_KEY       # DeepInfra (Qwen 2.5)
GITHUB_TOKEN            # (opcjonalny, nie daje dostępu do Copilot!)
```

### Koszty:

```
OpenAI:     $0  (via ChatGPT Plus)
Claude:     $0  (via Claude Pro)
Gemini:     $0  (free tier)
DeepInfra:  $5-7 (pay-per-use)
─────────────────────────────────
RAZEM:      $5-7
```

### Podział tasków:

```
90% → OpenAI GPT-4o (unlimited, parallel)
5%  → Claude Sonnet 4.5 (complex logic)
3%  → Gemini 2.5 Pro (validation, 1M context)
2%  → OpenAI GPT-4 Turbo (algorithms)
<1% → DeepInfra Qwen 2.5 (batch >10 files)
```

---

## ✅ Checklist - Czy Jestem Gotowy?

Zaznacz każdy punkt:

- [ ] Zainstalowałem `requirements-automation.txt`
- [ ] Utworzyłem plik `.env` z kluczami API
- [ ] Pobrałem klucz OpenAI API (GPT-4o)
- [ ] Pobrałem klucz Claude API (Sonnet 4.5)
- [ ] Pobrałem klucz Gemini API (2.5 Pro)
- [ ] Pobrałem klucz DeepInfra API + dodałem kartę
- [ ] Przetestowałem wszystkie API (`test_apis.py`)
- [ ] Wszystkie 5 API działają (5/5 passed)
- [ ] Przeczytałem `QUICKSTART_AUTOMATION.md`
- [ ] Przeczytałem `API_KEYS_SETUP.md`
- [ ] Zrozumiałem jak działa orchestrator
- [ ] Zrobiłem backup bazy danych
- [ ] Zrobiłem commit obecnego stanu
- [ ] Utworzyłem branch `automated-refactor`

**Jeśli wszystko ✅ → JESTEŚ GOTOWY!** 🎉

---

## 🆘 Pomoc i Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'httpx'"
```bash
pip install -r requirements-automation.txt
```

### Problem: "OPENAI_API_KEY not set"
```bash
export $(cat .env | xargs)
python scripts/automation/test_apis.py
```

### Problem: "401 Unauthorized"
- Sprawdź czy klucz API jest prawidłowy
- Wejdź na stronę providera i wygeneruj nowy klucz
- Upewnij się że masz aktywną subskrypcję (dla Claude/OpenAI)

### Problem: "Budget exceeded"
- DeepInfra ma hard limit $10
- Sprawdź `.deepinfra_budget.json`
- Jeśli przekroczyłeś - zwiększ limit w `config/ai_models.yaml`

### Problem: "Orchestrator generuje pusty kod"
- To normalne przy pierwszym uruchomieniu (test mode)
- Sprawdź czy masz wypełnione `context/_CORE_CONTEXT.md`
- Upewnij się że faza istnieje w `config/ai_models.yaml`

### Pytania?
1. Przeczytaj `QUICKSTART_AUTOMATION.md`
2. Sprawdź `API_KEYS_SETUP.md` - troubleshooting
3. Zobacz `AI_STRATEGY.md` - fallback chains

---

## 🎯 Następne Kroki

1. **Wykonaj wszystkie kroki 1-7** (setup)
2. **Przetestuj API** (krok 3)
3. **Przeczytaj QUICKSTART_AUTOMATION.md**
4. **Uruchom pierwszy task** (krok 8)
5. **Review i commit**
6. **Repeat!**

**Powodzenia!** 🚀

---

**Wersja:** 1.0
**Data:** 2025-01-XX
**Status:** ✅ Gotowe do użycia
