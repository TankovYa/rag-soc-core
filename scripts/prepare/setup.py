from setuptools import setup, find_packages

setup(
    name="hdx-converter",
    version="1.3.0",
    author="HDX Converter Team",
    description="Tool for converting HDX documentation to multiple formats with metadata",
    long_description="""
# HDX Converter

A modular tool for converting HDX documentation to multiple formats (TXT, MD, JSON) with comprehensive metadata extraction. 

## Features

- Extracts content from HDX (HTML) files
- Preserves internal links and navigation
- Generates structured metadata in JSON format (schema 1.2)
- Converts to multiple formats: TXT, Markdown, HTML backup
- Validates metadata completeness
- Handles images and tables
- Provides detailed statistics and reporting
- Modular architecture for easy extension
- Supports hierarchical navigation parsing
- Extracts section structure with proper formatting
- Includes progress bars for long conversions
- Validates required and strictly desirable fields
    """,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hdx-converter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "beautifulsoup4>=4.12.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "lxml>=4.9.0",
        "tqdm>=4.66.0",  # Добавляем для прогресс-баров
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "types-python-slugify>=8.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "hdx-converter=hdx_converter.cli:main",
        ],
    },
    include_package_data=True,
    keywords="hdx documentation converter html markdown metadata",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/hdx-converter/issues",
        "Source": "https://github.com/yourusername/hdx-converter",
        "Documentation": "https://github.com/yourusername/hdx-converter/wiki",
    },
)