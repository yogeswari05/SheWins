"""
Free AI chat service using Groq API."""
from __future__ import annotations

import json
from typing import Any, Dict, Optional

import httpx

from app.config import get_settings


class FreeAIChatService:
    """Free AI chat service using Groq API."""
    
    def __init__(self):
        settings = get_settings()
        self.groq_api_key = settings.groq_api_key
    
    async def chat(self, message: str, language: str = "en") -> Optional[Dict[str, Any]]:
        """Main chat function using Groq API."""
        
        # Use Groq for all chat requests
        groq_response = await self._groq_chat(message, language)
        if groq_response:
            return groq_response
        
        # Local fallback if Groq fails
        return self._local_fallback_response(message, language)
    
    async def _groq_chat(self, message: str, language: str) -> Optional[Dict[str, Any]]:
        """Chat using Groq API (Llama models, very fast)."""
        if not self.groq_api_key:
            return None
            
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        # Use Groq's fast Llama model
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system", 
                    "content": self._get_health_system_prompt(language)
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            "max_tokens": 200,
            "temperature": 0.7
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30.0
            )
            
                                    
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, dict) and "choices" in result:
                    generated_text = result["choices"][0]["message"]["content"]
                    
                    return {
                        "response": generated_text.strip(),
                        "source": "groq",
                        "model": "llama-3.1-8b-instant"
                    }
        
        return None
    
    def _get_health_system_prompt(self, language: str) -> str:
        """Get health-focused system prompt for AI."""
        if language == "en":
            return """You are a supportive AI assistant for EliteHer, a menstrual health tracking app for girls and women. 
            Be conversational, friendly, and encouraging while providing helpful information about menstrual health, cycle tracking, stress management, and wellness.
            
            Guidelines:
            - Be warm and supportive like a knowledgeable friend
            - Provide practical tips for menstrual health management
            - Offer encouragement for tracking cycles and symptoms
            - Share stress management techniques and lifestyle advice
            - Answer questions about periods, cramps, mood swings, nutrition, exercise, and sleep
            - Be understanding about irregular cycles and PCOD concerns
            - Suggest when to consult healthcare providers for specific medical issues
            - Keep responses positive and empowering
            - Adapt responses based on user's specific questions and needs
            
            Remember: You're supporting their menstrual health journey with helpful, personalized guidance while being clear about not being a medical professional."""
        else:
            return "मैं सासिक स्वास्थ्य का समर्थन करती है। 7-9 घंटे की नींद, नियमित मध्यम व्यायाम, फलों और सब्जियों से भरपूर संतुलित आहार, और तनाव प्रबंधन का लक्ष्य रखें।"
    
    def _get_period_response(self, message: str, language: str) -> str:
        """Get period-related responses."""
        if language == "en":
            # Check what specific period question they're asking
            message_lower = message.lower()
            
            if any(word in message_lower for word in ["when", "start", "date", "late", "early"]):
                return "For tracking your period, I recommend starting with the first day of your last period. If your cycles are irregular, don't worry - this is common! Try to note symptoms, flow intensity, and any patterns you notice. How long has it been since your last period?"
            
            elif any(word in message_lower for word in ["cramps", "pain", "headache", "bloating"]):
                return "I'm sorry you're experiencing cramps or pain! For relief, try a warm compress on your lower abdomen, gentle exercise like walking, or over-the-counter pain relievers if appropriate for you. Stay hydrated and rest when needed. Have you tried tracking what helps your cramps?"
            
            elif any(word in message_lower for word in ["flow", "heavy", "light"]):
                return "Flow intensity varies for everyone! Light flow typically lasts 4-7 days, while heavy flow can be 7+ days. Both are normal variations. What's your typical flow pattern like? This helps me understand your cycle better."
            
            elif any(word in message_lower for word in ["track", "help", "how"]):
                return "Great question about tracking! I'd suggest logging: start date, end date, flow intensity (light/medium/heavy), symptoms (cramps, mood changes, bloating), and notes about stress or sleep. Consistent tracking helps you predict your next period and understand your body's patterns."
            
            else:
                return "I'm here to help with your menstrual cycle questions! Whether you're asking about tracking, symptoms, or just need support, I'm ready to assist. What would you like to know about periods or cycle tracking?"
        else:
            return "मैं सासिक स्वास्थ्य का समर्थन करती है। 7-9 घंटे की नींद, नियमित मध्यम व्यायाम, फलों और सब्जियों से भरपूर संतुलित आहार, और तनाव प्रबंधन का लक्ष्य रखें।"
    
    def _get_stress_response(self, message: str, language: str) -> str:
        """Get stress-related responses."""
        if language == "en":
            return "Stress management is important for menstrual health! Try deep breathing exercises, regular exercise, adequate sleep, and talking about your feelings. Small daily habits can make a big difference in how you handle stress."
        else:
            return "तनाव प्रबंधन का प्रबंधन कर सकता है। नियमित मध्यम व्यायाम, फलों और सब्जियों से भरपूर संतुलित आहार, और तनाव प्रबंधन का लक्ष्य रखें।"
    
    def _get_pcod_response(self, message: str, language: str) -> str:
        """Get PCOD-related responses."""
        if language == "en":
            return "PCOD management requires a holistic approach! Focus on balanced nutrition, regular exercise, stress management, and medical guidance. Consider consulting with a healthcare provider for personalized treatment options."
        else:
            return "PCOD का प्रबंधन करने के लिए चिकित्सा आहार। डॉक्टर और नियमित मध्यम व्यायाम, फलों और सब्जियों से भरपूर संतुलित आहार, और तनाव प्रबंधन का लक्ष्य रखें।"
    
    def _get_lifestyle_response(self, message: str, language: str) -> str:
        """Get lifestyle-related responses."""
        if language == "en":
            return "A healthy lifestyle supports menstrual health! Aim for 7-9 hours of sleep, regular moderate exercise, a balanced diet rich in fruits and vegetables, and stress management. Stay hydrated and limit processed foods. Small, consistent changes can make a big difference in how you feel."
        else:
            return "स्वास्थ्य जीवनशैली मासिक स्वास्थ्य का समर्थन करती है। 7-9 घंटे की नींद, नियमित मध्यम व्यायाम, फलों और सब्जियों से भरपूर संतुलित आहार, और तनाव प्रबंधन का लक्ष्य रखें।"
    
    def _get_general_health_response(self, message: str, language: str) -> str:
        """Get general health responses."""
        if language == "en":
            return "I'm here to support your menstrual health journey! I can help track cycles, provide wellness tips, share stress management techniques, and offer information about menstrual health topics. While I'm not a medical professional, I'm trained to provide helpful guidance on period tracking, symptom management, and lifestyle wellness. What specific aspect of menstrual health would you like help with today?"
        else:
            return "मैं सासिक स्वास्थ्य का समर्थन करती है। 7-9 घंटे की नींद, नियमित मध्यम व्यायाम, फलों और सब्जियों से भरपूर संतुलित आहार, और तनाव प्रबंधन का लक्ष्य रखें। जबकि मैं सामान्य जानकारी और समर्थन प्रदान करना चाहते, मैं चिकित्सा आहार। जबकि मैं सामान्य जानकारी और समर्थन प्रदान करना चाहते, मैं चिकित्सा आहार।"
    
    def _local_fallback_response(self, message: str, language: str) -> Dict[str, Any]:
        """Local fallback responses when API is unavailable."""
        
        message_lower = message.lower()
        
        # Health-related responses
        if any(word in message_lower for word in ["period", "menstrual", "cycle"]):
            response = self._get_period_response(message_lower, language)
        elif any(word in message_lower for word in ["stress", "anxiety", "mood"]):
            response = self._get_stress_response(message_lower, language)
        elif any(word in message_lower for word in ["pcod", "pcos", "symptom"]):
            response = self._get_pcod_response(message_lower, language)
        elif any(word in message_lower for word in ["exercise", "diet", "lifestyle"]):
            response = self._get_lifestyle_response(message_lower, language)
        else:
            response = self._get_general_health_response(message_lower, language)
        
        return {
            "response": response,
            "source": "local_fallback",
            "model": "rule_based"
        }


# Global service instance
free_ai_chat_service = FreeAIChatService()
