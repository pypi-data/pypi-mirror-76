from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    setup(
        name="tabledbmapper",
        version="0.2.1",
        description=(
            "General query tool class of relational database."
        ),
        keywords="sql orm",
        long_description=open('README.md', 'r').read(),
        long_description_content_type="text/markdown",
        author='lyoshur',
        author_email='1421333878@qq.com',
        maintainer='lyoshur',
        maintainer_email='1421333878@qq.com',
        license='MIT License',
        packages=find_packages(),
        platforms=["ubuntu", 'windows'],
        url='https://github.com/lyoshur/tabledbmapper',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Operating System :: OS Independent',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: Implementation',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Topic :: Software Development :: Libraries'
        ],
        install_requires=[
            'Jinja2',
        ],
        zip_safe=False
    )
