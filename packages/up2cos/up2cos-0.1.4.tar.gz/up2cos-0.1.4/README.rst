up2cos
========

这是基于 `picbed <https://github.com/staugur/picbed>`_
的一个小的扩展模块，用来将上传的图片保存到腾讯云
`对象存储(COS) <https://cloud.tencent.com/product/cos>`_

安装
------

- 正式版本

    `$ pip install -U up2cos`

- 开发版本

    `$ pip install -U git+https://github.com/staugur/picbed-up2cos.git@master`


开始使用
----------

此扩展请在部署 `picbed <https://github.com/staugur/picbed>`_ 图床后使用，需要
其管理员进行添加扩展、设置钩子等操作。

添加：
^^^^^^^^

请在 **站点管理-钩子扩展** 中添加第三方钩子，输入模块名称：up2cos，
确认后提交即可加载这个模块（请在服务器先手动安装或Web上安装第三方包）。

配置：
^^^^^^^^

在 **站点管理-网站设置** 底部的钩子配置区域配置腾讯云相关信息，
如加速域名、Bucket、SecretID及KEY等（请在腾讯云创建一个对象存储服务，并在
访问管理-访问密钥-API密钥管理中拿到SecretId、SecretKey；允许使用子用户
的密钥，要求拥有COS管理权限）。

使用：
^^^^^^^^

同样在 **站点管理-网站设置** 上传区域中选择存储后端为up2cos即可，
后续图片上传时将保存到腾讯云。

上传图片的sender名称是：up2cos