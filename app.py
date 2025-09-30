from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("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")

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://faadhils.github.io"],  # In production, replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class GroceryItem(BaseModel):
    id: Optional[str] = None
    name: str
    quantity: Optional[str] = "1"
    completed: bool = False

class Reminder(BaseModel):
    id: Optional[str] = None
    title: str
    date: str
    time: str
    completed: bool = False

class RideBooking(BaseModel):
    pickup: str
    destination: str
    service: str  # "uber" or "pickme"
    time: Optional[str] = None

# In-memory storage (replace with database in production)
grocery_items = []
reminders = []
bookings = []

# AI Helper function
def get_ai_suggestion(prompt: str) -> str:
    """Get suggestions from GPT"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful household assistant for an elderly person. Be concise and friendly."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI suggestion unavailable: {str(e)}"

# Grocery Endpoints
@app.get("/api/groceries")
async def get_groceries():
    return {"items": grocery_items}

@app.post("/api/groceries")
async def add_grocery(item: GroceryItem):
    item.id = str(len(grocery_items) + 1)
    grocery_items.append(item.dict())
    return {"message": "Item added", "item": item}

@app.delete("/api/groceries/{item_id}")
async def delete_grocery(item_id: str):
    global grocery_items
    grocery_items = [item for item in grocery_items if item.get("id") != item_id]
    return {"message": "Item deleted"}

@app.post("/api/groceries/suggest")
async def suggest_groceries():
    """Get AI suggestions for groceries"""
    current_items = [item["name"] for item in grocery_items]
    prompt = f"Based on these grocery items: {', '.join(current_items)}, suggest 3 more essential items an elderly person might need. Return only the item names, separated by commas."
    
    suggestion = get_ai_suggestion(prompt)
    suggested_items = [item.strip() for item in suggestion.split(",")]
    
    return {"suggestions": suggested_items}

@app.post("/api/groceries/analyze")
async def analyze_groceries():
    """Analyze grocery list for completeness"""
    current_items = [item["name"] for item in grocery_items]
    prompt = f"Analyze this grocery list for an elderly person: {', '.join(current_items)}. What essential items might be missing? Keep response under 50 words."
    
    analysis = get_ai_suggestion(prompt)
    return {"analysis": analysis}

# Reminder Endpoints
@app.get("/api/reminders")
async def get_reminders():
    return {"reminders": reminders}

@app.post("/api/reminders")
async def add_reminder(reminder: Reminder):
    reminder.id = str(len(reminders) + 1)
    reminders.append(reminder.dict())
    return {"message": "Reminder added", "reminder": reminder}

@app.delete("/api/reminders/{reminder_id}")
async def delete_reminder(reminder_id: str):
    global reminders
    reminders = [r for r in reminders if r.get("id") != reminder_id]
    return {"message": "Reminder deleted"}

# Ride Booking Endpoints
@app.post("/api/rides/book")
async def book_ride(booking: RideBooking):
    booking_dict = booking.dict()
    booking_dict["id"] = str(len(bookings) + 1)
    booking_dict["status"] = "confirmed"
    booking_dict["booking_time"] = datetime.now().isoformat()
    bookings.append(booking_dict)
    
    # In real app, integrate with Uber/PickMe API here
    return {
        "message": f"Ride booked with {booking.service}",
        "booking": booking_dict,
        "estimated_arrival": "10-15 minutes"
    }

@app.get("/api/rides/recent")
async def get_recent_rides():
    return {"bookings": bookings[-5:]}  # Last 5 bookings

# Dashboard Stats
@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    return {
        "monthly_savings": 125.50,
        "tasks_completed": len([i for i in grocery_items if i.get("completed", False)]),
        "upcoming_tasks": len(reminders),
        "recent_activity": [
            {"type": "grocery", "description": "Grocery order placed", "time": "15 minutes ago"},
            {"type": "ride", "description": "PickMe ride scheduled", "time": "2 hours ago"},
            {"type": "reminder", "description": "Reminder set for laundry", "time": "Yesterday"}
        ]
    }

# Chat endpoint for natural language commands
@app.post("/api/chat")
async def chat(message: dict):
    user_message = message.get("message", "")
    
    # Process with GPT to understand intent
    prompt = f"""
    User said: "{user_message}"
    
    Determine if this is about:
    1. Groceries (adding items, ordering)
    2. Rides (booking transportation)
    3. Reminders (setting reminders)
    4. General conversation
    
    Respond naturally and suggest the appropriate action.
    """
    
    response = get_ai_suggestion(prompt)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
