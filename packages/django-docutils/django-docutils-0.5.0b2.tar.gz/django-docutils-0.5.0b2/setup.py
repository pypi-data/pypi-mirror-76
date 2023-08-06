# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_docutils',
 'django_docutils.favicon',
 'django_docutils.favicon.management',
 'django_docutils.favicon.management.commands',
 'django_docutils.favicon.rst',
 'django_docutils.favicon.rst.transforms',
 'django_docutils.favicon.tests',
 'django_docutils.favicon.tests.test_app',
 'django_docutils.lib',
 'django_docutils.lib.directives',
 'django_docutils.lib.fixtures',
 'django_docutils.lib.fixtures.directory',
 'django_docutils.lib.fixtures.directory.tests',
 'django_docutils.lib.fixtures.tests',
 'django_docutils.lib.metadata',
 'django_docutils.lib.metadata.tests',
 'django_docutils.lib.roles',
 'django_docutils.lib.templatetags',
 'django_docutils.lib.tests',
 'django_docutils.lib.transforms',
 'django_docutils.pygments',
 'django_docutils.references',
 'django_docutils.references.intersphinx',
 'django_docutils.references.management',
 'django_docutils.references.management.commands',
 'django_docutils.references.rst',
 'django_docutils.references.rst.transforms',
 'django_docutils.rst_post.management',
 'django_docutils.rst_post.management.commands',
 'django_docutils.rst_post.models',
 'django_docutils.rst_post.models.tests',
 'django_docutils.templatetags']

package_data = \
{'': ['*'], 'django_docutils.lib': ['templates/rst/*']}

install_requires = \
['Django>=2.2',
 'django-dirtyfields>1.3.0',
 'django-extensions>=2.2.5,<3.0.0',
 'django-randomslugfield',
 'django-slugify-processor',
 'docutils',
 'lxml',
 'pygments<3']

extras_require = \
{':extra == "favicon"': ['tldextract'],
 ':extra == "favicon" or extra == "intersphinx"': ['tqdm'],
 ':python_version < "3"': ['bitly-api'],
 ':python_version >= "3"': ['bitly-api-py3']}

