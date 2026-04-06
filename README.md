# VulnX Web — Intelligent Web Vulnerability Scanner Platform

## Overview
VulnX Web is a production-grade web-based vulnerability scanner platform. It provides automated security testing, real-time scanning progress tracking, and detailed report generation capabilities, packaged in a premium, dark-themed dashboard.

```text
 __  __     __  __     __         __   __     __  __    
/\ \/\ \   /\ \/\ \   /\ \       /\ "-.\ \   /\_\_\_\   
\ \ \_\ \  \ \ \_\ \  \ \ \____  \ \ \-.  \  \/_/\_\/_  
 \ \_____\  \ \_____\  \ \_____\  \ \_\\"\_\   /\_\/\_\ 
  \/_____/   \/_____/   \/_____/   \/_/ \/_/   \/_/\/_/ 
```

## Features
- **User Authentication:** Secure access control.
- **Scanner Engine:** Custom web crawler and payload injector for SQL Injection and XSS vulnerabilities.
- **Real-Time Feed:** Live AJAX polling displaying URLs discovered, payloads sent, and active vulnerability detections.
- **Reporting:** Export vulnerabilities in JSON or standalone HTML format.
- **Multi-threaded Execution:** Configure scan depth and the number of concurrent scanning threads.

## Technology Stack
- **Backend:** Django (Python), Django REST Framework
- **Frontend:** Django Templates, HTML, Vanilla CSS with Neon Aesthetics
- **Database:** SQLite
- **Execution Engine:** Async Threading

## Setup Instructions

1. **Activate the Virtual Environment**
   ```powershell
   .\venv\Scripts\activate
   ```

2. **Install Dependencies**
   (These are already installed if using the provided environment)
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the Server**
   ```powershell
   python manage.py runserver
   ```

4. **Initialize Your Operative Account**
   Navigate to `http://localhost:8000/users/register/` and register to access the dashboard.

## Scanner Behavior
- Designed to stay strictly within the chosen initial domain boundary.
- Generates live events visible immediately from your operations dashboard.
- Uses thread pooling for highly parallel injections.
- Does not crash on bad links.

## Disclaimer
This tool should only be used on networks and web servers where you have explicit permission.
