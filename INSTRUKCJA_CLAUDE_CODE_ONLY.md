# 🎯 Instrukcja - Refaktoryzacja TYLKO z Claude Code w VS Code

**Metoda:** Manualna praca z Claude Code (bez automatyzacji)
**Narzędzie:** Claude Code extension w VS Code
**Czas:** ~5-6 tygodni (vs 11-15 tyg manualnie)
**Koszt:** $0 dodatkowych (tylko subskrypcja Claude Pro $20/mies)

---

## 📋 Różnica: Automatyzacja vs Claude Code Only

### Automatyzacja (poprzednia instrukcja):
```
Python orchestrator
    ↓
Równoległe wywołania API (8 plików jednocześnie)
    ↓
Automatyczna walidacja
    ↓
5 minut → 8 modeli SQLAlchemy
```
**Zalety:** Bardzo szybkie, zero manualnej pracy
**Wady:** Wymaga setupu API keys, trudniejszy troubleshooting

### Claude Code Only (ta instrukcja):
```
Ty otwierasz plik w VS Code
    ↓
Wklejasz prompt do Claude Code
    ↓
Claude generuje kod
    ↓
Ty reviewujesz i akceptujesz
    ↓
20-30 minut → 8 modeli SQLAlchemy
```
**Zalety:** Prosty setup, pełna kontrola, łatwy troubleshooting
**Wady:** Wolniejsze, więcej manualnej pracy

---

## ✅ KROK 1: Sprawdź Setup (1 minuta)

### Wymagania:

1. **Claude Pro subscription** ($20/mies)
   - Sprawdź: https://claude.ai/settings/plan
   - Potrzebujesz: Pro lub Team plan

2. **VS Code z Claude Code**
   - Już masz ✅ (używasz teraz!)

3. **Limit daily:**
   - Claude Pro: ~500 wiadomości/dzień
   - Wystarczy na 100+ tasków dziennie

### Test:

Zapytaj Claude Code (w tym oknie):
```
Cześć! Jesteś gotowy do refaktoryzacji projektu Wallos?
```

Jeśli Claude odpowie ✅ → możesz kontynuować!

---

## 📂 KROK 2: Przygotuj Strukturę Projektu (5 minut)

### 2.1 Utwórz folder backend

```bash
mkdir -p backend/app/{models,schemas,api/v1,services,db,core,tests/unit,tests/integration}
```

### 2.2 Utwórz folder frontend

```bash
mkdir -p frontend/src/{components/{subscriptions,categories,settings,dashboard},api,hooks,utils,types,theme,i18n}
```

### 2.3 Przygotuj pliki konfiguracyjne

Zapytaj Claude Code:
```
Utwórz następujące pliki konfiguracyjne dla projektu:

1. backend/pyproject.toml - Poetry config z dependencies:
   - fastapi, uvicorn, sqlalchemy, aiosqlite, pydantic, pytest

2. backend/.python-version - Python 3.11

3. frontend/package.json - React 18 + TypeScript:
   - react, react-dom, @mui/material, react-query, react-hook-form, zod, i18next

4. .gitignore - Python + Node

Wygeneruj wszystkie 4 pliki.
```

---

## 🎯 KROK 3: Przygotuj "Core Context" (10 minut)

To najważniejszy krok! Stwórz plik z zasadami, których Claude **NIGDY** nie może zapomnieć.

### 3.1 Utwórz context/_CORE_CONTEXT.md

