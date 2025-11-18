#  NimbusOps
### Cloud-native MLOps framework for training, deployment, and observability.

A **production-ready MLOps framework** that streamlines model training, deployment, and monitoring in cloud environments using **Terraform**, **Docker**, and **MLflow**.

---

##  Overview
**NimbusOps** provides a scalable, opinionated foundation for running end-to-end machine learning workloads in the cloud.  
It integrates infrastructure-as-code, experiment tracking, and monitoring into a single reproducible system.

---

###  Features
- **Infrastructure-as-Code:** Reproducible environments via Terraform  
- **Containerized Pipelines:** Training, inference, and deployment using Docker  
- **Experiment Tracking:** Full model lineage with MLflow  
- **Monitoring:** Real-time metrics using Prometheus & Grafana  
- **Cloud Agnostic:** Works across AWS, GCP, and Azure  

---

###  Tech Stack
- **Languages:** Python, Bash  
- **Infrastructure:** Terraform, Docker, Kubernetes  
- **Cloud Providers:** AWS (default), GCP, Azure  
- **ML & Tracking:** MLflow, Scikit-learn, Pandas  
- **Monitoring:** Prometheus, Grafana  

---

###  Project Structure
NimbusOps/
```├── infrastructure/
│ ├── main.tf
│ ├── variables.tf
│ └── outputs.tf
│
├── src/
│ ├── train.py
│ ├── predict.py
│ └── pipeline.py
│
├── notebooks/
│ └── monitoring.ipynb
│
├── README.md
└── requirements.txt

```
### 🧠 Example Workflow

1. **Provision Cloud Infrastructure**
```
cd infrastructure
terraform init
terraform apply

Train and Log a Model
python src/train.py

Containerize and Deploy
docker build -t nimbusops-model .
docker run -p 8080:8080 nimbusops-model

```
Monitor Performance
Access Grafana dashboards for accuracy, latency, and uptime metrics.

📊 Example Metrics
| Metric             | Description                                 | Example |
| :----------------- | :------------------------------------------ | :------ |
| Model Accuracy     | Tracked via MLflow                          | 92.4 %  |
| Deployment Latency | Container response time                     | 180 ms  |
| Uptime             | Terraform-provisioned endpoint availability | 99.9 %  |



```
📦 Requirements
nginx
Copy code
mlflow
boto3
scikit-learn
pandas
prometheus-client 

🤝 Contributing
Contributions and extensions (e.g., GCP modules, CI/CD workflows) are welcome!
Fork the repo → create a branch → open a PR to collaborate.


How to run NimbusOps locally

From NimbusOps/:
```
# 1. Create venv & install deps
python -m venv .venv
. .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# 2. Train a model
python src/train.py

# 3. Start prediction API
uvicorn src.predict:app --reload


```
Then:

curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d "{\"features\": [[14.0, 20.0, 90.0, 600.0, 0.1, 0.2, 0.3, 0.1, 0.2, 0.05, 0.2, 0.8, 1.5, 15.0, 0.006, 0.02, 0.03, 0

