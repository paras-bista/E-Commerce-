
# 🛒 Django E-Commerce Web Application

A fully functional e-commerce web application built with Django. It includes user authentication, product browsing, shopping cart, and admin management.


## 🚀 Features

- ✅ User Signup/Login with authentication
- ✅ Product listing and detail pages
- ✅ Add to Cart / Remove from Cart
- ✅ Order Summary and Checkout logic
- ✅ Admin panel to manage products and orders
- ✅ Static/media file handling
- ✅ Responsive design with Bootstrap

## 📁 Project Structure


ecommerce/
├── authcart/          # Cart and Authentication logic
├── ecommerce/         # Project settings and URLs
├── ecommerce/...      # Django app files (views, models, urls, etc.)
├── templates/         # HTML templates
├── static/            # CSS, JS, images
├── media/             # Uploaded product images
├── db.sqlite3         # SQLite database
├── manage.py


## ⚙️ Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/paras-bista/E-Commerce-.git
cd E-Commerce-


### 2️⃣ Create Virtual Environment

```bash
python -m venv env
# Activate it:
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt


## 🔐 Setup Environment Variables

Create a `.env` file in the root directory and add the following:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
SERVER_EMAIL=your_email@gmail.com
```

**⚠️ DO NOT push `.env` to GitHub!**
Make sure your `.gitignore` includes:


.env


## 🗃️ Apply Migrations

```bash
python manage.py migrate


## 🧪 Create Superuser (Admin Login)

```bash
python manage.py createsuperuser


## ▶️ Run Development Server

```bash
python manage.py runserver


Open your browser:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔑 Admin Panel

Visit:
[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
Login using your superuser credentials.


## 🧑‍💻 Developer

* **Parash Bista**
  GitHub: [@paras-bista](https://github.com/paras-bista)


## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.

