# PingMe

## PingMe — just ping and talk.

PingMe is a **practice real-time chatting application** built with **Django**, **Django REST Framework (DRF)**, and **WebSockets**.  
The main goal of this project is to explore **real-time communication**, **backend architecture**, and the integration of **REST APIs with WebSocket-based messaging**.

This project is intended for **local development and learning purposes only**.

---

## 🚀 Features

- User authentication (login & signup)
- One-to-one real-time chat
- WebSocket-based instant messaging
- Message history using REST APIs
- Online/offline user status (basic)
- Clean backend architecture for practice

---

## 🛠️ Tech Stack

**Backend**
- Django
- Django REST Framework (DRF)
- Django Channels

**Real-Time Communication**
- WebSockets
- Redis (channel layer)

**Database**
- SQLite (for local development)

**Authentication**
- Django session-based authentication (can be extended to JWT)

---

## 🧠 What This Project Focuses On

- Understanding the difference between **HTTP APIs and WebSockets**
- Using **Django Channels** for real-time features
- Managing chat rooms and message broadcasting
- Structuring a Django project professionally
- Practicing async vs sync operations in Django


---

## 🔄 How It Works

* **REST APIs (DRF)** are used for:

  * Authentication
  * Fetching chat history
  * User-related operations

* **WebSockets (Django Channels)** are used for:

  * Sending and receiving messages instantly
  * Broadcasting messages to chat rooms
  * Handling real-time user presence

---

## ⚙️ Local Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Maruf346/PingMe.git
cd pingme
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Redis (Required for WebSockets)

Make sure Redis is running locally:

```bash
redis-server
```

### 5️⃣ Run Migrations

```bash
python manage.py migrate
```

### 6️⃣ Start the Development Server

```bash
python manage.py runserver
```

---

## 🧪 Testing the App

* REST APIs can be tested using **Postman** or **Thunder Client**
* WebSocket connections can be tested using:

  * Browser dev tools
  * WebSocket testing tools
  * Simple frontend or JS client

---

## 📌 Future Improvements (Optional)

* Group chat support
* Read receipts
* Typing indicators
* JWT authentication
* File and image sharing
* Frontend integration (React / Flutter)

---

## ⚠️ Note

This is a **practice project** created to improve backend development skills.
It is not intended for production use.

---

## 👤 Author

**Maruf Hossain**   
Department of CSE    
Green University of Bangladesh     
📧 mail: [maruf.bshs@gmail.com](mailto:maruf.bshs@gmail.com)     

