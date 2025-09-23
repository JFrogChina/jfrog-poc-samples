# Terraform Usage Guide with JFrog Platform

This guide explains how to run Terraform against JFrog Platform / Artifactory in an environment variable.

---

## 1. Set the Environment Variable

Export the JFrog access token as a Terraform variable.  
Terraform automatically maps environment variables prefixed with `TF_VAR_` to input variables defined in your configuration (`variables.tf`).

```bash
# Export the Artifactory token to Terraform variable "access_token"
export TF_VAR_access_token="$ARTIFACTORY_TOKEN"
```

- `ARTIFACTORY_TOKEN` is your local shell environment variable that stores the token.
- `TF_VAR_access_token` will be picked up by Terraform as the variable `access_token`.

---

## 2. Initialize Terraform

Run the initialization step before any operation:

```bash
terraform init
```

---

## 3. Review the Plan

Generate and review the execution plan before applying changes:

```bash
terraform plan
```

---

## 4. Apply the Configuration

Apply the plan to create or update resources:

```bash
terraform apply
```

You will be prompted for confirmation. To skip the prompt:

```bash
terraform apply -auto-approve
```

---

## 5. Destroy Resources

When you need to remove all resources managed by this configuration:

```bash
terraform destroy
```

Or without confirmation:

```bash
terraform destroy -auto-approve
```

---

## Notes

- Always make sure you are using the correct project and environment before running `apply` or `destroy`.
- Use `terraform plan` first to verify the expected changes.
- Store your access token securely; **never commit it to version control**.
