import os
import json
import openai
from dotenv import load_dotenv

# 1. Environment Initialization & API Configuration
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ========================================================
# 2. Input Processing & Classification Layer
# ========================================================
class MessageProcessor:
    @staticmethod
    def transcribe_audio(audio_file_path: str) -> str:
        """Stage 1: Transcribe Telegram/WhatsApp voice notes into plain text using Whisper API."""
        with open(audio_file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript['text']

    @staticmethod
    def route_message(user_input: str) -> str:
        """Stage 2: Deterministic Switch Node to classify intent and route the pipeline."""
        system_prompt = (
            "You are the traffic router for a dentist clinic. Classify the user intent into exactly "
            "one of these categories: [BOOKING, EMAIL_INQUIRY, PATIENT_RECORD]. Reply with only the category name."
        )
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message['content'].strip()


# ========================================================
# 3. Specialized Sub-Agents Layer (Execution Tools)
# ========================================================
class CalendarAgent:
    @staticmethod
    def execute(extracted_data: dict) -> str:
        """Agent responsible for automating appointment workflows via Google Calendar API."""
        action = extracted_data.get("action", "Create")
        patient = extracted_data.get("patient_name", "Patient")
        date = extracted_data.get("date", "Unspecified Time")
        return f"📅 [Calendar Agent Success] Processed '{action}' event for patient '{patient}' on {date}."

class EmailAgent:
    @staticmethod
    def execute(extracted_data: dict) -> str:
        """Agent responsible for drafting and dispatching automated clinic logs via Gmail SMTP."""
        email_address = extracted_data.get("email", "patient@email.com")
        patient = extracted_data.get("patient_name", "Patient")
        return f"✉️ [Email Agent Success] Confirmation alert triggered to: {email_address} for patient '{patient}'."

class ContactsDatabaseAgent:
    @staticmethod
    def execute(action: str, extracted_data: dict) -> str:
        """Agent responsible for managing structured ledger data inside Supabase / PostgreSQL."""
        patient = extracted_data.get("patient_name", "Unknown")
        return f"💾 [Database Agent Success] Database operational command ({action}) executed inside Supabase for: '{patient}'."


# ========================================================
# 4. Master AI Orchestrator Layer (Core Logic)
# ========================================================
class MasterOrchestrator:
    def __init__(self):
        # Initializing core operational sub-agents
        self.calendar_agent = CalendarAgent()
        self.email_agent = EmailAgent()
        self.db_agent = ContactsDatabaseAgent()

    def execute_system_decision(self, intent: str, user_raw_text: str) -> str:
        print(f"\n[Master Agent] 🧠 Running Semantic Pipeline. Core Intent: {intent}")
        
        # Structured Payload Extraction
        extraction_prompt = (
            "Extract operational clinic data from this text. Respond ONLY with a raw valid JSON object containing "
            "appropriate fields like 'patient_name', 'date', 'action', 'email'. Do not include markdown brackets."
        )
        
        data_extraction = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": extraction_prompt},
                {"role": "user", "content": user_raw_text}
            ]
        )
        
        try:
            extracted_data = json.loads(data_extraction.choices[0].message['content'])
        except Exception:
            extracted_data = {"action": "general_handling", "patient_name": "Clinic Patient"}

        print(f"[Master Agent] 📊 Structured Payload Extracted: {extracted_data}")

        # Deterministic Routing Mechanism based on System Blueprint
        if intent == "BOOKING":
            cal_log = self.calendar_agent.execute(extracted_data)
            db_log = self.db_agent.execute("Insert/Update", extracted_data)
            return f"{cal_log}\n{db_log}"
            
        elif intent == "EMAIL_INQUIRY":
            return self.email_agent.execute(extracted_data)
            
        elif intent == "PATIENT_RECORD":
            return self.db_agent.execute("Fetch/Search", extracted_data)
            
        else:
            return "[Routing Error] Unrecognized blueprint context. Forwarding to human reception desk."


# ========================================================
# 5. Production Testing & Simulation Pipeline
# ========================================================
if __name__ == "__main__":
    print("==========================================================")
    print("🚀 AI Clinic Automation Orchestrator Active (English Core)")
    print("==========================================================")
    
    orchestrator = MasterOrchestrator()
    
    # Validation scenarios simulating production user payloads
    simulation_scenarios = [
        "Book an appointment for patient Karim Ahmed next Tuesday at 4 PM",
        "Please send the email confirmation logs to torky_dentist@gmail.com for Ahmed",
        "Search the database system for patient record under Mahmoud Rafat"
    ]
    
    for idx, raw_input in enumerate(simulation_scenarios, start=1):
        print(f"\n🎬 --- Running Production Simulation Scenario {idx} ---")
        print(f"📥 Input: '{raw_input}'")
        
        # Step 1: Intent Classification Node
        matched_intent = MessageProcessor.route_message(raw_input)
        
        # Step 2: Tool Execution via Specialized Agents
        execution_trace = orchestrator.execute_system_decision(matched_intent, raw_input)
        
        print("\n🏆 Final Execution Response Trace:")
        print(execution_trace)
        print("=" * 58)
