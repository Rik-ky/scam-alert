# Scam Alert

Scam Alert is a web application built to empower people by helping them report and identify scammers quickly and reliably. It enforces user authentication, email verification, and ensures scam data is accessible only to verified users—making it safer and more trustworthy.

## ✨ Why This App Exists

I created Scam Alert because:

- Too many people fall victim to scammers with no place to report or warn others.
- There is a gap in public awareness and user-driven protection.
- I believe in using technology to help people **see the truth**, protect one another, and **give back** with every gift and skill I have.
- This project is part of my mission to give my all—to leave behind a legacy where my work serves others.

## 🔐 Features

- **User Authentication** – Register, login, and logout functionality.
- **Email Verification** – Users must verify their email before accessing scam reports.
- **Scam Reporting** – Authenticated users can submit scammer names, phone numbers, and descriptions.
- **Scam Reports Viewer** – A table of submitted scam data, visible only to verified users.
- **Session-based Access Control** – Prevents unauthenticated access to reports and reporting.

## 🚀 Tech Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS (Bootstrap)
- **Email Service:** Gmail SMTP
- **Database:** SQLite
- **Authentication:** Secure password hashing, session management

## 🛠 How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/Rik-ky/scam-alert.git
   cd scam-alert
2. python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. pip install -r requirements.txt

4.MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password

5. python init_db.py

6. flask run

💡 Future Ideas

    Add SMS verification

    Geo-tagged scam reports

    Community upvotes/downvotes on reports

    Admin dashboard for moderation

📜 License

This project is open-source and free to use. Use it to protect your community, learn, and give back.
