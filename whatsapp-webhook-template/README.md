# whatsapp-webhook-template

## Building project

### 2. Install dependencies

```bash
cd whatsapp-webhook-template && python3 -m venv .venv && source .venv/bin/activate
pip install -U pip setuptools
pip install .[code-quality,testing]
```

To install shared libs you need to get token from administrator

```bash
pip install .[shared]
```

### 3. Start the app

> Launch from project root folder

Fill env from [example file](./backend/config/environment/env.sh.template)

You can put it in `./whatsapp-webhook-template/.env` file and it will also works

Run

```bash
uvicorn main:app
```

or with hot reload

```bash
uvicorn main:app --reload
```

### Code quality

Install dependencies: `pip install .[code-quality]`  
  
[Docs: flake8](https://pypi.org/project/flake8/)  
[Docs: mypy](https://mypy.readthedocs.io/en/stable/)
[Docs: black](https://pypi.org/project/black/)  
[Docs: isort](https://pypi.org/project/isort/3.8.1/)  
[Docs: pylint](https://pypi.org/project/pylint/)
