from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='rotate-codepipeline-tokens',
    version='0.1.0',
    author='Peter Helewski',
    author_email='peter.helewski@stelligent.com',
    description='A utility for rotating GitHub Tokens for use in CodePipeline.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/phelewski/rotate-codepipeline-tokens',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['boto3', 'requests'],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'rotate-codepipeline-tokens=rotate_codepipeline_tokens.main:main'
        ]
    }
)