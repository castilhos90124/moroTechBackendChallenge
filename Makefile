run:
	docker-compose up --build $(dettach)

superuser:
	docker exec -it web-server python manage.py createsuperuser