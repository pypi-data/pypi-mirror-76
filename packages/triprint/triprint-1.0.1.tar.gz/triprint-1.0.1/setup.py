from setuptools import setup

def readme():
    with open('readme.md') as f:
        readme = f.read()
    return readme


setup( name="triprint",
     version="1.0.1",
     description="This package is created by Vikrant Singh. This package is used for printing '*' triangles for desired number of rows.",
     author_email="vikrants298@gmail.com",
     url="https://github.com/vikrantsingh298/Vikrant-s-Stuff/blob/master/triangle_print.py",
     long_description=readme(),
     long_description_content_type="text/markdown",
     author="Vikrant Singh",
     packages=['triprint'],
     install_requires=[ ],
     license="MIT",
     include_package_data=True,
)