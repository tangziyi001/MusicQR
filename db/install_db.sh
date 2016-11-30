#!/bin/bash

sql_file=musician.sql

set -x

if [ $# -gt 0 ]; then
  case $1 in
    "remove")
      sql_file=remove_musician.sql
      ;;
    *)
      echo "unknown command: $1"
      exit 1
  esac
fi

mysql -u root -p < ${sql_file}
