from setuptools import setup

def readme():
    with open('readme.md') as f:
        readme = f.read()
    return readme


setup( name="packagevikrant",
     version="1.3",
     description="This code is written by Vikrant Singh.",
     long_desription=readme(),
     long_description_content_type="text/markdown",
     author="Vikrant Singh",
     packages=['packagevikrant'],
     install_requires=['pyttsx3'],
     license="MIT",
     include_package_data=True,
)