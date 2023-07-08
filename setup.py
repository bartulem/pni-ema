from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='pni-ema',
    version='0.1.2',
    author='@bartulem',
    author_email='mimica.bartul@gmail.com',
    classifiers=[
        'Development Status :: Alpha',
        'Intended Audience :: Neuroscientists',
        'Topic :: Ecological Momentary Assessment ',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='neuroscience, psychology, behavior, ecological momentary assessment, survey',
    package_dir={'pni-ema': 'src'},
    include_package_data=False,
    python_requires="==3.10.*",
    description='Scripts to rum the ecological momentary assessment survey',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/bartulem/pni-ema',
    project_urls={
        'Bug Tracker': 'https://github.com/bartulem/pni-ema/issues'
    },
    license='GNU GENERAL PUBLIC LICENSE',
    install_requires=['pandas==2.0.1']
)
