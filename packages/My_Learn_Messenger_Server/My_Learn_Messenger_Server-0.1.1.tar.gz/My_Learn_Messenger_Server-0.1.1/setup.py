from setuptools import setup, find_packages

setup(name="My_Learn_Messenger_Server",
      version="0.1.1",
      description="Learn_GB_Messenger_Server",
      author="Nikolai Nikolaev by GB",
      author_email="nikolaeff2007@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )