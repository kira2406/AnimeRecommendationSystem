from setuptools import setup, find_packages

with open("requirements.txt") as file:
    requirements = file.read().splitlines()

setup(
    name="AnimeRecommendationSystem",
    version="0.1",
    author="Kushwanth Parameshwaraiah",
    packages=find_packages(),
    install_requires = requirements
)