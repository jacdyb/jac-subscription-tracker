# CORE PROJECT CONTEXT - DO NOT DEVIATE

**ALWAYS INCLUDE THIS FILE IN ALL AI PROMPTS**

This file contains critical project constraints and decisions that MUST NEVER be violated.

---

## CRITICAL CONSTRAINTS (NEVER FORGET)

### 1. Database: SQLite ONLY
- **NO PostgreSQL**
- **NO MySQL**
- **NO other databases**
- File: `wallos.db`
- Async driver: `aiosqlite`
- Reason: Simplicity, portability, backup-friendly

### 2. UI Library: Material-UI v5 ONLY
- **NO Chakra UI**
- **NO Radix UI**
- **NO TailwindCSS components**
- **NO other UI frameworks**
- Package: `@mui/material` v5
- Reason: Complete component set, built-in theming, dark mode support

### 3. Languages: Polish + English ONLY
- **NOT 25 languages**
- **ONLY 2 languages:** `pl`, `en`
- i18n library: `react-i18next` (frontend), custom (backend)
- Reason: Simplification, reduced maintenance

### 4. Auth: JWT + API Key ONLY
- **NO OIDC**
- **NO OAuth**
- **NO Auth0, Keycloak, etc.**
- JWT: Access token (15 min) + Refresh token (7 days)
- API Key: For programmatic access
- Reason: Simplicity, no external dependencies

### 5. Notifications: Webhooks ONLY
- **NO email notifications**
- **NO Discord notifications**
- **NO Telegram notifications**
- **NO SMS notifications**
- **ONLY webhooks**
- Reason: Simplification, user responsibility

### 6. Calendar View: OUT OF SCOPE
- **DO NOT implement calendar view**
- **DO NOT suggest calendar view**
- Reason: Removed from scope

### 7. AI Recommendations: OUT OF SCOPE
- **DO NOT implement AI recommendation features**
- **DO NOT suggest AI-based categorization**
- Reason: Removed from scope

---

## BUSINESS RULES (CRITICAL - ENFORCE IN CODE)

### Subscriptions

1. **Price MUST be > 0**
   - Validation: `price > 0`
   - Error: "Price must be greater than 0"

2. **Frequency: 1-365**
   - Validation: `1 <= frequency <= 365`
   - Error: "Frequency must be between 1 and 365"

3. **Cycle: Enum only**
   - Allowed: `days`, `weeks`, `months`, `years`
   - Validation: Must be one of enum values
   - Error: "Invalid cycle type"

4. **Next payment calculation**
   - Use `dateutil.relativedelta` for months/years
   - Use `timedelta` for days/weeks
   - Handle edge cases (e.g., Jan 31 + 1 month = Feb 28/29)

### Categories

5. **Category ID=1 CANNOT be deleted**
   - This is the default category
   - Validation: `category_id != 1` before delete
   - Error: "Cannot delete default category"

6. **Category deletion**
   - Check if category is in use: `SELECT COUNT(*) FROM subscriptions WHERE category_id = ?`
   - If count > 0: Error "Category is in use"
   - Else: Allow deletion

### User Ownership

7. **ALWAYS check user_id**
   - ALL queries MUST include: `WHERE user_id = :user_id`
   - Prevents unauthorized access to other users' data
   - Security critical!

8. **Cascade deletes**
   - When user is deleted:
     - Delete all subscriptions
     - Delete all categories (except default)
     - Delete all payment methods
     - Delete all household members
     - Delete notification settings
     - Delete user settings

### Logo Management

9. **Logo max size: 5MB**
   - Validation: File size <= 5 * 1024 * 1024 bytes
   - Error: "Logo file too large (max 5MB)"

10. **Logo resize: 135x42px**
    - Use Pillow: `image.thumbnail((135, 42))`
    - Maintain aspect ratio
    - Save as PNG

### Avatar Management

11. **Avatar max size: 5MB**
    - Same as logo validation

12. **Avatar resize: 200x200px**
    - Use Pillow: `image.thumbnail((200, 200))`
    - Circular crop
    - Save as PNG

---

## CODE STYLE REQUIREMENTS (ENFORCE)

### Backend (Python 3.11+)

#### Type Hints - EVERYWHERE
```python
# ✅ CORRECT
async def get_subscription(
    db: AsyncSession,
    subscription_id: int,
    user_id: int
) -> Optional[Subscription]:
    """Get subscription by ID."""
    ...

# ❌ INCORRECT (no type hints)
async def get_subscription(db, subscription_id, user_id):
    ...
```

#### Docstrings - Google Style
```python
# ✅ CORRECT
def calculate_next_payment(
    current_date: date,
    frequency: int,
    cycle: str
) -> date:
    """Calculate next payment date.

    Args:
        current_date: Current payment date
        frequency: Number of cycles
        cycle: Cycle type (days/weeks/months/years)

    Returns:
        Next payment date

    Raises:
        ValueError: If cycle is invalid
    """
    ...
```

#### Async/Await - All DB Operations
```python
# ✅ CORRECT
async def create_subscription(
    db: AsyncSession,
    subscription_in: SubscriptionCreate
) -> Subscription:
    subscription = Subscription(**subscription_in.model_dump())
    db.add(subscription)
    await db.commit()
    await db.refresh(subscription)
    return subscription

# ❌ INCORRECT (sync in async context)
def create_subscription(db, subscription_in):
    ...
    db.commit()  # Should be: await db.commit()
    ...
```

