import setuptools

setuptools.setup(
    name="tweepyauth",
    version="1.0.2",
    author="mocchapi",
    author_email="mocchapi@gmail.com",
    description="A small library to ease tweepy authentication",
    packages=setuptools.find_packages(),
    url="https://gitlab.com/mocchapi/tweepyauth",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)