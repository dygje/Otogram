# ADR-0003: Minimal Documentation Strategy

**Status**: Accepted  
**Date**: 2025-09-02  
**Deciders**: Development Team

## Context

Documentation often becomes outdated, bloated with AI-generated content, and creates maintenance overhead. We need a sustainable approach that provides value without becoming a burden.

## Decision

We will implement a **Minimal Documentation Strategy** based on:

1. **README-Driven Development (RDD)**
2. **Architecture Decision Records (ADRs)**  
3. **Self-Documenting Code**
4. **Living Documentation**

## Rationale

### Problems with Traditional Documentation
- ❌ Becomes outdated quickly
- ❌ AI-generated content creates bloat
- ❌ Maintenance overhead
- ❌ Developers don't read lengthy docs
- ❌ Duplication between code and docs

### Our Approach
- ✅ **README-First**: Clear entry point for any developer
- ✅ **Decision History**: ADRs capture WHY decisions were made
- ✅ **Code as Documentation**: Clear naming and structure
- ✅ **Essential Only**: Document what's truly needed

## Implementation

### Documentation Structure
```
docs/
├── README.md               # Quick start (root level)
├── GETTING_STARTED.md      # Complete setup guide
├── API.md                  # Code interfaces only
├── decisions/              # Architecture Decision Records
│   ├── 0001-clean-architecture.md
│   ├── 0002-dependency-management.md
│   └── 0003-documentation-strategy.md
└── [REMOVED: AI-generated bloat]
```

### Removed Documents
- ❌ `README_FULL.md` (12K+ lines of AI-generated content)
- ❌ `MODERN_BOT_INTERFACE.md` (outdated feature descriptions)
- ❌ `SLOWMODE_BEHAVIOR.md` (implementation details in code)
- ❌ `CLEANUP_REPORT.md` (temporary document)
- ❌ `USAGE_GUIDE.md` (merged into GETTING_STARTED.md)

### Documentation Principles

#### 1. README-Driven Development
- **Purpose**: Primary entry point for developers
- **Content**: Quick start, architecture overview, essential links
- **Length**: Maximum 100 lines
- **Maintenance**: Updated with every major change

#### 2. Architecture Decision Records
- **Purpose**: Capture decision rationale and context
- **Format**: Structured (Status, Context, Decision, Consequences)
- **Timing**: Created when architectural decisions are made
- **Benefits**: Future developers understand WHY, not just HOW

#### 3. Self-Documenting Code
```python
# Bad: Comments explaining WHAT
def calc_delay(min_val, max_val):  # Calculate delay between min and max
    return random.uniform(min_val, max_val)

# Good: Code that explains itself  
def generate_random_message_delay(min_seconds: int, max_seconds: int) -> float:
    """Generate random delay to avoid detection by Telegram rate limits."""
    return random.uniform(min_seconds, max_seconds)
```

#### 4. Living Documentation
- **Location**: Same repository as code
- **Format**: Markdown (version controllable)
- **Updates**: Alongside code changes
- **Validation**: Health check includes doc verification

## Consequences

### Positive
- ✅ **Lower Maintenance**: Only essential docs to maintain
- ✅ **Always Current**: Docs stay with code changes
- ✅ **Developer Friendly**: Quick to read and understand
- ✅ **Decision Traceability**: ADRs preserve reasoning
- ✅ **Reduced Bloat**: No AI-generated filler content

### Negative  
- ❌ **Less Comprehensive**: Some details only in code
- ❌ **Initial Learning**: Developers must understand architecture
- ❌ **Discipline Required**: Must maintain documentation boundaries

## Maintenance Guidelines

### When to Document
- ✅ **Architecture decisions**: Always create ADR
- ✅ **API changes**: Update API.md
- ✅ **Setup changes**: Update GETTING_STARTED.md
- ❌ **Implementation details**: Keep in code comments
- ❌ **Temporary issues**: Don't create permanent docs

### Documentation Reviews
- **Quarterly**: Review ADRs for relevance
- **With releases**: Update README if needed
- **Never**: Create documentation "just in case"

### Quality Checks
```bash
# Validate docs are current
python scripts/health_check.py

# Check for outdated references
grep -r "TODO\|FIXME\|DEPRECATED" docs/
```

## Related ADRs
- [0001-clean-architecture](0001-clean-architecture.md)
- [0002-dependency-management](0002-dependency-management.md)