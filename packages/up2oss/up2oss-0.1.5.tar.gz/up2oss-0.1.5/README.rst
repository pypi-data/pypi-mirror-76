up2oss
========

这是基于 `picbed <https://github.com/staugur/picbed>`_
的一个小的扩展模块，用来将上传的图片保存到阿里云
`对象存储(OSS) <https://www.aliyun.com/product/oss>`_

安装
------

- 正式版本

    `$ pip install -U up2oss`

- 开发版本

    `$ pip install -U git+https://github.com/staugur/picbed-up2oss.git@master`


开始使用
----------

此扩展请在部署 `picbed <https://github.com/staugur/picbed>`_ 图床后使用，需要
其管理员进行添加扩展、设置钩子等操作。

添加：
^^^^^^^^

请在 **站点管理-钩子扩展** 中添加第三方钩子，输入模块名称：up2oss，
确认后提交即可加载这个模块（请在服务器先手动安装或Web上安装第三方包）。

配置：
^^^^^^^^

在 **站点管理-网站设置** 底部的钩子配置区域配置阿里云相关信息，
如用户域名、Bucket、AK及SK等（请在阿里云创建一个对象存储服务，并在
AccessKey密钥管理中拿到AK、SK；允许使用RAM子用户的密钥（允许编程访问），
要求拥有OSS管理权限）。

使用：
^^^^^^^^

同样在 **站点管理-网站设置** 上传区域中选择存储后端为up2oss即可，
后续图片上传时将保存到阿里云。

上传图片的sender名称是：up2oss
