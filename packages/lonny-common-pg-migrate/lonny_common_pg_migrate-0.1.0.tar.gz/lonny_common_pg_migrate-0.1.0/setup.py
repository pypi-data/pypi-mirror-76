# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lonny_common_pg_migrate']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pg_migrate = lonny_common_pg_migrate.cli:run']}

setup_kwargs = {
    'name': 'lonny-common-pg-migrate',
    'version': '0.1.0',
    'description': 'A CLI for managing postgres DB migrations',
    'long_description': '# `lonny_pg_migrate`\n\nA CLI for managing postgres DB migrations. \n\n## Installation\n\n```bash\npip install lonny_pg_migrate\n```\n\n## Usage\n\nFirst, we must create a `MigrationRunner` object. We can do this like:\n\n```python\nfrom lonny_pg_migrate import MigrationRunner\n\n# Get a \'lonny_pg\' DB connection.\ndb = get_lonny_pg_connection()\n\nrunner = MigrationRunner(db)\n```\n\nTo define a migration, we can simply now do:\n\n```python\n# N.B. sort_key is optional and defaults to the slug.\n@runner.migrate("migration_0", sort_key = "0")\ndef migration_0(db):\n    do_some_action(db)\n```\n\nTo perform the migration, we can either invoke the runner directly using:\n\n```python\n# This will wipe the database\nrunner.drop()\n# This will run - in order of sort_key, all migrations which haven\'t yet run.\nrunner.migrate()\n```\n\nOr via the CLI using:\n\n```bash\npg_migrate path.to.module:runner_var\n```\n\nAs above, `drop` functionality is supported by passing in a `--drop` argument.',
    'author': 'tlonny',
    'author_email': 't@lonny.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lonny.io',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
