# Python Template Service

A production-ready FastAPI microservice template that demonstrates modern Python backend development practices, AWS cloud integration, and containerized deployment strategies. This project serves as a comprehensive example of building scalable, maintainable microservices with industry-standard tools and patterns.

## 🎯 Project Overview

This project is a **full-stack microservice template** designed to showcase best practices in modern Python backend development. It demonstrates how to build, test, and deploy a production-ready API service with the following key capabilities:

### What This Project Demonstrates

**🏗️ Architecture & Design Patterns**
- **Clean Architecture**: Separation of concerns with controllers, services, and interfaces
- **Dependency Injection**: Using FastAPI's dependency system for testability and maintainability
- **Interface-based Design**: Abstract interfaces for easy mocking and testing
- **Lifecycle Management**: Proper resource initialization and cleanup with FastAPI lifespan events

**☁️ AWS Cloud Integration**
- **DynamoDB**: NoSQL database integration with table creation and data modeling
- **S3**: File storage with presigned URL generation for secure file uploads
- **boto3**: Professional AWS SDK usage with proper configuration and error handling

**🔧 Modern Python Development**
- **FastAPI**: High-performance async web framework with automatic API documentation
- **Type Safety**: Full type hints with Pydantic for runtime validation
- **Modern Tooling**: `uv` for fast dependency management and project setup
- **Code Quality**: Pre-commit hooks, linting, and testing infrastructure

**🚀 DevOps & Deployment**
- **Multi-Environment Support**: Development, staging, and production configurations
- **Docker**: Containerized deployment with Docker Compose
- **Kubernetes**: Complete K8s manifests for both local (Minikube) and cloud (EKS) deployments
- **CI/CD Ready**: Structured for easy integration with CI/CD pipelines

**📊 Real-World Features**
- Health check endpoints for monitoring and load balancer integration
- Environment-based configuration management
- Structured logging and error handling
- Database migrations and fixture management
- Comprehensive testing setup

### Perfect For

- **Interview Demonstrations**: Showcase your ability to build production-ready services
- **Learning Modern Python**: Learn best practices for FastAPI and AWS integration
- **Project Templates**: Use as a starting point for new microservice projects
- **Portfolio Projects**: Demonstrate full-stack backend development skills

### Key Technologies

