title: "学习Android开发-用canvas绘图"
date: 2012-04-06 15:32
comments: true
Tags: Codes,Android,Linux
Category: Study 

接着[上一篇](/blog/2012/03/15/study-android-1/)所说，我们已经从SVG文件中得到了基本图形的定义信息，如圆的圆心坐标与半径，直线段的端点坐标，所以可以开始绘图了。我的想法是，一张SVG图片解析完成后，把所有图片画进一个*Bitmap*里，这样以后所有的对图片的操作都可以用*Android*自带的方法操作，应该会简单一些。*Bitmap*对象需要用工厂方法来创建。创建好空的bitmap后，将它传给一个*Canvas*对象，即可以通过*canvas*的方法，在该bitmap上绘制图形。如下：

        bitmap = Bitmap.createBitmap(1024, 768, Config.ALPHA_8);
        Canvas canvas = new Canvas(bitmap);

####画直线和圆####

*canvas*绘制直线的方法调用方法如下：

        canvas.drawLine(x1, y1, x2, y2, paint);
        
其中`(x1,y1)`,`(x2,y2)`为直线的起始，终止点坐标，*paint*为画笔类型*Paint*的对象，画出来图形的样式由它的参数来决定。这里我只在其中设置了颜色为蓝色。

        paint.setColor(Color.BLUE);
      
绘制圆的方法如下：

        canvas.drawCircle(cx, cy, r, paint);

其中`(cx,cy)`为圆心坐标，`r`为半径。这样画出来的圆是实心的，如果想要空心圆，则需要设置*paint*的类型：

        paint.setStyle(Style.STROKE);
写全一个就是如下：
```java
	public void draw(Canvas canvas)
	{
		// TODO Auto-generated method stub
		Paint paint = new Paint();
		paint.setStyle(Style.STROKE);
		paint.setColor(Color.BLACK);
		canvas.drawCircle(_cx, _cy, _r, paint);
		
	}
```
        

