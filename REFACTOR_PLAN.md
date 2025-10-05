# Plan Przepisania Wallos: PHP → Python + React

## Analiza Obecnego Projektu

### Architektura Obecna
- **Backend**: PHP 8.2 z SQLite3
- **Frontend**: Vanilla JavaScript z wieloma oddzielnymi plikami (dashboard.js, subscriptions.js, calendar.js, stats.js)
- **Baza danych**: SQLite (wallos.db)
- **Zarządzanie stanem**: Ciasteczka i sesje PHP
- **API**: Częściowe REST API w katalogu `/api/` (tylko GET) - **wymaga uzupełnienia do pełnego REST**
- **Autoryzacja**: Session-based z API key dla API calls
- **Cronjobs**: PHP scripts wykonywane przez cron

### Główne Moduły Funkcjonalne (Scope Migracji)

#### ✅ MIGROWANE (Core Features)
1. **Subscriptions Management** - zarządzanie subskrypcjami (CRUD + clone, renew)
2. **Statistics** - statystyki wydatków i wykresów
3. **Categories** - zarządzanie kategoriami (CRUD + sortowanie)
4. **Payment Methods** - metody płatności (CRUD + sortowanie)
5. **Household Members** - członkowie gospodarstwa (CRUD)
6. **Currencies** - obsługa walut z konwersją (Fixer API)
7. **Notifications** - **TYLKO webhooks** (test + send)
8. **Admin Panel** - zarządzanie użytkownikami
9. **User Profile** - awatar, hasło, ustawienia
10. **User Settings** - theme, currency, language, preferences
11. **Logo Management** - upload, search, resize
12. **Database Operations** - backup, restore, import
13. **i18n** - wsparcie dla 25 języków

#### ❌ POMINIĘTE (Simplified Scope)
- ~~**Calendar View**~~ - widok kalendarzowy (może być dodany później)
- ~~**OIDC/OAuth**~~ - tylko username+password + API key authentication
- ~~**AI Recommendations**~~ - ChatGPT/Gemini/Ollama (poza scope)
- ~~**Email Notifications**~~ - SMTP (poza scope)
- ~~**Discord Notifications**~~ - (poza scope)
- ~~**Telegram Notifications**~~ - (poza scope)
- ~~**Pushover Notifications**~~ - (poza scope)
- ~~**Gotify Notifications**~~ - (poza scope)
- ~~**Ntfy Notifications**~~ - (poza scope)
- ~~**PushPlus Notifications**~~ - (poza scope)

### Obecna Struktura Endpointów (PHP)

**Łącznie:** ~120 plików PHP
**W scope migracji:** ~70 plików (58%)

```
/endpoints/
├── admin/          - zarządzanie użytkownikami (✅ adduser, deleteuser, ❌ OIDC, ❌ SMTP)
├── ai/             - ❌ AI recommendations (POMINIĘTE)
├── categories/     - ✅ CRUD kategorii + sortowanie
├── cronjobs/       - ✅ zadania cykliczne (→ Celery tasks)
├── currency/       - ✅ zarządzanie walutami + Fixer API
├── db/             - ✅ backup, restore, migrate, import
├── household/      - ✅ członkowie gospodarstwa (CRUD)
├── logos/          - ✅ wyszukiwanie + upload logo
├── notifications/  - ⚠️ TYLKO webhooks (save + test)
├── payments/       - ✅ metody płatności (CRUD + sort + search)
├── settings/       - ✅ ustawienia użytkownika (theme, currency, preferences)
├── subscription/   - ✅ pojedyncza subskrypcja (add, get, edit, delete, clone, renew)
└── subscriptions/  - ✅ eksport (CSV), lista
```

### Obecne API (częściowe - TYLKO GET)

**⚠️ KRYTYCZNE:** Obecne API jest niekompletne - brakuje POST/PATCH/DELETE dla większości zasobów

```
/api/
├── admin/              - GET: admin settings (❌ GET: OIDC - pominięte)
├── categories/         - GET: categories
├── currencies/         - GET: currencies
├── fixer/              - GET: fixer settings
├── household/          - GET: household members
├── notifications/      - GET: notification settings (⚠️ tylko webhooks)
├── payment_methods/    - GET: payment methods
├── settings/           - GET: user settings
├── status/             - GET: version
├── subscriptions/      - GET: subscriptions, monthly cost, iCal feed
└── users/              - GET: user info
```

**Brakujące operacje (do uzupełnienia w nowym API):**
- POST/PATCH/DELETE dla categories, currencies, payment_methods, household, subscriptions
- Pełny CRUD przez REST API zamiast session-based endpoints

---

## Propozycja Nowej Architektury

### Backend: Python (FastAPI)

#### Stack Technologiczny

