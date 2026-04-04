# Architecture

This document explains the internal architecture of the Proxmox OpenAPI project, including how the components work together and key design decisions.

## Overview

The Proxmox OpenAPI server is a **dual-mode FastAPI application** that can operate in two distinct modes:

1. **Mock Mode (Default)** - Provides in-memory CRUD operations with pre-generated OpenAPI schema
2. **Real Mode** - Acts as a validated proxy to a real Proxmox VE API

```
┌─────────────────────────────────────────────────────────┐
│              Proxmox OpenAPI Server                     │
│                                                         │
│  ┌──────────────────┐         ┌──────────────────┐    │
│  │   Mock Mode      │   OR    │   Real Mode      │    │
│  │                  │         │                  │    │
│  │  In-memory CRUD  │         │  Proxmox Proxy   │    │
│  │  646 endpoints   │         │  + Validation    │    │
│  └──────────────────┘         └──────────────────┘    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │        FastAPI Core + Swagger UI                │  │
│  └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Mode Architecture

### Mock Mode

Mock mode loads pre-generated OpenAPI schemas and dynamically creates CRUD endpoints with in-memory state management.

```
┌───────────────┐
│  User Request │
└───────┬───────┘
        │
        ▼
┌───────────────────┐
│  FastAPI Router   │
└───────┬───────────┘
        │
        ▼
┌────────────────────────────┐
│  Generated Mock Endpoint   │  (created from OpenAPI schema)
│  - Validates request       │
│  - Performs CRUD operation │
│  - Returns response        │
└────────┬───────────────────┘
         │
         ▼
┌─────────────────────┐
│  MockState          │  (in-memory dictionary)
│  - Stores resources │
│  - Generates IDs    │
└─────────────────────┘
```

**Key Components:**

- **`mock/routes.py`** - Route builder that reads OpenAPI schema and generates FastAPI endpoints
- **`mock/state.py`** - In-memory state management with dict-based storage
- **`mock/loader.py`** - Custom mock data loader from JSON/YAML files
- **`schema.py`** - Schema loading utilities

**Flow:**

1. App startup loads `generated/proxmox/latest/openapi.json`
2. `register_generated_proxmox_mock_routes()` iterates through all paths/operations
3. For each operation, creates a dynamic FastAPI route with:
   - Path parameters from URL template
   - Query parameters from schema
   - Request body validation (Pydantic)
   - Response model validation (Pydantic)
4. Routes perform CRUD operations on `MockState`
5. Data persists only in memory (resets on restart)

### Real Mode

Real mode proxies requests to an actual Proxmox VE API with full request/response validation.

```
┌───────────────┐
│  User Request │
└───────┬───────┘
        │
        ▼
┌───────────────────┐
│  FastAPI Router   │
└───────┬───────────┘
        │
        ▼
┌────────────────────────────┐
│  Real API Endpoint         │
│  - Validates request       │
│  - Calls ProxmoxClient     │
│  - Validates response      │
└────────┬───────────────────┘
         │
         ▼
