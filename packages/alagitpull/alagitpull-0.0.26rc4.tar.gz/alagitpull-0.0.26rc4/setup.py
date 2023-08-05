# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alagitpull', 'alagitpull.writers']

package_data = \
{'': ['*'], 'alagitpull': ['static/*']}

install_requires = \
['alabaster<0.8']

entry_points = \
{'console_scripts': ['sphinx_themes = alagitpull:get_path'],
 'sphinx_themes': ['alagitpull = alagitpull:get_path']}

setup_kwargs = {
    'name': 'alagitpull',
    'version': '0.0.26rc4',
    'description': 'Cleverly-named alabaster sub-theme for git-pull projects',
    'long_description': '=====================\ngit-pull sphinx theme\n=====================\n\n`Sphinx`_ sub-theme of `Alabaster`_, for use on git-pull projects.\n\nWhat alagitpull adds to Alabaster\n---------------------------------\n\nSee the theme live on https://www.git-pull.com,\nhttps://tmuxp.git-pull.com, etc.\n\n- Table CSS tweaks\n- ``<pre>`` and code-block css tweaks\n- Additional theming tweaks for `admonitions`_ like ``..note``.\n- New sidebar template with links to projects\n\n  - Automatic unlinking of project if its the current docs\n  - Support for subprojects (put into parenthesis)\n- Sidebar CSS tweaks\n\nConfig options\n--------------\n\nTheme variables\n"""""""""""""""\n\nTo see a full list of options passible to HTML templates, see\n``theme.conf``. Not all of these options are used in the theme itself,\nbut to let ``html_theme_options`` pass them through, if you want.\n\nTo configure, *conf.py*:\n\n*html_theme_options* example:\n\n.. code-block:: python\n\n   html_theme_options = {\n       \'logo\': \'img/logo.svg\',\n       \'github_user\': \'git-pull\',\n       \'github_repo\': \'alagitpull\',\n       \'github_type\': \'star\',\n       \'github_banner\': True,\n       \'projects\': {},\n       \'project_name\': \'my project name\',\n   }\n\nFor an example of ``html_theme_options[\'projects\']`` see the\n*alagitpull/__init__.py* file.\n\nExample of using an optional variable such as\n``theme_show_meta_app_icons_tags``:\n\n.. code-block:: python\n\n   html_theme_options = {\n       # ...usual stuff, as above, and\n       \'project_description\': \'description of project\'\n   }\n\n\n.. code-block:: html\n\n   {%- if theme_show_meta_app_icon_tags == true %}\n   <meta name="theme-color" content="#ffffff">\n   <meta name="application-name" content="{{ theme_project_description }}">\n\n   <link rel="shortcut icon" href="/_static/favicon.ico">\n   <link rel="icon" type="image/png" sizes="512x512" href="/_static/img/icons/icon-512x512.png">\n   <link rel="icon" type="image/png" sizes="192x192" href="/_static/img/icons/icon-192x192.png">\n   <link rel="icon" type="image/png" sizes="32x32" href="/_static/img/icons/icon-32x32.png">\n   <link rel="icon" type="image/png" sizes="96x96" href="/_static/img/icons/icon-96x96.png">\n   <link rel="icon" type="image/png" sizes="16x16" href="/_static/img/icons/icon-16x16.png">\n\n   <!-- Apple -->\n   <meta name="apple-mobile-web-app-title" content="{{ theme_project_name }}">\n\n   <link rel="apple-touch-icon" sizes="192x192" href="/_static/img/icons/icon-192x192.png">\n   <link rel="mask-icon" href="/_static/img/{{ theme_project_name }}.svg" color="grey">\n\n   <!-- Microsoft -->\n   <meta name="msapplication-TileColor" content="#ffffff">\n   <meta name="msapplication-TileImage" content="/_static/img/icons/ms-icon-144x144.png">\n   {% endif -%}\n\n\nVariables\n"""""""""\n\n*alagitpull_external_hosts_new_window* (boolean, default: False): check if link \nis external domain/IP. If so, open in new window.\n\n.. code-block:: python\n\n   alagitpull_external_hosts_new_window = True\n\n*alagitpull_internal_hosts* (list) - whitelist of domains to open\nin same tab, *without* ``target="_blank"``. Only used if\n*alagitpull_external_hosts_new_window* enabled.\n\nExample:\n\n.. code-block:: python\n\n   alagitpull_internal_hosts = [\n      \'libtmux.git-pull.com\',\n      \'0.0.0.0\',\n   ]\n\nTheme options\n-------------\n\n``html_theme_options`` of sphinx\'s conf.py:\n\n- *projects* (dict) - Sidebar links.    \n- *project_name* (string) - Name of your project (helps with unlinking\n\n\n.. _Sphinx: http://www.sphinx-doc.org/\n.. _Alabaster: https://github.com/bitprophet/alabaster\n.. _admonitions: http://docutils.sourceforge.net/docs/ref/rst/directives.html#admonitions\n',
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/git-pull/alagitpull',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
