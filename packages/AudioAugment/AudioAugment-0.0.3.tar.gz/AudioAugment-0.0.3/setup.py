import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AudioAugment",
    version="0.0.3",
    author="Wesley Laurence",
    author_email="wesleylaurencetech@gmail.com",
    description="Audio data augmentation tool for machine learning projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wesleyLaurence/Audio-Augment",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = [
		'numpy',
		'pandas',
		'matplotlib',
		'librosa',
		'soundfile',
		'scipy'
	]
)