#!/bin/bash
# Installation d'ArgoCD 

kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo "Attente du démarrage des pods ArgoCD..."
kubectl wait --for=condition=Ready pods --all -n argocd --timeout=300s

kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "NodePort"}}'

echo "Mot de passe admin initial :"
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
echo ""

echo "Port d'accès HTTPS :"
kubectl get svc argocd-server -n argocd
