import re, os
m='android/app/src/main/AndroidManifest.xml'
s=open(m).read()
aid=open('admob_app_id.txt').read().strip()
if 'APPLICATION_ID' not in s:
 s=s.replace('</application>',f'<meta-data android:name="com.google.android.gms.ads.APPLICATION_ID" android:value="{aid}"/></application>')
s=s.replace('<activity','<activity android:screenOrientation="sensorLandscape" ',1)
open(m,'w').write(s)
for st in ['android/app/src/main/res/values/styles.xml','android/app/src/main/res/values/themes.xml']:
 if os.path.exists(st):
  t=open(st).read()
  t=re.sub(r'(<style name="AppTheme.NoActionBar"[^>]*>)',r'\1\n<item name="android:windowFullscreen">true</item>',t,count=1)
  open(st,'w').write(t)
print('manifest dan tema dipatch '+aid)
