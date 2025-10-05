#!/bin/bash
# Wallos Refactor Orchestration Script
# Lightweight task launcher for parallel AI execution
# Uses native VS Code plugins (Copilot, Claude Code, Gemini, ChatGPT Plus, DeepInfra)

set -e

PROJECT_ROOT="/Users/jacekdybowski/projects/jac-subscription-tracker"
cd "$PROJECT_ROOT"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

# Show usage
usage() {
    cat << EOF
Usage: ./scripts/orchestrate.sh <phase> [options]

PHASES:
  prep                 - Preparation phase (DB analysis, PHP inventory)
  phase1-models        - Generate SQLAlchemy models (8 files, parallel)
  phase1-schemas       - Generate Pydantic schemas (10 files, parallel)
  phase1-routes-simple - Generate simple API routes (12 files, parallel)
  phase1-routes-complex- Generate complex API routes (3 files, sequential)
  phase1-services      - Generate service layer (9 files, mixed)
  phase1-tests         - Generate backend tests (9 files, parallel)
  phase4-components    - Generate React components (20 files, parallel/batch)
  batch-i18n           - Convert i18n files (DeepInfra batch, \$0.40)
  validate             - Run quality gates (validator + mypy + ruff + pytest)
  review               - Full codebase review (Gemini 2.5 Pro, 1M context)

OPTIONS:
  --dry-run            - Show what would be executed without running
  --parallel N         - Number of parallel Copilot Chat sessions (default: 4)
  --skip-validation    - Skip quality gates (not recommended)

EXAMPLES:
  # Generate all 8 SQLAlchemy models in parallel
  ./scripts/orchestrate.sh phase1-models --parallel 8

  # Generate schemas with validation
  ./scripts/orchestrate.sh phase1-schemas

  # Batch process i18n files via DeepInfra
  ./scripts/orchestrate.sh batch-i18n

  # Full validation
  ./scripts/orchestrate.sh validate

EOF
    exit 0
}

# Check if help requested
if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]] || [[ -z "$1" ]]; then
    usage
fi

PHASE=$1
DRY_RUN=${2:-""}
PARALLEL=${3:-4}

# ============================================================================
# PREPARATION PHASE
# ============================================================================
run_prep() {
    log_info "PREPARATION PHASE - Database & PHP Analysis"

    echo ""
    echo "Step 1: Extract SQLite schema"
    if [[ ! -f "analysis/schema.sql" ]]; then
        mkdir -p analysis
        sqlite3 db/wallos.db .schema > analysis/schema.sql
        log_success "Schema extracted to analysis/schema.sql"
    else
        log_warn "Schema already exists, skipping"
    fi

    echo ""
    echo "Step 2: Analyze database schema"
    log_info "TODO: Open Claude Code and run:"
    echo ""
    echo "  @analysis/schema.sql Analyze this SQLite schema."
    echo "  For each table document:"
    echo "  1. Columns (name, type, constraints)"
    echo "  2. Foreign keys & relationships"
    echo "  3. Indexes"
    echo "  4. Business logic implications"
    echo ""
    echo "  Output to: analysis/database_analysis.md"
    echo ""

    echo "Step 3: PHP endpoint inventory"
    log_info "Counting PHP files..."
    ENDPOINT_COUNT=$(find endpoints -name "*.php" | wc -l)
    API_COUNT=$(find api -name "*.php" 2>/dev/null | wc -l || echo 0)
    log_success "Found $ENDPOINT_COUNT endpoint files, $API_COUNT API files"

    echo ""
    log_success "PREPARATION PHASE complete!"
    echo ""
    log_info "NEXT STEPS:"
    echo "  1. Review analysis/database_analysis.md (Claude Code output)"
    echo "  2. Run: ./scripts/orchestrate.sh phase1-models"
}

