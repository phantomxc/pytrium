init:
	pip install -r requirements.txt

coverage:
	py.test --cov-report html:cov_html --cov=atrium tests/

test:
	py.test tests

publish:
	python setup.py register
	python setup.py sdist upload
	python setup.py bdist_wheel --universal upload 

