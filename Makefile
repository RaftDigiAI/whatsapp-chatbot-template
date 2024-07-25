VENV_DIR = .venv

create_venv:
	test -d $(VENV_DIR) || (python3 -m venv $(VENV_DIR) && . $(VENV_DIR)/bin/activate && pip install -U setuptools)

migrations: create_venv
	. $(VENV_DIR)/bin/activate && cd db-migrations && docker-compose up -d && pip install . && python migrate.py

install-shared-lib: create_venv
	. $(VENV_DIR)/bin/activate && cd shared-lib-template && pip install .

install-webhook: create_venv
	. $(VENV_DIR)/bin/activate && cd whatsapp-webhook-template && pip install .

run-webhook: create_venv
	. $(VENV_DIR)/bin/activate && cd whatsapp-webhook-template && uvicorn main:app

launch: create_venv migrations install-shared-lib install-webhook run-webhook