Zapytaj Claude Code:
```
Utwórz plik context/_CORE_CONTEXT.md z następującą zawartością:

# CORE PROJECT CONTEXT - NIGDY NIE ODSTĘPUJ OD TYCH ZASAD

## ⛔ KRYTYCZNE OGRANICZENIA

1. **Baza danych:** TYLKO SQLite - NIE PostgreSQL, NIE MySQL
2. **UI Library:** TYLKO Material-UI v5 - NIE Chakra UI, NIE Radix UI
3. **Języki:** TYLKO Polish + English - NIE 25 języków
4. **Autentykacja:** JWT + API Key - NIE OIDC, NIE OAuth
5. **Powiadomienia:** TYLKO webhooks - NIE email, NIE Discord, NIE Telegram
6. **Kalendarz:** OUT OF SCOPE
7. **AI Rekomendacje:** OUT OF SCOPE

## 📏 REGUŁY BIZNESOWE

1. **Price:** MUSI być > 0
2. **Frequency:** 1-365
3. **Cycle:** TYLKO days|weeks|months|years (enum)
4. **Category ID=1:** NIE MOŻNA usunąć (default category)
5. **User ownership:** ZAWSZE sprawdzaj user_id w queries
6. **Cascade deletes:** User deleted → usuń wszystkie powiązane dane

## 💻 WYMAGANIA KODU

### Backend (Python 3.11+):
- Type hints WSZĘDZIE
- Docstrings: Google style
- Async/await dla wszystkich operacji DB
- Tests: >80% coverage WYMAGANE
- SQLAlchemy 2.0 (async)
- Pydantic v2

### Frontend (TypeScript):
- TypeScript strict mode
- NIE używaj `any`
- Material-UI components TYLKO
- React Hook Form + Zod dla formularzy
- React Query dla data fetching

## 🗄️ SCHEMAT BAZY (SQLite)

[Tutaj wklej schemat z analysis/schema.sql gdy będzie gotowy]
```

### 3.2 Zapisz ten plik i ZAWSZE go załączaj

**WAŻNE:** Przy każdym zapytaniu do Claude Code, zaczynaj od:
```
@context/_CORE_CONTEXT.md

[tutaj twoje zadanie]
```

Symbol `@` sprawia że Claude załaduje ten plik jako kontekst!

---

## 🔨 KROK 4: Phase 1 - Backend Models (2-3 godziny)

### 4.1 Ekstraktuj schemat bazy danych

```bash
# W terminalu
sqlite3 db/wallos.db .schema > analysis/schema.sql
```

### 4.2 Wygeneruj pierwszy model - User

**Otwórz nowy plik:** `backend/app/models/user.py`

