terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

provider "docker" {}

resource "docker_image" "fastapi" {
  name = "mi-fastapi:latest"
  build {
    context    = "${path.module}"
    dockerfile = "Dockerfile"
  }
}

resource "docker_container" "fastapi" {
  name  = "fastapi_app"
  image = docker_image.fastapi.image_id
  ports {
    internal = 80
    external = 8000
  }
}
