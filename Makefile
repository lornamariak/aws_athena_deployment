install:
	pip install -r requirements.txt

format:	
	black *py 

lint:
	pylint --disable=R, *py

refactor: format lint
		
all: install lint format