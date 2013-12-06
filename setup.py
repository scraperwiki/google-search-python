from setuptools import setup, find_packages

long_desc = """
Use the Google Custom Search API to search the web from Python.
"""
# See https://pypi.python.org/pypi?%3Aaction=list_classifiers for classifiers

setup(
    name='google-search',
    version='1.0.0',
    description="Use the Google Custom Search API to search the web.",
    long_description=long_desc,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
    ],
    keywords='',
    author='ScraperWiki Limited',
    author_email='feedback@scraperwiki.com',
    url='http://scraperwiki.com',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'requests>=1.2.3',
    ],
    tests_require=[],
    entry_points=\
    """
    """,
)
