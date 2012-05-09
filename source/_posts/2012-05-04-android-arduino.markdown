---
layout: post
title: "使用单片机Arduino(AVR)与Android设备通讯"
date: 2012-05-04 21:57
comments: true
categories: [Codes,Linux,Android,嵌入式]
---

###简述需求
现在的Android设备，像手机，平板等，有很多的资源，比如照相机，音箱等,同时CPU已经很好，运算能力很强。功能十分丰富，但是必须得人手操控才能使用。这么丰富的资源，如果能自动做点事情，或者作为一个控制核心控制其它的东西就更好了，所以Google官方提供了一种方法，将Android设备按附件模式与一个有[USB Host](http://baike.baidu.com/view/1402520.htm?fromTaglist)的设备相连，两者通过USB接口相连传输数据，从而实现通过单片机操控手机。（[USB](http://zh.wikipedia.org/zh-cn/USB)是主从结构的总线，这里要求Android设备作为从机，单片机作为主机，而一般的开发板附带的usb口都是client，如果需要做这个实验，则需要买[有USB Host的开发板](http://item.taobao.com/item.htm?id=12892248805)，或者买专门的 USB host shield模块放在开发板上。）

在这里，Google要求Android平台的版本至少为2.3.3，单片机要求实现了*Android Accessory Protocol*协议。其中Google官方支持了一个开源硬件平台[Arduino](http://www.arduino.cc/)。现阶段，Android只能支持一个USB设备，不过能满足大部分需求了。

Google官方提供了一个简洁的教程（[Arduino](http://developer.android.com/guide/topics/usb/adk.html)部分，与[Android](http://developer.android.com/guide/topics/usb/accessory.html)部分，以及一份代码示例（包括Android与Arduino部分，在对应的网页里下）。但是教程过于简洁而示例过于复杂：直接按照教程做，很多地方无从下手。按照代码改，代码结构又过于复杂，依然不好下手。于是我在这里耽误了一天多的时间。

###Arduino部分
1. 在[Arduino](http://www.arduino.cc/)下载最新的IDE，它是用JAVA开发的，跨平台。同时几乎所有底层的驱动全部写好，开发的时候只要调用即可，完全感觉不到是在开发单片机，实在很爽。
2. 下载[Google 提供的协议实现代码](https://dl-ssl.google.com/android/adk/adk_release_0512.zip)。解压出来后，将*firmware/arduino_libs/*下的*AndroidAccessory*和*USB_Host_Shield*复制到*Arduino IDE*的*libraries*目录下。这两个分别是Android附件协议的实现和USB的驱动。
3. 如果按照教程，现在只需要打开*firmware/demokit/demokit.pde*并烧写进开发板，就可以和教程配套的Android程序进行通讯并控制电机之类的驱动了。
4. 但是自己做开发的话就不要用上面的代码了，太复杂太麻烦。在IDE里新建一个文件，包含*USB*驱动和*AndroidAccessory*的头文件，并新建一个*AndroidAccessory*对象，比如叫acc。在*setup()*函数中，调用acc.powerOn()方法，即可开始试探链接Android设备。
5. 在我的应用中，我需要做的是把Android设备中计算的结果以串口的形式发给飞控模块，所以我只需要不断的把Android设备发送来的数据发给串口，再把串口接受到的数据发给Android设备。于是，代码如下：

{% codeblock lang:cpp %}

#include <Usb.h>
#include <AndroidAccessory.h>



AndroidAccessory acc("BuaaITR",
		     "Demo",
		     "DemoKit Arduino Board",
		     "1.0",
		     "http://www.android.com",
		     "0000000012345678");


void setup()
{
	Serial.begin(115200);
	Serial.print("\r\nStart");

	acc.powerOn();
}

void loop()
{
	
	byte msg[1024];
	
	if (acc.isConnected()) 
        {
                while(Serial.available()>0)
                {
                  msg[0]=Serial.read();
                  acc.write(msg,1);
                }
                int len = acc.read(msg, sizeof(msg), 1);
                if (len > 0) 
                {
                  Serial.write(msg,len);
                }
        }
	delay(200);
}

{% endcodeblock%}

#####一些解释
按照这样的方法，单片机这部分就很容易能搞定了，只要Android程序写好了，两个就能匹配工作了。

- Arduino简化了开发流程，去掉了主函数，只留下 *setup()*作为初始化，*loop()*不断循环。所以把初始化的部分写在*setup()*里，工作的部分写在*loop()*中。  
- *AndroidAccessory*对象的构造函数有6个参数，分别为：设备制造商，设备模型，设备描述，设备版本，网址和序列号。其中制造商，模型和版本必须与Android设备上的软件匹配。即开发Android设备上运行的软件时，也需要制定这三个参数，只有这三个参数相同的设备才能互相连接。  
- 调用*acc.powerOn();*来使单片机开始工作  
- 单片机与Android设备不一定会匹配，所以需要*acc.isConnected()*判断是否已经成功的连接。  
- 读写方法分别为`acc.write(char* msg,int length)` 和`acc.read(char* msg,int length ,int nakLimit)`。其中msg和length分别为存放数据的数组和期望读写的数据长度。读取函数的第三个参数*nakLimit*，目前我在网上还没找到有人知道是做什么用的，反正设为1就能用。   

###Android部分
首先声明，这里我是参考了Google的官方文档，同时在Google给的示例代码中改成的，代码已经十分精简，可以直接修改以完成所需的任务。如果有时间，完全可以读Google的代码，从那一大堆代码里修改。  
操作USB的时候，SDK版本为*2.3.3，即API 10*时是一种操作，版本为那之上的是另一种操作。*API 10*需要装[add-on library](http://code.google.com/android/add-ons/google-apis/installing.html)，我用的是*API 10*。


要想使*Accessory*工作，需要在*AndroidManifest.xml*中声明支持*UsbManager.ACTION_USB_ACCESSORY_DETACHED*，并添加一个过滤器，来过滤设备。如下：
{%codeblock lang:xml%}
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="me.ghdawn"
    android:versionCode="1"
    android:versionName="1.0" >

    <uses-feature android:name="android.hardware.usb.accessory" />

    <uses-sdk android:minSdkVersion="10" />

    <application
        android:icon="@drawable/ic_launcher"
        android:label="@string/app_name" >
        <uses-library android:name="com.android.future.usb.accessory" />

        <activity
            android:name=".UsbAccActivity"
            android:label="@string/app_name" >
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.hardware.usb.action.USB_ACCESSORY_ATTACHED" />
            </intent-filter>

            <meta-data
                android:name="android.hardware.usb.action.USB_ACCESSORY_ATTACHED"
                android:resource="@xml/accessory_filter" />
        </activity>
    </application>

</manifest>
{%endcodeblock%}
#####一些说明
- *API 10*使用的是*Addon library*,需要注明：*<uses-library android:name="com.android.future.usb.accessory" />*  
- 要说明支持*USB_ACCESSORY_ATTACHED*模式，所以加上

        <intent-filter>
                <action android:name="android.hardware.usb.action.USB_ACCESSORY_ATTACHED" />
        </intent-filter>

- 可能会有很多USB接口的设备，所以我们还需要筛选一下此程序能接的单片机，所以增加一个*accessory_filter.xml*来筛选设备。在*res*文件夹下新建文件夹*xml*，在其中新建文件*accessory_filter.xml*，在这里增加需要的单片机的条件。

         <meta-data
                android:name="android.hardware.usb.action.USB_ACCESSORY_ATTACHED"
                android:resource="@xml/accessory_filter" />

上面这段代码就是注册这个筛选器的。下面这段就是筛选器的内容。还记得上面的*Arduino*部分中，新建的*AndroidAccessory*对象吗？那里的第1，2，4个参数正是这里筛选的参数。只有这几个参数匹配的设备才能建立连接。当然，这里筛选条件是可以选的，那几个参数都可以作为筛选条件，只要加在下面就可以。

{%codeblock lang:xml%}
<?xml version="1.0" encoding="utf-8"?>

<resources>
    <usb-accessory manufacturer="BuaaITR" model="Demo" version="1.0" />
</resources>

{%endcodeblock%}

注：下文的所有*设备*一词，均指代*Arduino设备*，程序则代表*Android设备*。  
这样，就可以开始写代码了。首先需要一个*UsbManager*对象来管理USB设备，需要一个广播接收器，当系统有广播时，来判断是否为USB附件，并询问是否提供权限。广播的过滤器使用*UsbManager.ACTION_USB_ACCESSORY_DETACHED*作为*action*。当接受到一个满足过滤条件的广播时，并且获得了访问的权限，就可以获得该设备的信息，并进行读写了。

广播接收器的代码：
{%codeblock lang:java%}
private final BroadcastReceiver mUsbReceiver = new BroadcastReceiver()
	{
		@Override
		public void onReceive(Context context, Intent intent)
		{
			String action = intent.getAction();
			if (ACTION_USB_PERMISSION.equals(action))
			{
				synchronized (this)
				{
					UsbAccessory accessory = UsbManager.getAccessory(intent);
					if (intent.getBooleanExtra(
					        UsbManager.EXTRA_PERMISSION_GRANTED, false))
					{
						openAccessory(accessory);
					}
					else
					{
						Log.d(TAG, "permission denied for accessory "
						        + accessory);
					}
					mPermissionRequestPending = false;
				}
			}
			else if (UsbManager.ACTION_USB_ACCESSORY_DETACHED.equals(action))
			{
				UsbAccessory accessory = UsbManager.getAccessory(intent);
				if (accessory != null && accessory.equals(mAccessory))
				{
					closeAccessory();
				}
			}
		}
	};
{%endcodeblock%}

建立连接：


{%codeblock lang:java%}
	private void openAccessory(UsbAccessory accessory)
	{
		mFileDescriptor = mUsbManager.openAccessory(accessory);
		if (mFileDescriptor != null)
		{
			mAccessory = accessory;
			//获得该设备的输入输出流
			FileDescriptor fd = mFileDescriptor.getFileDescriptor();
			mInputStream = new FileInputStream(fd);
			mOutputStream = new FileOutputStream(fd);
			//是否能对设备进行读写操作
			canIO = true;
			//定时查询是否有数据可以接收
			timer.scheduleAtFixedRate(new TimerTask()
			{
				@Override
				public void run()
				{
					// TODO Auto-generated method stub
					int length = 0;
					byte[] buffer = new byte[maxBuffer];
					try
					{
						//如果有数据来，则接受数据。
						if(mInputStream.available()>0)
						{
							length=mInputStream.read(buffer);
							//处理接收到的数据，按需要自己改。
							usbuart.onReceive(buffer);
						}

					}
					catch (IOException e)
					{
						// tbhello.setText("IO error\n" + e.getMessage());

					}

				}
				
			}, 0, delaytime);
			Log.d(TAG, "accessory opened");

		}
		else
		{
			Log.d(TAG, "accessory open fail");
		}
	}
{%endcodeblock%}
这样，大部分功能就实现完了，现在需要注册广播接收器，并让程序监视USB设备。

{%codeblock lang:java%}
	@Override
	public void onCreate(Bundle savedInstanceState)
	{
		super.onCreate(savedInstanceState);
		//使用add-on library时，必须这样定义usbmanager对象
		mUsbManager = UsbManager.getInstance(this);
		mPermissionIntent = PendingIntent.getBroadcast(this, 0, new Intent(
		        ACTION_USB_PERMISSION), 0);
		//注册接收器和过滤器
		IntentFilter filter = new IntentFilter(ACTION_USB_PERMISSION);
		filter.addAction(UsbManager.ACTION_USB_ACCESSORY_DETACHED);
		registerReceiver(mUsbReceiver, filter);

		setContentView(R.layout.main);

	}

	@Override
	public void onResume()
	{
		super.onResume();

		Intent intent = getIntent();
		//如果已经打开了一个设备，就不再查询
		if (mInputStream != null && mOutputStream != null)
		{
			return;
		}
		//只能支持一个设备，如果发现了一个USB设备并且有权限访问，就打开
		UsbAccessory[] accessories = mUsbManager.getAccessoryList();
		UsbAccessory accessory = (accessories == null ? null : accessories[0]);
		if (accessory != null)
		{
			if (mUsbManager.hasPermission(accessory))
			{
				openAccessory(accessory);
			}
			
		}
		else
		{
			Log.d(TAG, "mAccessory is null");
		}
	}

	@Override
	public void onPause()
	{
		super.onPause();
		closeAccessory();
	}

	@Override
	public void onDestroy()
	{
		unregisterReceiver(mUsbReceiver);
		super.onDestroy();
	}
{%endcodeblock%}

如果需要发送数据，就这样：
{%codeblock lang:java%}
    public void send(byte[] data)
    {
	    if(canIO)
	    {
	    	try
            {
	            mOutputStream.write(data);
            }
            catch (IOException e)
            {	
	            // TODO Auto-generated catch block
	            e.printStackTrace();
            }
	    }
    }
    {%endcodeblock%}  
用到的对象如下：
{%codeblock lang:java%}
private static final String TAG = "DemoKit";

	private static final String ACTION_USB_PERMISSION = "com.google.android.DemoKit.action.USB_PERMISSION";

	private UsbManager mUsbManager;
	private PendingIntent mPermissionIntent;


	private int maxBuffer=1024;
	private boolean canIO = false;
	UsbAccessory mAccessory;
	ParcelFileDescriptor mFileDescriptor;
	FileInputStream mInputStream;
	FileOutputStream mOutputStream;

	Timer timer = new Timer();
{%endcodeblock%}  

如果步骤没出错的话，至此，把Arduino开发板插到Android设备上，应该就能互相传数据了。
