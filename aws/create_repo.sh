#! /bin/bash

. ./conf.env

aws ecr create-repository --repository-name $ECR_REPO_NAME