**Zapytaj Claude Code:**
```
@context/_CORE_CONTEXT.md
@analysis/schema.sql

Wygeneruj SQLAlchemy 2.0 model dla tabeli `users` z analysis/schema.sql.

Wymagania:
- Async support (AsyncSession)
- Full type hints (Python 3.11+)
- Relationships z backref
- __repr__ dla debugowania
- Docstrings (Google style)

Model powinien zawierać:
- Wszystkie kolumny z tabeli users
- Relationship do subscriptions (one-to-many)
- Relationship do categories (one-to-many)
- Cascade delete rules

Wzór:
```python
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    """User model representing application users.

    Attributes:
        id: Primary key
        username: Unique username
        ...
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # ... więcej kolumn

    # Relationships
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"
```

Wygeneruj pełny plik user.py.
```

**Co zrobić z odpowiedzią:**
1. Claude wygeneruje kod
2. Przejrzyj go (sprawdź czy nie ma PostgreSQL, czy są type hints)
3. Kliknij "Apply" lub skopiuj do pliku
4. Zapisz plik

### 4.3 Powtórz dla pozostałych 7 modeli

**Lista modeli do wygenerowania:**

1. ✅ `user.py` (zrobione wyżej)
2. `subscription.py` - główny model
3. `category.py` - kategorie subskrypcji
4. `currency.py` - waluty
5. `payment_method.py` - metody płatności
6. `household_member.py` - członkowie gospodarstwa
7. `notification.py` - ustawienia powiadomień
8. `setting.py` - globalne ustawienia

**Dla każdego modelu:**
```
@context/_CORE_CONTEXT.md
@analysis/schema.sql

Wygeneruj SQLAlchemy 2.0 model dla tabeli `[nazwa_tabeli]`.
Użyj tego samego wzorca co user.py.
```

**Czas:** ~15-20 minut per model = 2-3 godziny total

### 4.4 Walidacja modeli

**Zapytaj Claude Code:**
```
@backend/app/models/

Przeanalizuj wszystkie 8 modeli w folderze models/ i sprawdź:

1. Czy wszystkie relationships są poprawne (backref)?
2. Czy nie ma błędów typu (mypy)?
3. Czy wszystkie modele mają __repr__?
4. Czy są docstrings?
5. Czy NIE MA wzmianki o PostgreSQL?

Zgłoś błędy jako checklist.
```

### 4.5 Commit

```bash
git add backend/app/models/
git commit -m "feat: generate SQLAlchemy models (8 files) with Claude Code"
```

---

## 📝 KROK 5: Phase 1 - Pydantic Schemas (2-3 godziny)

### 5.1 Wygeneruj schema dla Subscription

**Otwórz:** `backend/app/schemas/subscription.py`

**Zapytaj Claude Code:**
```
@context/_CORE_CONTEXT.md
@backend/app/models/subscription.py

Wygeneruj Pydantic v2 schemas dla Subscription model.

Wymagania:
- 5 schematów: Base, Create, Update, Response, InDB
- Pydantic v2 syntax
- Full validation (email, URL, positive numbers, etc.)
- Field validators dla price (>0), frequency (1-365)
- Enum dla cycle (days/weeks/months/years)
- Type hints
- Docstrings

Wzór:
```python
from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Optional
from datetime import date, datetime
from enum import Enum

class CycleType(str, Enum):
    """Subscription cycle types."""
    DAYS = "days"
    WEEKS = "weeks"
    MONTHS = "months"
    YEARS = "years"

class SubscriptionBase(BaseModel):
    """Base subscription schema with shared fields."""
    name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0)
    # ... more fields

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('price must be greater than 0')
        return v

class SubscriptionCreate(SubscriptionBase):
    """Schema for creating subscription."""
    pass

class SubscriptionUpdate(BaseModel):
    """Schema for updating subscription (all optional)."""
    name: Optional[str] = None
    # ... all fields optional

class SubscriptionResponse(SubscriptionBase):
    """Schema for subscription response."""
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SubscriptionInDB(SubscriptionResponse):
    """Schema for subscription in database."""
    pass
```

Wygeneruj pełny plik subscription.py.
```

### 5.2 Powtórz dla pozostałych 9 schematów

**Lista:**
1. ✅ `subscription.py` (zrobione)
2. `user.py` / `auth.py` - user + auth schemas
3. `category.py`
4. `currency.py`
5. `payment_method.py`
6. `household.py`
7. `notification.py`
8. `setting.py`
9. `common.py` - pagination, errors

**Czas:** ~15-20 min per schema = 2-3 godziny total

---

## 🌐 KROK 6: Phase 1 - API Routes (4-5 godzin)

### 6.1 Wygeneruj routes dla Subscription

**Otwórz:** `backend/app/api/v1/subscriptions.py`

**Zapytaj Claude Code:**
```
@context/_CORE_CONTEXT.md
@backend/app/models/subscription.py
@backend/app/schemas/subscription.py
@USER_STORIES.md

Wygeneruj FastAPI router dla Subscription z full CRUD.

Endpoints (z USER_STORIES.md):
- GET /subscriptions - lista z filtrami (category, inactive, search)
- GET /subscriptions/{id} - pojedynczy
- POST /subscriptions - utworzenie
- PATCH /subscriptions/{id} - update
- DELETE /subscriptions/{id} - usunięcie
- POST /subscriptions/{id}/clone - klonowanie
- POST /subscriptions/{id}/renew - odnowienie (calculate next_payment)

Wymagania:
- Dependency injection: get_db, get_current_user
- Error handling: 400, 401, 404, 500
- OpenAPI docs: docstrings dla wszystkich endpoints
- Pagination: page, limit
- Sorting: sort, order
- Type hints wszędzie

Użyj SubscriptionService (zaimplementujemy później, na razie mock).

Wzór:
```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
from app.schemas.common import PaginatedResponse

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[SubscriptionResponse])
async def list_subscriptions(
    category_id: Optional[int] = Query(None),
    inactive: Optional[bool] = Query(None),
    sort: str = Query("next_payment"),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all subscriptions with filters and pagination."""
    # TODO: implement via SubscriptionService
    pass

# ... więcej endpoints
```

Wygeneruj pełny router.
```

### 6.2 Powtórz dla 11 pozostałych routers

**Lista:**
1. ✅ `subscriptions.py` (9 endpoints) - zrobione
2. `categories.py` (5 endpoints)
3. `currencies.py` (6 endpoints)
4. `payment_methods.py` (6 endpoints)
5. `household.py` (4 endpoints)
6. `auth.py` (4 endpoints) - login, register, etc.
7. `users.py` (8 endpoints)
8. `notifications.py` (3 endpoints)
9. `stats.py` (4 endpoints)
10. `admin.py` (5 endpoints)
11. `logos.py` (2 endpoints)
12. `database.py` (3 endpoints) - backup, export

