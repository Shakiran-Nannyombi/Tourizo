import os
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from langchain_groq import ChatGroq
from app.models import ChatbotSettings
from langchain_core.messages import SystemMessage, HumanMessage
from app.models.Tour import Tour
from app.models.Destination import Destination
import re

load_dotenv()

chatbot_bp = Blueprint('chatbot', __name__)

def extract_region_or_country(message):
    # Simple regex for 'trips in <region/country>'
    match = re.search(r'trips? in ([A-Za-z ]+)', message, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Add more patterns as needed
    return None

@chatbot_bp.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    settings = ChatbotSettings.get_settings()
    if not settings:
        return jsonify({"response": "Chatbot is not configured. Please contact admin."}), 500

    # Check if user is asking about trips in a region/country
    region = extract_region_or_country(user_message)
    if region:
        # Try to match region/country to destinations or countries in DB
        tours = Tour.query.filter(Tour.is_active == True).all()
        matching_tours = []
        for tour in tours:
            dest = tour.destination.lower()
            if region.lower() in dest:
                matching_tours.append(tour)
            else:
                # Try to match by country if Destination model is used
                dest_obj = Destination.query.filter(Destination.name.ilike(f"%{dest}%")).first()
                if dest_obj and region.lower() in dest_obj.country.lower():
                    matching_tours.append(tour)
        if matching_tours:
            response_text = f"Here are some trips available for {region.title()}:<br>"
            for t in matching_tours[:5]:
                response_text += f"<b>{t.title}</b>: {t.short_description or t.description[:80]+'...'}<br>"
            response_text += "You can view more options and book your trip by logging in to your Tourizo account."
            return jsonify({"response": response_text})
        else:
            return jsonify({"response": f"Sorry, we couldn't find any trips for {region.title()} in our system."})

    # Fallback to LLM for other questions
    system_prompt = (
        "You are the Tourizo assistant. You can answer questions about registration, booking, payments, "
        "policies, and all features of the Tourizo platform. Be concise and helpful."
    )
    llm = ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=0.7,
        max_tokens=131072,
        timeout=10
    )
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]
    try:
        response = llm.invoke(messages)
        return jsonify({"response": response.content})
    except Exception as e:
        # Provide a user-friendly error message
        if 'model' in str(e) and 'does not exist' in str(e):
            msg = "The selected AI model is not available. Please check your settings or contact admin."
        elif 'reasoning_format' in str(e):
            msg = "The selected model does not support advanced reasoning. Please update your settings."
        else:
            msg = "Sorry, the AI service is currently unavailable. Please try again later."
        return jsonify({"response": f"<span style='color:red;'>{msg}</span>"}), 500
