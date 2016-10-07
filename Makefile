init:
	pip install -r requirements.txt

test:
	py.test tests

publish:
	python setup.py register
	python setup.py sdist upload
	python setup.py bdist_wheel --universal upload 

