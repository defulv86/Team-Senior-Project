# **Team Senior Project**
---
This repository contains the code and resources for the **Philadelphia Pointing Span Test (PPST)** application, developed as part of our Senior Project. Follow the steps below to ensure proper installation and functionality.

---

## **Installation Instructions**

### **1. Clone the Repository**
Clone the repository to your local machine:
```bash
git clone https://github.com/defulv86/Team-Senior-Project.git
```

Navigate to the project directory:
```bash
cd Team-Senior-Project/ppst
```

---

### **2. Set Up a Virtual Environment**
Create and activate a virtual environment for dependency management.

#### **macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### **Windows:**
```bash
py -m venv venv
source venv\Scripts\activate
```

---

### **3. Install Required Dependencies**
Install Django and other dependencies using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

---

### **4. Apply Database Migrations**

#### **For Real Data (Regular Fixture):**
- **Windows:**
  ```bash
  py migrate_regular_fixture.py
  ```
- **macOS/Linux:**
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  python manage.py shell < regular_fixture.py
  ```

#### **For Fake Data:**
- **Windows:**
  ```bash
  py migrate_fake_test_data_fixture.py
  ```
- **macOS/Linux:**
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  python manage.py shell < fake_data_fixture.py
  ```

---

### **5. Update Admin Dashboard File**
To ensure proper functioning of the admin dashboard, make the following change:

1. Open the file:  
   ```
   venv/Lib/django/contrib/admin/templates/admin/base.html
   ```
2. Locate **line 48** and replace the line with:
   ```html
   Back to Admin Dashboard /
   ```
3. Save the file.

---

### **6. Run the Project**
Start the Django development server:

#### **Windows:**
```bash
py manage.py runserver
```

#### **macOS/Linux:**
```bash
python manage.py runserver
```

---

### **7. Access the Application**
Visit the application in your browser:
```
http://127.0.0.1:8000/
```

---

## **Notes**
- Ensure that your virtual environment is activated before running the project.
- Make sure to select the correct fixture (real or fake data) based on your testing needs.
