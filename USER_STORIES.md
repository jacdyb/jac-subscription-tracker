# User Stories - Wallos Refactor (PHP → Python + React)

**Wersja:** 1.0
**Data:** 2025-01-XX
**Scope:** Simplified (bez Calendar, OIDC, AI recommendations, email/telegram/discord notifications)

---

## Spis Treści

1. [Authentication & Authorization](#authentication--authorization)
2. [User Profile](#user-profile)
3. [Subscriptions](#subscriptions)
4. [Categories](#categories)
5. [Currencies](#currencies)
6. [Payment Methods](#payment-methods)
7. [Household Members](#household-members)
8. [Notifications (Webhooks Only)](#notifications-webhooks-only)
9. [Statistics](#statistics)
10. [Logo Management](#logo-management)
11. [Admin Panel](#admin-panel)
12. [Database Operations](#database-operations)
13. [Settings](#settings)

---

## Authentication & Authorization

### US-001: User Registration
**As a** new user
**I want to** register with username, email, and password
**So that** I can create an account and track my subscriptions

**Acceptance Criteria:**
- POST /api/v1/auth/register endpoint accepts: `username`, `email`, `password`
- Username must be unique (case-insensitive)
- Email must be valid format and unique
- Password must be min 8 characters
- Returns 201 Created with user data (without password)
- Returns 400 if validation fails with specific error messages
- Returns 409 if username/email already exists

**API Endpoints:**
- `POST /api/v1/auth/register`

**Business Rules:**
- Username: 3-50 characters, alphanumeric + underscore only
- Email: valid email format
- Password: min 8 characters, hashed with bcrypt
- Default language: `en`
- Default currency: first currency in database or USD

---

### US-002: User Login
**As a** registered user
**I want to** log in with username and password
**So that** I can access my subscription data

**Acceptance Criteria:**
- POST /api/v1/auth/login accepts: `username`, `password`
- Returns JWT access token (expiry: 15 minutes)
- Returns JWT refresh token (expiry: 7 days)
- Tokens stored as HttpOnly cookies
- Returns 401 if credentials invalid
- Returns user data with tokens

**API Endpoints:**
- `POST /api/v1/auth/login`

**Business Rules:**
- Both username and password are required
- Password is verified using bcrypt
- Failed attempts are logged (for potential rate limiting)

---

### US-003: Token Refresh
**As a** logged-in user
**I want to** refresh my access token using refresh token
**So that** I can stay logged in without re-entering credentials

**Acceptance Criteria:**
- POST /api/v1/auth/refresh accepts refresh token from cookie
- Returns new access token (15 min expiry)
- Optionally returns new refresh token
- Returns 401 if refresh token invalid/expired

**API Endpoints:**
- `POST /api/v1/auth/refresh`

---

### US-004: User Logout
**As a** logged-in user
**I want to** log out
**So that** my session is terminated securely

**Acceptance Criteria:**
- POST /api/v1/auth/logout clears JWT cookies
- Returns 204 No Content
- Client removes tokens from storage

**API Endpoints:**
- `POST /api/v1/auth/logout`

---

### US-005: API Key Authentication
**As a** third-party application
**I want to** authenticate using API key
**So that** I can access user data without session

**Acceptance Criteria:**
- API key sent via `X-API-Key` header
- API key is validated and mapped to user
- Returns 401 if API key invalid
- All API endpoints accept API key as alternative to JWT

**API Endpoints:**
- All `/api/v1/*` endpoints

**Business Rules:**
- API key is unique per user
- API key format: UUID v4
- API key stored hashed in database

---

## User Profile

### US-010: Get Current User
**As a** logged-in user
**I want to** retrieve my profile information
**So that** I can view my account details

**Acceptance Criteria:**
- GET /api/v1/users/me returns current user data
- Includes: id, username, email, avatar, is_admin, created_at
- Excludes: password, api_key
- Returns 401 if not authenticated

**API Endpoints:**
- `GET /api/v1/users/me`

---

### US-011: Update Profile
**As a** logged-in user
**I want to** update my email
**So that** I can keep my contact information current

**Acceptance Criteria:**
- PATCH /api/v1/users/me accepts: `email`
- Email must be unique
- Returns updated user data
- Returns 400 if email invalid
- Returns 409 if email already exists

**API Endpoints:**
- `PATCH /api/v1/users/me`

---

### US-012: Change Password
**As a** logged-in user
**I want to** change my password
**So that** I can maintain account security

**Acceptance Criteria:**
- PATCH /api/v1/users/me/password accepts: `current_password`, `new_password`
- Current password must be correct
- New password min 8 characters
- Password is hashed with bcrypt
- Returns 200 on success
- Returns 401 if current password incorrect

**API Endpoints:**
- `PATCH /api/v1/users/me/password`

---

### US-013: Upload Avatar
**As a** logged-in user
**I want to** upload profile picture
**So that** I can personalize my account

**Acceptance Criteria:**
- POST /api/v1/users/me/avatar accepts multipart/form-data with `file` field
- Allowed formats: png, jpg, jpeg, gif, webp
- Max size: 5MB
- Image resized to 200x200px
- Filename: `{user_id}-{timestamp}.{ext}`
- Stored in `/images/uploads/avatars/`
- Returns avatar URL
- Returns 400 if file invalid

**API Endpoints:**
- `POST /api/v1/users/me/avatar`

**Business Rules:**
- Old avatar is deleted when new one uploaded
- Avatar is optional (default: null)

---

### US-014: Delete Avatar
**As a** logged-in user
**I want to** remove my profile picture
**So that** I can use default avatar

**Acceptance Criteria:**
- DELETE /api/v1/users/me/avatar removes avatar file
- Sets user.avatar to null
- Returns 204 No Content
- Returns 404 if no avatar exists

**API Endpoints:**
- `DELETE /api/v1/users/me/avatar`

---

### US-015: Get API Key
**As a** logged-in user
**I want to** view my API key
**So that** I can use it for API access

**Acceptance Criteria:**
- GET /api/v1/users/me/api-key returns API key (unhashed)
- Returns 200 with `api_key` field
- If no API key exists, generates new one

**API Endpoints:**
- `GET /api/v1/users/me/api-key`

---

### US-016: Regenerate API Key
**As a** logged-in user
**I want to** regenerate my API key
**So that** I can revoke old key if compromised

**Acceptance Criteria:**
- POST /api/v1/users/me/api-key/regenerate generates new UUID
- Old API key is invalidated
- Returns new API key
- Returns 200

**API Endpoints:**
- `POST /api/v1/users/me/api-key/regenerate`

---

### US-017: Delete Account
**As a** logged-in user
**I want to** permanently delete my account
**So that** all my data is removed

**Acceptance Criteria:**
- DELETE /api/v1/users/me deletes user and all related data
- Cascade deletes: subscriptions, categories, payment_methods, household_members, settings
- Avatar file is deleted
- Returns 204 No Content
- User is logged out

**API Endpoints:**
- `DELETE /api/v1/users/me`

**Business Rules:**
- Soft delete is NOT implemented (hard delete)
- Action is irreversible

---

## Subscriptions

### US-020: List Subscriptions
**As a** logged-in user
**I want to** view all my subscriptions with filters and sorting
**So that** I can manage them efficiently

**Acceptance Criteria:**
- GET /api/v1/subscriptions returns paginated list
- Query params:
  - `category_id` (filter by category)
  - `payment_method_id` (filter by payment method)
  - `payer_user_id` (filter by household member)
  - `inactive` (boolean: show inactive)
  - `sort` (field: name, price, next_payment, created_at)
  - `order` (asc/desc)
  - `search` (partial match on name)
  - `page` (default: 1)
  - `limit` (default: 50, max: 100)
- Returns: `{data: [...], meta: {page, limit, total}}`
- Includes joined data: currency, category, payment_method, payer_user
- Returns 200

**API Endpoints:**
- `GET /api/v1/subscriptions`

**Business Rules:**
- Only returns subscriptions for current user
- Default sort: next_payment ASC

---

### US-021: Get Single Subscription
**As a** logged-in user
**I want to** view details of specific subscription
**So that** I can see all information

**Acceptance Criteria:**
- GET /api/v1/subscriptions/{id} returns single subscription
- Includes all fields + joined data
- Returns 404 if subscription doesn't exist or doesn't belong to user
- Returns 200

**API Endpoints:**
- `GET /api/v1/subscriptions/{id}`

---

### US-022: Create Subscription
**As a** logged-in user
**I want to** add new subscription
**So that** I can track recurring payment

**Acceptance Criteria:**
- POST /api/v1/subscriptions accepts:
  - Required: `name`, `price`, `currency_id`, `next_payment`, `cycle`, `frequency`
  - Optional: `logo` (file upload OR `logo_url`), `category_id`, `payment_method_id`, `payer_user_id`, `notes`, `url`, `notify`, `notify_days_before`, `inactive`, `cancellation_date`, `replacement_subscription_id`, `auto_renew`, `start_date`
- If `logo_url` provided: download, resize (135x42px), save
- If `logo` file provided: resize (135x42px), save
- Validates: price > 0, frequency 1-365, cycle in [days, weeks, months, years]
- Returns 201 Created with subscription data
- Returns 400 if validation fails

**API Endpoints:**
- `POST /api/v1/subscriptions`

**Business Rules:**
- Logo formats: png, jpg, jpeg, gif, webp (max 5MB)
- Logo filename: `{timestamp}-{sanitized_name}.{ext}`
- Default: `auto_renew = true`, `inactive = false`, `notify = false`
- `category_id`, `payment_method_id`, `payer_user_id` must belong to user

---

### US-023: Update Subscription
**As a** logged-in user
**I want to** edit subscription details
**So that** I can keep information accurate

**Acceptance Criteria:**
- PATCH /api/v1/subscriptions/{id} accepts partial update
- Accepts same fields as create (US-022)
- Logo update only if new file/URL provided
- Returns 200 with updated subscription
- Returns 404 if subscription doesn't exist or doesn't belong to user
- Returns 400 if validation fails

**API Endpoints:**
- `PATCH /api/v1/subscriptions/{id}`

---

### US-024: Delete Subscription
**As a** logged-in user
**I want to** remove subscription
**So that** I can delete canceled services

**Acceptance Criteria:**
- DELETE /api/v1/subscriptions/{id} deletes subscription
- Updates other subscriptions: SET `replacement_subscription_id = NULL` WHERE `replacement_subscription_id = {id}`
- Returns 204 No Content
- Returns 404 if subscription doesn't exist or doesn't belong to user

**API Endpoints:**
- `DELETE /api/v1/subscriptions/{id}`

---

### US-025: Clone Subscription
**As a** logged-in user
**I want to** duplicate existing subscription
**So that** I can quickly add similar ones

**Acceptance Criteria:**
- POST /api/v1/subscriptions/{id}/clone creates copy
- Copies all fields except: `id`, `created_at`
- Appends " (Copy)" to name
- Returns 201 Created with new subscription
- Returns 404 if source subscription doesn't exist

**API Endpoints:**
- `POST /api/v1/subscriptions/{id}/clone`

---

### US-026: Renew Subscription
**As a** logged-in user
**I want to** mark subscription as paid and calculate next payment
**So that** system tracks payment schedule

**Acceptance Criteria:**
- POST /api/v1/subscriptions/{id}/renew calculates next payment date
- If `auto_renew = true`: `next_payment` += (`frequency` * `cycle`)
- If `auto_renew = false`: `next_payment` unchanged
- Returns 200 with updated subscription
- Returns 404 if subscription doesn't exist

**API Endpoints:**
- `POST /api/v1/subscriptions/{id}/renew`

**Business Rules:**
- Cycle calculations:
  - `days`: add `frequency` days
  - `weeks`: add `frequency * 7` days
  - `months`: add `frequency` months
  - `years`: add `frequency` years

---

### US-027: Export Subscriptions to CSV
**As a** logged-in user
**I want to** download subscriptions as CSV file
**So that** I can use data in spreadsheet

**Acceptance Criteria:**
- GET /api/v1/subscriptions/export/csv returns CSV file
- Headers: name, price, currency, next_payment, cycle, frequency, category, payment_method, notes, url, inactive
- Respects same filters as list (US-020)
- Content-Type: text/csv
- Content-Disposition: attachment; filename="subscriptions-{date}.csv"
- Returns 200

**API Endpoints:**
- `GET /api/v1/subscriptions/export/csv`

---

### US-028: Get Subscription Statistics
**As a** logged-in user
**I want to** see summary statistics for subscriptions
**So that** I can understand my spending

**Acceptance Criteria:**
- GET /api/v1/subscriptions/stats returns:
  - `total_monthly_cost` (all active subscriptions converted to monthly)
  - `total_yearly_cost`
  - `active_subscriptions_count`
  - `inactive_subscriptions_count`
  - `upcoming_payments` (next 30 days)
- All costs in user's main currency
- Returns 200

**API Endpoints:**
- `GET /api/v1/subscriptions/stats`

**Business Rules:**
- Cost calculations:
  - Daily → × 30.44 (avg days/month)
  - Weekly → × 4.33 (avg weeks/month)
  - Monthly → × 1
  - Yearly → ÷ 12

---

## Categories

### US-030: List Categories
**As a** logged-in user
**I want to** view all my categories
**So that** I can organize subscriptions

**Acceptance Criteria:**
- GET /api/v1/categories returns all user categories
- Ordered by `order` field ASC
- Includes `subscription_count` (number of subscriptions using this category)
- Returns 200

**API Endpoints:**
- `GET /api/v1/categories`

---

### US-031: Create Category
**As a** logged-in user
**I want to** add custom category
**So that** I can organize by my preferences

**Acceptance Criteria:**
- POST /api/v1/categories accepts: `name`
- Default name: "Category" (if not provided)
- `order` = MAX(order) + 1
- Returns 201 Created with category data
- Returns 400 if name empty

**API Endpoints:**
- `POST /api/v1/categories`

---

### US-032: Update Category
**As a** logged-in user
**I want to** rename category
**So that** names are meaningful

**Acceptance Criteria:**
- PATCH /api/v1/categories/{id} accepts: `name`
- Name must not be empty
- Returns 200 with updated category
- Returns 404 if category doesn't exist or doesn't belong to user
- Returns 400 if name invalid

**API Endpoints:**
- `PATCH /api/v1/categories/{id}`

---

### US-033: Delete Category
**As a** logged-in user
**I want to** remove unused category
**So that** list stays clean

**Acceptance Criteria:**
- DELETE /api/v1/categories/{id} deletes category
- Checks if category is used by any subscription
- Returns 400 if category in use (with error message)
- Returns 204 No Content if deleted successfully
- Returns 404 if category doesn't exist

**API Endpoints:**
- `DELETE /api/v1/categories/{id}`

**Business Rules:**
- Cannot delete category ID=1 (default category)

---

### US-034: Reorder Categories
**As a** logged-in user
**I want to** change display order
**So that** important ones appear first

**Acceptance Criteria:**
- POST /api/v1/categories/sort accepts array: `[{id: 1, order: 2}, {id: 2, order: 1}]`
- Updates all categories in single transaction
- Returns 200
- Returns 400 if invalid data

**API Endpoints:**
- `POST /api/v1/categories/sort`

---

## Currencies

### US-040: List Currencies
**As a** logged-in user
**I want to** view all currencies
**So that** I can see available options

**Acceptance Criteria:**
- GET /api/v1/currencies returns all currencies
- Includes: id, code, name, symbol, rate
- Returns 200

**API Endpoints:**
- `GET /api/v1/currencies`

---

### US-041: Create Currency
**As a** logged-in user
**I want to** add custom currency
**So that** I can track in my preferred currency

**Acceptance Criteria:**
- POST /api/v1/currencies accepts: `code`, `name`, `symbol`, `rate`
- Code must be 3 characters (ISO 4217)
- Rate must be > 0
- Returns 201 Created
- Returns 400 if validation fails

**API Endpoints:**
- `POST /api/v1/currencies`

---

### US-042: Update Currency
**As a** logged-in user
**I want to** edit currency details
**So that** I can fix errors

**Acceptance Criteria:**
- PATCH /api/v1/currencies/{id} accepts: `code`, `name`, `symbol`, `rate`
- Returns 200 with updated currency
- Returns 404 if currency doesn't exist

**API Endpoints:**
- `PATCH /api/v1/currencies/{id}`

---

### US-043: Delete Currency
**As a** logged-in user
**I want to** remove currency
**So that** I keep only relevant ones

**Acceptance Criteria:**
- DELETE /api/v1/currencies/{id} deletes currency
- Checks if used by any subscription
- Returns 400 if in use
- Returns 204 if deleted
- Returns 404 if doesn't exist

**API Endpoints:**
- `DELETE /api/v1/currencies/{id}`

---

### US-044: Update Exchange Rates
**As a** logged-in user
**I want to** fetch latest rates from Fixer API
**So that** conversions are accurate

**Acceptance Criteria:**
- POST /api/v1/currencies/update-rates triggers Fixer API call
- Updates `rate` field for all currencies
- Requires Fixer API key in settings
- Returns 200 with updated count
- Returns 500 if API call fails

**API Endpoints:**
- `POST /api/v1/currencies/update-rates`

**Business Rules:**
- Fixer API URL: `https://api.apilayer.com/fixer/latest?base=USD`
- Rates cached for 24 hours (Celery task updates daily at 2:00 AM)

---

### US-045: Convert Currency
**As a** logged-in user
**I want to** convert amount between currencies
**So that** I can see equivalent values

**Acceptance Criteria:**
- GET /api/v1/currencies/convert?from=EUR&to=USD&amount=100 returns converted amount
- Query params: `from` (currency code), `to` (currency code), `amount` (number)
- Returns: `{from, to, amount, result, rate}`
- Returns 400 if currencies invalid
- Returns 200

**API Endpoints:**
- `GET /api/v1/currencies/convert`

**Business Rules:**
- Conversion formula: `result = amount * (to_rate / from_rate)`

---

## Payment Methods

### US-050: List Payment Methods
**As a** logged-in user
**I want to** view all payment methods
**So that** I can assign to subscriptions

**Acceptance Criteria:**
- GET /api/v1/payment-methods returns all user payment methods
- Ordered by `order` field ASC
- Includes `subscription_count`
- Returns 200

**API Endpoints:**
- `GET /api/v1/payment-methods`

---

### US-051: Create Payment Method
**As a** logged-in user
**I want to** add payment method
**So that** I can track which card/account is used

**Acceptance Criteria:**
- POST /api/v1/payment-methods accepts: `name`
- `order` = MAX(order) + 1
- Returns 201 Created
- Returns 400 if name empty

**API Endpoints:**
- `POST /api/v1/payment-methods`

---

### US-052: Update Payment Method
**As a** logged-in user
**I want to** rename payment method
**So that** I keep names accurate

**Acceptance Criteria:**
- PATCH /api/v1/payment-methods/{id} accepts: `name`
- Returns 200
- Returns 404 if doesn't exist

**API Endpoints:**
- `PATCH /api/v1/payment-methods/{id}`

---

### US-053: Delete Payment Method
**As a** logged-in user
**I want to** remove unused payment method
**So that** list is clean

**Acceptance Criteria:**
- DELETE /api/v1/payment-methods/{id} deletes payment method
- Checks if in use
- Returns 400 if in use
- Returns 204 if deleted

**API Endpoints:**
- `DELETE /api/v1/payment-methods/{id}`

---

### US-054: Reorder Payment Methods
**As a** logged-in user
**I want to** change display order
**So that** frequently used appear first

**Acceptance Criteria:**
- POST /api/v1/payment-methods/sort accepts array of {id, order}
- Returns 200

**API Endpoints:**
- `POST /api/v1/payment-methods/sort`

---

### US-055: Search Payment Methods
**As a** logged-in user
**I want to** search payment methods by name
**So that** I can find quickly

**Acceptance Criteria:**
- GET /api/v1/payment-methods/search?q=visa returns matching payment methods
- Partial match (case-insensitive)
- Returns 200

**API Endpoints:**
- `GET /api/v1/payment-methods/search`

---

## Household Members

### US-060: List Household Members
**As a** logged-in user
**I want to** view all household members
**So that** I can assign subscriptions to people

**Acceptance Criteria:**
- GET /api/v1/household/members returns all user's household members
- Includes `subscription_count`
- Returns 200

**API Endpoints:**
- `GET /api/v1/household/members`

---

### US-061: Create Household Member
**As a** logged-in user
**I want to** add household member
**So that** I can track who pays for what

**Acceptance Criteria:**
- POST /api/v1/household/members accepts: `name`
- Returns 201 Created
- Returns 400 if name empty

**API Endpoints:**
- `POST /api/v1/household/members`

---

### US-062: Update Household Member
**As a** logged-in user
**I want to** rename household member
**So that** names are correct

**Acceptance Criteria:**
- PATCH /api/v1/household/members/{id} accepts: `name`
- Returns 200
- Returns 404 if doesn't exist

**API Endpoints:**
- `PATCH /api/v1/household/members/{id}`

---

### US-063: Delete Household Member
**As a** logged-in user
**I want to** remove household member
**So that** list is accurate

**Acceptance Criteria:**
- DELETE /api/v1/household/members/{id} deletes member
- Checks if assigned to any subscription
- Returns 400 if in use
- Returns 204 if deleted

**API Endpoints:**
- `DELETE /api/v1/household/members/{id}`

---

## Notifications (Webhooks Only)

### US-070: Get Notification Settings
**As a** logged-in user
**I want to** view webhook notification settings
**So that** I can see current configuration

**Acceptance Criteria:**
- GET /api/v1/notifications/settings returns webhook settings
- Includes: `webhook_url`, `webhook_enabled`
- Returns 200

**API Endpoints:**
- `GET /api/v1/notifications/settings`

---

### US-071: Update Notification Settings
**As a** logged-in user
**I want to** configure webhook URL
**So that** I receive payment notifications

**Acceptance Criteria:**
- PATCH /api/v1/notifications/settings accepts: `webhook_url`, `webhook_enabled`
- Validates URL format
- Returns 200
- Returns 400 if URL invalid

**API Endpoints:**
- `PATCH /api/v1/notifications/settings`

---

### US-072: Test Webhook
**As a** logged-in user
**I want to** send test webhook
**So that** I verify configuration

**Acceptance Criteria:**
- POST /api/v1/notifications/test/webhook sends test payload to webhook_url
- Payload: `{test: true, message: "Test notification from Wallos"}`
- Returns 200 if webhook responds 200-299
- Returns 500 if webhook fails

**API Endpoints:**
- `POST /api/v1/notifications/test/webhook`

**Business Rules:**
- Timeout: 5 seconds
- HTTP method: POST
- Content-Type: application/json

---

## Statistics

### US-080: Get Overview Statistics
**As a** logged-in user
**I want to** see spending overview
**So that** I understand my finances

**Acceptance Criteria:**
- GET /api/v1/stats/overview returns:
  - `total_monthly_cost`
  - `total_yearly_cost`
  - `active_subscriptions`
  - `upcoming_payments_count` (next 30 days)
- Returns 200

**API Endpoints:**
- `GET /api/v1/stats/overview`

---

### US-081: Get Statistics by Category
**As a** logged-in user
**I want to** see spending per category
**So that** I know where money goes

**Acceptance Criteria:**
- GET /api/v1/stats/by-category returns array:
  - `category_name`
  - `category_id`
  - `total_monthly_cost`
  - `subscription_count`
- Sorted by cost DESC
- Returns 200

**API Endpoints:**
- `GET /api/v1/stats/by-category`

---

### US-082: Get Statistics by Payment Method
**As a** logged-in user
**I want to** see spending per payment method
**So that** I track which cards are used most

**Acceptance Criteria:**
- GET /api/v1/stats/by-payment-method returns array similar to US-081
- Returns 200

**API Endpoints:**
- `GET /api/v1/stats/by-payment-method`

---

### US-083: Get Timeline Statistics
**As a** logged-in user
**I want to** see historical spending
**So that** I track trends over time

**Acceptance Criteria:**
- GET /api/v1/stats/timeline?period=monthly returns:
  - Array of `{date, total_cost}`
  - Period: monthly (12 months) or yearly (5 years)
- Returns 200

**API Endpoints:**
- `GET /api/v1/stats/timeline`

---

## Logo Management

### US-090: Upload Logo
**As a** logged-in user
**I want to** upload logo file for subscription
**So that** I can use custom logo

**Acceptance Criteria:**
- POST /api/v1/logos/upload accepts multipart/form-data with `file` field
- Formats: png, jpg, jpeg, gif, webp
- Max size: 5MB
- Resized to 135x42px
- Returns `{filename, url}`
- Returns 400 if invalid

**API Endpoints:**
- `POST /api/v1/logos/upload`

---

### US-091: Search Logo
**As a** logged-in user
**I want to** find logo by company name
**So that** I don't need to upload manually

**Acceptance Criteria:**
- GET /api/v1/logos/search?q=netflix searches logo APIs (Clearbit, Google)
- Returns `{url, source}`
- Returns 404 if not found
- Returns 200

**API Endpoints:**
- `GET /api/v1/logos/search`

---

## Admin Panel

### US-100: List All Users
**As an** admin user
**I want to** view all users
**So that** I can manage accounts

**Acceptance Criteria:**
- GET /api/v1/admin/users returns all users
- Only accessible if `is_admin = true`
- Returns 403 if not admin
- Returns 200

**API Endpoints:**
- `GET /api/v1/admin/users`

---

### US-101: Create User (Admin)
**As an** admin user
**I want to** create user account
**So that** I can onboard users manually

**Acceptance Criteria:**
- POST /api/v1/admin/users accepts: `username`, `email`, `password`, `is_admin`
- Only accessible if `is_admin = true`
- Returns 201 Created
- Returns 403 if not admin

**API Endpoints:**
- `POST /api/v1/admin/users`

---

### US-102: Delete User (Admin)
**As an** admin user
**I want to** delete user account
**So that** I can remove inactive users

**Acceptance Criteria:**
- DELETE /api/v1/admin/users/{id} deletes user and all data
- Only accessible if `is_admin = true`
- Cannot delete own account
- Returns 204 No Content
- Returns 403 if not admin

**API Endpoints:**
- `DELETE /api/v1/admin/users/{id}`

---

### US-103: Get Admin Settings
**As an** admin user
**I want to** view admin settings
**So that** I can see configuration

**Acceptance Criteria:**
- GET /api/v1/admin/settings returns settings
- Includes: `open_registration`
- Returns 200
- Returns 403 if not admin

**API Endpoints:**
- `GET /api/v1/admin/settings`

---

### US-104: Update Admin Settings
**As an** admin user
**I want to** change admin settings
**So that** I can configure app

**Acceptance Criteria:**
- PATCH /api/v1/admin/settings accepts: `open_registration`
- Returns 200
- Returns 403 if not admin

**API Endpoints:**
- `PATCH /api/v1/admin/settings`

---

### US-105: Cleanup Unused Logos
**As an** admin user
**I want to** remove unused logo files
**So that** storage is optimized

**Acceptance Criteria:**
- POST /api/v1/admin/maintenance/cleanup-logos deletes logos not used by any subscription
- Returns count of deleted files
- Returns 200
- Returns 403 if not admin

**API Endpoints:**
- `POST /api/v1/admin/maintenance/cleanup-logos`

---

## Database Operations

### US-110: Backup Database
**As a** logged-in user
**I want to** download database backup
**So that** I can save my data

**Acceptance Criteria:**
- POST /api/v1/database/backup creates SQLite copy
- Returns file download
- Filename: `wallos-backup-{date}.db`
- Content-Type: application/octet-stream
- Returns 200

**API Endpoints:**
- `POST /api/v1/database/backup`

---

### US-111: Restore Database
**As a** logged-in user
**I want to** restore database from backup
**So that** I can recover data

**Acceptance Criteria:**
- POST /api/v1/database/restore accepts file upload
- Validates SQLite format
- Replaces current database
- Returns 200
- Returns 400 if invalid file

**API Endpoints:**
- `POST /api/v1/database/restore`

**Business Rules:**
- ⚠️ This is destructive operation - requires confirmation

---

### US-112: Import Data
**As a** logged-in user
**I want to** import subscriptions from CSV/JSON
**So that** I can migrate from other tools

**Acceptance Criteria:**
- POST /api/v1/database/import accepts CSV or JSON file
- Creates subscriptions from file
- Returns count of imported items
- Returns 200
- Returns 400 if format invalid

**API Endpoints:**
- `POST /api/v1/database/import`

---

## Settings

### US-120: Get User Settings
**As a** logged-in user
**I want to** view my settings
**So that** I can see preferences

**Acceptance Criteria:**
- GET /api/v1/settings returns user settings
- Includes: `main_currency_id`, `color_theme`, `dark_mode`, `custom_css`, etc.
- Returns 200

**API Endpoints:**
- `GET /api/v1/settings`

---

### US-121: Update Settings
**As a** logged-in user
**I want to** change preferences
**So that** app works how I want

**Acceptance Criteria:**
- PATCH /api/v1/settings accepts any settings field
- Validates values
- Returns 200
- Returns 400 if invalid

**API Endpoints:**
- `PATCH /api/v1/settings`

**Available Settings:**
- `main_currency_id`
- `color_theme` (blue, red, green, yellow, purple, pink, orange, gray)
- `dark_mode` (boolean)
- `custom_css` (string)
- `show_original_price` (boolean)
- `convert_currency` (boolean)
- `disabled_to_bottom` (boolean)
- `hide_disabled` (boolean)
- `monthly_price` (boolean)
- `subscription_progress` (boolean)
- `remove_background` (boolean)
- `mobile_navigation` (boolean)

---

## Celery Background Tasks

### TASK-001: Update Next Payment Dates
**Schedule:** Daily at 1:00 AM

**Purpose:** Automatically calculate next payment dates for all subscriptions

**Logic:**
- For each subscription with `auto_renew = true`:
  - If `next_payment < today`: update based on `frequency` and `cycle`
  - Repeat until `next_payment >= today`

---

### TASK-002: Update Exchange Rates
**Schedule:** Daily at 2:00 AM

**Purpose:** Fetch latest currency rates from Fixer API

**Logic:**
- Call Fixer API: `/latest?base=USD`
- Update `currencies.rate` for all currencies
- Log any errors

---

### TASK-003: Send Payment Notifications
**Schedule:** Daily at 9:00 AM

**Purpose:** Send webhook notifications for upcoming payments

**Logic:**
- Find subscriptions where `next_payment - notify_days_before = today` AND `notify = true`
- For each subscription:
  - Get user's `notification_settings`
  - If `webhook_enabled = true`: POST to `webhook_url`
- Payload:
  ```json
  {
    "type": "payment_reminder",
    "subscription": {...},
    "days_until": 3
  }
  ```

---

## Summary

**Total User Stories:** ~120
**Estimated Endpoints:** ~70
**Scope:** Simplified (no Calendar, OIDC, AI, email notifications)

---

**Next Steps:**
1. Review and approve this document
2. Use stories to generate API contract (OpenAPI spec)
3. Use stories to generate tests (pytest + Vitest)
4. Start implementation (Backend → Frontend)
