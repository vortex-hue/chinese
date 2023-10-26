# -*- coding: utf-8 -*-
from . import dbModel
from constants import SITE_CONFIG_CACHE, FRONT_CONFIG_CACHE


class SiteConfigModel(dbModel):
    """网站配置"""
    __tablename__ = 'site_config_table'
    uuid = dbModel.UUIDField()
    project_name = dbModel.StringField('项目名', nullable=False)
    secret_key = dbModel.StringField('项目秘钥', nullable=False)
    cms_prefix = dbModel.StringField('CMS登录目录', nullable=False)
    max_filesize = dbModel.IntegerField('项目最大文件限制/KB')
    cms_text = dbModel.StringField('后台名称')
    cms_icon = dbModel.StringField('后台ICON图标')
    front_domain = dbModel.StringField('网站前端域名', nullable=False)
    cms_domain = dbModel.StringField('网站后台域名', nullable=False)

    robots = dbModel.StringField('Robots文件')
    baidu_resou_link = dbModel.StringField('百度资源API链接')
    ip_black = dbModel.StringField('ip黑名单')

    # 网站功能
    site_statu = dbModel.BooleanField('网站状态', default=0, true_text='已开启', false_text='已关闭')
    cms_captcha = dbModel.BooleanField('CMS登录图片验证码', default=0, true_text='已开启', false_text='已关闭')
    cms_log_save_time = dbModel.IntegerField('CMS操作日志保存时间/天')
    front_log_save_time = dbModel.IntegerField('前端日志保存时间/天')

    @classmethod
    def edit_field_sort(cls):
        return ['cms_prefix', 'max_filesize', 'cms_text', 'cms_icon', 'baidu_resou_link', 'front_domain', 'cms_domain']
    @classmethod
    def update_site_config(cls, config={}):
        if not config:
            config = cls.find_one({}) or {}
        SITE_CONFIG_CACHE.__dict__.update(config)


class FrontConfigModel(dbModel):
    """前端网站配置"""
    __tablename__ = 'front_config_table'
    uuid = dbModel.UUIDField()
    site_name = dbModel.StringField('网站名称')
    site_icon = dbModel.ImagesField('网站icon图标')
    site_logo = dbModel.ImagesField('网站LOGO')
    service_telephone = dbModel.StringField('客服电话')
    service_qq = dbModel.StringField('客服QQ')
    service_qq_url = dbModel.StringField('客服QQ跳转链接')
    service_wechat = dbModel.StringField('客服微信')
    service_wechat_rqcode = dbModel.ImagesField('客服微信二维码')
    applets_rqcode = dbModel.ImagesField('小程序二维码')
    public_rqcode = dbModel.ImagesField('微信公众号二维码')
    company_name = dbModel.StringField('公司名称')
    company_adderss = dbModel.StringField('公司地址')
    record_code = dbModel.StringField('网站备案号')

    title_suffix = dbModel.StringField('前端网站标题后缀')
    suffix_symbol = dbModel.StringField('标题后缀连接符')
    default_thumbnail = dbModel.StringField('文章默认缩略图')
    @classmethod
    def edit_seo_field(cls):
        return ['title_suffix', 'suffix_symbol', 'default_thumbnail']
    @classmethod
    def edit_field_sort(cls):
        return ['site_name', 'site_icon', 'site_logo', 'service_telephone', 'service_qq', 'service_qq_url', 'service_wechat', 'service_wechat_rqcode', 'applets_rqcode', 'public_rqcode', 'company_name', 'company_adderss', 'record_code']
    @classmethod
    def update_site_config(cls, config={}):
        if not config:
            config = cls.find_one({}) or {}
        FRONT_CONFIG_CACHE.__dict__.update(config)

