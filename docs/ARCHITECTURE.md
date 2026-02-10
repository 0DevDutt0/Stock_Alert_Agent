# Stock Agent Architecture

## Overview

Stock Agent follows a clean, layered architecture pattern that separates concerns and promotes maintainability, testability, and scalability.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Health     │  │   Stocks     │  │    Agent     │  │
│  │   Router     │  │   Router     │  │   Router     │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
└─────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
┌─────────────────────────────▼─────────────────────────────┐
│                    Service Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │    Stock     │  │ Market Data  │  │    Alert     │   │
│  │   Service    │  │   Service    │  │   Service    │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
└─────────┼──────────────────┼──────────────────┼──────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────┐  ┌─────────────┐  ┌─────────────────┐
│   Repository    │  │  Yahoo      │  │   Telegram      │
│     Layer       │  │  Finance    │  │   Bot API       │
│  (JSON/DB)      │  │    API      │  │                 │
└─────────────────┘  └─────────────┘  └─────────────────┘
```

## Layers

### 1. API Layer (`api/`)

**Responsibility**: HTTP request/response handling

- **Routers**: Define endpoints and route requests
- **Dependencies**: Dependency injection for services
- **Validation**: Request/response validation via Pydantic
- **Error Handling**: HTTP exception mapping

**Key Files**:
- `app.py`: FastAPI application factory
- `routers/`: Endpoint definitions
- `dependencies.py`: DI container

### 2. Service Layer (`services/`)

**Responsibility**: Business logic and orchestration

- **StockService**: Core stock analysis and tracking logic
- **MarketDataService**: Market data fetching with retry logic
- **AlertService**: Notification management

**Design Patterns**:
- Dependency Injection
- Strategy Pattern (for different alert channels)
- Template Method (for alert formatting)

### 3. Repository Layer (`repositories/`)

**Responsibility**: Data persistence abstraction

- **StockRepository**: Abstract interface
- **JSONStockRepository**: JSON file implementation
- **DatabaseStockRepository**: Future SQL implementation (stub)

**Design Patterns**:
- Repository Pattern
- Abstract Factory

### 4. Models Layer (`models/`)

**Responsibility**: Data structures and validation

- **Pydantic Models**: Type-safe data validation
- **Enums**: Type-safe constants
- **DTOs**: Data transfer objects

### 5. Utilities (`utils/`)

**Responsibility**: Cross-cutting concerns

- **Logger**: Centralized logging
- **Exceptions**: Custom exception hierarchy

## Data Flow

### Stock Analysis Flow

```
1. API Request → Stock Router
2. Router → Stock Service (via DI)
3. Stock Service → Market Data Service (fetch price)
4. Stock Service → Calculate profit/decision
5. Stock Service → Return StockAnalysis
6. Router → JSON Response
```

### Autonomous Agent Flow

```
1. Cron Job → /api/v1/agent/run
2. Agent Router → Stock Service
3. Stock Service → Repository (get tracked stocks)
4. For each stock:
   a. Market Data Service → Fetch current price
   b. Calculate analysis
   c. If target reached → Alert Service
   d. If daily update time → Alert Service
5. Return AgentRunResult
```

## Design Principles

### SOLID Principles

1. **Single Responsibility**: Each class has one reason to change
2. **Open/Closed**: Open for extension, closed for modification
3. **Liskov Substitution**: Repository implementations are interchangeable
4. **Interface Segregation**: Focused interfaces
5. **Dependency Inversion**: Depend on abstractions, not concretions

### Clean Architecture

- **Independence**: Business logic independent of frameworks
- **Testability**: Easy to test without external dependencies
- **Flexibility**: Easy to swap implementations

## Configuration Management

- **Pydantic Settings**: Type-safe environment variables
- **Layered Configuration**: Defaults → .env → Environment
- **Validation**: Automatic validation on startup

## Error Handling

### Exception Hierarchy

```
StockAgentException (base)
├── StockNotFoundError
├── InvalidSymbolError
├── MarketDataError
├── AlertError
├── StorageError
└── DuplicateStockError
```

### Error Flow

1. Service layer raises domain exceptions
2. API layer catches and converts to HTTP exceptions
3. FastAPI returns appropriate status codes

## Testing Strategy

### Unit Tests

- Mock external dependencies
- Test business logic in isolation
- Fast execution

### Integration Tests

- Test API endpoints end-to-end
- Use TestClient
- Verify request/response contracts

## Scalability Considerations

### Current (Phase 1)

- JSON file storage
- Single instance deployment
- Synchronous processing

### Future (Phase 2+)

- Database migration (PostgreSQL)
- Horizontal scaling with load balancer
- Async task queue (Celery/Redis)
- Caching layer (Redis)
- WebSocket support for real-time updates

## Security

- **Environment Variables**: Sensitive data not in code
- **Input Validation**: Pydantic models
- **CORS**: Configurable origins
- **Rate Limiting**: Future implementation
- **Authentication**: Future implementation

## Monitoring & Observability

### Current

- Structured logging
- Log rotation
- Health check endpoint

### Future

- Prometheus metrics
- Distributed tracing (OpenTelemetry)
- Error tracking (Sentry)
- Performance monitoring (APM)
