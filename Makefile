install:
	poetry install
	poetry run pre-commit install


dev:
	poetry run fastapi dev referral_system/main.py

start:
	make migrate
	poetry run fastapi run referral_system/main.py

compose-dev:
	docker compose up -d --remove-orphans

compose-start:
	docker compose --profile full up --remove-orphans

build:
	docker compose --profile full build

lint:
	poetry run ruff check

lint_fix:
	poetry run ruff check --fix

format:
	poetry run ruff format

start_db:
	docker compose start db

enter_db:
	docker compose exec -it db psql -U pguser -d pgdb psql

# make migrations is not working for some reason
# make: 'migrations' is up to date.
db_migrations:
	@if [ -z "$(m)" ]; then \
		echo "poetry run alembic revision --autogenerate"; \
		poetry run alembic revision --autogenerate; \
	else \
		echo "poetry run alembic revision --autogenerate -m '$(m)'"; \
		poetry run alembic revision --autogenerate -m "$(m)"; \
	fi

migrate:
	poetry run alembic upgrade head
