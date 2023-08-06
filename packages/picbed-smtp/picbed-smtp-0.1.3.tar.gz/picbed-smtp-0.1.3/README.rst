picbed-smtp
===========

这是基于 `picbed <https://github.com/staugur/picbed>`_
的一个小的模块，用以扩展邮件发送服务。

安装
------

- 正式版本

    `$ pip install -U picbed-smtp`

- 开发版本

    `$ pip install -U git+https://github.com/staugur/picbed-smtp.git@master`

开始使用
----------

此扩展请在部署 `picbed <https://github.com/staugur/picbed>`_ 图床后使用，需要
其管理员进行添加扩展、设置钩子等操作。

添加：
^^^^^^^^

请在 **站点管理-钩子扩展** 中添加第三方钩子，输入模块名称：picbed_smtp，
确认后提交即可加载这个模块（请先手动或在线安装好此模块）。

配置：
^^^^^^^^

在 **站点管理-网站设置** 底部邮件服务设置中配置邮箱相关信息。

使用：
^^^^^^^^

发送邮件时，程序会调用邮件发送功能，目前有一内置钩子sendmail实现了功能。

如启用此picbed-smtp钩子扩展，那么，程序在发送时会按序调用（不一定谁优先），
某个发送失败才会进入下一个，任一发送成功则停止，全部发送失败则本次邮件发送
宣告失败。

所以，如果不想用内置邮件发送钩子，可以在 **站点管理-钩子扩展** 中禁用内置
的sendmail，仅启用本扩展。
