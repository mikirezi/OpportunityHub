# OpportunityHub — Remote Opportunity Finder

## 🔗 Quick Access

**GitHub Repository:**  
https://github.com/mikirezi/OpportunityHub

**Live Deployed Website:**  
https://rebate-railroad-health-webmasters.trycloudflare.com

**Demo Video:**  
https://youtu.be/x71WiAD8DvA

---

## 📌 Project Overview

OpportunityHub is a web application that helps users find remote job opportunities through the Himalayas Jobs API.

Users can search for opportunities using keywords and filter results by employment type and seniority level. The application displays relevant job information and provides links to apply for available positions.

The project was built as part of the **Playing Around with APIs** assignment.

---

## ✨ Features

- Search remote job opportunities by keyword
- Filter jobs by employment type
- Filter jobs by seniority level
- Sort job results
- Display job title, company, location, salary and other relevant information
- Provide application links
- Handle API errors and unavailable results
- Responsive and simple user interface

---

## 🛠️ Technologies Used

- **Python**
- **Flask**
- **HTML**
- **CSS**
- **JavaScript**
- **Requests**
- **Himalayas Jobs API**
- **Nginx**
- **Docker**
- **Cloudflare Tunnel**

---

## 🔌 API Used

OpportunityHub uses the **Himalayas Jobs API** to retrieve remote job opportunities.

The application sends requests to the Himalayas job search endpoint and uses the returned information to display job opportunities to users.

API documentation:  
https://himalayas.app/api

The API key is stored securely in an environment variable and is not included in the repository.

---

## 🏗️ Deployment Architecture

The application is deployed using two web servers behind a dedicated load balancer.

```text
User
  |
  v
Cloudflare Tunnel
  |
  v
Load Balancer (Lb01)
  |
  +-------------------+
  |                   |
  v                   v
Web01               Web02
  |                   |
  +---------+---------+
            |
            v
        Flask App
            |
            v
     Himalayas API
```

The load balancer distributes requests between Web01 and Web02, allowing users to access the application through a single endpoint.

---

## 💻 Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/mikirezi/OpportunityHub.git
cd OpportunityHub
```

### 2. Create and activate a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure the API key

Create a `.env` file inside the `backend` folder:

```text
HIMALAYS_API_KEY=your_api_key_here
```

Do not commit the `.env` file to GitHub.

### 5. Start the Flask application

```bash
cd backend
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

---

## 🚀 Deployment

The application was deployed across:

- **Web01** — Flask application behind Nginx
- **Web02** — Flask application behind Nginx
- **Lb01** — Nginx load balancer

The load balancer forwards incoming requests to the two web servers.

The deployed application is exposed publicly using a Cloudflare Quick Tunnel.

**Live application:**  
https://rebate-railroad-health-webmasters.trycloudflare.com

---

## 🧪 Testing

The application was tested at different stages of deployment:

1. Flask application tested locally.
2. Web01 tested through Nginx.
3. Web02 tested through Nginx.
4. Load balancer tested through Lb01.
5. API requests tested through the load balancer.
6. Public access tested through the Cloudflare tunnel.

The `/api/jobs` endpoint successfully returns job data from the Himalayas API through the deployed architecture.

---

## ⚠️ Challenges and Solutions

### API Authentication

The application required authentication when communicating with the Himalayas API.

**Solution:**  
The API key was stored in a `.env` file and loaded using environment variables instead of placing the key directly in the source code.

### Running Flask on the Web Servers

The application needed to run independently on both Web01 and Web02.

**Solution:**  
The Flask application was installed and configured on both servers, with Nginx forwarding incoming HTTP requests to the Flask application.

### Load Balancer Configuration

Requests needed to reach both web servers through one endpoint.

**Solution:**  
Nginx was configured on Lb01 with an upstream containing Web01 and Web02.

### Public Deployment

The load balancer was initially accessible only through the local machine.

**Solution:**  
A Cloudflare Quick Tunnel was used to expose the load balancer's HTTP endpoint through a public HTTPS URL.

---

## 🎥 Demo Video

The demonstration video shows the OpportunityHub application and its deployed functionality.

https://youtu.be/x71WiAD8DvA

---

## 📚 Resources and Attribution

- **Himalayas Jobs API:** https://himalayas.app/
- **Flask:** https://flask.palletsprojects.com/
- **Nginx:** https://nginx.org/
- **Cloudflare:** https://www.cloudflare.com/

Job information displayed by OpportunityHub is provided by the Himalayas Jobs API.

---

## 👤 Repository

GitHub:  
https://github.com/mikirezi/OpportunityHub
