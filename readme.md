👉 text-converter-pro
(customized based on your idea: *text conversion system using user credits via API token*)

---

# 🚀 Text Converter Pro

A powerful **API-based text conversion platform** where users can convert text formats using **credits**. Each API request consumes credits, making it ideal for SaaS-style usage, monetization, and developer integrations.

---

## 📌 Features

* 🔐 **User Authentication (Token-based)**
* 💳 **Credit System (Pay-per-use)**
* 🔄 **Text Conversion APIs**
* 📊 **Usage Tracking & Logs**
* ⚡ Fast & Scalable API
* 🛠 Developer-friendly endpoints
* 🧾 Request approval system (Admin controlled)

---

## 🎯 Use Cases

* SaaS text conversion tools
* Developer APIs for automation
* Content formatting services
* AI / NLP preprocessing pipelines

---

## ⚙️ Tech Stack

* Backend: Python (FastAPI)
* Database: SQLite
* Auth: JWT / API Token
* ORM: SQLAlchemy

---

## 🔑 Authentication

All API requests require a **Bearer Token**:

```
Authorization: Bearer YOUR_API_TOKEN
```

---

## 💰 Credit System

* Each user has a **credit balance**
* Every API request **deducts credits**
* Requests can be:

  * `pending`
  * `approved`
  * `rejected`

---

## 🔌 API Endpoints

### 🔹 Convert Text

```
POST /api/converter/convert
```

**Request Body:**

```json
{
  "text": "hello world",
  "type": "uppercase"
}
```

**Response:**

```json
{
  "converted_text": "HELLO WORLD",
  "credits_used": 1
}
```

---

### 🔹 Request Credits

```
POST /api/converter/request-credit
```

```json
{
  "credits_requested": 10
}
```

---

### 🔹 Approve Request (Admin)

```
POST /api/converter/approve-request/{id}
```

---

### 🔹 Check Balance

```
GET /api/user/credits
```

---

## 🔄 Supported Conversions

* lowercase → UPPERCASE
* UPPERCASE → lowercase
* Title Case
* snake_case ↔ camelCase
* Remove extra spaces
* Custom transformations

---

## 🗂 Project Structure

```
text-converter-pro/
│── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── schemas/
│── requirements.txt
│── main.py
```

---

## 🧠 How It Works

1. User registers & gets API token
2. User requests credits
3. Admin approves request
4. User calls API → credits deducted
5. Conversion result returned

---

## 🚀 Installation

```bash
git clone https://github.com/cseshahriar/text-converter-pro.git
cd text-converter-pro

pip install -r requirements.txt
fastapi dev app/main.py or uvicorn app.main:app --reload
```

---

## 🧪 Example (cURL)

```bash
curl -X POST \
  http://127.0.0.1:8000/api/converter/convert \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"hello","type":"uppercase"}'
```

---

## 🔐 Security

* Token-based authentication
* Rate limiting (recommended)
* Credit validation before processing

---

## 📈 Future Improvements

* 💳 Payment gateway integration
* 📊 Dashboard (Admin + User)
* 📦 Subscription plans
* 🤖 AI-based text transformations
* 🌍 Multi-language support

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT License

---

## 👨‍💻 Author

**Shahriar Hosen**
Full Stack Developer (Python, Django, FastAPI)
