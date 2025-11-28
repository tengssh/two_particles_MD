.PHONY: help run app test coverage clean install

help:
	@echo "Two-Particle MD Simulation - Available Commands"
	@echo "================================================"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  run        - Run the command-line simulation"
	@echo "  app        - Launch the interactive Streamlit web app"
	@echo "  test       - Run all tests with pytest"
	@echo "  coverage   - Run tests with coverage report"
	@echo "  clean      - Remove Python cache files and build artifacts"
	@echo "  install    - Install project dependencies"
	@echo "  help       - Show this help message"

run:
	@echo "Running MD simulation..."
	python src/md_simulation.py

app:
	@echo "Launching Streamlit app..."
	@echo "Opening browser at http://localhost:8501"
	streamlit run src/streamlit_app.py

test:
	@echo "Running tests..."
	pytest tests/ -v

coverage:
	@echo "Running tests with coverage..."
	pytest tests/ --cov=src --cov-report=term --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage 2>/dev/null || true
	@echo "Cleanup complete!"

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Installation complete!"
