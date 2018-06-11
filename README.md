## Training Provider Outcomes Toolkit (TPOT) - Transactional Data Store

Transactional database holding pre-aggregated data that services the outcomes warehouse

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Updates](https://pyup.io/repos/github/workforce-data-initiative/tpot-warehouse/shield.svg)](https://pyup.io/repos/github/workforce-data-initiative/tpot-warehouse/)
[![Python 3](https://pyup.io/repos/github/workforce-data-initiative/tpot-warehouse/python-3-shield.svg)](https://pyup.io/repos/github/workforce-data-initiative/tpot-warehouse/)
[![CircleCI](https://circleci.com/gh/workforce-data-initiative/tpot-warehouse.svg?style=shield)](https://circleci.com/gh/workforce-data-initiative/tpot-warehouse)


## Developer Guide

To set up in local development environment:

### Requirements

1. Install Python 3.6.1 as applicable using [_downloads here_](https://www.python.org/downloads)
2. Pip install the virtualenv module

   ```
   python3 -m pip install -U virtualenv
   ```
   
3. Get latest source code from repository

   ```
   git clone https://github.com/workforce-data-initiative/tpot-warehouse.git
   cd tpot-warehouse
   ```

### Setup: Transactional Database

1. Update `sqlite.transactional.database` element in `conf/db.dev.yml` with the absolute path to the location where SQLite database file will be saved.

   _Note: The `.db` file will be created when the migration(s) are run however all parent directories need to exist and current user have w+ permissions on those directories_

3. Create Python virtualenv and install requirements

   ```
   python3 -m venv ${VENV_NAME} ${ENV_DIR}
   . ${ENV_DIR}/bin/activate
   pip install -r requirements.dev.txt
   ```
   
4. Run tests to verify install

   ```
   PYTHONPATH="." pytest -v -s --name transactional --adapter sqlite \
                              --dbconf conf/db.dev.yml tests/test_dbtransactional.py
   ```
   
5. Run migrations to setup local transactional database instance

   ```
   PYTHONPATH='.' alembic -c alembic.ini -n transactional \
                          -x dbconf=conf/db.dev.yml -x adapter=sqlite upgrade head
   ```
   
6. Connect to SQLite instance of transactional database from your database client of choice, using the absolute path set in Step 1
