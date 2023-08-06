from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="backmusic",
    version="0.3",
    description="back_music_player  Its Extract audio url from video and play in background.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ScRiPt1337/back_music_player",
    author="script1337",
    author_email="anon42237@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["backmusic"],
    include_package_data=True,
    install_requires=["playsound", "argparse", "pynput", "clint", "youtube-dl"],
    entry_points={
        "console_scripts": [
            "backmusic=backmusic.main:main",
        ]
    },
)
