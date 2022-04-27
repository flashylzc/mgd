# 工学云/蘑菇丁自动打卡
## 此项目仅供学习参考，请勿用于非法行为，本人概不负责
### 本项目所设置的定时运行时间为每天10:30左右

将config.yaml文件中的信息改成自己需要签到的位置信息

这里推荐使用[高德地图api][api]查询坐标

然后点击右边Setting，下拉选到Secrets，点击Actions，然后点击右边的New repository secret
将蘑菇丁的账号密码分别添加到secret。请严格按照下图中的命名方式填写！

![image](https://user-images.githubusercontent.com/43723206/165421657-a7dde620-5335-44a7-9e45-ab9e483ff4eb.png)

如需要微信推送的请前往[WxPusher][wxpusher]获取apptoken 以及自己的uid添加到secret中，如上图中所示即可。















[api]: https://lbs.amap.com/tools/picker
[wxpusher]: https://wxpusher.zjiecode.com/admin/login