**Czas:** ~20-30 min per router = 4-5 godzin total

---

## 🏗️ KROK 7: Phase 2 - Service Layer (1 tydzień)

To najtrudniejsza część - tutaj jest cała logika biznesowa!

### 7.1 Wygeneruj SubscriptionService

**Otwórz:** `backend/app/services/subscription_service.py`

**Zapytaj Claude Code:**
```
@context/_CORE_CONTEXT.md
@backend/app/models/subscription.py
@backend/app/schemas/subscription.py
@endpoints/subscription/ (wszystkie PHP pliki z tego folderu)

Wygeneruj SubscriptionService z całą logiką biznesową z PHP.

Metody (z PHP endpoints/subscription/):
1. list_subscriptions() - filters, pagination, sorting
2. get_subscription() - single by ID + ownership check
3. create_subscription() - with logo handling
4. update_subscription() - partial update
5. delete_subscription() - with cleanup
6. clone_subscription() - duplicate logic
7. renew_subscription() - calculate next_payment
8. calculate_next_payment_date() - helper (days/weeks/months/years)

Wymagania:
- Async methods
- Type hints
- Error handling
- Docstrings
- Ownership checks (user_id)
- Transaction handling (commit/rollback)

Wzór:
```python
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate
from app.schemas.common import PaginatedResponse

class SubscriptionService:
    """Service for subscription operations."""

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
        """List subscriptions with filters and pagination."""
        query = select(Subscription).where(Subscription.user_id == user_id)

        if category_id is not None:
            query = query.where(Subscription.category_id == category_id)

        # ... więcej logiki

    def calculate_next_payment_date(
        self,
        current_date: date,
        frequency: int,
        cycle: str
    ) -> date:
        """Calculate next payment date based on frequency and cycle."""
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

Wygeneruj pełny serwis (~400 linii).
```

**UWAGA:** To zajmie 1-2 godziny i wymaga **CRITICAL REVIEW**!

### 7.2 Powtórz dla 8 pozostałych serwisów

**Lista:**
1. ✅ `subscription_service.py` (~400 linii) - zrobione
2. `category_service.py` (~150 linii) - simple CRUD
3. `currency_service.py` (~250 linii) - Fixer API integration
4. `payment_method_service.py` (~150 linii) - simple CRUD
5. `household_service.py` (~150 linii) - simple CRUD
6. `notification_service.py` (~200 linii) - webhooks
7. `logo_service.py` (~250 linii) - Pillow, search, download
8. `stats_service.py` (~300 linii) - calculations, aggregations
9. `user_service.py` (~200 linii) - user management

**Czas:** ~2-3 godziny per complex service = **1 tydzień total**

---

## 🧪 KROK 8: Phase 1 - Backend Tests (2-3 dni)

### 8.1 Wygeneruj testy dla SubscriptionService

**Otwórz:** `backend/tests/unit/test_subscription_service.py`

**Zapytaj Claude Code:**
```
@context/_CORE_CONTEXT.md
@backend/app/services/subscription_service.py

Wygeneruj pytest tests dla SubscriptionService.

Wymagania:
- pytest-asyncio dla async tests
- Fixtures: db_session, test_user, sample_subscription
- Test wszystkich metod
- Test happy path + edge cases
- Mock external dependencies
- >80% coverage

Metody do przetestowania:
1. test_create_subscription_success()
2. test_create_subscription_invalid_price() - ValidationError
3. test_list_subscriptions_with_filters()
4. test_get_subscription_not_found()
5. test_calculate_next_payment_date_monthly()
6. test_calculate_next_payment_date_yearly()
7. test_calculate_next_payment_date_leap_year() - edge case!
8. test_renew_subscription_auto_renew_true()
9. test_clone_subscription()
10. test_delete_subscription_cascade()

Wzór:
```python
import pytest
from datetime import date, timedelta
from app.services.subscription_service import SubscriptionService
from app.schemas.subscription import SubscriptionCreate

@pytest.mark.asyncio
async def test_create_subscription_success(db_session, test_user):
    """Test creating subscription successfully."""
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

@pytest.mark.asyncio
async def test_calculate_next_payment_date_leap_year():
    """Test payment date calculation for leap year edge case."""
    service = SubscriptionService(None)

    # Feb 29, 2024 (leap year) + 1 year = Feb 28, 2025
    current = date(2024, 2, 29)
    next_payment = service.calculate_next_payment_date(current, 1, "years")

    assert next_payment == date(2025, 2, 28)
```

