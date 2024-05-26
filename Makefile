build:
	docker-compose build

up: build
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	docker-compose run --rm test

# Install all dependencies inside the Docker container
install:
	docker-compose run --rm web pip install --no-cache-dir -r requirements.txt

# Remove all containers, images, and volumes
clean: down
	docker system prune -f
	docker volume prune -f
	docker image prune -f

# Remove and reinstall all dependencies
reinstall: clean
	docker-compose build
	docker-compose run --rm web pip install --no-cache-dir -r requirements.txt

# Run database scripts (assuming a script located at ./scripts/init_db.py)
run-db-scripts:
	docker-compose run --rm web python scripts/init_db.py

.PHONY:  build up down logs test install clean reinstall run-db-scripts