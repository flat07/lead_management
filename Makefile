# Run the local development server
run:
	python manage.py runserver

# Make database migrations based on model changes
mm:
	python manage.py makemigrations

# Apply migrations to the database
migrate:
	python manage.py migrate

# Create a new superuser account
superuser:
	python manage.py createsuperuser
flush:
	python manage.py flush --no-input
# Run your Django unit tests
test:
	python -m pytest

# Open the interactive Django shell
shell:
	python manage.py shell
check:
	python manage.py check
seed:
	python manage.py seed

# Install python dependencies from your requirements file
freeze:
	pip freeze > requirements.txt
install:
	python -m pip install -r requirements.txt

# Show all available shortcuts in this file
help:
	@echo "Available commands:"
	@echo "  make run       - Run development server"
	@echo "  make mm        - Create new database migrations"
	@echo "  make migrate   - Apply database migrations"
	@echo "  make superuser - Create administrative user"
	@echo "  make test      - Run application test suites"
	@echo "  make shell     - Open Django interactive shell"
	@echo "  make install   - Install pip requirements"
