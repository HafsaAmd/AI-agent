import os
from openai import OpenAI
from models import Product
from flask import current_app

class AIController:
    def __init__(self):
        # getting API key from Flask config first, then environment
        try:
            api_key = current_app.config.get('OPENAI_API_KEY') or os.environ.get("OPENAI_API_KEY")
        except RuntimeError:
            # If no app context, fall back to environment variable
            api_key = os.environ.get("OPENAI_API_KEY")
            
        if api_key:
            self.client = OpenAI(api_key=api_key)
            self.api_available = True
        else:
            self.client = None
            self.api_available = False

    def get_product_recommendations(self, user_query):
        print(f"DEBUG: API available: {self.api_available}")
        
        if not self.api_available:
            return "The OpenAI API is not configured. Please set the OPENAI_API_KEY environment variable to use AI recommendations."
        
        try:
            # Get available products
            products = Product.objects()
            product_list = "\n".join([f"- {p.name}: {p.description} (${p.price})" for p in products])
            print(f"DEBUG: Found {len(products)} products")

            system_prompt = """You are a friendly and helpful AI assistant for a product management system. You can:
1. **Recommend products as a top priorit task** - When users ask about products, shopping, or need recommendations
2. **Answer general questions** - Have normal conversations, provide information, help with various topics
3. **Be conversational** - Feel free to chat naturally and be engaging

You have access to these products in the inventory:
{product_list}

Guidelines:
- If the user asks about products, recommendations, shopping, or mentions needing something specific, provide relevant product suggestions from the inventory
- For general questions (greetings, how are you, general knowledge, etc.), respond naturally without forcing product recommendations
- Be helpful, friendly, and conversational
- You can mix general conversation with product suggestions when appropriate
- If you don't have relevant products for a specific request, suggest alternatives or ask clarifying questions""".format(product_list=product_list)

            user_prompt = f"User message: {user_query}"

            print("DEBUG: Calling OpenAI API...")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=400,
                temperature=0.7  
            )
            print("DEBUG: OpenAI API call successful")
            return response.choices[0].message.content
        except Exception as e:
            print(f"DEBUG: Error occurred: {str(e)}")
            print(f"DEBUG: Error type: {type(e).__name__}")
            return f"Sorry, I encountered an error while processing your request: {e}"