from infra import Infra
if __name__ == "__main__":
  setup = Infra()
  # created_repo = setup.create_ecr_repository()
  setup.build_push_docker_image()
