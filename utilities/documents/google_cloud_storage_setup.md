# Google Cloud

## googleCloudStorageサービスアカウントを環境変数に登録

https://cloud.google.com/storage/docs/reference/libraries

### unix

1. `cd`

2. `nano .profile`

3. `export GOOGLE_APPLICATION_CREDENTIALS="/home/{username}/project/filename.json"`

4. *----- Restart PC -----*

### windows

env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\{username}\project\filename.json"


#### command pront
set GOOGLE_APPLICATION_CREDENTIALS="C:\Users\user\project\config\filename.json"

*----- Restart PC -----*
