from setuptools import setup, find_packages

setup(
    name="asteriskinterfacelogger",
    version="0.6",
    packages=find_packages(),
    author="Juares Vermelho Diaz (CL3k)",
    author_email="jvermelho@cl3k.com",
    description="Common log configuration for Asterisk Interface microservices",
    keywords="AsteriskInterface log logger logging",
    # package_data={"asteriskinterfacelogger": ["logging.conf"],},
    install_requires=["python3-logstash", "python-json-logger"],
    # url="http://example.com/HelloWorld/",   # project home page, if any
    # project_urls={
    #     "Bug Tracker": "https://bugs.example.com/HelloWorld/",
    #     "Documentation": "https://docs.example.com/HelloWorld/",
    #     "Source Code": "https://code.example.com/HelloWorld/",
    # },
)
