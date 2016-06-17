from setuptools import setup
import os
import sys

if sys.version_info[0] < 3:
    from codecs import open

with open(os.path.join(os.path.dirname(__file__), 'README.md'),
          'r', encoding='utf-8') as f:
    long_description = f.read()

    try:
        import pypandoc
        long_description = pypandoc.convert(
                long_description, 'rst', format='md')
    except BaseException as e:
        print(("DEBUG: README in Markdown format. It's OK if you're only "
               "installing this program. (%s)") % e)

setup(
    name='jollanote',
    py_modules=['jollanote'],
    package_data={
        '': [
            'README.md'
        ]
    },
    version='0.0.4',
    author='TylerTemp',
    author_email='tylertempdev@gmail.com',
    url='https://github.com/TylerTemp/jolla-note-cli',
    download_url='https://github.com/TylerTemp/jolla-note-cli/zipball/master/',
    license='MIT',
    description=('Jolla Note app command line interface'),
    keywords='jolla sailfish',
    long_description=long_description,
    install_requires=[
        'docpie'
    ],
    entry_points={
        'console_scripts': [
        'note = jollanote:main'
        ]
    },
    platforms='linux',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Operating System :: Other OS',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        ],
)
