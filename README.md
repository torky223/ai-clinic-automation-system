# AI Clinic Automation System

A production-grade, enterprise automation system designed to fully manage dentist clinics and medical facilities. Operating as an autonomous **Execution Agent**, the system decodes end-user intents from voice and text metadata and fires integrated tool chains (Google Calendar, Supabase, and Gmail APIs) with zero human overhead.

---

## 📊 System Workflow Architecture

```mermaid
graph TD
    Incoming[📥 Incoming Message: Telegram/WhatsApp] --> Router{🧠 Switch Node:<br>Intent Classification}
    
    Router -->|Voice Node| Whisper[🎙️ Whisper API:<br>Audio-to-String]
    Router -->|Text Node| Master[👑 Master AI Agent:<br>Orchestrator]
    
    Whisper --> Master

    Master -->|Execute Action| CalAgent[📅 Calendar Agent:<br>Google Calendar API]
    Master -->|Sync Records| DBAgent[💾 Database Agent:<br>Supabase / PostgreSQL]
    Master -->|Dispatch Alert| MailAgent[✉️ Notification Agent:<br>Gmail SMTP]

    CalAgent --> Final[🏆 Execution Success & User Notified]
    DBAgent --> Final
    MailAgent --> Final
