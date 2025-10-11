# Makefile in the root directory

# Use .PHONY to declare targets that are not actual files.
.PHONY: all build build-frontend build-backend install install-frontend install-backend clean

# Default target: running 'make' will run 'make all'
all: build

# ------------------
# BUILD TARGETS
# ------------------

# Master build command for Vercel. It builds both the frontend and prepares the backend.
build: build-frontend build-backend

# Builds the SvelteKit application.
# Vercel automatically caches node_modules, but 'pnpm install' is safe to run.
build-frontend:
	@echo "--- Building SvelteKit Frontend ---"
	cd frontend && pnpm install && pnpm build

# Prepares the backend for Vercel.
# The primary job here is to create a requirements.txt file that Vercel's Python
# builder can use automatically. We use 'uv' since you have a uv.lock file.
build-backend:
	@echo "--- Preparing FastAPI Backend ---"
	@echo "Generating requirements.txt from pyproject.toml..."
	uv pip compile backend/pyproject.toml -o backend/requirements.txt
	@echo "backend/requirements.txt created successfully."


# ------------------
# LOCAL DEVELOPMENT TARGETS
# ------------------

# Install all dependencies for local development.
install: install-frontend install-backend

# Install frontend dependencies.
install-frontend:
	@echo "--- Installing Frontend Dependencies ---"
	cd frontend && pnpm install

# Install backend dependencies using uv.
install-backend:
	@echo "--- Installing Backend Dependencies ---"
	@echo "Creating virtual environment in backend/.venv..."
	python3 -m venv backend/.venv
	@echo "Installing dependencies with uv..."
	uv pip sync --python backend/.venv/bin/python backend/pyproject.toml


# ------------------
# UTILITY TARGETS
# ------------------

# Clean up build artifacts and caches.
clean:
	@echo "--- Cleaning Project ---"
	rm -rf frontend/.svelte-kit
	rm -rf frontend/build
	rm -rf backend/__pycache__
	rm -rf backend/app/__pycache__
	rm -rf backend/.venv
	rm -f backend/requirements.txt
	@echo "Clean complete."