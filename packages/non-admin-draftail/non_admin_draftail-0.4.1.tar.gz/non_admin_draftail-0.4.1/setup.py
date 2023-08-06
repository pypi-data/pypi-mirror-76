# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['non_admin_draftail', 'non_admin_draftail.templatetags']

package_data = \
{'': ['*'],
 'non_admin_draftail': ['static/non_admin_draftail/draftail/*',
                        'static/non_admin_draftail/fonts/*',
                        'static_src/*',
                        'static_src/src/*',
                        'static_src/src/components/Draftail/*',
                        'static_src/src/components/Draftail/EditorFallback/*',
                        'static_src/src/components/Draftail/EditorFallback/__snapshots__/*',
                        'static_src/src/components/Draftail/Tooltip/*',
                        'static_src/src/components/Draftail/Tooltip/__snapshots__/*',
                        'static_src/src/components/Draftail/__snapshots__/*',
                        'static_src/src/components/Draftail/blocks/*',
                        'static_src/src/components/Draftail/blocks/__snapshots__/*',
                        'static_src/src/components/Draftail/decorators/*',
                        'static_src/src/components/Draftail/decorators/__snapshots__/*',
                        'static_src/src/components/Draftail/sources/*',
                        'static_src/src/components/Draftail/sources/__snapshots__/*',
                        'static_src/src/components/Icon/*',
                        'static_src/src/components/Icon/__snapshots__/*',
                        'static_src/src/components/Modal/*',
                        'static_src/src/components/Portal/*',
                        'static_src/src/components/Portal/__snapshots__/*',
                        'static_src/src/config/*',
                        'static_src/src/sources/EmbedSource/*',
                        'static_src/src/sources/LinkSource/*',
                        'static_src/src/styles/*',
                        'templates/non_admin_draftail/tags/*',
                        'templates/non_admin_draftail/widgets/*']}

setup_kwargs = {
    'name': 'non-admin-draftail',
    'version': '0.4.1',
    'description': 'You can now use Wagtail Draftail editor on non-admin pages',
    'long_description': None,
    'author': 'Tim Kamanin',
    'author_email': 'tim@timonweb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://timonweb.com',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
