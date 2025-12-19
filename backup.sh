#!/bin/bash
#
backupDir=("/opt" "/home/ec2-user")
backupTarget=/tmp/backup
# Создадим директорию для архивов
mkdir -p $backupTarget

for dir in "${backupDir[@]}"; 
do
  backupFile="$backupTarget/$(basename "$dir")-backup-$(date +%Y-%m-%d).tar.gz"
  tar -czf  "$backupFile" "$dir"
done


