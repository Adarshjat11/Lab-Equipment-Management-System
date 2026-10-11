# 🧪 Lab Equipment Management System

A full-stack academic inventory and equipment tracking platform built to manage institutional resources, process real student data, and streamline lab operations in a live college deployment[cite: 1].

---

## 🚀 Features

- **Role-Based Access Control (RBAC):** Secure portal separation for **Students** and **Admins** with integrated enrollment verification[cite: 1].
- **Real-Time Inventory Tracking:** Live dashboards to monitor equipment availability, status, and usage analytics[cite: 1].
- **Automated Notifications:** Integrated **Gmail SMTP** for sending automated status alerts and system emails[cite: 1].
- **Data Processing & Analytics:** Built using high-performance Python libraries for seamless tabular record handling and Excel processing[cite: 1].

---

## 🛠️ Tech Stack

- **Core Language:** Python[cite: 1]
- **Web Framework:** Streamlit[cite: 1]
- **Data Manipulation & Export:** Pandas, OpenPyXL[cite: 1]
- **Communication:** Gmail SMTP[cite: 1]

---

## 📂 Project Structure

```text
Lab-Equipment-Scheduler/
│
├── app.py              # Main Streamlit application and UI entry point
├── requirements.txt    # Project dependencies
├── utils/              # Helper modules (Auth, Database, SMTP)
└── assets/             # Static files and images

```

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
```bash
git clone [https://github.com/Adarshjat11/Lab-Equipment-Scheduler.git](https://github.com/Adarshjat11/Lab-Equipment-Scheduler.git)
cd Lab-Equipment-Scheduler

```


2. **Create a virtual environment (Recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Configure Environment Variables:**
Create a `.env` file in the root directory and add your configuration details (such as Gmail SMTP credentials for notifications):
```env
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

```


5. **Run the Application:**
```bash
streamlit run app.py

```



---

## 💡 Usage

* **Students:** Log in with institutional credentials to request equipment, track approval statuses, and view active bookings.
* **Admins:** Oversee user registrations, review equipment requests via the admin dashboard, and manage inventory logs.

---

## 👤 Author

**Adarsh Jat**

* GitHub: [@Adarshjat11](https://www.google.com/search?q=https://github.com/Adarshjat11)
* Email: adarshjat3011@gmail.com



```

```