setup_kwargs = {
    'name': 'django-docutils',
    'version': '0.5.0b2',
    'description': 'Documentation Utilities (Docutils, reStructuredText) for django.)',
    'long_description': '|pypi| |docs| |build-status| |coverage| |license|\n\ndjango-docutils, docutils (reStructuredText) support for Django\n\nDocumentation\n-------------\n\nThe full documentation is at https://django-docutils.git-pull.com.\n\nQuickstart\n----------\n\nInstall django-docutils:\n\n.. code-block:: sh\n\n    pip install django-docutils\n\nTemplate filter\n---------------\n\nIf you want to use the template filter, add it to your ``INSTALLED_APPS``\nin your settings file:\n\n.. code-block:: python\n\n    INSTALLED_APPS = [ # ... your default apps,\n        \'django_docutils\'\n    ]\n\nThen in your template:\n\n.. code-block:: django\n\n    {% load django_docutils %}\n    {% filter restructuredtext %}\n    # hey\n    # how\'s it going\n    A. hows\n    B. it\n\n    C. going\n    D. today\n\n    **hi**\n    *hi*\n    {% endfilter %}\n\n\nTemplate engine (class-based view)\n----------------------------------\n\nYou can also use a class-based view to render restructuredtext.\n\nIf you want to use reStructuredText as a django template engine,\n``INSTALLED_APPS`` *isn\'t* required, instead you add this to your\n``TEMPLATES`` variable in your settings:\n\n.. code-block:: python\n\n    TEMPLATES = [ # .. your default engines\n    {\n        \'NAME\': \'docutils\',\n        \'BACKEND\': \'django_docutils.engines.Docutils\',\n        \'DIRS\': [],\n        \'APP_DIRS\': True,\n    }]\n\nNow django will be able to scan for .rst files and process them. In your\nview:\n\n.. code-block:: python\n\n   from django_docutils.views import DocutilsView\n\n   class HomeView(DocutilsView):\n       template_name = \'base.html\'\n       rst_name = \'home.rst\'\n\n## Settings\n\n\n.. code-block:: python\n\n    BASED_LIB_RST = {  # Optional, automatically maps roles, directives and transformers\n        \'docutils\': {\n            \'raw_enabled\': True,\n            \'strip_comments\': True,\n            \'initial_header_level\': 2,\n        },\n        \'roles\': {\n            \'local\': {\n                \'gh\': \'django_docutils.lib.roles.github.github_role\',\n                \'twitter\': \'django_docutils.lib.roles.twitter.twitter_role\',\n                \'email\': \'django_docutils.lib.roles.email.email_role\',\n            }\n        },\n        \'font_awesome\': {  # Transformer to inject <em class="<class>"></em>\n            \'url_patterns\': {\n                r\'.*github.com.*\': \'fab fa-github\',\n                r\'.*twitter.com.*\': \'fab fa-twitter\',\n                r\'.*amzn.to.*\': \'fab fa-amazon\',\n                r\'.*amazon.com.*\': \'fab fa-amazon\',\n                r\'.*news.ycombinator.com*\': \'fab fa-hacker-news\',\n                r\'.*leanpub.com.*\': \'fab fa-leanpub\',\n                r\'.*python.org.*\': \'fab fa-python\',\n                r\'.*pypi.org.*\': \'fab fa-python\',\n                r\'.*djangoproject.com.*\': \'fab fa-python\',\n                r\'.*wikipedia.org.*\': \'fab fa-wikipedia\',\n                r\'((rtfd|readthedocs).)*$\': \'fab fa-books\',\n                r\'^mailto:.*\': \'fas fa-envelope\',\n                r\'((?!mywebsite.com|localhost).)*$\': \'fas fa-external-link\',\n            }\n        },\n    }\n\n    BASED_LIB_TEXT = {  # Optional\n        \'uncapitalized_word_filters\': [\'project.my_module.my_capitalization_fn\']\n    }\n\n    BASED_ADS = {  # If injecting ads\n        \'AMAZON_AD_CODE\': """\n        <script type="text/javascript">\n        amzn_assoc_placement = "adunit0";\n        amzn_assoc_search_bar = "true";\n        amzn_assoc_tracking_id = "mytracking-20";\n        amzn_assoc_search_bar_position = "bottom";\n        amzn_assoc_ad_mode = "search";\n        amzn_assoc_ad_type = "smart";\n        amzn_assoc_marketplace = "amazon";\n        amzn_assoc_region = "US";\n        amzn_assoc_title = "You may be interested in";\n        amzn_assoc_default_search_phrase = "{keyword}";\n        amzn_assoc_default_category = "All";\n        amzn_assoc_linkid = "6efef5538142e4a4031b04de66b6e804";\n        </script>\n        <script src="//z-na.amazon-adsystem.com/widgets/onejs?MarketPlace=US"></script>\n        """,\n        \'AMAZON_AD_STRIP\': (\n            \'<script src="//z-na.amazon-adsystem.com/widgets/onejs?MarketPlace=US&\'\n            \'adInstanceId=521gc14d-d9f1-4691-8af2-a38de0d0cbad"></script>\'\n        ),\n        \'GOOGLE_AD_CODE\': """\n        <script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js">\n        </script>\n        <ins class="adsbygoogle"\n             style="display:block; text-align:center;"\n             data-ad-layout="in-article"\n             data-ad-format="fluid"\n             data-ad-client="ca-pub-5555555555555555"\n             data-ad-slot="5555555555"></ins>\n        <script>\n             (adsbygoogle = window.adsbygoogle || []).push({});\n        </script>\n        """,\n    }\n\n.. |pypi| image:: https://img.shields.io/pypi/v/django-docutils.svg\n    :alt: Python Package\n    :target: http://badge.fury.io/py/django-docutils\n\n.. |docs| image:: https://github.com/tony/django-docutils/workflows/Publish%20Docs/badge.svg\n   :alt: Docs\n   :target: https://github.com/tony/django-docutils/actions?query=workflow%3A"Publish+Docs"\n\n.. |build-status| image:: https://github.com/tony/django-docutils/workflows/django-docutils%20CI/badge.svg\n   :alt: Build Status\n   :target: https://github.com/tony/django-docutils/actions?query=workflow%3A"django-docutils+CI"\n\n.. |coverage| image:: https://codecov.io/gh/tony/django-docutils/branch/master/graph/badge.svg\n    :alt: Code Coverage\n    :target: https://codecov.io/gh/tony/django-docutils\n\n.. |license| image:: https://img.shields.io/github/license/tony/django-docutils.svg\n    :alt: License \n',
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://django-docutils.git-pull.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
