run:
	docker-compose up --build -d
test: run
	docker exec -it web-server python manage.py test