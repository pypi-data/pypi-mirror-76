# -*- coding: utf-8 -*-
"""
    picbed-smtp
    ~~~~~~~~~~~

    Send email with third smtp server.

    :copyright: (c) 2020 by staugur.
    :license: BSD 3-Clause, see LICENSE for more details.
"""

__version__ = '0.1.3'
__author__ = 'staugur <staugur@saintic.com>'
__hookname__ = 'picbed-smtp'
__description__ = '通过SMTP发送邮件'

from utils.tool import Mailbox, mail_pat
from flask import g

intpl_emailsetting = '''
<div class="layui-col-xs12 layui-col-sm12 layui-col-md12">
    <fieldset class="layui-elem-field layui-field-title">
        <legend>SMTP</legend>
        <div class="layui-field-box">
            <div class="layui-form-item">
                <label class="layui-form-label">发件人</label>
                <div class="layui-input-block">
                    <input type="text" name="email_smtp_from"
                        value="{{ g.site.email_smtp_from }}" placeholder="发件邮箱地址"
                        autocomplete="off" class="layui-input">
                </div>
            </div>
            <div class="layui-form-item">
                <label class="layui-form-label">密码</label>
                <div class="layui-input-block">
                    <input type="password" name="email_smtp_passwd"
                        value="{{ g.site.email_smtp_passwd }}" placeholder="邮箱授权码或密码"
                        autocomplete="off" class="layui-input">
                </div>
            </div>
            <div class="layui-form-item">
                <label class="layui-form-label">SMTP</label>
                <div class="layui-input-block">
                    <input type="text" name="email_smtp_server" id="render_email_server"
                        value="{{ g.site.email_smtp_server }}" placeholder="SMTP服务器域名:端口(默认25)"
                        autocomplete="off" class="layui-input">
                </div>
            </div>
        </div>
    </fieldset>
</div>
'''

intpl_adminscript = '''
<script>
    layui.use(['tableSelect', 'jquery'], function () {
        var $ = layui.jquery,
            tableSelect = layui.tableSelect;

        function renderEmailSelect() {
            var elem = "#render_email_server",
                selectd = "{{ g.site.email_smtp_server }}";
            let list = [{
                    value: "smtp.qq.com:465",
                    title: "QQ邮箱",
                    href: "https://mail.qq.com",
                },
                {
                    value: "smtp.exmail.qq.com:465",
                    title: "腾讯企业邮",
                    href: "https://exmail.qq.com/",
                },
                {
                    value: "smtp.163.com:995",
                    title: "网易163邮箱",
                    href: "https://mail.163.com",
                },
                {
                    value: "smtp.ym.163.com:994",
                    title: "网易免费企业邮",
                    href: "http://ym.163.com",
                },
                {
                    value: "",
                    title: "更多邮箱请手动输入",
                },
            ];
            if (selectd) {
                $(elem).attr("ts-selected", selectd);
            }
            tableSelect.render({
                elem: elem,
                checkedKey: 'value',
                selectText: '确认选择',
                table: {
                    data: list,
                    page: false,
                    size: 'sm',
                    cols: [
                        [{
                            type: "radio"
                        }, {
                            field: "title",
                            title: "邮箱",
                            templet: function(d) {
                                return d.href ? (
                                    '<a href="' + d.href + '" target="_blank">' + d.title + '</a>'
                                ) : d.title;
                            }
                        }, {
                            field: "value",
                            title: "SMTP",
                        }]
                    ]
                },
                done: function (e, data) {
                    var NEWJSON = [];
                    layui.each(data.data, function (index, item) {
                        NEWJSON.push(item.value);
                    });
                    $(elem).val(NEWJSON.join(","));
                }
            });
        }

        renderEmailSelect()
    });
</script>
'''


def sendmail(subject, message, to_addr):
    res = dict(code=1)
    from_name = g.cfg.email_from_name or g.cfg.title_name or "picbed"
    smtp_server = g.cfg.email_smtp_server
    smtp_from = g.cfg.email_smtp_from
    smtp_passwd = g.cfg.email_smtp_passwd
    if smtp_server and smtp_from and mail_pat.match(smtp_from) and smtp_passwd:
        if ":" in smtp_server:
            smtp_server, smtp_port = smtp_server.split(":")
        else:
            smtp_port = 25
        try:
            smtp_port = int(smtp_port)
        except (ValueError, TypeError):
            res.update(code=3, msg="Parameter error")
        else:
            smtp = Mailbox(smtp_from, smtp_passwd, smtp_server, smtp_port)
            res = smtp.send(subject, message, to_addr, from_name)
    else:
        res.update(code=2, msg="Parameter error")
    res["method"] = "smtp"
    return res
