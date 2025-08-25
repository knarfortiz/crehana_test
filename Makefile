DOCKER_COMPOSE_FILE=docker-compose.yml

up:
	@echo "🚀 Starting services with Docker Compose..."
	docker compose -f $(DOCKER_COMPOSE_FILE) up --build -d

down:
	@echo "🛑 Stopping and removing services..."
	docker compose -f $(DOCKER_COMPOSE_FILE) down

logs:
	@echo "📜 Showing logs..."
	docker compose -f $(DOCKER_COMPOSE_FILE) logs -f

restart:
	@echo "🔄 Restarting services..."
	docker compose -f $(DOCKER_COMPOSE_FILE) down
	docker compose -f $(DOCKER_COMPOSE_FILE) up --build -d

ps:
	@echo "📦 Listing active containers..."
	docker compose -f $(DOCKER_COMPOSE_FILE) ps

clean:
	@echo "🧹 Removing containers, images, and volumes..."
	docker compose -f $(DOCKER_COMPOSE_FILE) down --rmi all --volumes --remove-orphans

help:
	@echo "Available commands:"
	@echo "  make up        - Start services in detached mode"
	@echo "  make down      - Stop and remove services"
	@echo "  make logs      - Show logs in real-time"
	@echo "  make restart   - Restart services"
	@echo "  make ps        - List running containers"
	@echo "  make clean     - Remove everything (containers, images, and volumes)"
