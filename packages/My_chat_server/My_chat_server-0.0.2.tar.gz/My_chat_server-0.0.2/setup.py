from setuptools import setup, find_packages

setup(name="My_chat_server",
      version="0.0.2",
      description="My_chat_server",
      author="Sergey Sergeev",
      author_email="ss2576@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )