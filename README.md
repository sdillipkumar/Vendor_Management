# 🚀 Vendor Management System with Performance Metrics (VMS)
A modern, full-featured Vendor Management System (VMS) built with **Django**, **Tailwind CSS**, and **PostgreSQL**, designed to streamline vendor interactions, performance tracking, purchase orders, and ratings with a sleek, responsive UI.


## 🚀 Features

- 🔐 **Role-Based Access Control** (Admin & Vendor)
- 📦 **Vendor Profiles** – Add, edit, and manage vendors
- 📝 **Purchase Orders** – Track and update order statuses
- 📊 **Performance Metrics** – Vendor rating and analytics
- 🎨 **Modern UI** – Tailwind CSS + animations + glossy dark sidebar
- 📈 **Dashboard Charts** – Visual performance with Chart.js
- 🔍 **Responsive Design** – Fully mobile-friendly

---

## 📸 Homepage Preview

![Homepage Slider](static/images/home_slider_preview.png)

Includes:
- 🎞️ Full-width **image slider**
- 🖱️ Animated **"Go to Dashboard"** CTA button over images

---

## 🛠️ Tech Stack

| Technology        | Usage                           |
|------------------|--------------------------------  |
| 🐍 Django         | Backend & Template Engine       |
| 🌐 Django REST Framework | API layer                |
| 🎨 Tailwind CSS   | UI Styling & Responsiveness     |
| 🗃️ PostgreSQL     | Database                        |
| 📊 Chart.js       | Performance Graphs              |
| ✅ Pytest         | Unit Testing                    |

---

## 📁 Project Structure

vendor_mgmt_project/
├── vendors/               # Vendor app
├── purchase_orders/       # Purchase order management
├── historical/            # Historical performance tracking
├── static/                # CSS, JS, Images
├── templates/             # HTML Templates with Tailwind
├── dashboard/             # Dashboard views and charts
├── manage.py
├── requirements.txt
└── README.md

##⚙️ Setup Instructions

1.Clone the repository:

git clone https://github.com/your-username/vendor-mgmt-system.git
cd vendor-mgmt-system

2.Create virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3.Apply migrations & run the server:

python manage.py migrate
python manage.py runserver

4.Create a superuser for admin login:

python manage.py createsuperuser
![index 1](https://github.com/user-attachments/assets/5d428f25-a51a-4031-a7d6-753ce588176a)

![Dashboard](https://github.com/user-attachments/assets/2394b4d0-58be-46cb-beb1-31d87e9a142f)

![vendor_list](https://github.com/user-attachments/assets/3e53e876-2014-4a72-a4f2-9443ece10052)

