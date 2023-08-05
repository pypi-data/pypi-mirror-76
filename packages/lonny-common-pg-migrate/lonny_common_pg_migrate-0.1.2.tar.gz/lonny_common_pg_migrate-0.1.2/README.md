# `lonny_common_pg_migrate`

A CLI for managing postgres DB migrations. 

## Installation

```bash
pip install lonny_common_pg_migrate
```

## Usage

First, we must create a `MigrationRunner` object. We can do this like:

```python
from lonny_common_pg_migrate import MigrationRunner

# Get a 'lonny_common_pg' DB connection.
db = get_lonny_pg_connection()

runner = MigrationRunner(db)
```

To define a migration, we can simply now do:

```python
# N.B. sort_key is optional and defaults to the slug.
@runner.migrate("migration_0", sort_key = "0")
def migration_0(db):
    do_some_action(db)
```

To perform the migration, we can either invoke the runner directly using:

```python
# This will wipe the database
runner.drop()
# This will run - in order of sort_key, all migrations which haven't yet run.
runner.migrate()
```

Or via the CLI using:

```bash
pg_migrate path.to.module:runner_var
```

As above, `drop` functionality is supported by passing in a `--drop` argument.