**✅ Wymagania:**
- **Gotowe biblioteki** - maksymalne wykorzystanie proven solutions
- **Maksymalna modularność** - każdy moduł niezależny
- **Type safety** - pełne type hints (Python 3.11+)
- **Testy >80% coverage** - pytest dla każdego modułu
- **Przejrzystość** - SOLID principles, clear naming

**Technologie:**
- **Framework**: FastAPI 0.104+ (async, auto OpenAPI docs)
- **ORM**: SQLAlchemy 2.0 (async support)
- **Baza danych**: **SQLite tylko** (zachowanie pełnej kompatybilności ze starą bazą)
  - Plik: `wallos.db`
  - Async driver: `aiosqlite`
  - Backup-friendly (prosty plik)
- **Migracje**: Alembic
- **Autoryzacja**:
  - JWT tokens (access 15min + refresh 7 days) - `python-jose`
  - API Key (dla API access) - custom middleware
  - ❌ ~~OAuth2/OIDC~~ - poza scope
- **Task Queue**: Celery + Redis (zastąpienie cronjobs)
- **Walidacja**: Pydantic v2
- **HTTP Client**: httpx (async, dla Fixer API + webhooks)
- **Image Processing**: Pillow (logo resize)
- **Testing**: pytest + pytest-asyncio + pytest-cov
- **Linting**: ruff + mypy (type checking)

#### Struktura Katalogów
```
backend/
├── alembic/                    # migracje bazy danych
├── app/
│   ├── __init__.py
│   ├── main.py                 # główny plik FastAPI
│   ├── config.py               # konfiguracja (env vars)
│   ├── dependencies.py         # dependency injection
│   │
│   ├── core/
│   │   ├── auth.py            # JWT + API Key auth
│   │   ├── security.py        # password hashing, token generation
│   │   └── exceptions.py      # custom exceptions
│   │
│   ├── models/                # SQLAlchemy models (1 plik = 1 tabela)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── subscription.py
│   │   ├── category.py
│   │   ├── currency.py
│   │   ├── payment_method.py
│   │   ├── household_member.py
│   │   ├── notification_settings.py
│   │   └── settings.py
│   │
│   ├── schemas/               # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── auth.py           # Login, Token, Register
│   │   ├── user.py           # User, UserCreate, UserUpdate
│   │   ├── subscription.py   # Subscription, SubscriptionCreate, etc.
│   │   ├── category.py
│   │   ├── currency.py
│   │   ├── payment_method.py
│   │   ├── household.py
│   │   ├── notification.py
│   │   └── common.py         # Shared schemas (pagination, etc.)
│   │
│   ├── api/
│   │   ├── deps.py           # route dependencies (get_db, get_current_user)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py       # /auth/login, /auth/register, /auth/refresh
│   │       ├── users.py      # /users/me, /users/me/password, /users/me/api-key
│   │       ├── subscriptions.py  # Full CRUD + /clone, /renew, /export
│   │       ├── categories.py     # Full CRUD + /sort
│   │       ├── currencies.py     # Full CRUD + /convert, /update-rates
│   │       ├── payment_methods.py  # Full CRUD + /sort
│   │       ├── household.py      # Full CRUD
│   │       ├── notifications.py  # GET/PATCH settings, POST /test/webhook
│   │       ├── admin.py      # /admin/users (list, create, delete)
│   │       ├── stats.py      # Statistics endpoints
│   │       ├── logos.py      # /upload, /search
│   │       └── database.py   # /backup, /restore, /import
│   │
│   ├── services/              # Business logic (testowane niezależnie)
│   │   ├── __init__.py
│   │   ├── subscription_service.py  # clone, renew, calculate_next_payment
│   │   ├── currency_service.py      # Fixer API, conversions
│   │   ├── notification_service.py  # webhook sending
│   │   ├── logo_service.py          # upload, resize, search
│   │   ├── stats_service.py         # calculations
│   │   └── user_service.py          # user operations
│   │
│   ├── tasks/                 # Celery tasks (cronjobs)
│   │   ├── __init__.py
│   │   ├── celery_app.py     # Celery config
│   │   ├── notifications.py  # send_payment_notifications (cron)
│   │   ├── currency_update.py  # update_exchange_rates (daily)
│   │   └── payment_updates.py  # update_next_payment_dates (daily)
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── i18n.py           # translations helper
│   │   ├── formatters.py     # date, currency formatting
│   │   └── validators.py     # custom validators
│   │
│   └── db/
│       ├── __init__.py
│       ├── base.py           # SQLAlchemy declarative base
│       ├── session.py        # database session factory
│       └── init_db.py        # create_tables, seed data
│
├── tests/                     # >80% coverage required
│   ├── conftest.py           # pytest fixtures (db, client, auth)
│   ├── unit/                 # Unit tests (services, utils)
│   │   ├── test_subscription_service.py
│   │   ├── test_currency_service.py
│   │   ├── test_notification_service.py
│   │   └── ...
│   ├── integration/          # Integration tests (API endpoints)
│   │   ├── test_auth_api.py
│   │   ├── test_subscriptions_api.py
│   │   ├── test_categories_api.py
│   │   └── ...
│   └── fixtures/             # Test data (JSON fixtures)
│       ├── users.json
│       └── subscriptions.json
│
├── requirements.txt          # Pin dependencies
├── requirements-dev.txt      # Dev dependencies (pytest, ruff, mypy)
├── pyproject.toml            # Project config (ruff, mypy, pytest)
└── .env.example              # Environment variables template
```