┌─────────────────────┐
│  ProxmoxClient      │  (aiohttp)
│  - Authenticates    │
│  - Makes HTTP call  │
│  - Handles errors   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Real Proxmox API   │
│  (8.1 or later)     │
└─────────────────────┘
```

**Key Components:**

- **`proxmox/config.py`** - Configuration loading from environment variables
- **`proxmox/client.py`** - aiohttp-based client with authentication
- **`proxmox/routes.py`** - Route builder that proxies to real API
- **`schema.py`** - Shared schema utilities

**Flow:**

1. App startup loads `ProxmoxConfig` from environment
2. `register_proxmox_routes()` creates endpoints similar to mock mode
3. For each request:
   - Validate request using Pydantic models
   - Call `ProxmoxClient.request()`
   - ProxmoxClient authenticates (API token or username/password)
   - Forward request to real Proxmox API
   - Validate response
   - Return to user
4. All data comes from real Proxmox server

## Code Generation Pipeline

The project includes a sophisticated code generation pipeline that converts the Proxmox VE API into OpenAPI schemas and Pydantic models.

```
┌──────────────────┐
│  Proxmox VE API  │
│  /api2/json/...  │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│  ProxmoxCrawler      │  (recursive API exploration)
│  - GET /api2/json    │
│  - Follow children   │
│  - Capture metadata  │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  raw_capture.json    │  (646 endpoints)
│  - Paths             │
│  - Methods           │
│  - Parameters        │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  Pipeline            │  (normalization)
│  - Deduplicate       │
│  - Enrich metadata   │
│  - Extract schemas   │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  OpenAPIBuilder      │  (schema generation)
│  - Create paths      │
│  - Build schemas     │
│  - Add security      │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  openapi.json        │  (5.2MB OpenAPI 3.1)
│  - 646 operations    │
│  - 428 paths         │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  PydanticBuilder     │  (model generation)
│  - Parse schemas     │
│  - Generate classes  │
│  - Add validators    │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  pydantic_models.py  │  (Python models)
│  - Request models    │
│  - Response models   │
└──────────────────────┘
```

**Key Classes:**

- **`ProxmoxCrawler`** - Recursively explores Proxmox API structure
- **`ProxmoxCodegenPipeline`** - Orchestrates the full pipeline
- **`OpenAPIBuilder`** - Converts normalized data → OpenAPI schema
- **`PydanticBuilder`** - Converts OpenAPI schema → Pydantic models

## Data Flow

### Mock Mode Request Flow

```
User → FastAPI → validate_request() → mock_endpoint()
                                           │
                                           ▼
                                    MockState.get()
                                           │
                                           ▼
                                    validate_response()
                                           │
                                           ▼
                                    Return JSON
```

### Real Mode Request Flow

```
User → FastAPI → validate_request() → real_endpoint()
                                           │
                                           ▼
                                    ProxmoxClient
                                           │
                                           ▼
                                    auth_headers()
                                           │
                                           ▼
                                    aiohttp.request()
                                           │
                                           ▼
                                    Proxmox VE API
                                           │
                                           ▼
                                    validate_response()
                                           │
                                           ▼
                                    Return JSON
