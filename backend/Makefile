

build: clean

	./venv/bin/python3 -m fastapi dev app/main.py 
	
setup: pyproject.toml
	python3 -m venv venv
	./venv/bin/pip3 install .

clean:

	rm -rf __pycache__ app/__pycache__ app/authentication/__pycache__ app/crud/__pycache__ app/data/__pycache__ app/models/__pycache__ app/routers/__pycache__ app/schemas/__pycache__
	rm -rf WOOF.egg-info
	rm -rf build
	echo '' > app/data/sample.db 


