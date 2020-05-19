from setuptools import setup, find_packages

setup(name="enzona_api",
      version="1",
      description="Enzona's payment platform API access library",
      author="Josué Carballo Baños",
      author_email='josueccb@yandex.com',
      license="GPL 3.0",
      url="https://github.com/JosueCarballo/enzona_api",
      packages=['enzona_api'],
      #packages=find_packages()
      install_requires=["json>=2.0.9", "requests>=2.23.0", "base64>=0.01", "qrcode>=6.1"],
)