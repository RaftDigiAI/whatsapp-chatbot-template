from setuptools import setup


version = "1.0.0"

setup(
    name="whatsapp-template-db-migrations",
    version=version,
    description="Postgres migrations",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    author="Raft",
    author_email="sales@raftds.com",
    include_package_data=True,
    install_requires=[
        "alembic~=1.13.1",
        "psycopg2-binary~=2.9.9",
    ],
    extras_require={
        "code-quality": [
            "black~=23.11.0",
            "flake8~=6.1.0",
            "isort~=5.12.0",
            "mypy~=1.7.1",
            "pylint~=3.0.2",
            "pylint_pydantic~=0.3.0",
            "types-setuptools~=68.2.0.2",
            "types-psycopg2~=2.9.21.20240201",
        ],
    },
    packages=[],
    python_requires=">=3.10",
    keywords="whatsapp template postgres alembic migrations",
)
