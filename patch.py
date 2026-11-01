import re,os
from PIL import Image,ImageDraw
R='android/app/src/main/'
# 1) manifest: ID AdMob + landscape
m=R+'AndroidManifest.xml';s=open(m).read()
aid=open('admob_app_id.txt').read().strip()
if 'APPLICATION_ID' not in s:
    s=s.replace('</application>','<meta-data android:name="com.google.android.gms.ads.APPLICATION_ID" android:value="%s"/></application>'%aid)
s=s.replace('<activity','<activity android:screenOrientation="sensorLandscape"',1)
open(m,'w').write(s)
# 2) tema layar penuh
st=R+'res/values/styles.xml';t=open(st).read()
t=re.sub(r'(<style name="AppTheme.NoActionBar"[^>]*>)',r'\1<item name="android:windowFullscreen">true</item>',t,count=1)
open(st,'w').write(t)
# 3) ikon aplikasi dari icon.png
base=Image.open('icon.png').convert('RGBA')
for d,(a,f) in {'mdpi':(48,108),'hdpi':(72,162),'xhdpi':(96,216),'xxhdpi':(144,324),'xxxhdpi':(192,432)}.items():
    p=R+'res/mipmap-'+d+'/';os.makedirs(p,exist_ok=True)
    base.resize((a,a),Image.LANCZOS).save(p+'ic_launcher.png')
    r=base.resize((a,a),Image.LANCZOS);mk=Image.new('L',(a,a),0);ImageDraw.Draw(mk).ellipse((0,0,a-1,a-1),fill=255);r.putalpha(mk);r.save(p+'ic_launcher_round.png')
    fg=Image.new('RGBA',(f,f),(0,0,0,0));sz=int(f*.64);fg.paste(base.resize((sz,sz),Image.LANCZOS),((f-sz)//2,(f-sz)//2));fg.save(p+'ic_launcher_foreground.png')
os.makedirs(R+'res/values',exist_ok=True)
open(R+'res/values/ic_launcher_background.xml','w').write('<?xml version="1.0" encoding="utf-8"?><resources><color name="ic_launcher_background">#0B1230</color></resources>')
os.makedirs(R+'res/mipmap-anydpi-v26',exist_ok=True)
for n in ('ic_launcher','ic_launcher_round'):
    open(R+'res/mipmap-anydpi-v26/%s.xml'%n,'w').write('<?xml version="1.0" encoding="utf-8"?><adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/ic_launcher_background"/><foreground android:drawable="@mipmap/ic_launcher_foreground"/></adaptive-icon>')
# 4) layar penuh sungguhan (sembunyikan bar sistem)
d=R+'java/com/gembox/app/';os.makedirs(d,exist_ok=True)
open(d+'MainActivity.java','w').write('''package com.gembox.app;
import android.os.Build;
import android.os.Bundle;
import android.view.WindowManager;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import com.getcapacitor.BridgeActivity;
public class MainActivity extends BridgeActivity {
  @Override public void onCreate(Bundle b){super.onCreate(b);hide();}
  @Override public void onWindowFocusChanged(boolean f){super.onWindowFocusChanged(f);if(f)hide();}
  private void hide(){
    WindowCompat.setDecorFitsSystemWindows(getWindow(),false);
    WindowInsetsControllerCompat c=WindowCompat.getInsetsController(getWindow(),getWindow().getDecorView());
    c.setSystemBarsBehavior(WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
    c.hide(WindowInsetsCompat.Type.systemBars());
    if(Build.VERSION.SDK_INT>=28){WindowManager.LayoutParams lp=getWindow().getAttributes();lp.layoutInDisplayCutoutMode=WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;getWindow().setAttributes(lp);}
  }
}
''')
print('patch selesai')
