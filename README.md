# OpportunityHub — Remote Opportunity Finder

## 🔗 Quick Access

**GitHub Repository:**  
https://github.com/mikirezi/OpportunityHub

**Live Deployed Website (Load Balancer Lb01):**  
http://18.171.165.187

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
- **Gunicorn**
- **HTML**
- **CSS**
- **JavaScript**
- **Requests**
- **Himalayas Jobs API**
- **Nginx** (on Web01 and Web02)
- **HAProxy** (on Lb01)
- **systemd** (keeps the Flask app running)

---

## 🔌 API Used

OpportunityHub uses the **Himalayas Jobs API** to retrieve remote job opportunities.

The application sends requests to the Himalayas job search endpoint and uses the returned information to display job opportunities to users.

API documentation:  
https://himalayas.app/api

The API key is stored in a `.env` file as an environment variable and is not included in the repository.

---

## 🏗️ Deployment Architecture

The application is deployed on three servers: two web servers behind a dedicated load balancer.

```text
Public Internet
       |
       v
Load Balancer (Lb01)  -  HAProxy, round-robin
       |
  +----+--------------+
  |                   |
  v                   v
Web01               Web02
Nginx -> Flask      Nginx -> Flask
  |                   |
  +---------+---------+
            |
            v
      Himalayas API
```

| Server | Role | Public IP |
|--------|------|-----------|
| Web01 | Web server (Nginx + Flask/Gunicorn) | 13.135.254.60 |
| Web02 | Web server (Nginx + Flask/Gunicorn) | 13.40.178.57 |
| Lb01  | Load balancer (HAProxy) | 18.171.165.187 |

Users access the application through the Lb01 address. HAProxy distributes requests between Web01 and Web02 using round-robin, with health checks on both servers. Each web server adds an `X-Served-By` header with its hostname, which makes it possible to verify that requests alternate between the two servers.

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

## 🚀 Deployment Instructions

These steps were used on **both** Web01 and Web02 (Ubuntu 20.04, Python 3.8).

### 1. Install tools and download the code

```bash
sudo apt update && sudo apt install -y git python3-venv python3-pip
git clone https://github.com/mikirezi/OpportunityHub.git
cd OpportunityHub/backend
```

### 2. Create the environment and install packages

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask requests python-dotenv gunicorn
```

### 3. Add the API key

Create `backend/.env` on the server (it is not stored in GitHub):

```text
HIMALAYS_API_KEY=your_api_key_here
```

### 4. Run Flask as a service

Create `/etc/systemd/system/opportunityhub.service`:

```ini
[Unit]
Description=OpportunityHub Flask app
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/OpportunityHub/backend
ExecStart=/home/ubuntu/OpportunityHub/backend/venv/bin/gunicorn -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Then start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now opportunityhub
```

The service starts automatically on reboot and restarts if it crashes.

### 5. Configure Nginx to forward requests to Flask

Create `/etc/nginx/opportunityhub.conf`:

```nginx
location = / {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
location = /styles.css {
    proxy_pass http://127.0.0.1:5000;
}
location /api/ {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

Add `include /etc/nginx/opportunityhub.conf;` inside the `server` block of `/etc/nginx/sites-enabled/default`, then:

```bash
sudo nginx -t && sudo systemctl reload nginx
```

### 6. Configure the load balancer (Lb01)

`/etc/haproxy/haproxy.cfg`:

```text
frontend http_front
    bind *:80
    default_backend web_servers

backend web_servers
    balance roundrobin
    server 7340-web-01 13.135.254.60:80 check
    server 7340-web-02 13.40.178.57:80 check
```

---

## 🧪 Testing

The application was tested at different stages of deployment:

1. Flask application tested locally.
2. The app was first rehearsed locally in Docker containers (web-01, web-02, lb-01) before the real deployment.
3. Web01 tested in the browser at its public IP.
4. Web02 tested in the browser at its public IP.
5. Load balancing verified on Lb01: repeated requests returned alternating `X-Served-By` headers (`7340-web-01`, `7340-web-02`).
6. Public access tested from a phone on mobile data using the Lb01 address.

The `/api/jobs` endpoint successfully returns job data from the Himalayas API through the deployed architecture.

---

## ⚠️ Challenges and Solutions

### API Authentication

The application required authentication when communicating with the Himalayas API.

**Solution:**  
The API key is stored in a `.env` file and loaded with environment variables instead of being placed in the source code. Because `.env` is not committed to GitHub, it had to be created manually on each web server. Until it was added, the API returned a 401 error.

### Python Version on the Servers

The servers run Python 3.8, but the pinned versions in `requirements.txt` need a newer Python, so installation failed.

**Solution:**  
The core packages (Flask, Requests, python-dotenv and Gunicorn) were installed without exact version pins, letting pip choose versions compatible with Python 3.8.

### Running Flask Reliably

Flask needed to keep running on both web servers without a terminal open.

**Solution:**  
Flask was run with Gunicorn as a systemd service that starts on boot and restarts on failure, with Nginx forwarding HTTP requests to it.

### Keeping Existing Server Configuration Working

The web servers were already used for other configuration work.

**Solution:**  
The application routes were added through a separate Nginx include file, after making a backup of the original config and testing it with `nginx -t` before reloading.

### Public Deployment

The Docker setup on a local machine was only reachable from that machine, and a temporary tunnel could not be relied on.

**Solution:**  
The application was deployed on real cloud servers with public IP addresses (Web01, Web02 and Lb01), so the site stays available without depending on a personal computer.

---

## 🎥 Demo Video

The demonstration video shows the OpportunityHub application and its deployed functionality.

https://youtu.be/x71WiAD8DvA

---

## 📚 Resources and Attribution

- **Himalayas Jobs API:** https://himalayas.app/
- **Flask:** https://flask.palletsprojects.com/
- **Gunicorn:** https://gunicorn.org/
- **Nginx:** https://nginx.org/
- **HAProxy:** https://www.haproxy.org/

Job information displayed by OpportunityHub is provided by the Himalayas Jobs API.

---

## 👤 Repository

GitHub:  
https://github.com/mikirezi/OpportunityHub
