# force-backup-automator-jp

## これは何?
forked from stefanzepeda/force-backup-automator

## 使い方
run.pyにmain関数を実装する   
```
backup_instance = BackupController(org_link="組織リンク(my domain)", is_headless=0)
backup_instance.download_backups(download_location="ダウンロードパス", backup_url="メールに記載しているバックアップリンク", user_name="", password="")
```

