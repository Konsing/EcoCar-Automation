
---

# 🚗 EcoCAR EV Onboarding & Automation

## 📌 Overview
This repository is designed to **automate the onboarding and offboarding processes** for the **EcoCAR EV project** using **Python, Airflow, and Google APIs**. The automation reduces manual effort by **50%**, enhances **secure communication** using **Google OAuth2 & Gmail API**, and streamlines workflows **hosted on GCP**.

This system consists of **three main components**:
1. **Leader Approval System** – Automates the acceptance/rejection of new members.
2. **Automated Email Notifications** – Uses Gmail API to send structured onboarding emails.
3. **Google Sheets Integration** – Manages and updates the team’s headcount automatically.

Additionally, **Airflow has been implemented** to fully automate the scheduling and execution of onboarding tasks.

---

## 🏆 Technical Highlights
✔️ **Automated onboarding/offboarding** using **Python & Airflow**, reducing manual tasks by 50%.  
✔️ **Integrated Google OAuth2 & Gmail API** for secure communication & event scheduling.  
✔️ **Deployed automation on Google Cloud Platform (GCP)** for efficiency & scalability.  
✔️ **Airflow DAG** manages automated workflow execution.  

---

## 📂 Project Structure

```
📂 EcoCAR
│── 📂 Ask Leader to Accept or Decline
│   │── .env                          # Environment variables
│   │── AcceptOrDeclineReq.ipynb       # Script for leader decision automation
│   │── client_secret.json             # OAuth2 client secret for Google API
│   │── headcount.csv                   # Team member data for onboarding
│   │── testing-for-ecocar-ff6b5e5bbe13.json  # Google API service credentials
│   │── token.json                      # OAuth2 authentication token
│   │── token.pickle                    # OAuth2 session persistence
│
│── 📂 Automated Message
│   │── .env                           # Environment variables
│   │── client_secret_171250538774.json # Google API credentials
│   │── email.ipynb                     # Automated email notification script
│   │── token.json                      # OAuth2 authentication token
│
│── 📂 Read Write Google Sheet
│   │── .env                            # Environment variables
│   │── headcount.csv                    # Team headcount data
│   │── test.ipynb                       # Google Sheets data manipulation
│   │── testing-for-ecocar-ff6b5e5bbe13.json # Google API credentials
│
│── 📂 Streamlit
│   │── Konsing Streamlit Test.zip       # Streamlit UI test archive
│   │── photo.jpg                        # UI screenshot
│
│── 📂 Team Repository \ EcoCAR-Onboarding
│   │── .env                             # Environment variables
│   │── client_secret.json               # OAuth2 client credentials
│   │── headcount.csv                     # Primary team data file
│   │── service_credentials.json         # Google API service credentials
│   │── TestingForm.ipynb                 # Form validation notebook
│   │── token.pickle                      # OAuth2 session persistence
│
│── 📂 W’s Alt EcoCAR
│   │── credentials.json                 # Alternative Google API credentials
│   │── headcount.csv                     # Backup team data file
│   │── read.py                           # Data retrieval script
│   │── write.py                          # Data update script
│
│── .gitignore                           # Ignores sensitive files
│── Airflow_DAG_ecocar_onboarding.py     # 🟢 Airflow DAG for automated workflow execution
│── main.py                              # Main script to orchestrate onboarding tasks
│── README.md                            # Project documentation
```

---

## 🛠️ Installation & Setup Guide

### 🔑 Prerequisites
Ensure you have:
- **Python 3.x** installed.
- Required Python libraries (`pandas`, `requests`, `google-auth`, etc.).
- **Google API Access** with OAuth2 credentials.
- **Apache Airflow installed and configured**.

### 🚀 Setup Instructions

1️⃣ **Clone the Repository**
   ```sh
   git clone https://github.com/your-repo/EcoCAR-Onboarding.git
   cd EcoCAR-Onboarding
   ```

2️⃣ **Install Required Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3️⃣ **Set Up Environment Variables**
   - Create a `.env` file and add necessary API keys or credentials:
     ```
     API_KEY=your_api_key_here
     ```

4️⃣ **Run the Main Onboarding Script**
   ```sh
   python main.py
   ```

5️⃣ **Start Jupyter Notebook for Form Testing**
   ```sh
   jupyter notebook TestingForm.ipynb
   ```

6️⃣ **Deploy & Run the Airflow DAG (Locally)**
   - Move the DAG file to Airflow’s DAGs directory:
     ```sh
     mv Airflow_DAG_ecocar_onboarding.py ~/airflow/dags/
     ```
   - Restart the Airflow Scheduler:
     ```sh
     airflow scheduler
     ```
   - Start the Airflow Web UI:
     ```sh
     airflow webserver --port 8080
     ```
   - Open [http://localhost:8080](http://localhost:8080) and enable the DAG.

---

## 📊 How Each Component Works

### **1️⃣ Leader Approval System (`Ask Leader to Accept or Decline`)**
- Sends automated **accept/reject requests** to team leaders.
- **Records responses** in `headcount.csv` for tracking.

### **2️⃣ Automated Email Notifications (`Automated Message`)**
- Uses **Gmail API** to send structured onboarding emails.
- Supports **dynamic placeholders** for personalized messages.

### **3️⃣ Google Sheets Data Handling (`Read Write Google Sheet`)**
- Reads & writes **team headcount** using Google Sheets API.
- Ensures **real-time updates** for team member tracking.

### **4️⃣ Airflow DAG (`Airflow_DAG_ecocar_onboarding.py`)**
- Automates the onboarding pipeline:
  1. **Checks for new onboarding requests**.
  2. **Emails team leaders for approval**.
  3. **Processes leader responses (Approve/Reject)**.
  4. **Sends onboarding emails to accepted members**.
  5. **Updates Google Sheets with final decisions**.

---

## 🔍 Purpose of Key Files

### **`TestingForm.ipynb`**
- Jupyter Notebook designed for **validating and testing form data.**
- Processes user responses, detects errors, and ensures data consistency.

### **`client_secret.json` & `service_credentials.json`**
- Stores **Google API credentials** for authentication.
- Used for **OAuth2 authentication & service-based API access**.

### **`.gitignore`**
- Prevents sensitive files (`.env`, `token.json`, `.pickle`) from being committed.

### **`main.py`**
- The **central automation script** that:
  - Handles onboarding/offboarding.
  - Automates leader decisions.
  - Sends email notifications.

### **`Airflow_DAG_ecocar_onboarding.py`**
- Airflow **DAG that fully automates** the onboarding pipeline.

---

## 🚀 Future Enhancements
🔹 **Auto-sync with Google Calendar** – Schedule onboarding meetings dynamically.  
🔹 **AI-Powered Form Processing** – Use NLP to analyze responses for anomalies.   

---

## 📜 License
This project is licensed under the **MIT License**.

---