#### Struktura API REST (Kompletne CRUD)

**⚠️ UWAGA:** W odróżnieniu od obecnego PHP API (tylko GET), nowe API będzie **w pełni RESTful** z wszystkimi operacjami CRUD.

**Authentication** (tylko username+password, bez OIDC)
```
POST   /api/v1/auth/register          # Request: {username, email, password}
POST   /api/v1/auth/login             # Request: {username, password} → JWT tokens
POST   /api/v1/auth/refresh           # Request: {refresh_token} → new access token
POST   /api/v1/auth/logout            # Invalidate tokens
```

**Users**
```
GET    /api/v1/users/me               # Current user info
PATCH  /api/v1/users/me               # Update profile (email, avatar, settings)
DELETE /api/v1/users/me               # Delete account
POST   /api/v1/users/me/avatar        # Upload avatar (multipart/form-data)
DELETE /api/v1/users/me/avatar        # Remove avatar
PATCH  /api/v1/users/me/password      # Change password
GET    /api/v1/users/me/api-key       # Get current API key
POST   /api/v1/users/me/api-key/regenerate  # Generate new API key
```

**Subscriptions** (Full CRUD)
```
GET    /api/v1/subscriptions              # List with filters, pagination, sort
                                           # Query params: ?category_id=1&inactive=false&sort=price&order=desc&page=1&limit=50
POST   /api/v1/subscriptions              # Create new subscription
GET    /api/v1/subscriptions/{id}         # Get single subscription
PATCH  /api/v1/subscriptions/{id}         # Update subscription (partial update)
DELETE /api/v1/subscriptions/{id}         # Delete subscription
POST   /api/v1/subscriptions/{id}/clone   # Clone subscription (creates copy)
POST   /api/v1/subscriptions/{id}/renew   # Mark as paid, calculate next_payment
GET    /api/v1/subscriptions/export/csv   # Export to CSV
GET    /api/v1/subscriptions/stats        # Statistics (total cost, by category, etc.)
```

**Categories** (Full CRUD + ordering)
```
GET    /api/v1/categories                 # List all user categories (ordered)
POST   /api/v1/categories                 # Create new category
PATCH  /api/v1/categories/{id}            # Update category name
DELETE /api/v1/categories/{id}            # Delete (if not in use)
POST   /api/v1/categories/sort            # Update order: [{id: 1, order: 1}, {id: 2, order: 2}]
```

**Currencies** (Full CRUD + Fixer API)
```
GET    /api/v1/currencies                 # List all currencies
POST   /api/v1/currencies                 # Add custom currency
PATCH  /api/v1/currencies/{id}            # Update currency
DELETE /api/v1/currencies/{id}            # Delete currency (if not in use)
POST   /api/v1/currencies/update-rates    # Trigger Fixer API update (manual)
GET    /api/v1/currencies/convert?from=EUR&to=USD&amount=100  # Convert amount
```

**Payment Methods** (Full CRUD + ordering)
```
GET    /api/v1/payment-methods            # List all payment methods
POST   /api/v1/payment-methods            # Create new payment method
PATCH  /api/v1/payment-methods/{id}       # Update payment method
DELETE /api/v1/payment-methods/{id}       # Delete (if not in use)
POST   /api/v1/payment-methods/sort       # Update order
GET    /api/v1/payment-methods/search?q=visa  # Search payment methods
```

**Household** (Full CRUD)
```
GET    /api/v1/household/members          # List household members
POST   /api/v1/household/members          # Add member
PATCH  /api/v1/household/members/{id}     # Update member
DELETE /api/v1/household/members/{id}     # Delete member (if not assigned)
```

**Notifications** (tylko webhooks)
```
GET    /api/v1/notifications/settings     # Get webhook settings
PATCH  /api/v1/notifications/settings     # Update webhook URL + config
POST   /api/v1/notifications/test/webhook # Test webhook (send test notification)
```

