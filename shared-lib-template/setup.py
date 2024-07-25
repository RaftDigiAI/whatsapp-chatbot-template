from setuptools import find_packages, setup


version = "0.0.1"

packages = find_packages(include=["shared_lib_template", "shared_lib_template.*"])

setup(
    name="shared-lib-template",
    version=version,
    description="shared lib",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    author="Raft",
    author_email="sales@raftds.com",
    include_package_data=True,
    install_requires=[
        "aiohttp~=3.9.5",
        "aiohttp-retry~=2.8.3",
        "asyncpg==0.29.0",
        "pydantic~=2.7.4",
        "pydantic-settings~=2.3.3",
        "fastapi~=0.111.0",
    ],
    extras_require={
        "code-quality": [
            "asyncpg-stubs~=0.29.1",
            "black~=24.4.2",
            "flake8~=7.0.0",
            "isort~=5.13.2",
            "mypy~=1.10.0",
            "pylint~=3.2.2",
            "pylint_pydantic~=0.3.0",
            "types-cachetools~=5.3.0.7",
            "types-setuptools~=68.2.0.2",
        ],
    },
    packages=packages,
    package_data={package: ["*.pyi", "py.typed"] for package in packages},
    python_requires=">=3.10",
    keywords="shared",
)
