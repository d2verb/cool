.PHONY: test
test:
	pytest tests

.PHONY: check
check:
	black cool/* tests/*
	flake8 cool/* tests/*
	mypy ./cool/* ./tests/*