```

## Key Design Decisions

### 1. Dual-Mode Architecture

**Why?**

- Development teams need mock APIs for testing without real infrastructure
- Production deployments need validated proxies to real Proxmox servers
- Single codebase reduces maintenance burden

**Trade-offs:**

- ✅ Maximum flexibility for different use cases
- ✅ Same API surface in both modes
- ❌ More complex startup logic
- ❌ Two code paths to maintain

### 2. Dynamic Route Generation

**Why?**

Instead of hardcoding 646 routes, we generate them from OpenAPI schema at runtime.

**Benefits:**

- Schema updates automatically create new routes
- No manual route maintenance
- Guaranteed schema/implementation consistency
- Smaller codebase

**Trade-offs:**

- ✅ Extremely maintainable
- ✅ Easy to update to new Proxmox versions
- ❌ Slightly slower startup time (~1s)
- ❌ More complex debugging

### 3. Pre-Generated Schemas

**Why?**

We ship pre-generated OpenAPI schemas instead of requiring live Proxmox access.

**Benefits:**

- Users can run mock mode without any Proxmox server
- Faster startup (no crawling needed)
- Offline development support
- Version pinning for reproducibility

**Trade-offs:**

- ✅ Zero dependencies for mock mode
- ✅ Works completely offline
- ❌ Schema updates require regeneration
- ❌ Larger repository size (~5MB per version)

### 4. Full Request/Response Validation

**Why?**

Every request and response passes through Pydantic validation.

**Benefits:**

- Type safety for client applications
- Early error detection
- Self-documenting API via schemas
- Swagger UI with accurate models

**Trade-offs:**

- ✅ Production-quality reliability
- ✅ Better developer experience
- ❌ Small performance overhead
- ❌ Stricter than raw Proxmox API

### 5. In-Memory Mock State

**Why?**

Mock mode uses a simple dict-based state instead of a database.

**Benefits:**

- Zero dependencies (no database needed)
- Fast CRUD operations
- Simple testing
- Easy to reset state

**Trade-offs:**

- ✅ Extremely simple and fast
- ✅ Perfect for testing/development
- ❌ Data lost on restart
- ❌ Not suitable for persistent mock environments

### 6. aiohttp for Real Mode

**Why?**

We chose aiohttp over httpx or requests.

**Benefits:**

- Async/await native (matches FastAPI)
- Battle-tested and mature
- Excellent session/connection pooling
- Good SSL/TLS handling

**Trade-offs:**

- ✅ High performance
- ✅ Native async integration
- ❌ More complex than synchronous clients
- ❌ Requires async context management

## Performance Characteristics

### Mock Mode

- **Startup:** ~1 second (schema loading + route generation)
- **Request latency:** <5ms (in-memory operations)
- **Memory usage:** ~100MB (schema + state)
- **Throughput:** 10,000+ req/s (limited by FastAPI)

### Real Mode

- **Startup:** ~500ms (config loading + client setup)
- **Request latency:** Proxmox latency + validation (~20-100ms overhead)
- **Memory usage:** ~80MB (schema + client session)
- **Throughput:** Limited by Proxmox server capacity

## Security Model

### Mock Mode

- **No authentication** by default (safe for development)
- Can add custom auth middleware if needed
- Intended for trusted development environments only

### Real Mode

- **API Token authentication** (recommended)
- **Username/Password authentication** (fallback)
- SSL/TLS verification (configurable)
- All auth handled by `ProxmoxClient`
- No credential storage in memory after initial auth

## Extension Points

The architecture is designed for easy extension:

1. **Custom Mock Data Loaders**
   - Implement `load_custom_mock_data()`
   - Support new file formats (currently JSON/YAML)

2. **Custom Route Middleware**
   - Add FastAPI middleware for auth, logging, etc.
   - Works with both mock and real modes

3. **New API Versions**
   - Run codegen pipeline with new Proxmox version
   - Store in `generated/proxmox/<version>/`
   - Switch via version parameter

4. **Alternative Backends**
   - Implement new mode (e.g., "database mode")
   - Register routes conditionally in `main.py`

## Testing Strategy

### Unit Tests

- `test_schema.py` - Schema loading and validation
- `test_mock_routes.py` - Individual CRUD operations
- `test_proxmox_client.py` - Client auth and requests (mocked)

### Integration Tests

- `test_main_app.py` - Full app startup in both modes
- `test_custom_mock_data.py` - Data loading from files

### End-to-End Tests

- Manual testing via Swagger UI
- Real Proxmox environment testing for real mode

## Future Architecture Considerations

Potential improvements for future versions:

1. **Database-Backed Mock Mode**
   - SQLite or PostgreSQL for persistent mock data
   - Would enable multi-user testing scenarios

2. **Caching Layer**
   - Cache frequently-accessed Proxmox resources
   - Reduce load on real Proxmox API

3. **WebSocket Support**
   - Real-time updates for task status
   - Event streaming for cluster changes

4. **Plugin System**
   - Allow custom endpoint extensions
   - Third-party Proxmox integrations

5. **GraphQL Layer**
   - Alternative query interface
   - More flexible client queries

## Conclusion

The Proxmox OpenAPI architecture balances:

- **Flexibility** - Mock and real modes for different use cases
- **Simplicity** - Minimal dependencies, straightforward code
- **Maintainability** - Schema-driven, auto-generated routes
- **Reliability** - Full validation, type safety, error handling

This design enables rapid development, comprehensive testing, and production-ready Proxmox API integration.
