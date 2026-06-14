"""
Free AI chat service using LangChain, RAG (FAISS), and Groq API.
"""
from __future__ import annotations

import os
from typing import Any, Dict, Optional
from pathlib import Path

from app.config import get_settings

try:
    from langchain_groq import ChatGroq
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain.schema import HumanMessage, SystemMessage
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.docstore.document import Document
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False


class FreeAIChatService:
    """Free AI chat service with RAG capabilities."""
    
    def __init__(self):
        settings = get_settings()
        self.groq_api_key = settings.groq_api_key
        self.vectorstore = None
        self.vectorstore_path = Path(__file__).resolve().parent.parent.parent / "models" / "faiss_index"
        
        if LANGCHAIN_AVAILABLE and self.groq_api_key:
            self._init_rag()
            
    def _init_rag(self):
        """Initializes the FAISS vector store."""
        try:
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            if self.vectorstore_path.exists():
                self.vectorstore = FAISS.load_local(
                    folder_path=str(self.vectorstore_path), 
                    embeddings=embeddings, 
                    allow_dangerous_deserialization=True
                )
            else:
                # Create a simple synthetic knowledge base
                kb_text = """
                Menstrual Cycle Basics: A normal menstrual cycle lasts 21 to 35 days, with bleeding lasting 2 to 7 days.
                Irregular periods: Cycles outside the 21-35 day range, missing 3 or more periods in a row, or bleeding much heavier than usual.
                PCOD/PCOS: Polycystic Ovary Syndrome (PCOS) is a hormonal disorder common among women of reproductive age. Symptoms include irregular periods, excess androgen, and polycystic ovaries. Weight management and lifestyle changes are primary treatments.
                Stress and Periods: High stress levels can interfere with the hormones that regulate your cycle, potentially causing missed or late periods.
                Symptom Management: For cramps, apply a heating pad, exercise lightly, or take over-the-counter pain relievers like ibuprofen. 
                Sleep: Aim for 7-9 hours of sleep. Poor sleep can exacerbate premenstrual syndrome (PMS) symptoms.
                Nutrition: A balanced diet rich in iron, calcium, and vitamins can help manage PMS. Avoid excess salt and caffeine if you experience bloating or breast tenderness.
                """
                docs = [Document(page_content=kb_text)]
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
                splits = text_splitter.split_documents(docs)
                self.vectorstore = FAISS.from_documents(splits, embeddings)
                self.vectorstore_path.parent.mkdir(exist_ok=True)
                self.vectorstore.save_local(str(self.vectorstore_path))
        except Exception as e:
            print(f"RAG initialization failed: {e}")
            self.vectorstore = None

    async def chat(self, message: str, language: str = "en") -> Optional[Dict[str, Any]]:
        """Main chat function using LangChain RAG + Groq."""
        if LANGCHAIN_AVAILABLE and self.groq_api_key:
            try:
                # Retrieve relevant context
                context = ""
                if self.vectorstore:
                    docs = self.vectorstore.similarity_search(message, k=2)
                    context = "\n".join([d.page_content for d in docs])
                
                llm = ChatGroq(
                    temperature=0.7, 
                    groq_api_key=self.groq_api_key, 
                    model_name="llama-3.1-8b-instant"
                )
                
                system_prompt = self._get_health_system_prompt(language, context)
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=message)
                ]
                
                response = llm.invoke(messages)
                return {
                    "response": response.content.strip(),
                    "source": "groq_rag",
                    "model": "llama-3.1-8b-instant"
                }
            except Exception as e:
                print(f"Groq API error: {e}")
                
        # Local fallback
        return self._local_fallback_response(message, language)
    
    def _get_health_system_prompt(self, language: str, context: str) -> str:
        """Get health-focused system prompt augmented with retrieved context."""
        if language == "en":
            base = "You are a supportive AI health assistant for EliteHer. Answer the user's question empathetically and accurately."
            if context:
                base += f"\n\nUse the following medical knowledge to ground your answer:\n{context}"
            base += "\n\nAlways clarify you are an AI, not a doctor."
            return base
        else:
            return "मैं सासिक स्वास्थ्य का समर्थन करती है। हमेशा स्पष्ट करें कि आप डॉक्टर नहीं हैं।"
            
    def _local_fallback_response(self, message: str, language: str) -> Dict[str, Any]:
        """Local fallback responses when API is unavailable."""
        return {
            "response": "I'm currently operating in offline mode. Please ensure your API keys are configured correctly or try again later.",
            "source": "local_fallback",
            "model": "rule_based"
        }

# Global service instance
free_ai_chat_service = FreeAIChatService()

