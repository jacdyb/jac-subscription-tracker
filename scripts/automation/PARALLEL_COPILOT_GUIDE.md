# Parallel Copilot Execution Guide

**Maksymalizacja efektywności: 8 tasków jednocześnie zamiast sekwencyjnie**

---

## Koncepcja

Zamiast generować 8 plików sekwencyjnie (8 × 10 min = **80 minut**), uruchamiasz **8 równoległych sesji Copilot Chat** (1 × 10 min = **10 minut**).

**Oszczędność:** 87% czasu!

---

## Metoda 1: VS Code Split Editor (Zalecana)

### Setup (jednorazowo, 2 minuty)

1. Otwórz VS Code
2. Włącz "Grid Editor Layout":
   - `Cmd+K` → `Cmd+Shift+\` (Mac)
   - `Ctrl+K` → `Ctrl+Shift+\` (Windows/Linux)

3. Podziel ekran na 4 kolumny:
   - `View` → `Editor Layout` → `Grid (2×2)`

4. W każdej kolumnie otwórz inny plik:
   ```
   ┌─────────────┬─────────────┬─────────────┬─────────────┐
   │ user.py     │ subscr...py │ category.py │ currency.py │
   ├─────────────┼─────────────┼─────────────┼─────────────┤
   │ payment.py  │ household.py│ notif...py  │ settings.py │
   └─────────────┴─────────────┴─────────────┴─────────────┘
   ```

### Wykonanie (każdy task, ~2 minuty setup + 10 min AI)

1. **Otwórz Copilot Chat w KAŻDEJ kolumnie:**
   - Kliknij w pierwszą kolumnę → `Ctrl+Shift+I` (Copilot Chat)
   - Kliknij w drugą kolumnę → `Ctrl+Shift+I`
   - ... powtórz dla wszystkich 8 kolumn

2. **Przygotuj prompt** (skopiuj raz, wklej 8 razy):
   ```
   @workspace Generate SQLAlchemy 2.0 model for [TABLE_NAME].

   See:
   - analysis/schema.sql for structure
   - context/_CORE_CONTEXT.md for constraints

   Requirements:
   - Async support (Base from app.db.base)
   - Full type hints (Python 3.11+)
   - Relationships with back_populates
   - Google-style docstring
   ```

3. **Wklej prompt do WSZYSTKICH 8 Copilot Chat:**
   - Zmień tylko `[TABLE_NAME]` w każdym:
     - Kolumna 1: `users`
     - Kolumna 2: `subscriptions`
     - Kolumna 3: `categories`
     - itd.

4. **Uruchom WSZYSTKIE naraz:**
   - Ctrl+Click (przytrzymaj Ctrl/Cmd) na każdej kolumnie
   - Naciśnij `Enter` w ostatniej aktywnej
   - **LUB:** Kliknij po kolei Enter w każdej (szybko, <5 sekund)

5. **Czekaj 5-10 minut** - wszystkie AI generują jednocześnie! ☕

6. **Review wyników:**
   - Przejrzyj każdy plik
   - Akceptuj sugestie (`Ctrl+Enter`)
   - Ewentualne poprawki

**Total czas:** ~12 minut (zamiast 80!)

---

## Metoda 2: Wiele VS Code Windows (Alternative)

Jeśli nie lubisz split editor:

### Setup

1. Otwórz 4-8 **osobnych okien VS Code:**
   ```bash
   # Terminal
   code -n backend/app/models/user.py
   code -n backend/app/models/subscription.py
   code -n backend/app/models/category.py
   code -n backend/app/models/currency.py
   # ... itd
   ```

2. Ułóż okna obok siebie (tile windows):
   - **Mac:** Rectangle app (darmowy) lub BetterSnapTool
   - **Windows:** Win+Arrow keys
   - **Linux:** i3wm / GNOME tiling

### Wykonanie

1. W każdym oknie: `Ctrl+Shift+I` (Copilot Chat)
2. Wklej prompt (z modyfikacjami dla każdego pliku)
3. Naciśnij Enter w każdym oknie
4. Czekaj na wyniki

**Zaleta:** Każde okno ma pełny ekran (łatwiej czytać)
**Wada:** Więcej przełączania między oknami

---

## Metoda 3: Copilot Edits (Experimental - Beta)

**Nowość w Copilot Pro (2024-12+):** Copilot Edits pozwala na edycję wielu plików jednocześnie.

### Jak używać:

1. Otwórz Command Palette: `Cmd+Shift+P` / `Ctrl+Shift+P`
2. Wpisz: `Copilot Edits: Start`
3. Dodaj pliki do edycji:
   ```
   backend/app/models/user.py
   backend/app/models/subscription.py
   backend/app/models/category.py
   ... (wszystkie 8)
   ```
4. Podaj **jeden prompt dla wszystkich:**
   ```
   Generate SQLAlchemy 2.0 models for all these files based on:
   - analysis/schema.sql (table structure)
   - context/_CORE_CONTEXT.md (constraints)

   For EACH file:
   - Extract table name from filename (e.g., user.py → users table)
   - Generate async model with relationships
   - Full type hints
   - Google-style docstring
   ```
5. Copilot generuje **wszystkie pliki naraz**
6. Review diffs → Accept / Reject

**Zaleta:** Najbardziej zautomatyzowane
**Wada:** Beta feature, może być niestabilne
**Status:** Sprawdź dostępność: `GitHub Copilot` settings → `Edits`

---

## Best Practices

### 1. Przygotuj Context przed Parallel Run

**NIE rób tego:**
```bash
# Zła kolejność - każdy Copilot musi analizować osobno
[Copilot 1] Generate user model
[Copilot 2] Generate subscription model
# ... każdy analizuje schema.sql od zera
```

**ZAMIAST:**
```bash
# Dobra kolejność - raz przygotuj context
1. Claude Code: "Analyze analysis/schema.sql → create database_analysis.md"
2. NASTĘPNIE: Parallel Copilot (każdy czyta gotowy analysis)
```

### 2. Użyj `@workspace` dla Auto-Context

Copilot automatycznie znajdzie:
- `context/_CORE_CONTEXT.md`
- `analysis/schema.sql`
- `analysis/database_analysis.md`

Wystarczy:
```
@workspace Generate [MODEL] model
```

### 3. Limits & Rate Limiting

**GitHub Copilot (GPT-4o free tier):**
- ✅ **Unlimited requests** (0x tier)
- ❌ **Brak limitu!** Możesz uruchomić 100 równolegle

**Inne modele (w Copilot Pro):**
- ⚠️ Claude Sonnet 4, Gemini 2.5 Pro - limit ~50/day (1x tier)
- Nie używaj ich do parallel (zachowaj na złożone taski)

**Strategia:**
- Parallel = TYLKO GPT-4o (unlimited)
- Sequential = Claude S4.5, Gemini (limited)

### 4. Validation po Parallel Run

**ZAWSZE uruchom po parallel generation:**
```bash
./scripts/orchestrate.sh validate
```

Sprawdzi:
- Context violations (PostgreSQL? Chakra UI?)
- Type hints (mypy)
- Linting (ruff)
- Imports

### 5. Git Commits po Każdej Fazie

```bash
# Po wygenerowaniu 8 modeli
git add backend/app/models/
git commit -m "feat: generate SQLAlchemy models (8 files, parallel Copilot)

