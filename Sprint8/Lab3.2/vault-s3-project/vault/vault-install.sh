#!/bin/bash

# Script para instalar Vault en Kubernetes usando Helm

echo "=== Installing Vault with Helm ==="

# Añadir el repositorio de Helm de HashiCorp
echo "Adding HashiCorp Helm repository..."
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update

# Instalar Vault en modo Dev (para testing)
# Para producción, usar modo HA
echo "Installing Vault in dev mode..."
helm install vault hashicorp/vault \
  --set "server.dev.enabled=true" \
  --set "injector.enabled=true" \
  --set "ui.enabled=true" \
  --set "ui.serviceType=NodePort" \
  --namespace default

echo "Waiting for Vault pod to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=vault --timeout=120s

echo "Vault installation completed!"

# Obtener el token root (solo en modo dev)
echo ""
echo "=== Vault Root Token ==="
echo "In dev mode, the root token is: root"
echo ""

# Información de acceso
echo "=== Access Information ==="
echo "Vault UI: Access via NodePort service"
kubectl get svc vault-ui -o wide

echo ""
echo "To access Vault from inside the cluster:"
echo "kubectl exec -it vault-0 -- /bin/sh"
echo ""
echo "Next steps: Run vault-config.sh to configure Vault"