# DevSecOps Platform

Plateforme DevSecOps de lab : CI/CD sécurisé (GitHub Actions, SonarQube, Trivy),
GitOps sur Kubernetes (ArgoCD, Helm), gestion des secrets (Vault),
monitoring (Prometheus, Grafana).

## VMs
- vm-tools : 192.168.195.10
- vm-k8s-master : 192.168.195.11
- vm-k8s-worker1 : 192.168.195.12

## Structure du projet
- `app/` : code source de l'application de démonstration (Flask)
- `docker/` : Dockerfile
- `helm-charts/` : chart Helm de déploiement (à venir)
- `k8s-manifests/` : manifests Kubernetes bruts si besoin
- `gitops/` : configuration désirée pour ArgoCD par environnement
- `.github/workflows/` : pipelines CI
- `infra/` : scripts de provisioning des VMs et du cluster
- `docs/` : documentation complémentaire

## Cluster Kubernetes
- vm-k8s-master : control-plane, Ready
- vm-k8s-worker1 : worker, Ready
- CNI : Calico v3.28.0
- Pod network CIDR : 192.168.0.0/16

## Ingress & Metrics
- Helm 3 installé sur k8s-master
- Ingress Controller : ingress-nginx (NodePort 30080/30443)
- metrics-server : opérationnel (kubectl top disponible)