# ============================================================================
# PHASE 1: MODELS (8 files, parallel)
# ============================================================================
run_phase1_models() {
    log_info "PHASE 1 - Generate SQLAlchemy Models (8 files)"

    MODELS=(
        "user"
        "subscription"
        "category"
        "currency"
        "payment_method"
        "household_member"
        "notification_settings"
        "settings"
    )

    echo ""
    log_info "Strategy: Parallel execution via GitHub Copilot Chat (GPT-4o, free tier)"
    log_info "Files to generate: ${#MODELS[@]}"
    log_info "Parallel sessions: $PARALLEL (you can open up to 8 VS Code windows)"
    echo ""

    if [[ "$DRY_RUN" == "--dry-run" ]]; then
        log_warn "DRY RUN - would generate:"
        for model in "${MODELS[@]}"; do
            echo "  - backend/app/models/${model}.py"
        done
        return
    fi

    echo "==================== MANUAL INSTRUCTIONS ===================="
    echo ""
    echo "1. Open $PARALLEL VS Code windows (Cmd+Shift+N on Mac)"
    echo ""
    echo "2. In each window, open a different model file:"
    for i in $(seq 0 $((PARALLEL - 1))); do
        if [[ $i -lt ${#MODELS[@]} ]]; then
            echo "   Window $((i+1)): backend/app/models/${MODELS[$i]}.py"
        fi
    done
    echo ""
    echo "3. In EACH window, open Copilot Chat (Ctrl+Shift+I / Cmd+Shift+I)"
    echo ""
    echo "4. Paste this prompt in ALL Copilot Chat windows:"
    echo ""
    echo "------- PROMPT START -------"
    cat << 'PROMPT'
@workspace Generate SQLAlchemy 2.0 model for this table.

Context files:
- analysis/schema.sql - database schema
- analysis/database_analysis.md - table relationships
- context/_CORE_CONTEXT.md - constraints & style

Requirements:
1. Async support (use Base from app.db.base)
2. Full type hints (Python 3.11+)
3. Relationships with back_populates
4. __repr__ for debugging
5. Google-style docstring

Example pattern:
```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Subscription(Base):
    """Subscription model.

    Attributes:
        id: Primary key
        user_id: Foreign key to users
        name: Subscription name
        ...
    """
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # ... other columns

    # Relationships
    user = relationship("User", back_populates="subscriptions")

    def __repr__(self) -> str:
        return f"<Subscription(id={self.id}, name={self.name})>"
```

Generate the model for the current file.
PROMPT
    echo "------- PROMPT END -------"
    echo ""
    echo "5. Press Enter in ALL windows at the same time"
    echo ""
    echo "6. Wait for all 8 models to be generated (parallel execution!)"
    echo ""
    echo "7. When done, run validation:"
    echo "   ./scripts/orchestrate.sh validate"
    echo ""
    echo "============================================================"
    echo ""

    read -p "Press Enter when you've completed all 8 models..."

    echo ""
    log_info "Running validation..."
    python scripts/automation/context_validator.py

    if [[ $? -eq 0 ]]; then
        log_success "All models validated successfully!"
    else
        log_error "Validation failed - review errors above"
        exit 1
    fi
}

# ============================================================================
# PHASE 1: SCHEMAS (10 files, parallel)
# ============================================================================
run_phase1_schemas() {
    log_info "PHASE 1 - Generate Pydantic Schemas (10 files)"

    SCHEMAS=(
        "user"
        "subscription"
        "category"
        "currency"
        "payment_method"
        "household_member"
        "notification_settings"
        "settings"
        "auth"
        "common"
    )

    echo ""
    log_info "Strategy: Parallel execution via GitHub Copilot Chat (GPT-4o)"
    log_info "Files to generate: ${#SCHEMAS[@]}"
    echo ""

    echo "==================== MANUAL INSTRUCTIONS ===================="
    echo ""
    echo "1. Open $PARALLEL VS Code windows"
    echo ""
    echo "2. In each window, open a schema file:"
    for i in $(seq 0 $((PARALLEL - 1))); do
        if [[ $i -lt ${#SCHEMAS[@]} ]]; then
            echo "   Window $((i+1)): backend/app/schemas/${SCHEMAS[$i]}.py"
        fi
    done
    echo ""
    echo "3. Use this prompt in Copilot Chat:"
    echo ""
    cat << 'PROMPT'
@workspace Generate Pydantic v2 schemas for this model.

For each model create:
1. {Model}Base - shared fields
2. {Model}Create - for POST requests
3. {Model}Update - for PATCH requests (all optional)
4. {Model}Response - for GET responses
5. {Model}InDB - with id, timestamps

Requirements:
- Pydantic v2 syntax (Field, ConfigDict)
- Full validation (email, URL, gt=0, etc.)
- Type hints everywhere
- Google-style docstrings

See backend/app/models/{model}.py for field reference.
See context/_CORE_CONTEXT.md for business rules.

Example: subscriptions should validate price > 0, frequency 1-365, etc.
PROMPT
    echo ""
    echo "4. After generation, validate with Gemini Code Assist:"
    echo "   - Open Gemini Chat"
    echo "   - Prompt: 'Review validation rules in all schemas'"
    echo ""
    echo "============================================================"
    echo ""

    read -p "Press Enter when done..."
}

# ============================================================================
# BATCH: i18n CONVERSION (DeepInfra, $0.40)
# ============================================================================
run_batch_i18n() {
    log_info "BATCH PROCESSING - i18n Conversion (DeepInfra)"
    log_warn "Estimated cost: \$0.40"

    echo ""
    read -p "Convert 25 language files to 2 (pl, en) via DeepInfra? [y/N] " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Cancelled"
        exit 0
    fi

    if [[ -z "${DEEPINFRA_API_KEY}" ]]; then
        log_error "DEEPINFRA_API_KEY not set!"
        echo "Export it first: export DEEPINFRA_API_KEY='your-key'"
        exit 1
    fi

    log_info "Running DeepInfra batch conversion..."
    python scripts/automation/deepinfra_batch.py --task=i18n

    log_success "i18n conversion complete!"
    log_info "Review: frontend/src/locales/pl.json, en.json"
}

# ============================================================================
# VALIDATION
# ============================================================================
run_validate() {
    log_info "Running Quality Gates..."

    echo ""
    echo "1. Context Validator (check constraints)"
    python scripts/automation/context_validator.py
    if [[ $? -ne 0 ]]; then
        log_error "Context validation failed!"
        exit 1
    fi
    log_success "Context validation passed"

    echo ""
    echo "2. Type Checking (mypy)"
    if [[ -d "backend/app" ]]; then
        mypy backend/app --strict
        if [[ $? -ne 0 ]]; then
            log_error "Type checking failed!"
            exit 1
        fi
        log_success "Type checking passed"
    fi

    echo ""
    echo "3. Linting (ruff)"
    if [[ -d "backend/app" ]]; then
        ruff check backend/app
        if [[ $? -ne 0 ]]; then
            log_warn "Linting issues found (not critical)"
        else
            log_success "Linting passed"
        fi
    fi

    echo ""
    echo "4. Tests (pytest)"
    if [[ -d "backend/tests" ]]; then
        pytest backend/tests -v --cov=app --cov-report=term-missing
        if [[ $? -ne 0 ]]; then
            log_error "Tests failed!"
            exit 1
        fi
        log_success "All tests passed"
    fi

    echo ""
    log_success "All quality gates passed! ✨"
}

# ============================================================================
# CODE REVIEW (Gemini 2.5 Pro, 1M context)
# ============================================================================
run_review() {
    log_info "FULL CODEBASE REVIEW - Gemini 2.5 Pro (1M context)"

    echo ""
    echo "==================== MANUAL INSTRUCTIONS ===================="
    echo ""
    echo "1. Open Gemini Code Assist in VS Code"
    echo ""
    echo "2. Use this prompt:"
    echo ""
    cat << 'PROMPT'
@workspace Review entire codebase against context/_CORE_CONTEXT.md

Check for:
1. Constraint violations (PostgreSQL? Chakra UI? Wrong languages?)
2. Business rules enforcement (price > 0, user_id checks, etc.)
3. Code style compliance (type hints, docstrings, async/await)
4. Security issues (SQL injection, missing auth checks)
5. Performance concerns (N+1 queries, missing indexes)

Provide structured feedback:
- Critical issues (MUST fix)
- Warnings (SHOULD fix)
- Suggestions (NICE to have)

Focus on: backend/app/ and frontend/src/
PROMPT
    echo ""
    echo "3. Review Gemini's output carefully"
    echo ""
    echo "4. Fix critical issues before committing"
    echo ""
    echo "============================================================"
}

# ============================================================================
# MAIN DISPATCHER
# ============================================================================
case $PHASE in
    prep)
        run_prep
        ;;
    phase1-models)
        run_phase1_models
        ;;
    phase1-schemas)
        run_phase1_schemas
        ;;
    batch-i18n)
        run_batch_i18n
        ;;
    validate)
        run_validate
        ;;
    review)
        run_review
        ;;
    *)
        log_error "Unknown phase: $PHASE"
        usage
        ;;
esac

log_success "Done!"
