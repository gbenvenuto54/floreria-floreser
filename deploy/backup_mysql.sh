#!/usr/bin/env bash
set -euo pipefail
# Configurar
DB_NAME="floreria"
DB_USER="root"
DB_PASS="TU_PASSWORD"
BACKUP_DIR="/var/backups/floreria"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"
mysqldump -u"$DB_USER" -p"$DB_PASS" --databases "$DB_NAME" --single-transaction --routines --events | gzip > "$BACKUP_DIR/${DB_NAME}_${DATE}.sql.gz"
# Mantener 14 días
find "$BACKUP_DIR" -type f -name "${DB_NAME}_*.sql.gz" -mtime +14 -delete
