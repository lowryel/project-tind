setup:
	# python3 -m venv ~/.django
	# source ~/.django/bin/activate

install:
	pip install -r requirements.txt

test:
	python manage.py test

lint:
	hadolint Dockerfile

