# UPF Bank App Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [User Stories](#user-stories)
5. [Tasks](#tasks)
6. [Azure Infrastructure](#azure-infrastructure)
7. [Terraform Scripts](#terraform-scripts)
8. [Application Code](#application-code)
9. [Deployment Process](#deployment-process)
10. [Testing](#testing)
11. [Documentation](#documentation)
12. [CI/CD Pipeline](#cicd-pipeline)
13. [Docker Containerization](#docker-containerization)
14. [Azure Functions](#azure-functions)
15. [CI/CD and Docker Considerations](#cicd-and-docker-considerations)
16. [Conclusion and Acknowledgments](#conclusion-and-acknowledgments)

## 1. Introduction

### Overview
UPF Bank is a modern banking application designed to provide users with a seamless and secure banking experience. This documentation outlines the technology stack, project structure, user stories, tasks, and deployment steps for UPF Bank.

## 2. Technology Stack

### Tools and Technologies
1. **Frontend:**
   - Framework: CSS
   - Language: HTML, Jinja2 (for templating)

2. **Backend:**
   - Framework: Flask
   - Language: Python
   - Database: Azure sql database

## 3. Project Structure

### Directory Structure
1. **Root Directory:**
   - `app.py`: Main application file.
   - `.venv`: Virtual environment directory.
   - `static`: Directory for static assets.
   - `templates`: HTML templates.
   - `UPFBANK`: Additional application files.

## 4. User Stories

### Epic
The Epic involves creating a robust banking application with features such as user authentication, dashboard, fund transfer, loan application, and transaction history.

### Features
1. **User Authentication:**
   - **Description:** Implement user registration and login functionality.
   - **Acceptance Criteria:** Users can sign up, log in, and reset their password.

2. **Dashboard:**
   - **Description:** Create a user dashboard displaying account information.
   - **Acceptance Criteria:** Users see their account balance, recent transactions,apply loan, upload kyc.

3. **Fund Transfer**
   - **Description:** user transfers fund from one account to another.


   ![Utasks list](docs/s2.png)![Utasks list](docs/s3.png)![Utasks list](docs/s4.png)

## 5. Tasks

### Task List
1. **User Registration Task:**
   - **Task:** Implement registration form.

2. **User Login Task:**
   - **Task:** Implement login form.

   Here are my tasks listed in boards.

   ![Utasks list](docs/s1.png)


## 6. Azure Infrastructure

   ## Step 1: Create a Virtual Machine

   1. Click "Create a resource."
   2. In the left navigation pane, click on "Virtual machines."
   3. Click on "+ Add" to create a new virtual machine.
   4. Fill in the required details, including VM name, OS disk, and authentication.
   5. Choose the appropriate size and configure other settings.
   6. Click "Review + create" and then "Create."

       ![Utasks list](docs/v1.png)

   ## Step 2: Connect to the Virtual Machine

   1. Once the VM is created, go to the VM's overview page.
   2. Click on "Connect" to get connection details.
   3. Use your preferred method (SSH for Linux or RDP file)

       ![Utasks list](docs/v2.png)

### Azure Resources
1. **Azure SQL Database:**
- **Description:** Set up Azure SQL Database for storing user data.

   #### Step 1: Create a New SQL Database
   1. Click on the resource created
   2. Search for "SQL Database" and select it.
   3. Fill in basic details: database name, server, and configure server settings.

   #### Step 3: Configure and Create
   1. Set up server details (create a new server or use an existing one).
   2. Configure networking and additional settings.
   3. Choose pricing tier and review configurations.
   4. Click "Create" for deployment.

   #### Step 4: Access and Manage
   1. Monitor deployment progress in Azure Portal.
   2. Once deployed, access the database.
   3. Use tools like Azure Data Studio for database management.
      - **Configuration:** Connection string, firewall rules.

   This is the db and server i have created

     ![Utasks list](docs/s5.png) 

- **Connection String:** Driver={ODBC Driver 17 for SQL Server};Server=tcp:fractalbankserver.database.windows.net,1433;Database=upfdb;Uid=bindu;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
   
   #### Step 5: Connecting to ODBC sever
   1. Download ODBC server 17 for azure.
   2. Open ODBC data source and add the server.
   3. authenticate server and test source.
      
      ![Utasks list](docs/s6.png)
      ![Utasks list](docs/s12.png)
      ![Utasks list](docs/s13.png)


### Step 2: Blob Storage

**Step 2.1: Create Blob Storage Account**
1. Navigate to the Azure Portal.
2. Click on the resource which is created and search for "Storage Account."
3. Provide necessary details: account name, replication, and other settings.
4. Click "Review + Create" and then "Create" to deploy.
      
      ![Utasks list](docs/s7.png)

**Step 2.2: Access and Use**
1. Access the Blob Storage account.
2. Create containers and upload blobs using Azure Portal or tools like Azure Storage Explorer.
3. Using this container we can connect this container to store KYC forms.

      ![Utasks list](docs/s8.png)

### Step 3: Function Apps

**Step 3.1: Create a Function App**

Because of the free trail we cant deploy function app these are the steps how we can create and deploy

1. In Azure Portal, click on the resource which is created and search for "Function App."
2. Fill in details: app name, runtime stack, region, and storage account.
3. Click "Review + Create" and then "Create" to deploy.

      ![Utasks list](docs/s9.png)

**Step 3.2: Develop and Deploy Functions**
1. Access the Function App.
2. Create functions using supported languages (JavaScript, C#, Python, etc.).
3. Deploy functions and configure triggers

### Step 4: Docker Containerization

**Step 4.1: Dockerize Your Application**
1. Create a Dockerfile in your project directory.
2. Define the image, dependencies, and build steps.
3. Build the Docker image using `docker build -t UPF_BANK_APP .`

     ![Utasks list](docs/d1.png)

**Step 4.2: Run Docker Container Locally**
1. Use `docker run -p 8008:80 UPF_BANK_APP` to run the container locally.
2. Access your application at `http://localhost:8008`.

### Step 5: Deploying Flask Application to Azure Web App with Docker

**Step 5.1: Azure Web App Setup**
1. In the Azure Portal, click "Create a resource" and search for "Web App."
2. Provide details like app name, subscription, resource group, and runtime stack.
3. Configure additional settings and deploy the Web App.

     ![Utasks list](docs/w1.png)

**Step 5.2: Configure Docker Container Settings**
1. Navigate to the created Web App in the Azure Portal.
2. In the left menu, go to "Settings" > "Docker settings."
3. Configure Docker Container settings, including the Docker Hub or Azure Container Registry image source.

**Step 5.3: Deploy Dockerized Flask Application**
1. Build your Docker image locally using `docker build -t UPF_BANK_APP .`
2. Tag the image with the Web App URL: `docker tag UPF_BANK_APP <web-app-url>/UPF_BANK_APP:v1`
3. Push the Docker image to Azure Container Registry or Docker Hub: `docker push <web-app-url>/UPF_BANK_APP:v1`
4. In the Azure Portal, navigate to the Web App, go to "Container settings," and update the image source.
5. Azure Web App will pull and deploy the Dockerized Flask application.

**Step 5.4: Access the Deployed Application**
1. Once deployment is complete, access your Flask application at the Web App URL.
2. Monitor logs and performance in the Azure Portal.

## 6. Terraform Scripts

### Infrastructure as Code
1. I have included main.tf in my folderr

## 7. Application Code

### Frontend and Backend
1. **Frontend Code Overview:**
   - **Description:** HTML templates, Bulma CSS styling.

2. **Backend Code Overview:**
   - **Description:** Flask routes, user authentication logic.

## 9. Deployment Process

### Deployment Steps
1. **Local Deployment:**
   - **Step 1:** Install dependencies (`pip install -r requirements.txt`).
   - **Step 2:** Configure environment variables (`.env` file).

2. **Azure Deployment:**
   - **Step 1:** Run Terraform scripts (`terraform apply`).
   - **Step 2:** Deploy application code (`git push` to Azure Web App).

### Integration Considerations
1. **CI/CD Integration with Docker:**

   Because of the free trail and environment issues ci/cd can't be performed but these are the steps and pictures some pictures are taken from internet 

   ## Step 1: Create a New Project

   1. Go to [Azure DevOps](https://dev.azure.com/) and log in.
   2. Click on "New Project" to create a new project.

      ![Utasks list](docs/s11.png)

   ## Step 2: Set Up Your Repository

   1. Navigate to your project.
   2. Click on "Repos" in the left sidebar.
   3. Create a new Git repository or link to an existing one.

      ![Utasks list](docs/p1.jpg)

   ## Step 3: Create a New Pipeline

   1. In your project, click on "Pipelines" in the left sidebar.
   2. Click on "New pipeline."
   3. Azure DevOps will prompt you to select the source of your code. Choose the repository you set up in the previous step.

      ![Utasks list](docs/p2.jpg)

   ## Step 4: Choose a Template

   1. Select a pipeline template that fits your project (e.g., ASP.NET, Node.js, Python).
   2. Azure DevOps will generate a YAML file for your pipeline.

      ![Utasks list](docs/p3.jpg)

   ## Step 5: Configure Build Pipeline

   1. Review and edit the auto-generated YAML file if needed.
   2. Click "Save and run" to trigger a manual build.

      ![Utasks list](docs/p4.jpg)

   ## Step 6: Monitor Build Progress

   1. Once the build is initiated, you can monitor the progress on the "Runs" page.
   2. Verify that the build completes successfully.

      ![Utasks list](docs/p5.jpg)

## 11. Documentation

 **README file:**
- **Description:** Project overview, setup instructions.

## 16. Conclusion and Acknowledgments

### Final Thoughts
1. **Project Conclusion:**
   - **Description:** Reflect on the project and its achievements.

2. **Acknowledgments:**
   - **Description:** Thank You.
