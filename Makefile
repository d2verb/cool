.PHONY: test
test:
	pytest tests

.PHONY: fmt
fmt:
	black cool/* tests/*

.PHONY: lint
lint:
	flake8 cool/* tests/*
	mypy ./cool/* ./tests/*