# Kubernetes Mutating Admission Webhook (ARM64 Edge Deployment)

## 📌 Overview
A production-grade Kubernetes Mutating Admission Webhook built from scratch and deployed on a local edge computing environment (Raspberry Pi 5 running k3s). This project demonstrates cloud-native support operations, infrastructure-as-code (IaC), and API automation. 

The webhook intercepts Pod creation requests at the Kubernetes API Server level and dynamically injects mandatory compliance labels (e.g., `env: production`) via JSONPatch before the objects are persisted to the etcd database.

## 🛠️ Technology Stack
| Category | Technology |
|---|---|
| **Hardware / OS** | Raspberry Pi 5 (ARM64), Raspberry Pi OS |
| **Orchestration** | Kubernetes (k3s containerd) |
| **API Development** | Python 3.13, FastAPI, Uvicorn, Docker |
| **Infrastructure as Code** | Terraform (HashiCorp Kubernetes Provider) |
| **Security & TLS** | OpenSSL (Custom CA & Server Certificates), K8s Secrets |
| **API Testing** | Postman, cURL |

## 🏗️ Architecture Flow
1. **API Server Interception**: A user or pipeline attempts to create a Pod via `kubectl`.
2. **Admission Review**: The Kubernetes API Server intercepts the request and forwards an `AdmissionReview` JSON payload over HTTPS to the webhook service.
3. **Webhook Processing**: The Python FastAPI backend validates the TLS connection, parses the JSON payload, and checks for existing labels.
4. **JSONPatch Generation**: If the `env` label is missing, the application generates a Base64-encoded JSONPatch (`[{"op": "add", "path": "/metadata/labels/env", "value": "production"}]`).
5. **Mutation**: The API Server applies the patch and successfully spins up the Pod with the injected compliance labels.

## 🚀 Deployment Steps

### 1. Certificate Authority & TLS Generation
Kubernetes strictly requires webhooks to communicate over HTTPS. 
```bash
# Generate CA and Server Certificates for webhook-service.default.svc
openssl genrsa -out certs/ca.key 2048
openssl req -new -x509 -days 365 -key certs/ca.key -subj "/CN=Webhook CA" -out certs/ca.crt
# (Additional server certificate generation steps using server.conf)

# Inject the TLS keys into the cluster as a Secret
kubectl create secret tls webhook-tls --cert=certs/tls.crt --key=certs/tls.key