Wygeneruj kompletny test file z >10 testami.
```

### 8.2 Powtórz dla 8 pozostałych serwisów

**Czas:** ~1-2 godziny per service = **2-3 dni total**

---

## ⚛️ KROK 9: Phase 4 - Frontend Setup (1 dzień)

### 9.1 Wygeneruj MUI Theme

**Otwórz:** `frontend/src/theme/index.ts`

**Zapytaj Claude Code:**
```
@context/_CORE_CONTEXT.md

Wygeneruj Material-UI theme z 8 kolorami + dark mode.

Wymagania:
- 8 primary colors: blue, green, red, yellow, purple, pink, orange, gray
- Dark/Light mode support
- Custom theme factory
- TypeScript types
- Polish + English typography

Kolory (z Wallos PHP):
- blue: #2196F3
- green: #4CAF50
- red: #F44336
- yellow: #FFC107
- purple: #9C27B0
- pink: #E91E63
- orange: #FF9800
- gray: #607D8B

Wzór:
```typescript
import { createTheme, ThemeOptions, PaletteMode } from '@mui/material/styles';

const colorPalettes = {
  blue: {
    main: '#2196F3',
    light: '#64B5F6',
    dark: '#1976D2',
  },
  // ... więcej kolorów
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
      // ... more
    },
    typography: {
      fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
      // ... more
    },
    components: {
      MuiButton: {
        styleOverrides: {
          root: {
            textTransform: 'none',
          },
        },
      },
      // ... more overrides
    },
  });
};
```

Wygeneruj pełny theme.
```

### 9.2 Wygeneruj i18n setup

**Zapytaj Claude Code:**
```
@context/_CORE_CONTEXT.md

Wygeneruj i18n setup dla React z Polish + English.

Pliki:
1. frontend/src/i18n/index.ts - i18next config
2. frontend/src/i18n/locales/pl.json - Polish translations
3. frontend/src/i18n/locales/en.json - English translations

TYLKO 2 języki: pl, en (NIE 25!)

Tłumaczenia z PHP (endpoints/langs/):
- Subscription, Category, Currency, etc.
- Dashboard, Settings, Stats
- Buttons: Save, Cancel, Delete, etc.
- Errors: "Invalid price", "Required field", etc.
```

---

## 🎨 KROK 10: Phase 5 - React Components (2 tygodnie)

### 10.1 Wygeneruj SubscriptionList (complex)

**Otwórz:** `frontend/src/components/subscriptions/SubscriptionList.tsx`

**Zapytaj Claude Code:**
```
@context/_CORE_CONTEXT.md
@USER_STORIES.md (sekcja: Lista subskrypcji)

Wygeneruj SubscriptionList component z MUI.

Wymagania:
- Material-UI DataGrid lub custom list
- Filters: category, inactive, search
- Sorting: name, price, next_payment
- Pagination: page, limit
- Actions: edit, delete, clone, renew
- Loading states
- Error handling
- TypeScript strict
- React Query dla data fetching
- i18n (useTranslation)

Features:
- Wyświetl logo subscription
- Kolorowe badges dla categories
- Countdown do next_payment
- Formatowanie ceny (PLN, USD, EUR)
- Responsive (mobile-first)

Wzór:
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
  CircularProgress,
  Alert,
} from '@mui/material';
import { Edit, Delete, ContentCopy, Refresh } from '@mui/icons-material';
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

  if (isLoading) return <CircularProgress />;
  if (error) return <Alert severity="error">{t('errors.loading')}</Alert>;

  return (
    <Box>
      {/* Filters */}
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <TextField
            label={t('search')}
            value={filters.search}
            onChange={(e) => setFilters({ ...filters, search: e.target.value })}
          />
          {/* More filters */}
        </CardContent>
      </Card>

      {/* List */}
      {data?.data.map((subscription) => (
        <SubscriptionCard
          key={subscription.id}
          subscription={subscription}
          onEdit={() => onEdit(subscription)}
          onDelete={() => deleteMutation.mutate(subscription.id)}
        />
      ))}
    </Box>
  );
};
```

Wygeneruj pełny component (~300 linii).
```