- **Python 3.12+** - Latest Python features and performance improvements
- **FastAPI** - Modern, fast web framework for building APIs
- **AWS Services** - DynamoDB, S3, and boto3 SDK
- **Docker & Kubernetes** - Container orchestration and deployment
- **uv** - Next-generation Python package manager
- **Pydantic** - Data validation using Python type annotations

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Usage](#-usage)
  - [Running the Service](#running-the-service)
  - [Database Setup](#database-setup)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
  - [Docker](#docker)
  - [Kubernetes (Minikube)](#kubernetes-minikube)
  - [Kubernetes (EKS)](#kubernetes-eks)
- [License](#-license)

## 🚀 Features

- **Environment-specific configuration** - Support for development, staging, and production environments
- **FastAPI integration** - Modern, fast web framework for building APIs
- **AWS boto3 integration** - Ready-to-use AWS services (DynamoDB, S3)
- **Docker support** - Containerized deployment with Docker Compose
- **Kubernetes ready** - Deployment configurations for Minikube and EKS
- **Modern Python tooling** - Uses `uv` for fast dependency management
- **Type safety** - Built with type hints and Pydantic for validation

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python** >= 3.12
- **uv** - Modern Python package manager ([Installation guide](https://github.com/astral-sh/uv))
- **Docker** (optional) - For containerized deployment
- **kubectl** (optional) - For Kubernetes deployment
- **AWS CLI** (optional) - For AWS service configuration

## ⚡ Quick Start

```bash
# 1. Install dependencies
uv sync

# 2. Activate virtual environment (optional, uv run handles this automatically)
# Bash/Zsh:
source .venv/bin/activate
# PowerShell:
.venv\Scripts\Activate.ps1

# 3. Configure your environment (see Configuration section)
# Edit config/secrets/secret-python-template-service.env

# 4. Run the service
# Using uv run (recommended, cross-platform):
env ENVIRONMENT=development uv run fastapi dev src/main.py

# Or with activated venv:
ENVIRONMENT=development fastapi dev src/main.py
```

The service will be available at `http://localhost:8000` with API documentation at `http://localhost:8000/docs`.

## 🔧 Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd python-template-service
```

### Step 2: Install Dependencies

```bash
uv sync
```

This command will:
- Create a virtual environment (`.venv`)
- Install all project dependencies
- Install development dependencies

### Step 3: Activate Virtual Environment (Optional)

While `uv run` automatically uses the virtual environment, you can manually activate it:

**Bash/Zsh:**
```bash
source .venv/bin/activate
```

**PowerShell (Windows):**
```powershell
.venv\Scripts\Activate.ps1
```

If you encounter execution policy restrictions in PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```

**Fish Shell:**
```fish
# Fish shell users should use uv run instead of manual activation
```

## ⚙️ Configuration

The service uses environment-specific configuration files that are automatically loaded based on the `ENVIRONMENT` variable.

### Configuration Files

#### Environment-Specific Configs
Located in `config/env/`:
- `python-template-service.development.env` - Development settings
- `python-template-service.staging.env` - Staging settings
- `python-template-service.production.env` - Production settings

These files typically contain:
```env
DEBUG=True
API_VERSION=1.0
```

#### Secrets File
Located in `config/secrets/secret-python-template-service.env`:
```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
```

**⚠️ Important:** 
- The secrets file should **never** be committed to version control
- Add `config/secrets/` to your `.gitignore`
- Use environment variables or secret management tools in production

### How Configuration Works

The service automatically loads configuration in this order:
1. Environment-specific config file (`config/env/python-template-service.{ENVIRONMENT}.env`)
2. Secrets file (`config/secrets/secret-python-template-service.env`)
3. Environment variables (highest priority)

Set the `ENVIRONMENT` variable to switch between configurations:
```bash
ENVIRONMENT=development  # Uses development config
ENVIRONMENT=staging     # Uses staging config
ENVIRONMENT=production  # Uses production config
```

## 📁 Project Structure

```
python-template-service/
├── config/
│   ├── env/                          # Environment-specific configs
│   │   ├── python-template-service.development.env
│   │   ├── python-template-service.staging.env
│   │   └── python-template-service.production.env
│   └── secrets/                      # Secrets (not in version control)
│       └── secret-python-template-service.env
├── deployment/
│   ├── eks/                          # EKS deployment configs
│   └── minikube/                     # Minikube deployment configs
├── src/
│   ├── common/                       # Shared utilities
│   │   ├── config.py                 # Settings and configuration
│   │   ├── databases/
│   │   │   └── dynamoDB/             # DynamoDB client and models
│   │   ├── s3/                       # S3 service integration
│   │   ├── loggers/                  # Logging configuration
│   │   └── utils/                    # Utility functions
│   ├── health/                       # Health check endpoints
│   └── main.py                       # FastAPI application entry point
├── docker-compose.yml                # Docker Compose for development
├── docker-compose.stag.yml           # Docker Compose for staging
├── docker-compose.prod.yml           # Docker Compose for production
├── Dockerfile.local                  # Local development Dockerfile
├── pyproject.toml                     # Project dependencies and config
└── README.md                          # This file
```

## 🏁 Usage

### Running the Service

The service can be run in different environments. Choose the method that works best for your shell:

#### Development Environment

**Bash/Zsh:**
```bash
ENVIRONMENT=development fastapi dev src/main.py
```

**Fish Shell / Universal (Recommended):**
```bash
env ENVIRONMENT=development uv run fastapi dev src/main.py
```

**PowerShell (Windows):**
```powershell
$env:ENVIRONMENT="development"; fastapi dev src/main.py
# Or using uv run (recommended):
$env:ENVIRONMENT="development"; uv run fastapi dev src/main.py
```

#### Staging Environment

**Bash/Zsh:**
```bash
ENVIRONMENT=staging fastapi dev src/main.py
```

**Fish Shell / Universal:**
```bash
env ENVIRONMENT=staging uv run fastapi dev src/main.py
```

**PowerShell:**
```powershell
$env:ENVIRONMENT="staging"; uv run fastapi dev src/main.py
```

#### Production Environment

**Bash/Zsh:**
```bash
ENVIRONMENT=production fastapi dev src/main.py
```

**Fish Shell / Universal:**
```bash
env ENVIRONMENT=production uv run fastapi dev src/main.py
```

**PowerShell:**
```powershell
$env:ENVIRONMENT="production"; uv run fastapi dev src/main.py
```

### Database Setup

#### Initialize DynamoDB Tables

Run the setup script to create DynamoDB tables. Ensure your AWS credentials are configured in `config/secrets/secret-python-template-service.env`:

```bash
uv run task setup-db
```

#### Populate Mock Data

To populate the database with mock data for testing:

```bash
uv run task mock-student-teacher-relationships-table
```

## 💻 Development

### Code Quality

Run pre-commit hooks to ensure code quality:

```bash
uv run pre-commit run --all-files --verbose
```

### Project Tasks

Available tasks are defined in `pyproject.toml`:

- `setup-db` - Initialize DynamoDB tables
- `mock-student-teacher-relationships-table` - Populate mock data

Run tasks using:
```bash
uv run task <task-name>
```

## 🧪 Testing

Run the test suite:

```bash
uv run pytest
```

For verbose output:
```bash
uv run pytest -v
```

For coverage report:
```bash
uv run pytest --cov=src --cov-report=html
```

## 🚀 Deployment

### Docker

The service can be deployed using Docker Compose for different environments.

#### Development

```bash
# Build the image
docker-compose -f docker-compose.yml build

# Start the service
docker-compose -f docker-compose.yml up

# Run in detached mode
docker-compose -f docker-compose.yml up -d
```

#### Staging

```bash
docker-compose -f docker-compose.stag.yml build
docker-compose -f docker-compose.stag.yml up
```

#### Production

```bash
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up
```

The service will be exposed on port 8000 (or the port specified in `APP_PORT` environment variable).

### Kubernetes (Minikube)

Deploy the service to a local Minikube cluster:

#### Prerequisites

- Minikube installed and running
- kubectl configured

#### Steps

1. **Start Minikube:**
```bash
minikube start --driver=docker
```

2. **Build and Load Docker Image:**
```bash
# Build the image
docker-compose -f docker-compose.prod.yml build

# Load image into Minikube
# Note: Update the image name according to your docker-compose configuration
minikube image load python-template-service:latest
```

3. **Encode Secrets:**
```bash
input_file="./config/secrets/secret-python-template-service.env"
output_file="./config/secrets/encoded-secret-python-template-service.env"
while IFS='=' read -r key value; do
    echo "$key=$(echo -n "$value" | base64)"
done < "$input_file" > "$output_file"
```

4. **Deploy to Kubernetes:**
```bash
cd deployment/minikube
kubectl apply -f ./namespace.yaml
kubectl apply -f ./secret.yaml
kubectl apply -f ./configmap.yaml
kubectl apply -f ./deployment.yaml
```

5. **Verify Deployment:**
```bash
kubectl get pods
kubectl get svc
```

6. **Access the Service:**
```bash
# Note: Update the service name and namespace according to your deployment configuration
minikube service python-template-service -n python-template-service --url
```

### Kubernetes (EKS)

Deploy the service to Amazon EKS:

#### Prerequisites

- AWS CLI configured
- kubectl configured for EKS cluster
- ECR repository created
- AWS Load Balancer Controller installed ([Installation guide](https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html))

#### Steps

1. **Encode Secrets:**
```bash
input_file="./config/secrets/secret-python-template-service.env"
output_file="./config/secrets/encoded-secret-python-template-service.env"
while IFS='=' read -r key value; do
    echo "$key=$(echo -n "$value" | base64)"
done < "$input_file" > "$output_file"
```

2. **Authenticate Docker to ECR:**
```bash
aws ecr get-login-password --region <region> | \
  docker login --username AWS --password-stdin \
  <aws_account_id>.dkr.ecr.<region>.amazonaws.com
```

3. **Find or Create ECR Repository:**
```bash
aws ecr describe-repositories --output json
# Create if needed: aws ecr create-repository --repository-name python-template-service
```

4. **Build and Push Image:**
```bash
# Build the image
docker-compose -f docker-compose.prod.yml build

# Tag and push to ECR
# Replace ${ECR_REPO} with your ECR repository URI
docker tag python-template-service:latest ${ECR_REPO}:latest
docker push ${ECR_REPO}:latest
```

5. **Connect to EKS Cluster:**
```bash
aws eks --region <region> update-kubeconfig --name <cluster-name>
```

6. **Deploy to Kubernetes:**
```bash
cd deployment/eks
kubectl apply -f ./namespace.yaml
kubectl apply -f ./secret.yaml
kubectl apply -f ./configmap.yaml
kubectl apply -f ./deployment.yaml
kubectl apply -f ./ingress.yaml
```

7. **Verify Deployment:**
```bash
kubectl get pods -n python-template-service
kubectl get svc -n python-template-service
kubectl get ingress -n python-template-service
```

8. **Access the Service:**
The service will be accessible via the ingress address. For public access, ensure the ingress annotation `alb.ingress.kubernetes.io/scheme: internet-facing` is set.

Example output:
```
NAME                          CLASS   HOSTS   ADDRESS                                                              PORTS   AGE
python-template-ingress       alb     *       k8s-pythontemp-pythontemp-f048b2d71b-2114603642.us-east-1.elb.amazonaws.com   80      2d
```

For detailed EKS deployment documentation, see: [EKS Deployment Guide](https://oupagile.atlassian.net/wiki/spaces/OUPHKRD/pages/6102122501/EKS+How+to+host+a+backend+to+EKS)

## 📄 License

This project is licensed under the MIT License.
# python-backend-micro-service
