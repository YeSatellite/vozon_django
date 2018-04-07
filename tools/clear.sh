#!/usr/bin/env bash
find . -path "../apps/*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "../apps/*/migrations/*.pyc"  -delete
rm ../db.sqlite3