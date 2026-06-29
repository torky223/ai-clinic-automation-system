# نظام أتمتة العيادات الذكي القائم على وكلاء الذكاء الاصطناعي (AI Clinic Automation System)

نظام متكامل (Enterprise Automation System) مصمم لإدارة وأتمتة عيادات الأسنان والمؤسسات الطبية بشكل كامل. يمثل النظام الجيل الحديث من الأنظمة الذكية حيث يعمل كـ **Execution Agent** يتخذ القرارات وينفذ العمليات (حجز، تعديل، تسجيل، إرسال) بناءً على المدخلات الصوتية والنصية للمستخدم دون أي تدخل بشري.

---

## 📊 مخطط تدفق العمليات (System Workflow Architecture)

```mermaid
graph TD
    %% تعريف الألوان والتنسيقات لـ Dark Mode
    classDef inputNode fill:#218838,stroke:#28a745,stroke-width:2px,color:#fff;
    classDef processNode fill:#17a2b8,stroke:#117a8b,stroke-width:2px,color:#fff;
    classDef agentNode fill:#6f42c1,stroke:#8a59e3,stroke-width:2px,color:#fff;
    classDef dbNode fill:#fd7e14,stroke:#f85a1b,stroke-width:2px,color:#fff;

    %% تدفق الداتا عبر المراحل الأربعة
    Incoming[📥 Incoming Message: Telegram/WhatsApp] :::inputNode --> Router{🧠 Switch Node:<br>Intent Classification}
    
    %% تفريع بناء على نوع الداتا
    Router -->|Audio/Voice| Whisper[🎙️ Whisper API:<br>Audio-to-String] :::processNode
    Router -->|Text| Master[👑 Master AI Agent:<br>Orchestrator] :::agentNode
    
    Whisper --> Master

    %% استدعاء الأدوات والوكلاء الفرعيين
    Master -->|Execute Action| CalAgent[📅 Calendar Agent:<br>Google Calendar API] :::agentNode
    Master -->|Sync Records| DBAgent[💾 Database Agent:<br>Supabase / PostgreSQL] :::dbNode
    Master -->|Dispatch Alert| MailAgent[✉️ Notification Agent:<br>Gmail SMTP] :::agentNode

    %% المخرجات النهائية
    CalAgent --> Final[🏆 Execution Success & User Notified] :::inputNode
    DBAgent --> Final
    MailAgent --> Final
iption.
