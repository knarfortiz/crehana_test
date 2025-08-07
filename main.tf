terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

provider "docker" {}


# Network
resource "docker_network" "app_network" {
  name = "app_network"
}



# Config Mailhog
resource "docker_image" "mailhog" {
  name = "mailhog/mailhog:latest"
}

resource "docker_container" "mailhog" {
  name  = "mailhog"
  image = docker_image.mailhog.image_id

  ports {
    internal = 1025
    external = 1025
  }

  ports {
    internal = 8025
    external = 8025
  }

  networks_advanced {
    name = docker_network.app_network.name
  }
}


# Config App
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

  env = [
    "SMTP_HOST=mailhog",
    "SMTP_PORT=1025",
    "FROM_EMAIL=no-reply@miapp.local"
  ]

  depends_on = [
    docker_container.mailhog
  ]

  networks_advanced {
    name = docker_network.app_network.name
  }
}

