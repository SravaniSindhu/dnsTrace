# 🌐 Domain Intelligence Tool

## 📌 Overview

This project is a **DNSTrace** that allows users to analyze any domain name and retrieve important network and security-related information.

By providing a domain name as input, the tool will:

* 🔍 Fetch DNS records (A, MX, NS, etc.)
* 🔐 Retrieve SSL/TLS certificate details
* 🌍 Perform a traceroute to the domain

This can be useful for:

* Security analysis
* Network debugging
* Learning how domains and internet routing work

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

---

### 2️⃣ Create Virtual Environment

#### On Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

Run the main script:

```bash
python run.py
```

---

## 🧪 Example

```bash
Enter domain: google.com
```

### Output may include:

* DNS Records (A, MX, NS, etc..)
* SSL Certificate Info
* Traceroute path

---

## 🛠️ Requirements

Make sure you have:

* Python 3.8+
* pip installed


---

## 📌 Future Improvements

* Export results to JSON/CSV
* Add WHOIS lookup

---

