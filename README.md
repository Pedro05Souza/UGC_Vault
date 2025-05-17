<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#project-dependencies">Project Dependencies</a></li>
    <li><a href="#running-the-bot">Running the Bot</a></li>
  </ol>
</details>

## 🔧 Setting Up Project Dependencies

Follow the steps below to set up the project and get it running.

### 1️⃣ Setting Up a Virtual Environment  

To install dependencies, you must first clone the repo onto a directory of your choice. After proceed with the following terminal command:

```bash
python -m venv venv
```

This will create a virtual python enviroment necessary for installing the dependancies.

### 2️⃣ Activate the Virtual Environment

### Windows

  ```bash
  venv/Scripts/activate
 ```

Note: If you encounter a permission issue, execute the following command in PowerShell:

  ```bash
 Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser 
 ```

### macOS/Linux

  ```bash
source venv/bin/activate
 ```

### 📦 Installing Dependencies

 After activating the virtual environment, install the necessary dependencies with:

  ```bash
pip install -r requirements.txt
 ```

## Running the Bot


1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop.).

2. After installation, confirm Docker is correctly set up by running the following command in your terminal:

```powershell
docker --version
```

3. Start the containers:

```powershell
docker compose up
```
