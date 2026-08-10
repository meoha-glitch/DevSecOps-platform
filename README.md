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

## Chart Helm
- helm-charts/mon-app : Deployment (2 replicas), Service (ClusterIP), Ingress (nginx)
- Probes liveness/readiness sur /health
- Requests/limits CPU et mémoire définis
- Testé avec helm lint, helm template, et une installation réelle de validation

## ArgoCD
- Installé dans le namespace argocd (manifest officiel)
- Interface web accessible via NodePort sur k8s-master (port variable, voir kubectl get svc argocd-server -n argocd)
- CLI argocd installée sur vm-tools
- Script d'installation : infra/argocd/install.sh

## GitOps (ArgoCD)
- Application ArgoCD "mon-app-dev" : infra/argocd/application-dev.yaml
- Valeurs d'environnement dev : gitops/dev/values-dev.yaml
- Sync automatique + selfHeal activés : toute dérive manuelle du cluster est
  automatiquement corrigée pour revenir à l'état défini dans Git
- Testé : scale manuel annulé automatiquement, changement via Git appliqué automatiquement

## Boucle CI/CD complète
- Job push-image : construit et pousse l'image vers ghcr.io après validation
  de tous les contrôles qualité/sécurité (Sonar, Trivy image, Trivy IaC)
- Mise à jour automatique du tag dans gitops/dev/values-dev.yaml par un commit bot
- ArgoCD détecte et synchronise automatiquement le déploiement
- Flux validé de bout en bout : commit → tests → build → scan → push → GitOps → déploiement
- securityContext (pod + container) durci : non-root, UID fixe, readOnlyRootFilesystem,
  capabilities dropped, seccompProfile RuntimeDefault
- Volume emptyDir monté sur /tmp : nécessaire car gunicorn écrit des fichiers temporaires
  de worker, incompatible avec readOnlyRootFilesystem sans cet espace dédié

## HashiCorp Vault
- Déployé en mode production (Raft storage) dans le namespace vault
- Nécessite local-path-provisioner comme StorageClass (voir infra/storage/local-path-provisioner.md)
- UI accessible via kubectl get svc -n vault | grep vault-ui (port NodePort dynamique)
- Vault Agent Injector activé 
- IMPORTANT : Vault se reverrouille (sealed) à chaque redémarrage du pod ;
  procédure de déverrouillage dans infra/vault/unseal-procedure.md
- Clés d'unseal et root token stockés uniquement en local

## Intégration Vault ↔ application
- Authentification Kubernetes activée sur Vault (auth/kubernetes)
- Moteur KV v2 sur le chemin secret/devsecops-demo-app/dev
- Policy devsecops-app-policy : lecture seule, chemin unique (moindre privilège)
- Rôle devsecops-app lié au ServiceAccount devsecops-app-sa (namespace dev)
- Vault Agent Injector : secrets injectés dans /vault/secrets/db-creds au démarrage du pod
- Aucun secret n'apparaît dans Git ni dans les manifests Kubernetes

## Monitoring (Prometheus)
- kube-prometheus-stack installé dans le namespace monitoring
- Prometheus UI : http://192.168.195.11:30900
- Alertmanager UI : http://192.168.195.11:30903
- Application instrumentée avec prometheus-flask-exporter (endpoint /metrics)
- ServiceMonitor mon-app-dev configuré pour scraper toutes les 15s

## Monitoring

L'application expose les métriques Prometheus sur `/metrics`.
