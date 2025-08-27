import configparser
import boto3
import docker
from pathlib import Path

class Infra:
  def __init__(self):
    self.config = configparser.ConfigParser()
    self.config.read('conf.ini')
  def create_ecr_repository(self, region="ap-southeast-1"):
    """
    Creates an Amazon ECR repository.

    Args:
      name (str): The name of the ECR repository to create.
      region (str): The AWS region where the repository will be created.
    """
    try:
      ecr_client = boto3.client('ecr', region_name=region)
      response = ecr_client.create_repository(
        repositoryName=self.config['ECR']['ECR_REPO_NAME'],
        imageScanningConfiguration={
          'scanOnPush': True  # Optional: Enable image scanning on push
        },
        imageTagMutability='MUTABLE' # Optional: 'MUTABLE' or 'IMMUTABLE'
      )
      repoUri = response['repository']['repositoryUri']
      print(f"Successfully created ECR repository: {repoUri}")

      repoName = response["repository"]["repositoryName"]
      baseUri =  repoUri.replace(f'/{repoName}', '')
      self.config.set('ECR', 'BASE_REPOSITORY_URI', baseUri)
      with open('conf.ini', 'w') as configfile:
        self.config.write(configfile)

      return response['repository']
    except Exception as e:
      print(f"Error creating ECR repository: {e}")
      return None
    
  def build_push_docker_image(self):
    try:
      client = docker.from_env()

      repoName = self.config['ECR']['ECR_REPO_NAME']
      ctfdPath = Path('.').parent.absolute().parent

      image, build_log = client.images.build(path=str(ctfdPath), tag=repoName, rm=True, quiet=False, nocache=False)
      for chunk in build_log:
        if 'stream' in chunk:
          print(chunk['stream'].strip())
      # Only for AWS resources
      # baseUri = self.config['ECR']['BASE_REPOSITORY_URI']
      # image.tag(repository=f'{baseUri}/{repoName}:latest')
      # response = client.api.push(f'{baseUri}/{repoName}:latest')

      dockerUser = self.config['DOCKER_HUB_USER']
      dockerPassword = self.config['DOCKER_HUB_PASS']
      dockerHubRepositoryName = f'{dockerUser}/{repoName}'

      image.tag(repository=dockerHubRepositoryName)
      client.login(username=dockerUser, password=dockerPassword)
      for line in client.images.push(dockerHubRepositoryName, stream=True, decode=True):
        print(line)
    except Exception as e:
      print(f"Error creating image: {e}")
      return None