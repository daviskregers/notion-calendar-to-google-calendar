.PHONY: test coverage

test:
	python -m unittest

coverage:
	rm -r coverage || true
	coverage run \
	  --branch \
	  -m unittest
	coverage html -d coverage
	coverage report
