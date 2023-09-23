# 屏幕监控
  截取电脑屏幕图片发送到群聊

## 打包脚本
```bash
# pyinstaller --onefile --paths=D:\Python\ --hidden-import=pytz --add-data='D:\Python\Lib\site-packages\pytz\;.' .\main.py
  pyinstaller -F -D --add-data='./config.yml;.' .\main.py
--paths=D:\env\Lib\site-packages
pyinstaller --onefile --paths=D:\Python\ --hidden-import=pytz --add-data='D:\Python\Lib\site-packages\pytz\;.' --paths=D:\Python  .\main.py
pyinstaller -F --paths=D:\Python\ --hidden-import=pytz --add-data='D:\Python\;.' --paths=D:\Python  -D .\main.py
```
