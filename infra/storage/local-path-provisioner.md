# StorageClass requise pour les volumes persistants

Un cluster kubeadm de base n'a aucune StorageClass par défaut. Tout pod
demandant un PersistentVolumeClaim (comme Vault) reste bloqué en `Pending`
sans jamais être scheduled, avec l'erreur :
"pod has unbound immediate PersistentVolumeClaims"

## Installation (à faire une seule fois pour tout le cluster)

kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
kubectl patch storageclass local-path -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

## Vérification

kubectl get storageclass
# doit afficher "local-path (default)"
