import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name='dtlapse',
        version='1.0.0',
        author='Jochen Keil',
        author_email='jochen.keil@gmail.com',
        description='Create smooth timelapse videos with darktable',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://gitlab.com/jochen.keil/dtlapse',
        packages=setuptools.find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Operating System :: OS Independent',
            'Topic :: Artistic Software',
            'Topic :: Multimedia',
            'Topic :: Multimedia :: Video'
            ],
        python_requires='>=3',
        install_requires=[
            'matplotlib>=3.1.1',
            'numpy>=1.16.4',
            'scipy>=1.3.0',
            'attrdict>=2.0.1',
            ],
        package_data={
            'dtlapse': [os.path.join('iops', '*.json')]
            },
        entry_points={
            'console_scripts': [
                'dtlapse=dtlapse.dtlapse:main'
                ],
            },
        )
