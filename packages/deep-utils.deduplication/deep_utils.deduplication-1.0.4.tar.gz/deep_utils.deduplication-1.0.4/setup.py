from setuptools import setup, find_namespace_packages

setup(
    name='deep_utils.deduplication',
    version='1.0.4',
    description='Document deduplication package for DEEP',
    long_description_content_type='text/markdown',
    long_description=open('./README.md').read(),
    license="MIT",

    author='Bibek Pandey',
    author_email='bibek.pandey@togglecorp.com',
    url="https://github.com/the-deep/deep-server-utils",

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: General",
        "Topic :: Utilities",
        "Operating System :: OS Independent",
    ],

    packages=find_namespace_packages(),
    install_requires=[
        'boto3==1.9.88',
        'elasticsearch==7.8.1',
        'requests-aws4auth==1.0',
    ],
    zip_safe=False
)
