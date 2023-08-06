###########
Quick Hand
###########

快速的仿手写文字的图片生成器。基于 https://github.com/Gsllchb/Handright/ 的 GUI。

它是开源的，你可以免费使用它。下载请到 release 界面。

目前在两个仓库更新：

- https://github.com/HaujetZhao/QuickHand
- https://gitee.com/haujet/QuickHand

关于软件参数的帮助，你可以参照：https://github.com/Gsllchb/Handright/blob/master/docs/tutorial.md


###########
原理
###########

原理：首先，在水平位置、竖直位置和字体大小三个自由度上，对每个字的整体做随机扰动。随后，在水平位置、竖直位置和旋转角度三个自由度上，对每个字的每个笔画做随机扰动。