### 10.2 Lista 25 komponentów do wygenerowania

**Simple (15 komponentów):** ~20 min każdy = 5 godzin
1. `SubscriptionCard.tsx` - pojedyncza karta
2. `CategoryBadge.tsx` - badge kategorii
3. `PriceDisplay.tsx` - formatowanie ceny
4. `DateCountdown.tsx` - countdown do płatności
5. `LoadingSpinner.tsx`
6. `ErrorAlert.tsx`
7. `EmptyState.tsx`
8. `ConfirmDialog.tsx`
9. `Navbar.tsx`
10. `Sidebar.tsx`
11. `Footer.tsx`
12. `ThemeToggle.tsx` - przełącznik dark mode
13. `LanguageToggle.tsx` - przełącznik pl/en
14. `ColorThemePicker.tsx` - wybór koloru (8 opcji)
15. `Logo.tsx`

**Complex (10 komponentów):** ~1-2h każdy = 10-20 godzin
1. ✅ `SubscriptionList.tsx` - lista (zrobione)
2. `SubscriptionForm.tsx` - formularz (React Hook Form + Zod)
3. `Dashboard.tsx` - dashboard z kartami
4. `Statistics.tsx` - wykresy (Recharts)
5. `CategorySettings.tsx` - zarządzanie kategoriami
6. `CurrencySettings.tsx` - zarządzanie walutami
7. `NotificationSettings.tsx` - webhooks
8. `UserSettings.tsx` - ustawienia użytkownika
9. `PaymentMethodSettings.tsx`
10. `HouseholdSettings.tsx`

**Total:** ~2 tygodnie

---

## 📊 KROK 11: Monitoruj Postęp

### Checklist - Backend

**Phase 1: Backend Foundation**
- [ ] 8 SQLAlchemy models (2-3h)
- [ ] 10 Pydantic schemas (2-3h)
- [ ] 12 API routers (4-5h)
- [ ] 9 Services (1 tydzień) ← NAJTRUDNIEJSZE
- [ ] 9 Test files (2-3 dni)

**Phase 2: Backend Advanced**
- [ ] Celery tasks (1 dzień)
- [ ] OpenAPI docs (automatyczne)
- [ ] Migrations (Alembic)

**Phase 3: Backend Infrastructure**
- [ ] Docker setup
- [ ] CI/CD

### Checklist - Frontend

**Phase 4: Frontend Setup**
- [ ] MUI Theme (2h)
- [ ] i18n setup (1h)
- [ ] API client (1h)
- [ ] React Query setup (30 min)

**Phase 5: React Components**
- [ ] 15 simple components (5h)
- [ ] 10 complex components (10-20h)

**Phase 6: Frontend Tests**
- [ ] Vitest setup
- [ ] Component tests

---

## 💡 KROK 12: Najlepsze Praktyki z Claude Code

### ✅ DO:

1. **Zawsze załączaj @context/_CORE_CONTEXT.md**
   ```
   @context/_CORE_CONTEXT.md

   Wygeneruj...
   ```

2. **Używaj @references do plików**
   ```
   @backend/app/models/subscription.py
   @backend/app/schemas/subscription.py

   Wygeneruj service...
   ```

3. **Dziel duże zadania na mniejsze**
   ❌ "Wygeneruj całą aplikację"
   ✅ "Wygeneruj model User"
   ✅ "Wygeneruj schema User"
   ✅ "Wygeneruj router User"

4. **Review przed Apply**
   - Sprawdź czy nie ma PostgreSQL
   - Sprawdź czy są type hints
   - Sprawdź czy jest walidacja

5. **Commit często**
   ```bash
   git add backend/app/models/user.py
   git commit -m "feat: add User model"
   ```

6. **Waliduj co fazę**
   ```
   @backend/app/models/

   Przeanalizuj wszystkie modele i znajdź błędy.
   ```

### ❌ NIE:

1. **Nie proś o za dużo na raz**
   ❌ "Wygeneruj backend + frontend"

2. **Nie zapominaj o CORE_CONTEXT**
   Bez niego Claude może zapomnieć o SQLite!

