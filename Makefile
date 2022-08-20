run:
	docker-compose up --build
test:
	docker-compose up --build -d web-server
	docker exec -it web-server python manage.py test