**Admin** (user management only)
```
GET    /api/v1/admin/users                # List all users (admin only)
POST   /api/v1/admin/users                # Create new user (admin only)
DELETE /api/v1/admin/users/{id}           # Delete user (admin only)
GET    /api/v1/admin/settings             # Get admin settings
PATCH  /api/v1/admin/settings             # Update admin settings (open_registration, etc.)
POST   /api/v1/admin/maintenance/cleanup-logos  # Remove unused logos
```

**Logos**
```
POST   /api/v1/logos/upload               # Upload logo file (multipart/form-data)
GET    /api/v1/logos/search?q=netflix     # Search logo URL (Clearbit/Google)
```

**Database**
```
POST   /api/v1/database/backup            # Create database backup (returns file)
POST   /api/v1/database/restore           # Restore from backup file
POST   /api/v1/database/import            # Import data (CSV/JSON)
```

**Statistics**
```
GET    /api/v1/stats/overview             # Total cost, active subs, upcoming payments
GET    /api/v1/stats/by-category          # Spending by category
GET    /api/v1/stats/by-payment-method    # Spending by payment method
GET    /api/v1/stats/timeline             # Historical spending (monthly/yearly)
```

---

### Frontend: React

#### Stack Technologiczny
- **Framework**: React 18+
- **Build Tool**: Vite
- **Router**: React Router v6
- **State Management**:
  - React Query (TanStack Query) - server state
  - Zustand - client state
- **Forms**: React Hook Form + Zod
- **UI Library**: **Material-UI (MUI) v5**
  - Kompletny zestaw komponentów
  - Built-in theming system (wspiera 8 kolorów + dark mode)
  - Accessibility out-of-the-box
  - TypeScript support
- **Charts**: Recharts (dla statistics)
- **Date Handling**: date-fns
- **i18n**: react-i18next (**tylko polski + angielski**)
- **HTTP Client**: Axios z interceptorami
- **Icons**: Material Icons (wbudowane w MUI)
- **Testing**: Vitest + React Testing Library

#### Struktura Katalogów
```
frontend/
├── public/
│   ├── locales/              # pliki tłumaczeń JSON (tylko 2 języki)
│   │   ├── en/
│   │   │   └── translation.json
│   │   └── pl/
│   │       └── translation.json
│   └── manifest.json
│
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── vite-env.d.ts
│   │
│   ├── api/                  # API client
│   │   ├── client.ts        # axios instance
│   │   ├── auth.ts
│   │   ├── subscriptions.ts
│   │   ├── categories.ts
│   │   └── ...
│   │
│   ├── components/
│   │   ├── common/          # reusable components
│   │   │   ├── Button/
│   │   │   ├── Input/
│   │   │   ├── Modal/
│   │   │   ├── Card/
│   │   │   └── ...
│   │   │
│   │   ├── layout/
│   │   │   ├── Header/
│   │   │   ├── Sidebar/
│   │   │   ├── Footer/
│   │   │   └── MainLayout/
│   │   │
│   │   ├── subscriptions/
│   │   │   ├── SubscriptionList/
│   │   │   ├── SubscriptionCard/
│   │   │   ├── SubscriptionForm/
│   │   │   ├── SubscriptionFilters/
│   │   │   └── SubscriptionSort/
│   │   │
│   │   ├── stats/
│   │   │   ├── StatsOverview/
│   │   │   ├── ExpenseChart/
│   │   │   └── CategoryBreakdown/
│   │   │
│   │   └── settings/
│   │       ├── ThemeSettings/
│   │       ├── NotificationSettings/
│   │       ├── CurrencySettings/
│   │       └── ProfileSettings/
│   │
│   ├── pages/
│   │   ├── Auth/
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   └── PasswordReset.tsx
│   │   ├── Dashboard/
│   │   ├── Subscriptions/
│   │   ├── Statistics/
│   │   ├── Settings/
│   │   ├── Profile/
│   │   ├── Admin/
│   │   └── NotFound/
│   │
│   ├── hooks/               # custom hooks
│   │   ├── useAuth.ts
│   │   ├── useSubscriptions.ts
│   │   ├── useCategories.ts
│   │   ├── useCurrencies.ts
│   │   ├── useTheme.ts
│   │   └── useDebounce.ts
│   │
│   ├── store/               # Zustand stores
│   │   ├── authStore.ts
│   │   ├── themeStore.ts
│   │   └── filterStore.ts
│   │
│   ├── types/               # TypeScript types
│   │   ├── api.ts
│   │   ├── subscription.ts
│   │   ├── user.ts
│   │   └── ...
│   │
│   ├── utils/
│   │   ├── formatters.ts    # currency, date formatters
│   │   ├── validators.ts
│   │   ├── constants.ts
│   │   └── helpers.ts
│   │
│   ├── styles/
│   │   ├── theme.ts         # theme config
│   │   └── global.css
│   │
│   └── i18n/
│       └── config.ts        # i18next config
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── package.json
├── tsconfig.json
├── vite.config.ts
└── .env.example
```

