import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from .prompts import SYSTEM_PROMPT, INSIGHT_PROMPT
from .shopify_client import ShopifyClient

app = FastAPI()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "mock_key"))
model = genai.GenerativeModel('gemini-1.5-flash')

class QuestionRequest(BaseModel):
    store_id: str
    question: str
    access_token: str

@app.post("/process")
async def process_question(request: QuestionRequest):
    try:
        # 1. Understand intent & Generate ShopifyQL
        # For the demo, if GEMINI_API_KEY is mock, we provide hardcoded mappings
        if os.getenv("GEMINI_API_KEY") == "mock_key" or not os.getenv("GEMINI_API_KEY"):
            shopify_ql = simulate_query_generation(request.question)
        else:
            chat = model.start_chat(history=[])
            response = chat.send_message(f"{SYSTEM_PROMPT}\n\nQuestion: {request.question}")
            shopify_ql = response.text.strip()

        # 2. Execute Query against Shopify
        client = ShopifyClient(request.store_id, request.access_token)
        raw_data = await client.execute_shopify_ql(shopify_ql)

        # 3. Post-process & Generate Insight
        if os.getenv("GEMINI_API_KEY") == "mock_key" or not os.getenv("GEMINI_API_KEY"):
            final_response = simulate_insight_generation(request.question, raw_data)
        else:
            prompt = INSIGHT_PROMPT.format(question=request.question, data=json.dumps(raw_data))
            response = model.generate_content(prompt)
            final_response = json.loads(response.text.strip())

        return final_response

    except Exception as e:
        print(f"Error in AI Service: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def simulate_query_generation(question: str) -> str:
    q = question.lower()
    if "top" in q and "selling" in q:
        return "SHOW total_sales BY product_title FROM sales DURING last_week LIMIT 5"
    if "inventory" in q or "stock" in q:
        return "SHOW quantity_available BY product_title FROM inventory"
    if "customers" in q:
        return "SHOW orders_count BY first_name, last_name FROM customers"
    return "SHOW total_sales FROM sales DURING last_30_days"

def simulate_insight_generation(question: str, data: any) -> dict:
    # Mimic the sample output in the prompt
    if "inventory" in question.lower() or "reorder" in question.lower():
        return {
            "answer": "Based on the last 30 days, you sell around 10 units per day. You should reorder at least 70 units of 'Awesome Hoodie' to avoid stockouts next week.",
            "confidence": "medium"
        }
    if "top" in question.lower():
        return {
            "answer": "Your top selling product last week was 'Cool T-Shirt' with 500 in total sales, followed by 'Awesome Hoodie'.",
            "confidence": "high"
        }
    return {
        "answer": f"I found some interesting data for your question: {json.dumps(data)}",
        "confidence": "medium"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
