PROJECT_NAME=pet_food_calculator

run-dev:  ## Runs dev server
	pipenv run python manage.py runserver

docker-run-dev:  ## Runs dev server in docker
	python3 ./utils/wait_for_postgres.py
	python3 manage.py migrate
	python3 manage.py runserver 0.0.0.0:8000

docker-run-production: docker-migrate
	cp -r /app/static /tmp/
	gunicorn PetFoodCalculator.asgi:application -w 4 -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --capture-output --log-level debug --access-logfile - --error-logfile -

docker-migrate:
	python3 manage.py migrate

migrate:  ## Migrate database to the latest version
	pipenv run python3 manage.py migrate

.PHONY: \
  run-dev \
  docker-run-dev \
  migrate \
  requirements \