#### Główne Komponenty i Routing

```tsx
// Struktura routingu (bez calendar)
/                           → Dashboard
/login                      → Login
/register                   → Register
/subscriptions              → SubscriptionList
/subscriptions/new          → SubscriptionForm (create)
/subscriptions/:id          → SubscriptionForm (edit)
/statistics                 → Statistics (charts + overview)
/settings                   → Settings
  /settings/profile         → ProfileSettings (avatar, password)
  /settings/notifications   → NotificationSettings (webhooks only)
  /settings/currencies      → CurrencySettings
  /settings/categories      → CategorySettings
  /settings/payment-methods → PaymentMethodSettings
  /settings/household       → HouseholdSettings
  /settings/theme           → ThemeSettings (8 colors + dark mode)
/admin                      → Admin (tylko dla is_admin=true)
```

---

## Plan Migracji

**⚠️ ZMIANA:** Zaktualizowany timeline z uwzględnieniem simplified scope (bez Calendar, OIDC, AI, większości notifications)

### PRZYGOTOWANIE (1-2 dni - KRYTYCZNE)
**📋 Wymagane przed rozpoczęciem kodowania:**
1. **Przygotowanie USER_STORIES.md**
   - Analiza wszystkich PHP endpoints (AI-assisted)
   - Definicja acceptance criteria dla każdego story
   - ~80-100 user stories (podstawa dla API design + testów)
2. **Analiza bazy danych**
   - Ekstrakcja schema SQLite
   - Mapowanie tabel → SQLAlchemy models
   - Identyfikacja relationships
3. **API Contract**
   - Precyzyjna specyfikacja wszystkich endpointów
   - Request/Response schemas (OpenAPI preview)

### Faza 1: Backend Foundation (1.5-2 tygodnie)
**Cel:** Działające API dla core operations

1. **Setup projektu**
   - FastAPI skeleton + structure
   - Alembic migrations setup
   - pytest + fixtures
   - ruff + mypy config

2. **Database Layer**
   - SQLAlchemy models (8 tabel): User, Subscription, Category, Currency, PaymentMethod, HouseholdMember, NotificationSettings, Settings
   - Database session management
   - Initial migration (compatible z starą bazą)

3. **Autoryzacja** (uproszczona bez OIDC)
   - JWT implementation (access + refresh tokens)
   - API Key middleware
   - Password hashing (bcrypt)
   - `/auth/login`, `/auth/register`, `/auth/refresh`

4. **Core CRUD endpoints** (modularnie, z testami)
   - `/api/v1/subscriptions` (full CRUD + clone + renew)
   - `/api/v1/categories` (full CRUD + sort)
   - `/api/v1/payment-methods` (full CRUD + sort)
   - `/api/v1/household/members` (full CRUD)
   - `/api/v1/users/me` (profile operations)

5. **Testy** (>80% coverage dla Phase 1)
   - Unit tests dla services
   - Integration tests dla API endpoints

### Faza 2: Backend Advanced Features (1.5-2 tygodnie)
**Cel:** Kompletne API z wszystkimi funkcjonalnościami

1. **Currencies + Fixer API**
   - CRUD endpoints
   - Fixer API integration (httpx async)
   - Currency conversion logic
   - `/currencies/convert`, `/currencies/update-rates`

2. **Notification system** (TYLKO webhooks)
   - Webhook service (httpx async POST)
   - Test endpoint `/notifications/test/webhook`
   - Settings CRUD

3. **Logo Management**
   - Upload endpoint (Pillow resize)
   - Logo search (Clearbit/Google API)
   - Image validation + storage

4. **Statistics**
   - Calculation services (by category, payment method, timeline)
   - `/stats/*` endpoints
   - Aggregation queries (SQLAlchemy)

5. **Export**
   - CSV export functionality
   - Response streaming dla dużych plików

6. **Testy** (>80% coverage dla Phase 2)

### Faza 3: Backend Infrastructure (1 tydzień)
**Cel:** Production-ready backend

1. **Celery tasks** (zastąpienie cronjobs)
   - Setup Celery + Redis
   - Task: `update_next_payment_dates` (daily 1:00)
   - Task: `update_exchange_rates` (daily 2:00)
   - Task: `send_payment_notifications` (daily 9:00 - webhooks)

2. **Database operations**
   - Backup endpoint (SQLite copy)
   - Restore endpoint
   - Import CSV/JSON

3. **Admin endpoints**
   - User management (list, create, delete)
   - Admin settings
   - Maintenance (cleanup logos)

4. **OpenAPI Documentation**
   - Auto-generated Swagger UI
   - Request/response examples
   - Authentication documentation

