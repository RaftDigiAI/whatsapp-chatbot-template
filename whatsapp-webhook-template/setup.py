from setuptools import setup


version = "0.0.1"

setup(
    name="whatsapp-webhook-template",
    version=version,
    description="FastAPI app for whatsapp chat webhook Service",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    author="Raft",
    author_email="sales@raftds.com",
    include_package_data=True,
    install_requires=[
        "aiohttp~=3.9.5",
        "aiohttp-retry~=2.8.3",
        "asyncpg==0.29.0",
        "fastapi~=0.111.0",
        "pydantic~=2.7.4",
        "pydantic-settings~=2.3.3",
        "python-dotenv~=1.0.1",
        "python-multipart~=0.0.9",
        "pytz~=2024.1",
        "uvicorn~=0.30.1",
    ],
    extras_require={
        "code-quality": [
            "asyncpg-stubs~=0.29.1",
            "black~=23.11.0",
            "flake8~=6.1.0",
            "isort~=5.12.0",
            "mypy~=1.7.1",
            "pylint~=3.0.2",
            "pylint_pydantic~=0.3.0",
            "types-pytz~=2024.1.0.20240203",
            "types-setuptools~=68.2.0.2",
        ],
        "testing": [
            "httpx~=0.26.0",
            "pytest~=7.4.3",
            "pytest_asyncio~=0.23.2",
        ],
    },
    packages=[],
    python_requires=">=3.10",
    keywords="FastAPI Whatsapp chat webhook",
)
