from setuptools import setup, find_packages


def read(filename):
    """Read file content."""
    with open(filename) as f:
        return f.read()


name = "gocept.patch_keyreferences"
version = '0.1'


setup(
    name=name,
    version=version,
    author="gocept gmbh & co. kg",
    author_email="mail@gocept.com",
    url='https://github.com/gocept/gocept.patch_keyreferences',
    description="Fix for the comparison of security wrapped keyreferences.",
    long_description=(
        read('README.rst')
        + "\n\n" + read('CHANGES.rst')
    ),
    license="MIT",
    keywords="zodb zope reference fix",
    classifiers=(
        "Topic :: Software Development",
        "Topic :: Database",
        "Framework :: ZODB",
        "Framework :: Zope3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ),
    zip_safe=False,
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['gocept'],
    install_requires=[
        'ZODB',
        'collective.monkeypatcher',
        'zope.security',
    ],
    extras_require={
        'test': [
            'zope.app.catalog[test]',
        ]
    },
)