3. **Nie akceptuj kodu bez review**
   Zawsze przejrzyj przed Apply

4. **Nie mieszaj języków w jednym zapytaniu**
   ✅ Pisz po polsku ALBO po angielsku
   ❌ Nie mieszaj: "Generate user model dla subscriptions"

---

## 📈 Szacowany Czas vs Automatyzacja

| Faza | Manualnie | Claude Code Only | Automatyzacja |
|------|-----------|------------------|---------------|
| Models | 1 tydzień | **2-3h** | **5 min** |
| Schemas | 3 dni | **2-3h** | **6 min** |
| Routes | 2 tygodnie | **4-5h** | **10 min** |
| Services | 2 tygodnie | **1 tydzień** | **1h** |
| Tests | 1 tydzień | **2-3 dni** | **20 min** |
| Frontend | 3 tygodnie | **2 tygodnie** | **1 tydzień** |
| **TOTAL** | **11-15 tyg** | **5-6 tyg** | **2-3 tyg** |

**Claude Code Only:**
- ✅ Prostszy setup (zero API keys)
- ✅ Pełna kontrola
- ✅ Łatwiejszy troubleshooting
- ❌ Wolniejsze (2x wolniej niż automatyzacja)
- ❌ Więcej manualnej pracy

---

## 🆘 Troubleshooting

### Problem: Claude generuje PostgreSQL zamiast SQLite

**Rozwiązanie:**
```
@context/_CORE_CONTEXT.md

STOP! Sprawdź poprzednią odpowiedź.

Czy użyłeś PostgreSQL? Jeśli tak, to BŁĄD!

Popraw kod na SQLite. Wymagania:
- TYLKO SQLite (aiosqlite)
- NIE PostgreSQL (psycopg2)
```

### Problem: Claude zapomina o Material-UI

**Rozwiązanie:**
```
@context/_CORE_CONTEXT.md

PRZYPOMNIENIE: TYLKO Material-UI v5!

NIE używaj:
- Chakra UI
- Radix UI
- Ant Design

Popraw component na Material-UI.
```

### Problem: Claude generuje 25 języków w i18n

**Rozwiązanie:**
```
@context/_CORE_CONTEXT.md

BŁĄD! TYLKO 2 języki: Polish + English!

Usuń wszystkie inne języki z konfiguracji i18n.
```

### Problem: Hit daily limit (500 msg/day)

**Rozwiązanie:**
- Poczekaj do następnego dnia (limit resetuje się co 24h)
- Lub skup się na review/testowaniu zamiast generowania
- Lub użyj automatyzacji z API (poprzednia instrukcja)

---

## 🎯 Quick Reference - Komendy

```bash
# Setup
mkdir -p backend/app/{models,schemas,api/v1,services}
mkdir -p frontend/src/components/{subscriptions,categories}

# Git workflow
git add backend/app/models/user.py
git commit -m "feat: add User model"
git push

# Testy
pytest backend/tests/unit/test_subscription_service.py -v
npm test -- SubscriptionList.test.tsx

# Budowanie
cd backend && poetry install
cd frontend && npm install

# Uruchamianie
cd backend && uvicorn app.main:app --reload
cd frontend && npm run dev
```

---

## ✅ Podsumowanie

### Co masz:
- ✅ Claude Pro subscription ($20/mies)
- ✅ VS Code z Claude Code extension
- ✅ 500 wiadomości/dzień (wystarczy!)
- ✅ Pełna kontrola nad procesem

### Co potrzebujesz:
- ⏱️ **5-6 tygodni** pracy (vs 11-15 tyg manualnie)
- 🎯 **Systematyczność** - fase po fazie
- 📋 **Załączanie @context/_CORE_CONTEXT.md** przy każdym zapytaniu
- 👀 **Review każdego** wygenerowanego pliku

### Następny krok:
1. Przejdź do **KROK 2** - przygotuj strukturę projektu
2. Wykonaj **KROK 3** - utwórz `context/_CORE_CONTEXT.md`
3. Zacznij od **KROK 4** - wygeneruj pierwszy model (User)

**Powodzenia!** 🚀

---

**Pytania?** Zapytaj Claude Code:
```
@INSTRUKCJA_CLAUDE_CODE_ONLY.md

Mam pytanie: [twoje pytanie]
```
