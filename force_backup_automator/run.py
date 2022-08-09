from BackupController import BackupController

def main():
    print('----------------Script開始----------------')
    backup_instance = BackupController(org_link="組織リンク", is_headless=1)
    '''
    lightningのリンクは：ORG_URL/lightning/setup/DataManagementExport/home
    classicは：https://YOURDOMAIN.my.salesforce.com/ui/setup/export/DataExportPage/d?setupid=DataManagementExport
    '''
    backup_instance.download_backups(download_location="ダウンロードパス", backup_url="メールに記載しているバックアップリンク", user_name="", password="")
    print('----------------Script完了----------------')

if __name__ == "__main__":
    main()