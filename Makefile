all:run

run:
	@echo "executing ./src/main.py"
	@python3 src/main.py

config: 
	@echo "installing precommit hooks..."
	@pip install pre-commit
	@pre-commit install
	@pre-commit autoupdate
	@pre-commit run --all-files
	@echo "WARNING: these are meant for testing and not to be run in production!"
	@echo "installing dependancies for local development..."
	@pip install -r requirements.txt
	@playwright install
