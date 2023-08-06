from setuptools import setup, find_packages
import os

version = "0.5.0"

tests_require = [
    "Products.PloneTestCase",
]

setup(
    name="collective.contentrules.mailfromfield",
    version=version,
    description="A Plone content rule for send e-mail to addresses taken from the content",
    long_description=open("README.rst").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.rst")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    keywords="plone rules mail plonegov",
    author="RedTurtle Technology",
    author_email="sviluppoplone@redturtle.it",
    url="http://plone.org/products/collective.contentrules.mailfromfield",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["collective", "collective.contentrules"],
    include_package_data=True,
    zip_safe=False,
    tests_require=tests_require,
    extras_require=dict(test=tests_require),
    install_requires=[
        "setuptools",
        "plone.contentrules",
        # -*- Extra requirements: -*-
    ],
    entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
