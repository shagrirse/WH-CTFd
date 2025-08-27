# Guide to Deploying CTFd

1. Download and configure AWS CLI (access keys, region, etc.)
2. Configure CTFd-related configurations in `conf.ini`
3. Deploy Docker Hub image using 
4. Download and install Terraform
5. Configure `tfvars` with the example in `./infra/terraform.tfvars.example`
6. `cd aws/infra && terraform init`
7. `terraform plan -var-file="terraform.tfvars"` to check variables and `terraform apply -var-file="terraform.tfvars"` to push changes to the Cloud