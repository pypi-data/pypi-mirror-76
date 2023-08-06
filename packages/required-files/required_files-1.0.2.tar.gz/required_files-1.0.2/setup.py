#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'required_files',
        version = '1.0.2',
        description = '',
        long_description = 'Simple but effective checking if required externals are present.',
        author = "Steven 'KaReL' Van Ingelgem",
        author_email = 'steven@vaningelgem.be',
        license = 'MIT',
        url = 'https://github.com/svaningelgem/required_files',
        scripts = [],
        packages = ['required_files'],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'BeautifulSoup4',
            'requests'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = 'required files github bitbucket zip',
        python_requires = '',
        obsoletes = [],
    )
