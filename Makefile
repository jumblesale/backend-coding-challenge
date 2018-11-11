mypy:
	pipenv run mypy --package unbabel --strict --ignore-missing-imports

test-unit:
	pipenv run pytest --ignore=unbabel

test-integration:
	pipenv run behave test/integration/features
