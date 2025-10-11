
build: clean setup
	./venv/bin/python3 -m fastapi dev app/main.py 
	
setup: pyproject.toml
	python3 -m venv venv
	./venv/bin/pip3 install .

clean:
	rm -rf __pycache__
	rm -rf app/__pycache__
	rm -rf WOOF.egg-info
	rm -rf build
	rm -rf venv

