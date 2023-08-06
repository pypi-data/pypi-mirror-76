from distutils.core import setup
setup(
    name='pystickmover',
    packages=['pystickmover'],
    version='0.1',
    license='MIT',
    description='Python library for controlling AVIrem StickMover',
    author='Nicholas Robinson',
    author_email='me@nicholassavilerobinson.com',
    url='https://github.com/nicholasrobinson/pystickmover',
    download_url='https://github.com/nicholasrobinson/pystickmover/archive/v_01.tar.gz',
    keywords=['AVIrem', 'StickMover', 'Python', 'Library'],
    install_requires=[
        'pyserial',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