5. **Final tests** (integration + E2E)

### Faza 4: Frontend Foundation (1.5-2 tygodnie)
**Cel:** Działająca aplikacja React z auth + routing

1. **Setup**
   - Vite + React + TypeScript
   - Router (React Router v6)
   - State management (React Query + Zustand)
   - UI library (Material-UI v5)
   - MUI theming (8 kolorów + dark mode)

2. **Auth Flow**
   - Login page
   - Register page
   - JWT token handling (interceptors)
   - Protected routes
   - Logout

3. **Layout**
   - Header + Sidebar + Footer
   - Responsive navigation
   - Mobile menu

4. **Theme System**
   - 8 color themes
   - Dark/Light mode toggle
   - Custom CSS override
   - LocalStorage + backend sync

5. **i18n Setup**
   - react-i18next config
   - **2 języki: polski + angielski** (możliwość rozszerzenia w przyszłości)
   - Language switcher (prosty toggle PL/EN)
   - Tłumaczenia z PHP scripts/i18n/pl.js i en.js

6. **API Client**
   - Axios instance
   - Request/Response interceptors
   - Error handling
   - Type-safe (OpenAPI codegen)

### Faza 5: Frontend Core Features (2-3 tygodnie)
**Cel:** Wszystkie główne widoki działające

1. **Dashboard**
   - Overview cards (total cost, active subs, upcoming)
   - Quick actions
   - Recent subscriptions

2. **Subscriptions**
   - SubscriptionList (filters, sort, pagination)
   - SubscriptionForm (create + edit)
   - SubscriptionCard
   - Delete confirmation
   - Clone action
   - Renew action

3. **Settings Pages**
   - Profile (avatar upload, password change)
   - Categories (CRUD + drag-drop sort)
   - Payment Methods (CRUD + sort)
   - Household Members (CRUD)
   - Currencies (CRUD + Fixer settings)
   - Notifications (webhook URL + test)
   - Theme (colors + dark mode)

4. **Forms** (React Hook Form + Zod)
   - Validation
   - Error messages
   - i18n

### Faza 6: Frontend Advanced Features (1.5-2 tygodnie)
**Cel:** Statistics, Admin, Polish

1. **Statistics Page**
   - StatsOverview (cards)
   - ExpenseChart (Recharts - timeline)
   - CategoryBreakdown (pie chart)
   - PaymentMethodBreakdown

2. **Admin Panel**
   - User list
   - Create user form
   - Delete user
   - Admin settings

3. **Logo Management**
   - Logo upload (drag & drop)
   - Logo search integration
   - Preview

4. **Export**
   - CSV export button
   - Download handling

5. **Testy Frontend** (Vitest + RTL)
   - Component tests
   - Integration tests
   - E2E critical flows (Playwright opcjonalnie)

### Faza 7: Polish & Migration (1 tydzień)
**Cel:** Production-ready app

1. **Mobile Responsiveness**
   - Test all pages na mobile
   - Touch-friendly interactions

2. **PWA** (opcjonalne)
   - Service worker
   - Offline support
   - Install prompt

3. **Data Migration Script**
   - PHP SQLite → Python SQLite (compatibility check)
   - Migration guide dla userów

4. **Performance**
   - React Query caching optimization
   - Image lazy loading
   - Bundle size analysis (Vite bundle analyzer)

5. **Bug Fixes** (user testing feedback)

### Faza 8: Deployment (0.5-1 tydzień)
**Cel:** Deployable containers

1. **Docker**
   - Dockerfile (multi-stage: backend + frontend)
   - docker-compose.yml (app + redis + celery worker)
   - Health checks
   - Volume mounts (db, logos)

2. **Environment Variables**
   - .env.example
   - Documentation

3. **Documentation**
   - README.md (installation, usage)
   - API docs (Swagger)
   - Migration guide (PHP → Python)

4. **Release**
   - GitHub release
   - Docker Hub push
   - Changelog

---

## Kluczowe Decyzje Projektowe

### 1. Baza Danych
**SQLite** (definitywna decyzja):
- Zachowanie 100% kompatybilności ze starą bazą (wallos.db)
- Zero konfiguracji - single file database
- Łatwe backup/restore (kopiowanie pliku)
- Wystarczające dla single-user / small household deployments
- aiosqlite dla async support w FastAPI
- Brak potrzeby dodatkowych kontenerów
- Prostota deploymentu

### 2. Task Queue
**Celery + Redis** zastąpi cronjobs:
- `update_next_payment_dates` → codziennie o 1:00 (automatyczne obliczanie next_payment)
- `update_exchange_rates` → codziennie o 2:00 (Fixer API sync)
- `send_payment_notifications` → codziennie o 9:00 (webhooks dla upcoming payments)
- ❌ ~~`sendverificationemails`~~ - poza scope (bez email)
- ❌ ~~`sendresetpasswordemails`~~ - poza scope (bez email)
- ❌ ~~`checkforupdates`~~ - poza scope
- ❌ ~~`storetotalyearlycost`~~ - poza scope

