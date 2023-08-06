import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dominicus88",  # Replace with your own username
    version="1.1.0",
    author="Marco",
    author_email=None,
    description="The unofficial Notion API extended with the option to sync your Notion events to Google Calendar.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glowingkitty/Notion-Calendar-Sync",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'notion',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib'
    ]
)
