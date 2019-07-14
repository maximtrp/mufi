from setuptools import setup
from os.path import join, dirname

setup(name='mufi',
        version='0.1.0',
        description='Mufi: simple music finder for command-line',
        long_description=open(join(dirname(__file__), 'README.md')).read(),
        long_description_content_type='text/markdown',
        url='http://github.com/maximtrp/mufi',
        author='Maksim Terpilowski',
        author_email='maximtrp@gmail.com',
        license='BSD',
        packages=['mufi'],
        keywords='python music cli',
        install_requires=['selenium'],
        entry_points = {
            'console_scripts': ['mufi=mufi.mufi:main',
                                'mufi-recs=mufi.mufi_recs:main'],
        },
        classifiers=[
		'Development Status :: 3 - Alpha',

		'Intended Audience :: Information Technology',
		'Intended Audience :: End Users/Desktop',

		'Topic :: Home Automation',
		'Topic :: Internet',
		'Topic :: Text Processing :: General',

		'License :: OSI Approved :: BSD License',

		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
	    ],
        zip_safe=False)
