# ADR-0001: Clean Architecture Implementation

**Status**: Accepted  
**Date**: 2025-09-02  
**Deciders**: Development Team

## Context

The Telegram Automation System needed a maintainable, scalable architecture that separates concerns and allows for easy testing and modification.

## Decision

We will implement Clean Architecture with the following layers:

```
src/
├── core/           # Infrastructure Layer
├── models/         # Entity Layer  
├── services/       # Use Case Layer
└── telegram/       # Interface Layer
```

## Rationale

### Benefits
- **Separation of Concerns**: Each layer has single responsibility
- **Testability**: Business logic isolated from external dependencies
- **Maintainability**: Changes in one layer don't affect others
- **Scalability**: Easy to add new features without breaking existing code

### Layers Explanation
- **Core**: Database connections, configuration, logging
- **Models**: Domain entities and business objects
- **Services**: Business logic and use cases
- **Telegram**: External interface (Bot API, MTProto)

## Consequences

### Positive
- ✅ Code is more organized and easier to understand
- ✅ New developers can navigate codebase quickly
- ✅ Business logic is independent of Telegram API changes
- ✅ Easy to unit test individual components

### Negative
- ❌ Slightly more complex file structure initially
- ❌ Requires discipline to maintain boundaries

## Implementation

```python
# Example: Message creation flow
# Interface Layer
@bot.message_handler(commands=['addmessage'])
async def add_message_handler(message):
    # Use Case Layer
    service = MessageService()
    result = await service.create(text=message.text)
    # Return to interface
    await bot.reply(f"Message created: {result.id}")

# Service Layer (Business Logic)
class MessageService:
    async def create(self, text: str) -> Message:
        # Entity Layer
        message = Message(text=text, is_active=True)
        # Infrastructure Layer
        return await self.repository.save(message)
```

## Related ADRs
- [0002-dependency-management](0002-dependency-management.md)
- [0003-documentation-strategy](0003-documentation-strategy.md)