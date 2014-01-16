Title: "为OMAP4430安装Linux/Android系统"
date: 2012-02-13 12:33
comments: true
Tags: Codes,嵌入式,Linux
Category: Study 


这块开发板没有板载flash，所以操作系统从SD卡引导。这样，我们的操作系统就需要安装在SD卡上。
##准备sd卡

1. 插入sd卡，运行如下命令察看sd卡是否已经挂载

``` bash
df -h
文件系统            容量  已用  可用 已用%% 挂载点
/dev/sda7              30G   15G   14G  52% /
udev                  1.5G  4.0K  1.5G   1% /dev
tmpfs                 602M  1.1M  601M   1% /run
none                  5.0M     0  5.0M   0% /run/lock
none                  1.5G  472K  1.5G   1% /run/shm
/dev/mmcblk0p1        1.8G   35M  1.7G   3% /media/KINGSTON
```
       
2. 如果已挂载，就卸载它(我的sd卡,设备为/dev/mmcblk0,分区为/dev/mmcblk0p1,挂载在/media/KINGSTON下了）

        sudo umount /media/KINGSTON

##将sd卡格式化成双分区

####先说点别的
如果有兴趣，请仔细阅读[这篇](http://code.google.com/p/beagleboard/wiki/LinuxBootDiskFormat)文档，在网上能找到的所有关于SD双分区的教程，几乎全部和他一样，比如[这里](http://blog.csdn.net/lqf785435771/article/details/7096320)，[这里](http://www.fengfly.com/plus/view-163969-1.html)，和[这里](http://www.anddev.org/zoom-mdk-f25/part-5-booting-x-loader-and-u-boot-from-sd-card-t2500.html)。当然，如果懒得看英文，不看也无妨。我认为其重点如下

1. 记住sd卡的格式化目标格式，即磁头数255，每个磁道上有63个扇区，以及计算出来的柱面数。原文如下：
    #cylinders = FLOOR (the number of Bytes on the SD Card (from above) / 255 / 63 / 512 )
    总的字节数，即运行如下命令，看到的bytes
          
        sudo fdisk /dev/mmcblk0 #换成你的设备，切记是设备不是分区，如mmcblk0p1,或sdb1等为分区，mmcblk0,sdb为设备
         
   这样即可获得这h,s,c这三个参数

2. 第一分区的系统类型的十六进制代码，我已经查过了，可以告诉你是 c (W95 FAT32 (LBA))

有了这两个信息（虽然不知道为什么要这样设定h,s,c这三个信息），有兴趣的同学可以按照上述文章进行格式化。

注意注意！！首先，这些地方写的fdisk命令中，单位都是cylinder，而这是已经废弃了的单位，现在用的都是sector。所以这些文档的内容，都太太太老了，即使文章是新发的。其次，我也不知道为什么，反正我这样做完，没有用，fdisk可以格式化的的sd卡，却不能指定上述信息。所以在格式化完以后，我的开发板不能用这个sd卡启动，会出现这么几个错误：

- 找不到sd卡
- 无法执行MLO
- 执行MLO，找不到分区表

我还是想不通为什么，反正我这样做没有用，不知道他们是怎么做到的，能成功引导。
我很奇怪，这么这么多人都用了这个方法并写了出来，为什么我就是做不成功？

####开始格式化sd卡
我的解决方案是：使用sfdisk，另一个分区程序。用*man*得到的这两个程序的信息差不多，但是fdisk的界面要友好很多，操作也简单，只是，没用。sfdisk的用户界面和操作恶心到了极致，但是将就一下能给我把活干了。

1. 在命令行内执行如下命令，清除sd卡开头的1024个字节（这里似乎存放的分区表，fdisk和sfdisk都不会清除那块信息，但是如果不清空，还是有问题）
         
        sudo dd if=/dev/zero of=/dev/mmcblk0 bs=1024 count=1024 #of后换成你的设备

2. 执行命令，其中h，s，c为上一步说的信息，请提前算好。-D表示支持dos方式。因为要格式的双分区，第一个分区是fat格式的。
        
         sudo sfdisk -D -H 255 -S 63 -C 243 /dev/mmcblk0

3. 这时应该会提示找不到分区（第一步已经清除了），并让你输入分区信息。这里会需要设定四个分区。我们只要前两个分区把空间填满，后两个设置为empty就好了。输入如下
        
        0 9 c * 回车      
        9 (你的c数-9） L 回车          
        回车           
        回车           

4. 解释：此处输入格式为起始柱面，柱面数，系统类型，是否可启动。第一个分区用于引导启动，大小不用太大，于是给了9个柱面的空间，c表示fat32（见上一块），*表示可引导启动。第二个分区使用剩下所有空间，系统类型为Linux。其余的均为空

5. 这样设置完后，会提示是否写入，输入y即可完成设置，得到两个分区mmcblk0p1,mmcblk0p2。如果用USB口的读卡器，则可能是sdb1,sdb2。
6. 输入以下命令，将两个分区格式化。*mkfs.vfat*用于格式化fat系列分区，*-F 32*指定分区表为32位。*-n* 给分区起名字为boot。*mkfs.ext3*用于格式化ext3分区，*-L* 也是起名字(我叫它 linux_fs）
        
        sudo mkfs.vfat -F 32 -n boot /dev/mmcblk0p1          
        sudo mkfs.ext3 -L linux_fs /dev/mmcblk0p2        

至此，最令人头疼的部分就解决了。

在头疼这么久以后，我发现[这里](http://git.openembedded.org/openembedded/tree/contrib/angstrom/omap3-mkcard.sh)有一个脚本可以很好的做完这些事情，只要以管理员身份执行，并将你的设备路径作为第一个参数即可。

##安装系统

###安装Linux
1. 挂载SD卡
2. 在[这里](https://gforge.ti.com/gf/download/frsrelease/387/4170/L24.9-PandaBoard_minimal-fs.tar.gz)下载linux最小系统，并解压缩（可能需要sudo）。
3. 把其中的*boot*文件夹下的*MLO*，*u-boot.bin*,*uImage*复制进boot分区
        
        sudo cp boot/* /media/boot/        
        
4. 把*angstrom_minimal-fs*内的文件和文件夹复制进第二个分区 *linux_fs* （可能需要sudo）
        
        sudo cp -rf angstrom/* /media/linux_fs        
        
5. 刷新文件缓冲，确认文件都已经复制进去（如果不执行这句，有可能文件没拷进分区内）
        
        sync        

6. 把卡插进开发板，开机实验吧！

###安装Android

其实方法都一样，只是格式化的时候建议把第二个分区名字改成类似android_fs之类的好认的名字，并且在[这里](http://code.google.com/p/pandroid/downloads/list)下载android文件系统，其余操作同上。