- user, subscription, category, currency
- payment_method, household_member
- notification_settings, settings

Generated via: GitHub Copilot Chat (GPT-4o)
Validated via: context_validator.py + mypy

Co-Authored-By: GitHub Copilot <noreply@github.com>"
```

---

## Przykładowe Timings

### SQLAlchemy Models (8 plików)

| Metoda | Setup | Execution | Review | **Total** |
|--------|-------|-----------|--------|-----------|
| Sequential (1 at a time) | 0 min | 80 min | 20 min | **100 min** |
| Parallel Split Editor (8) | 2 min | 10 min | 20 min | **32 min** |
| Parallel Windows (8) | 5 min | 10 min | 20 min | **35 min** |
| Copilot Edits (beta) | 1 min | 12 min | 15 min | **28 min** |

**Oszczędność:** 68-72% czasu!

### Pydantic Schemas (10 plików)

| Metoda | Total Time |
|--------|------------|
| Sequential | 125 min |
| Parallel (10×) | 40 min |
| **Saved** | **85 min (68%)** |

### API Routes (12 prostych)

| Metoda | Total Time |
|--------|------------|
| Sequential | 150 min |
| Parallel (12×) | 45 min |
| **Saved** | **105 min (70%)** |

---

## Troubleshooting

### Problem: "Copilot Chat nie otwiera się w drugiej kolumnie"

**Rozwiązanie:**
1. Kliknij w kolumnę (musi być aktywna)
2. Sprawdź czy plik jest otwarty w kolumnie
3. `Ctrl+Shift+I` ponownie

### Problem: "Wszystkie Copilot Chat generują ten sam kod"

**Przyczyna:** Nie zmieniłeś promptu dla każdej kolumny

**Rozwiązanie:**
- Każdy prompt MUSI mieć unikalną część:
  - `@workspace Generate USER model`
  - `@workspace Generate SUBSCRIPTION model`
  - itd.

### Problem: "Copilot zwraca błędy dla wielu plików jednocześnie"

**Rozwiązanie:**
1. Sprawdź `context/_CORE_CONTEXT.md` - czy istnieje?
2. Sprawdź `analysis/schema.sql` - czy jest kompletny?
3. Zmniejsz liczbę równoległych (zamiast 8 → 4)

### Problem: "VS Code zwalnia przy 8 Copilot Chat"

**Rozwiązanie:**
- Zwiększ RAM dla VS Code:
  - `Code` → `Preferences` → `Settings`
  - Szukaj: `"window.maximumRamUsage"`
  - Ustaw: `8192` (8GB)
- LUB: Użyj mniej równoległych (4 zamiast 8)

---

## Checklista przed Parallel Run

- [ ] Context przygotowany (`context/_CORE_CONTEXT.md`)
- [ ] Analysis gotowy (`analysis/database_analysis.md`)
- [ ] Copilot Pro aktywny (sprawdź status)
- [ ] Pliki utworzone (puste) w `backend/app/models/`
- [ ] Split editor skonfigurowany (2×2 lub 2×4)
- [ ] Prompt przygotowany (skopiowany do schowka)
- [ ] Validation script gotowy (`./scripts/orchestrate.sh validate`)

---

## Next Steps

Po opanowaniu parallel Copilot:

1. **Phase 1 Complete:** Models + Schemas + Routes = **~4 godziny** (zamiast 12)
2. **Phase 4:** React components (20×) = **~2 godziny** (zamiast 8)
3. **Total project:** 5-6 tygodni → **3-4 tygodnie** 🚀

**ROI:** Parallel execution oszczędza ~40% czasu na całym projekcie!

---

**Pytania?** Zobacz: `AUTOMATION_PLAN.md` sekcja "Parallel Execution"
