# Shopify AI Analytics

A mini AI-powered analytics application that connects to Shopify, translates natural language into ShopifyQL, and provides business insights.

## Architecture

1.  **Backend Gateway (Node.js/Express)**: 
    - Handles authentication (mocked) and API requests.
    - Endpoints: `POST /api/v1/questions`.
2.  **AI Service (Python/FastAPI)**:
    - **Agent Logic**: Interprets intent, plans data retrieval.
    - **ShopifyQL Generator**: Uses LLM (Gemini) to build queries.
    - **Shopify Client**: Mocks interactions with Shopify API for this demo.
    - **Insight Generator**: Converts raw data into human-friendly explanations.

## Setup Instructions

### Pre-requisites
- Node.js
- Python 3.10+

### 1. Backend Gateway (Ruby on Rails)
```bash
cd backend_gateway
bundle install
rails s -p 3000
```

### 2. AI Service
```bash
cd ai_service
pip install -r requirements.txt
python -m main
```

## Sample API Requests

### POST `/api/v1/questions`

**Request Body:**
```json
{
  "store_id": "example-store.myshopify.com",
  "question": "How much inventory should I reorder for next week?"
}
```

**Response Body:**
```json
{
  "answer": "Based on the last 30 days, you sell around 10 units per day. You should reorder at least 70 units of 'Awesome Hoodie' to avoid stockouts next week.",
  "confidence": "medium"
}
```

## Agent Flow
1. **Interpret**: User asks "Top 5 selling products".
2. **Plan**: Agent decides it needs data from the `sales` table.
3. **Generate**: Agent builds `SHOW total_sales BY product_title FROM sales DURING last_week LIMIT 5`.
4. **Execute**: Shopify Client fetch raw data.
5. **Explain**: Agent converts `[{"product_title": "T-Shirt", "total_sales": 500}, ...]` into "Your top selling product was T-Shirt...".
