from setuptools import setup, find_packages

setup(name="mess_client",
      version="0.8.9",
      description="mess_client",
      author="Ivan Ivanov",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
