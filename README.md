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

## CI/CD
- Runner GitHub Actions self-hosted installé sur vm-tools (service systemd actif)
- Permet à la CI d'accéder au réseau privé (SonarQube, Vault, cluster K8s) sans exposition publique

## Pipeline CI
- Déclenché sur push (main, feature/**) et Pull Request vers main
- Étapes : installation des dépendances, tests unitaires (pytest), build de l'image Docker, smoke test /health
- Exécuté sur le runner self-hosted (vm-tools)

## Qualité de code
- SonarQube Community déployé sur vm-tools (Docker Compose), accessible sur http://192.168.195.10:9000
- Analyse automatique à chaque exécution du pipeline CI (job sonarqube-scan)

## Quality Gate
- Quality Gate "Sonar way" appliqué sur devsecops-demo-app
- Pipeline CI bloquant : job sonarqube-scan + check obligatoire sur main


## Sécurité des images (Trivy)
- Scan automatique de l'image Docker à chaque exécution du pipeline (job trivy-image-scan)
- Bloque le pipeline sur toute vulnérabilité HIGH/CRITICAL avec correctif disponible
- Les vulnérabilités sans correctif (ignore-unfixed) ne bloquent pas, car non actionnables
- Premier scan ~25min (téléchargement de la base CVE), scans suivants nettement plus rapides

## Sécurité de la configuration (Trivy IaC)
- Scan du Dockerfile (et futurs manifests K8s/Helm) à chaque exécution du pipeline (job trivy-iac-scan)
- Résultats visibles dans l'onglet Security > Code scanning de GitHub (format SARIF)
- Bloque le pipeline sur toute mauvaise configuration HIGH/CRITICAL
- Dockerfile durci : --no-install-recommends, HEALTHCHECK, mise à jour des paquets système
