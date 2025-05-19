# 🚀 DevConnect Backend

This is the **backend API** for [DevConnect](https://github.com/BimalDevasia/Devconnect_frontend) — a full-stack developer community platform. The backend is built using **FastAPI** with **PostgreSQL** as the database and **JWT** for secure authentication.

---

## 📌 Table of Contents

- [🧠 About the Project](#-about-the-project)
- [✨ Features](#-features)
- [🛠️ Tech Stack](#-tech-stack)
- [⚙️ Installation](#-installation)
- [🚀 Usage](#-usage)
- [📁 Folder Structure](#-folder-structure)
- [📬 Contact](#-contact)

---

## 🧠 About the Project

The backend handles user authentication, post creation, project collaborations, and other core functionalities. It's designed to be scalable, secure, and developer-friendly.

---

## ✨ Features

- 🔐 **JWT-based Authentication** – Secure login and registration  
- 👤 **User Profiles** – Store bios, skills, and social links  
- 📝 **Post Management** – Create, fetch, and delete developer posts  
- 👥 **Group/Project Collaboration** – APIs to manage group-based project collaboration  
- 📦 **Modular & Scalable Structure** – Easy to maintain and extend  

---

## 🛠️ Tech Stack

- **FastAPI** – Web framework  
- **PostgreSQL** – Relational database  
- **SQLAlchemy** – ORM  
- **Pydantic** – Data validation  
- **Uvicorn** – ASGI server  
- **Python Dotenv** – Environment variable management  
- **JWT** – Authentication  

---

## ⚙️ Installation

> ⚠️ Make sure you have Python and PostgreSQL installed. Also create a PostgreSQL database for DevConnect (e.g., `devconnect_db`).

```bash
# Clone the repository
git clone https://github.com/BimalDevasia/devconnect_backend.git
cd devconnect_backend

# Create and activate virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Make sure to configure your environment variables in a `.env` file

# (Optional) Run migrations if using Alembic
# alembic upgrade head

# Start the FastAPI server
uvicorn main:app --reload
