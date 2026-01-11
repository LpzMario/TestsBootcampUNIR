# Policy for vault-s3-app
# This policy allows the application to read AWS credentials from Vault

path "secret/data/vault-s3-app/aws" {
  capabilities = ["read"]
}

path "secret/metadata/vault-s3-app/*" {
  capabilities = ["list", "read"]
}