### 3. Autoryzacja (uproszczona)
- **JWT tokens**: HttpOnly cookies dla web app (access 15min + refresh 7 days)
- **API Key**: zachowane dla API access (X-API-Key header)
- ❌ ~~**OAuth/OIDC**~~ - poza scope
- ❌ ~~**2FA/TOTP**~~ - poza scope

### 4. File Upload
- Logos: `/api/v1/logos/upload` (Pillow dla resize/optimize)
- Avatars: `/api/v1/users/me/avatar` (Pillow)
- Storage: filesystem (z opcją S3 w przyszłości)

### 5. Internationalization
- **Backend**: Python dict dla 2 języków (pl, en)
- **Frontend**: react-i18next
- **Tylko 2 języki: polski + angielski**
  - Konwersja z PHP: `scripts/i18n/pl.js` → `public/locales/pl/translation.json`
  - Konwersja z PHP: `scripts/i18n/en.js` → `public/locales/en/translation.json`
- Shared translation keys między BE/FE
- Możliwość rozszerzenia w przyszłości (struktura gotowa)

### 6. Themes (Material-UI)
MUI Theme Provider wspiera:
- **Light/Dark mode** (MUI built-in)
- **8 kolorów** jako primary palette (blue, green, red, yellow, purple, pink, orange, gray)
- **Custom CSS override** (MUI sx prop + GlobalStyles)
- **Zachowanie preferencji** w localStorage + sync z backend (settings.color_theme, settings.dark_mode)
- Automatyczny mode (system preference detection)

---

## Estymacja Czasu

**⚠️ ZAKTUALIZOWANE:** Reduced scope (bez Calendar, OIDC, AI, email notifications)

| Faza | Czas (manualny) | Czas (AI-assisted) | Zadania |
|------|-----------------|-------------------|---------|
| **PRZYGOTOWANIE** | **2-3 dni** | **1 dzień** | USER_STORIES.md, schema analysis, API contract |
| 1. Backend Foundation | 1.5-2 tyg | **4-5 dni** | Models, Auth (JWT), Basic CRUD |
| 2. Backend Advanced | 1.5-2 tyg | **5-6 dni** | Currencies, Webhooks, Stats, Logos |
| 3. Backend Infrastructure | 1 tyg | **3-4 dni** | Celery, Tests, Admin, OpenAPI |
| 4. Frontend Foundation | 1.5-2 tyg | **4-5 dni** | Setup, Routing, Auth, i18n, Theme |
| 5. Frontend Core | 2-3 tyg | **1-1.5 tyg** | Dashboard, Subscriptions, Settings |
| 6. Frontend Advanced | 1.5-2 tyg | **4-5 dni** | Stats, Admin, Logo, Export |
| 7. Polish & Migration | 1 tyg | **4-5 dni** | Mobile, PWA, Migration, Bugs |
| 8. Deployment | 0.5-1 tyg | **2-3 dni** | Docker, Docs, Release |
| **TOTAL** | **~11-15 tyg** | **~6-8 tyg** | **~2.5-3.5 miesięcy** → **~1.5-2 miesięcy** |

**Oszczędność czasu dzięki AI:** ~40-50%

**Krytyczne dependency:**
- USER_STORIES.md MUSI być gotowe przed Phase 1
- Backend API musi być gotowe przed Frontend Core (Phase 4 może zacząć się po Phase 1)

---

## Dodatkowe Zalety Nowej Architektury

1. **Type Safety**: TypeScript frontend + Pydantic backend
2. **API Documentation**: Auto-generated Swagger/OpenAPI
3. **Better Testing**: pytest + Vitest
4. **Modern DX**: Hot reload, better debugging
5. **Scalability**: Możliwość łatwego przejścia na microservices
6. **Performance**: React Query caching, FastAPI async
7. **Mobile-first**: React components łatwiej responsive
8. **Maintainability**: Separacja concerns, SOLID principles

---

## Ryzyka i Mitygacje

| Ryzyko | Mitygacja |
|--------|-----------|
| Utrata funkcjonalności | Dokładna analiza każdego endpointa przed migracją |
| Breaking changes dla użytkowników | Script migracji danych + kompatybilny API |
| Performance regression | Load testing, benchmarking |
| Problemy z i18n | Wczesne setup, reuse istniejących tłumaczeń |
| Długi czas migracji | Iteracyjny rollout, feature flags |

---

---

## Wymagania Techniczne i Best Practices

