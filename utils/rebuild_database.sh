#!/bin/sh

export PGPASSWORD="test"

psql -h localhost -p 5432 -U librarian -d library -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
psql -h localhost -p 5432 -U librarian <./utils/db.sql
psql -h localhost -p 5432 -U librarian <./utils/insert.sql
