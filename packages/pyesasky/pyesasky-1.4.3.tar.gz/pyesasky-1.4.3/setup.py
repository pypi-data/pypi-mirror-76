from __future__ import print_function

import os
from glob import glob
from os.path import join as pjoin 

from setupbase import (
    create_cmdclass, install_npm, ensure_targets,
    find_packages,  combine_commands, ensure_python, 
    get_version, HERE
)

from setuptools import setup

name = 'pyesasky'

# Ensure a valid python version
ensure_python('>=2.7')

# Get our version
version = get_version(pjoin(name, '_version.py'))

nb_path = pjoin(HERE, name, 'nbextension', 'static')
lab_path = pjoin(HERE, name, 'labextension') 

# Representative files that should exist after a successful build
jstargets = [
    pjoin(nb_path, 'index.js'),
    pjoin(HERE, 'lib', 'plugin.js'),
    pjoin(HERE, 'lib', 'extension.js'),
]

package_data_spec = {
    'pyesasky': [
        'nbextension/static/*.*js*',
        'nbextension/static/*.html',
        'labextension/*.tgz'
    ]
}

data_files_spec = [
    ('share/jupyter/nbextensions/pyesasky', nb_path, '*.js*'),
    ('share/jupyter/nbextensions/pyesasky', nb_path, '*.css*'),
    ('share/jupyter/nbextensions/pyesasky', nb_path, '*.html'),
    ('share/jupyter/nbextensions/pyesasky', pjoin(HERE, 'lib'),  'extension.js'),
    
    ('share/jupyter/nbextensions/pyesasky/js', pjoin(nb_path, 'js'), '*.js*'),
    
    ('share/jupyter/nbextensions/pyesasky/js/jquery/1.9.1', pjoin(nb_path, 'js', 'jquery', '1.9.1'), '*.js*'),
    ('share/jupyter/nbextensions/pyesasky/js/highcharts/5.0.12', pjoin(nb_path, 'js', 'highcharts', '5.0.12'), '*.js*'),
    ('share/jupyter/nbextensions/pyesasky/js/highcharts/5.0.12/modules', pjoin(nb_path, 'js', 'highcharts', '5.0.12','modules'), '*.js*'),
    ('share/jupyter/nbextensions/pyesasky/js/resizeEvents', pjoin(nb_path, 'js', 'resizeEvents'), '*.js*'),
    ('share/jupyter/nbextensions/pyesasky/js/colorpicker', pjoin(nb_path, 'js', 'colorpicker'), '*.js*'),
    ('share/jupyter/nbextensions/pyesasky/js/colorpicker', pjoin(nb_path, 'js', 'colorpicker'), '*.css'),
    ('share/jupyter/nbextensions/pyesasky/js/sliderSelector', pjoin(nb_path, 'js', 'sliderSelector'), '*.js*'),
    ('share/jupyter/nbextensions/pyesasky/js/sliderSelector', pjoin(nb_path, 'js', 'sliderSelector'), '*.css'),
    ('share/jupyter/nbextensions/pyesasky/js/datepicker', pjoin(nb_path, 'js', 'datepicker'), '*.*'),
    ('share/jupyter/nbextensions/pyesasky/js/xregexp', pjoin(nb_path, 'js', 'xregexp'), '*.js*'),
    ('share/jupyter/nbextensions/pyesasky/js/api', pjoin(nb_path, 'js', 'api'), '*.js*'),
    ('share/jupyter/nbextensions/pyesasky/js/filesaver', pjoin(nb_path, 'js', 'filesaver'), '*.js*'),
    ('share/jupyter/nbextensions/pyesasky/esaskyweb/', pjoin(nb_path, 'esaskyweb'), '*.js*'),
    ('share/jupyter/nbextensions/pyesasky/esaskyweb', pjoin(nb_path, 'esaskyweb'), '*.png'),
    
    ('share/jupyter/nbextensions/pyesasky/images', pjoin(nb_path, 'images'), '*.gif*'),
    ('share/jupyter/nbextensions/pyesasky/images', pjoin(nb_path, 'images'), '*.png*'),
    ('share/jupyter/nbextensions/pyesasky/images', pjoin(nb_path, 'images'), '*.ico*'),
    
    ('share/jupyter/nbextensions/pyesasky/internationalization', pjoin(nb_path, 'internationalization'), '*.xml*'),
    
    ('share/jupyter/nbextensions/pyesasky/css', pjoin(nb_path, 'css'), '*.css*'),
    ('share/jupyter/nbextensions/pyesasky/css/images', pjoin(nb_path, 'css', 'images'), '*.gif*'),
    ('share/jupyter/nbextensions/pyesasky/css/images', pjoin(nb_path, 'css', 'images'), '*.png*'),
    
    ('share/jupyter/nbextensions/pyesasky/esaskyweb/gwt/aladinlite', pjoin(nb_path, 'esaskyweb','gwt','aladinlite'), '*.css*'),
    ('share/jupyter/nbextensions/pyesasky/esaskyweb/gwt/dark', pjoin(nb_path, 'esaskyweb','gwt','dark'), '*.css*'),
    ('share/jupyter/nbextensions/pyesasky/esaskyweb/gwt/dark/images', pjoin(nb_path, 'esaskyweb','gwt','dark','images'), '*.gif*'),
    ('share/jupyter/nbextensions/pyesasky/esaskyweb/gwt/dark/images', pjoin(nb_path, 'esaskyweb','gwt','dark','images'), '*.png*'),
    ('share/jupyter/nbextensions/pyesasky/esaskyweb/gwt/dark/images', pjoin(nb_path, 'esaskyweb','gwt','dark','images'), '*.jpg*'),
    
    
    #('share/jupyter/lab/extensions', lab_path, '*.tgz'),
    ('etc/jupyter/nbconfig/notebook.d' , os.path.join(HERE, 'jupyter.d', 'notebook.d'), 'pyesaky.json'),
    ('etc/jupyter/jupyter_notebook_config.d' , os.path.join(HERE, 'jupyter.d', 'jupyter_notebook_config.d'), 'pyesaky.json')]


