#!/bin/bash

# Script para configurar Vault con secretos de AWS S3 y autenticación de Kubernetes

echo "=== Configuring Vault for S3 Integration ==="

# Variables - REEMPLAZAR CON TUS CREDENCIALES REALES DE AWS
AWS_ACCESS_KEY="YOUR_AWS_ACCESS_KEY"
AWS_SECRET_KEY="YOUR_AWS_SECRET_KEY"

# Vault root token (en modo dev es 'root')
VAULT_TOKEN="root"

echo "Executing commands inside Vault pod..."

# 1. Habilitar el motor KV v2
echo "Enabling KV secrets engine..."
kubectl exec vault-0 -- vault secrets enable -path=secret kv-v2

# 2. Crear los secretos de AWS
echo "Creating AWS S3 credentials in Vault..."
kubectl exec vault-0 -- vault kv put secret/vault-s3-app/aws \
  accessKey="$AWS_ACCESS_KEY" \
  secretKey="$AWS_SECRET_KEY"

# 3. Verificar que los secretos se crearon correctamente
echo "Verifying secrets..."
kubectl exec vault-0 -- vault kv get secret/vault-s3-app/aws

# 4. Crear la política
echo "Creating Vault policy..."
kubectl cp vault-policy.hcl vault-0:/tmp/vault-policy.hcl
kubectl exec vault-0 -- vault policy write vault-s3-app /tmp/vault-policy.hcl

# 5. Habilitar autenticación de Kubernetes
echo "Enabling Kubernetes authentication..."
kubectl exec vault-0 -- vault auth enable kubernetes

# 6. Configurar la autenticación de Kubernetes
echo "Configuring Kubernetes auth method..."
kubectl exec vault-0 -- sh -c 'vault write auth/kubernetes/config \
  kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443" \
  token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
  kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
  issuer="https://kubernetes.default.svc.cluster.local"'

# 7. Crear el rol para la aplicación
echo "Creating Kubernetes role in Vault..."
kubectl exec vault-0 -- vault write auth/kubernetes/role/vault-s3-app \
  bound_service_account_names=vault-s3-app \
  bound_service_account_namespaces=vault-s3-demo \
  policies=vault-s3-app \
  ttl=24h

echo ""
echo "=== Vault Configuration Completed ==="
echo ""
echo "Summary:"
echo "- KV secrets engine enabled at: secret/"
echo "- AWS credentials stored at: secret/vault-s3-app/aws"
echo "- Policy created: vault-s3-app"
echo "- Kubernetes auth enabled and configured"
echo "- Role created: vault-s3-app"
echo ""
echo "Next steps:"
echo "1. Create namespace: kubectl apply -f k8s/namespace.yaml"
echo "2. Create service account: kubectl apply -f k8s/serviceaccount.yaml"
echo "3. Build Docker image: docker build -t vault-s3-app:latest ."
echo "4. Deploy application: kubectl apply -f k8s/deployment.yaml"
echo "5. Create service: kubectl apply -f k8s/service.yaml"