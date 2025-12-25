# Architecture and Design Reasoning

## Overview
This application follows a **decoupled microservices-oriented architecture**, separating the entry-point gateway from the core AI reasoning engine. This ensures scalability, security, and clear separation of concerns.

## 1. Backend Gateway (Ruby on Rails)
The Rails application acts as a secure buffer between the client and the AI service.

### Design Decisions:
- **API-Only Mode**: Minimal footprint, optimized for JSON responses.
- **Service Layer (`AiServiceClient`)**: Instead of putting logic in the controller, we used a service object to handle external communication. This follows the **Single Responsibility Principle**.
- **Shopify Authentication**: Using the standard `shopify_app` pattern ensures session security and easy transition to production-ready OAuth.

## 2. Python AI Service (FastAPI)
The Python service houses the "Agentic" logic. Python was chosen for its superior LLM library ecosystem (LangChain, Google Generative AI).

### Agent Flow Reasoning:
1. **Intent Interpretation**: Before querying data, the agent classifies the user's intent. This prevents unnecessary API calls and narrow down the table selection (sales, inventory, customers).
2. **ShopifyQL over GraphQL**: ShopifyQL is specialized for analytics. It allows for high-level aggregations (e.g., `total_sales BY product_title`) which are much simpler to generate than complex GraphQL fragments for the same data.
3. **Double-Pass LLM Strategy**: 
   - *Pass 1*: Translate natural language to query.
   - *Pass 2*: Translate raw data to human-friendly insight.
   - This "Chain of Thought" approach ensures the technical output is valid and the final answer is business-relevant.

## 3. Query Validation Layer
A dedicated validation step ensures the generated ShopifyQL conforms to expected patterns before execution, preventing accidental data leaks or malformed queries.

## 4. Scalability & Caching
The architecture is designed to support:
- **Caching**: Shopify responses can be cached in Redis at the Gateway level.
- **Async Processing**: For long-running analytical queries, the Gateway can return a task ID and use WebSockets/Polling for the result.