cmdclass = create_cmdclass('jsdeps', package_data_spec=package_data_spec,
    data_files_spec=data_files_spec)
cmdclass['jsdeps'] = combine_commands(
    install_npm(HERE, build_cmd='build:all'),
    ensure_targets(jstargets),
    
)


with open("README.md", "r") as fh:
    long_description = fh.read()


setup_args = dict(
    name                    = name,
    description             = 'ESASky Python wrapper',
    version                 = version,  
    scripts                 = glob(pjoin('scripts', '*')),
    cmdclass                = cmdclass,
    long_description        = long_description,
    long_description_content_type = "text/markdown",  
    packages                = find_packages(),
    author                  = 'Fabrizio Giordano <fgiordano@sciops.esa.int>, Mattias Wångblad <mattias@winterway.eu>, ESDC ', 
    #author_email            = 'fgiordano@sciops.esa.int',
    url                     = 'https://github.com/esdc-esac-esa-int/pyesasky',
    license                 = 'GNU Lesser General Public License',
    platforms               = 'Linux, Mac OS X, Windows',
    keywords                = ['ipython','jupyter','widgets'],
    classifiers             = [
        'Development Status :: 5 - Production/Stable',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Multimedia :: Graphics',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    include_package_data    = True,
    data_files=[
        # like `jupyter nbextension install --sys-prefix`
        ("share/jupyter/nbextensions/pyesasky", [
            "pyesasky/nbextension/static/index.js",
        ]),
        # like `jupyter nbextension enable --sys-prefix`
        ("etc/jupyter/nbconfig/notebook.d", [
            "jupyter.d/jupyter_notebook_config.d/pyesasky.json"
        ]),
    ],
    install_requires        = [
        'numpy>=1.9',
        'matplotlib>1.5',
        'astropy>=1.0',
        'requests',
        'beautifulsoup4',
        'python-dateutil',
        'lxml',
        'ipywidgets>=7.5.1',
        'ipykernel>=5.0.0',
        'ipyevents',
        'traitlets',
        'qtpy',
        'flask',
        'flask-cors',
        'six',
        'requests',
        'configparser'
    ],    
    extras_require = {
        'test': [
            'pytest',
            'pytest-cov',
            'nbval',
        ],
        'examples': [
            # Any requirements for the examples to run
        ],
        'docs': [
            'sphinx>=1.5',
            'recommonmark',
            'sphinx_rtd_theme',
            'nbsphinx>=0.2.13',
            'jupyter_sphinx',
            'nbsphinx-link',
            'pytest_check_links',
            'pypandoc',
        ],
    },
    entry_points = {
    },
    zip_safe=False
)

if __name__ == '__main__':
    setup(**setup_args)
