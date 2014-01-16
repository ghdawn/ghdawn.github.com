---
layout: post
title: "学习Android开发-SVG文件解析"
date: 2012-03-15 18:57
comments: true
categories: [Codes,Linux,Android]
---

我毕业设计的题目是在安卓平台上开发一个工程图的浏览器。需要从服务器中读取用户选择的图纸，并在终端上显示。我所接收到的图纸的类型是SVG格式。

Android并没有直接支持渲染SVG格式，而CodeProject和GitHub上的那些SVG库又都很不靠谱，所以我需要自己解析并绘图。SVG格式的图片是基于XML的，所以图片相当于一个文档，可以用解析XML文档的方式来解析图片。关于SVG图片的详情请见[这里](http://www.w3school.com.cn/svg/svg_intro.asp)

由于SVG是基于XML的，即需要解析的是一个XML文件，所以需要一个*Document*对象。这里我使用了JAVA自带的DOM（Document Object Model）方式解析，所以需要一个*DocumentBuilder*对象来从XML文件中获取DOM文档的实例,然后将解析出的文档传给*Document*对象。而这个*DocumentBuilder*对象的初始化又需要用*DocumentBuilderFactory*的工厂方法。所以初始化的代码如下：

{%codeblock lang:csharp %}
private InputStream _svgFile;
Document doc;
NodeList nList;
public SVGParase(InputStream svgFile) throws SAXException, IOException
{
	_svgFile=svgFile;
	DocumentBuilderFactory dbFactory = DocumentBuilderFactory
	        .newInstance();
	DocumentBuilder dBuilder;
       try
       {
        dBuilder = dbFactory.newDocumentBuilder();
        doc = dBuilder.parse(_svgFile);        
	doc.getDocumentElement().normalize();
       }
       catch (ParserConfigurationException e)
       {
        // TODO Auto-generated catch block
        e.printStackTrace();
       }
}
{% endcodeblock %}

SVG中图形的形式主要有直线段，圆，椭圆，文本等，标签名为polyline，circile，eclipse，text等。所以要解析某一种图形，先查找所有拥有该标签的节点。下面以圆为例：
首先查找有circle标签的结点，其中查到的每一个结点如果类型为element，则它代表了一个圆。每一个圆通过 *圆心坐标和半径* 三个属性来定义，所以在其中查找属性：*cx*,*cy*,*r*即为圆的参数。代码如下：
{%codeblock lang:java %}
public ArrayList<Circle> getCircles()
	{
		ArrayList<Circle> circles=new ArrayList<Circle>(100);
		Circle circle;
		nList = doc.getElementsByTagName("circle");
		for (int temp = 0; temp < nList.getLength(); temp++)
		{

			Node nNode = nList.item(temp);
			
			if (nNode.getNodeType() == Node.ELEMENT_NODE)
			{

				Element eElement = (Element) nNode;
				String cx = eElement.getAttribute("cx");
				String cy = eElement.getAttribute("cy");
				String r = eElement.getAttribute("r");
				circle=new Circle(cx, cy, r);
				circles.add(circle);
			}
		}
		return circles;
	}
{%endcodeblock%}
对于直线等其他的图形，也是同样的解析方式，只要把所有图形存下来就可以绘制了~~