### Backend Requirements
1. **Type Safety**
   - Wszystkie funkcje z type hints (Python 3.11+)
   - mypy strict mode (zero errors)
   - Pydantic schemas dla wszystkich API requests/responses

2. **Modularność**
   - Każdy serwis w osobnym pliku
   - Dependency injection (FastAPI Depends)
   - Clear separation: routes → services → models
   - SOLID principles

3. **Testy**
   - >80% code coverage (pytest-cov)
   - Unit tests dla wszystkich services
   - Integration tests dla wszystkich API endpoints
   - Fixtures dla test data (conftest.py)
   - Mocking external APIs (Fixer, logo search)

4. **Code Quality**
   - ruff linter (zero warnings)
   - Black/ruff formatter
   - Sorted imports (isort via ruff)
   - No commented-out code
   - Clear docstrings (Google style)

5. **Gotowe Biblioteki**
   - FastAPI (routing, OpenAPI)
   - SQLAlchemy (ORM)
   - Pydantic (validation)
   - python-jose (JWT)
   - httpx (async HTTP)
   - Pillow (images)
   - Celery (tasks)
   - pytest (testing)

### Frontend Requirements
1. **Type Safety**
   - TypeScript strict mode
   - No `any` types (use `unknown` lub specific types)
   - Auto-generated types z OpenAPI (openapi-typescript-codegen)

2. **Modularność**
   - Component per file
   - Custom hooks dla reusable logic
   - Atomic design pattern (atoms → molecules → organisms)
   - Storybook dla component documentation (opcjonalne)

3. **Testy**
   - Component tests (Vitest + React Testing Library)
   - Integration tests (API mocking z MSW)
   - E2E critical paths (Playwright - opcjonalne)

4. **Code Quality**
   - ESLint (zero errors)
   - Prettier (consistent formatting)
   - No console.log w production
   - PropTypes validation (lub TypeScript interfaces)

5. **Gotowe Biblioteki**
   - React Router (routing)
   - React Query (server state)
   - Zustand (client state)
   - React Hook Form (forms)
   - Zod (validation)
   - Axios (HTTP)
   - react-i18next (i18n - tylko pl + en)
   - Material-UI v5 (UI components + theming)
   - Material Icons (icons)
   - Recharts (charts)
   - date-fns (date formatting)

### API Design Requirements
1. **RESTful**
   - Proper HTTP methods (GET, POST, PATCH, DELETE)
   - Proper status codes (200, 201, 204, 400, 401, 403, 404, 500)
   - Consistent naming (plural nouns: `/subscriptions`, `/categories`)
   - Versioning (`/api/v1/...`)

2. **Responses**
   - Consistent response format:
     ```json
     {
       "data": {...},
       "meta": {"page": 1, "limit": 50, "total": 100}
     }
     ```
   - Error format:
     ```json
     {
       "error": {
         "message": "Validation failed",
         "details": [{"field": "price", "message": "must be > 0"}]
       }
     }
     ```

3. **Documentation**
   - OpenAPI 3.0 spec (auto-generated przez FastAPI)
   - Swagger UI dla interaktywnego testowania
   - Request/response examples
   - Authentication documentation

---

## Następne Kroki

### 🎯 KROK 1: USER_STORIES.md (PRIORYTET)
**Czas:** 1-2 dni (może być AI-assisted)
1. **Analiza PHP endpoints** - przejrzeć wszystkie pliki w `/endpoints/` i `/api/`
2. **Ekstrakcja operacji** - dla każdego endpointa: co robi, jakie parametry, jaki output
3. **Generacja User Stories** - wykorzystać AI (Claude Code) do generacji stories z PHP code
4. **Review + uzupełnienie** - ręczne sprawdzenie i dodanie acceptance criteria
5. **Output:** `USER_STORIES.md` z ~80-100 stories

**Template User Story:**
```markdown
### US-XXX: [Tytuł]
**As a** [role]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [kryteria 1]
- [kryteria 2]
- ...

**API Endpoints:**
- [METHOD] /api/v1/[path]

**Business Rules:**
- [reguła 1]
- [reguła 2]
```

### 🎯 KROK 2: AUTOMATION_PLAN.md (następny)
**Czas:** 1 dzień
- Strategia automatyzacji z wykorzystaniem AI tools
- Orchestration workflow (VS Code + AI)
- Quality gates
- Delegacja zadań (Claude Code, Copilot, Gemini)

### 🎯 KROK 3: Database Schema Analysis
**Czas:** 0.5 dnia
- Ekstrakcja schema z SQLite
- Diagram relationships
- Mapping do SQLAlchemy models

### 🎯 KROK 4: Start Development
- Zgodnie z Plan Migracji (Faza 1 → Faza 8)
- Tracking progress (todo list, GitHub issues)
- Regular reviews (po każdej fazie)
