import setuptools

with open("README.md", "r") as fh:
    ld = fh.read()

setuptools.setup(
    name="lollygag-cli",
    version="0.0.1",
    author="Philip Woods",
    description="a flexible task manager",
    long_description=ld,
    long_description_content_type="text/markdown",
    keywords='task manager cli tasks ',
    url="https://github.com/pvwoods/lollygag",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.5',
    install_requires=[
        "SQLAlchemy==1.3.18",
        "windows-curses>=2.0;platform_system=='Windows'"
    ],
    entry_points={
        'console_scripts': [
            'lollygag=lollygag.__main__:main'
        ]
    },
)