#### Imports - Sorted (ruff/isort)
```python
# ✅ CORRECT
from datetime import date, datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate
```

#### Line Length - 100 chars max
```python
# ✅ CORRECT
subscription = await service.create_subscription(
    user_id=current_user.id,
    subscription_in=subscription_in
)

# ❌ INCORRECT (too long)
subscription = await service.create_subscription(user_id=current_user.id, subscription_in=subscription_in, extra_param=value)
```

#### Tests - >80% Coverage REQUIRED
- Use pytest + pytest-asyncio
- Test happy path + edge cases
- Mock external dependencies (Fixer API, logo downloads)
- File naming: `test_{module_name}.py`

### Frontend (TypeScript)

#### TypeScript Strict Mode
```typescript
// tsconfig.json MUST include:
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

#### NO `any` Types
```typescript
// ✅ CORRECT
interface Subscription {
  id: number;
  name: string;
  price: number;
  // ...
}

const handleSubmit = (data: SubscriptionCreate): void => {
  // ...
};

// ❌ INCORRECT
const handleSubmit = (data: any): any => {
  // ...
};
```

#### Material-UI Components ONLY
```tsx
// ✅ CORRECT
import { Button, TextField, Card } from '@mui/material';

const MyComponent = () => (
  <Card>
    <TextField label="Name" />
    <Button variant="contained">Submit</Button>
  </Card>
);

// ❌ INCORRECT
import { Button } from '@chakra-ui/react';
import { TextField } from '@radix-ui/react';
```

#### React Hook Form + Zod
```typescript
// ✅ CORRECT
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  name: z.string().min(1),
  price: z.number().positive(),
});

const { handleSubmit, control } = useForm({
  resolver: zodResolver(schema),
});
```

---

## FILE NAMING CONVENTIONS

### Backend

- **Models:** singular, snake_case
  - Example: `subscription.py`, `user.py`, `category.py`

- **Schemas:** singular, PascalCase classes
  - File: `subscription.py`
  - Classes: `SubscriptionBase`, `SubscriptionCreate`, `SubscriptionUpdate`, `SubscriptionResponse`

- **Routes:** plural, snake_case
  - Example: `subscriptions.py`, `categories.py`, `users.py`

- **Services:** singular with `_service` suffix
  - Example: `subscription_service.py`, `currency_service.py`

### Frontend

- **Components:** PascalCase
  - Example: `SubscriptionList.tsx`, `SubscriptionForm.tsx`, `Dashboard.tsx`

- **Hooks:** camelCase with `use` prefix
  - Example: `useSubscriptions.ts`, `useAuth.ts`

- **Utils:** camelCase
  - Example: `formatDate.ts`, `calculateNextPayment.ts`

---

## VALIDATION CHECKLIST

Before submitting ANY code, verify:

- [ ] **Database:** SQLite only (no PostgreSQL/MySQL mentioned)
- [ ] **UI:** Material-UI only (no Chakra/Radix)
- [ ] **Languages:** Polish + English only (not 25 languages)
- [ ] **Auth:** JWT + API Key only (no OIDC/OAuth)
- [ ] **Notifications:** Webhooks only (no email/discord/telegram)
- [ ] **Type hints:** Everywhere (Python)
- [ ] **TypeScript:** Strict mode, no `any`
- [ ] **Business rules:** Price > 0, Category 1 protected, user_id checked
- [ ] **Tests:** >80% coverage
- [ ] **Imports:** Sorted
- [ ] **Line length:** <= 100 chars

---

## FORBIDDEN PATTERNS

### ❌ NEVER DO THIS

```python
# NO PostgreSQL
from sqlalchemy.dialects import postgresql

# NO Chakra UI
from chakra_ui import Button

# NO multiple languages
LANGUAGES = ['en', 'pl', 'fr', 'de', ...]  # ONLY en, pl!

# NO OIDC
from authlib.integrations.fastapi import OAuth2

# NO any types
def process_data(data: any) -> any:

# NO sync DB operations in async context
def create_subscription(db, ...):
    db.commit()  # Should be: await db.commit()

# NO missing user_id check
query = select(Subscription).where(Subscription.id == subscription_id)
# Missing: .where(Subscription.user_id == user_id)
```

---

## DECISION LOG

### Why SQLite?
- Original Wallos uses SQLite
- Simple deployment (single file)
- No external database server needed
- Easy backups (copy file)
- Sufficient for personal finance tracking

### Why MUI v5?
- Complete component library
- Built-in theming (8 colors + dark mode)
- Accessibility out of the box
- Well-documented
- Active development

### Why 2 Languages?
- Original had 25 languages - too much maintenance
- Polish (developer native) + English (international)
- Reduces i18n file size by 92%
- Easier to maintain translations

### Why JWT only?
- No external auth provider needed
- Simple implementation
- Sufficient for personal use
- API key for automation

### Why Webhooks only?
- Users can integrate with their preferred notification service (Zapier, IFTTT, n8n)
- No SMTP/Discord/Telegram credentials to manage
- Simpler codebase

---

**REMEMBER:** This is a SIMPLIFIED version of Wallos. We intentionally removed features to reduce complexity and speed up development. DO NOT add them back without explicit user request.

**END OF CORE CONTEXT**
