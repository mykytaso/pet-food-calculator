PROJECT_NAME=pet_food_calculator

run-dev:  ## Runs dev server
	 pipenv run python manage.py runserver

docker-run-dev:  ## Runs dev server in docker
	python3 ./utils/wait_for_postgres.py
	python3 manage.py migrate
	python3 manage.py runserver 127.0.0.1:8000

docker-run-production: docker-migrate
	gunicorn PetFoodCalculator.asgi:application -w 2 -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:8814 --capture-output --log-level debug --access-logfile - --error-logfile -

docker-migrate:
	python3 manage.py migrate

run-uvicorn:  ## Runs uvicorn (ASGI) server in managed mode
	pipenv run uvicorn --fd 0 --lifespan off PetFoodCalculator.asgi:application


migrate:  ## Migrate database to the latest version
	pipenv run python3 manage.py migrate

.PHONY: \
  run-dev \
  run-uvicorn \
  docker-run-dev \
  migrate \
  requirements \
