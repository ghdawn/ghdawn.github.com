Title: "学习在自动控制中应用MATLAB-1"
date: 2012-02-17 17:20
comments: true
Tags: matlab,automatic
Category: Study 

##建立系统传递函数

设系统的传递函数为：
$$
\frac{s+1}{2s^3+3s^2+4s+5}
$$
则在matlab中输入如下命令，可得到其传递函数：   
``` matlab
num=[1 2];den=[2 3 4 5];G=tf(num,den)
 
Transfer function:
         s + 2
-----------------------
2 s^3 + 3 s^2 + 4 s + 5
```

令：
``` matlab
>> G1=tf([1 2],[1 2 3])
 
Transfer function:
    s + 2
-------------
s^2 + 2 s + 3
 
>> G2=tf([1],[1 0])
 
Transfer function:
1
-
s
```

- 如果需要串联两个模块G1，G2，则用命令：   
``` matlab
>>G1*G2
 
Transfer function:
      s + 2
-----------------
s^3 + 2 s^2 + 3 s
```

- 需要并联两个模块G1，G2，则用命令：
``` matlab
>>G1+G2
 
Transfer function:
 2 s^2 + 4 s + 3
-----------------
s^3 + 2 s^2 + 3 s
```       
- 需要反馈链接，则用：
``` matlab
>> G=feedback(G1,G2,-1)
 
Transfer function:
      s^2 + 2 s
---------------------
s^3 + 2 s^2 + 4 s + 2
```
其中-1表示单位负反馈

##判断系统稳定性

设系统传递函数为：
$$
G(s)=\frac{s^3+7s^2+24s+24}{s^8+2s^7+3s^6+4^s5+6s^3+7s^2+8s+9}
$$

在matlab中输入如下命令：

``` matlab
den=[1:9]; %建立特征多项式
roots(den) %求根，通过根的正负判定系统是否稳定

ans =

  -1.2888 + 0.4477i
  -1.2888 - 0.4477i
  -0.7244 + 1.1370i
  -0.7244 - 1.1370i
   0.1364 + 1.3050i
   0.1364 - 1.3050i
   0.8767 + 0.8814i
   0.8767 - 0.8814i
```

由4个极点有正实部可知，系统不稳定。

##求系统响应
$$
G(s)=\frac{s+24}{s^2+4s+9}
$$
新建.m文件，在编辑器里输入：
``` matlab
num=[1 24];
den=[1 4 9];
G=tf(num,den);
t=0:0.1:10;
y=step(G,t);
plot(t,y)
Y=dcgain(G)
```
运行可得结果：

![阶跃响应](/image/2jiestep.png)

###指令解释
- _step_ 给出了系统的阶跃响应，y保存了每个t时刻的响应
- 如果用_impulse()_代替_step_则可求得系统的脉冲响应
- _plot_ 以t为自变量，y为函数值画出图像
- _dcgain_得出系统的稳态值

##绘制跟轨迹
设系统闭环传递函数为：   
$$
\Phi (s)=\frac{K(s+1)(s+3)}{s(s+2)(s+3)+K(s+1)}
$$

特征方程可写为   
$$
1+K\frac{s+1}{s(s+2)(s+3)}=1+K\frac{s+1}{s^3+5s^2+6s}=0
$$
新建.m文件，输入如下语句：

``` matlab
num=[1 1];
den=[1 5 6 0];
G=tf(num,den);
hold on;
rlocus(G);
[K,P]=rlocfind(G)
```
运行可得结果：

![根轨迹](/image/rootlocus.png)

###指令解释
- *hold on* 使得多次次绘图可以在一个Figure窗口中叠加展出
- *rlocus* 绘制给定系统的根轨迹
- *rlocufind* 函数允许用户求取根轨迹上指定点处的开环增益，K为选定点对应的开环增益，P为该增益下的闭环极点位置。

感谢参考书：[《自动控制原理》](http://book.douban.com/subject/1655949/)
