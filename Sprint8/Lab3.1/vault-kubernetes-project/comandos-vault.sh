#!/bin/bash

# Script para configurar Vault dentro del pod
# Ejecutar estos comandos desde dentro del pod de Vault

echo "=================================="
echo "CONFIGURACIÓN DE VAULT"
echo "=================================="
echo ""

echo "1. Habilitando motor de secretos KV v2..."
vault secrets enable -path=secret kv-v2

echo ""
echo "2. Creando secreto de ejemplo..."
vault kv put secret/webapp/config \
    username="admin" \
    password="secretpassword123"

echo ""
echo "3. Verificando que el secreto fue creado..."
vault kv get secret/webapp/config

echo ""
echo "4. Habilitando autenticación de Kubernetes..."
vault auth enable kubernetes

echo ""
echo "5. Configurando autenticación de Kubernetes..."
vault write auth/kubernetes/config \
    kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443"

echo ""
echo "6. Creando política de acceso..."
vault policy write webapp - <<EOF
path "secret/data/webapp/config" {
  capabilities = ["read"]
}

path "secret/metadata/webapp/*" {
  capabilities = ["list"]
}
EOF

echo ""
echo "7. Verificando la política creada..."
vault policy read webapp

echo ""
echo "8. Creando rol de Kubernetes..."
vault write auth/kubernetes/role/webapp \
    bound_service_account_names=vault-auth \
    bound_service_account_namespaces=vault-demo \
    policies=webapp \
    ttl=24h

echo ""
echo "9. Verificando el rol creado..."
vault read auth/kubernetes/role/webapp

echo ""
echo "=================================="
echo "CONFIGURACIÓN COMPLETADA"
echo "=================================="
echo ""
echo "Ahora puedes desplegar la aplicación con:"
echo "kubectl apply -f 05-app-deployment.yaml"