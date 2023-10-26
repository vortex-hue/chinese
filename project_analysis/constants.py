# -*- coding: utf-8 -*-
import time

CMS_USER_SESSION_KEY = 'cms_user_session_@13141152099'
FRONT_USER_SESSION_KEY = 'front_user_session_@13141152099'

# 缓存机制
SITE_CONFIG_CACHE = type('SiteConfigCache', (object,), {})()
FRONT_CONFIG_CACHE = type('FrontConfigCache', (object,), {})()
SITE_SETTING_CACHE = type('SiteSettingCache', (object,), {})()

CMS_MENUS_GROUPS = []
FRONT_CATEGORY_CACHE = {}

# 导出文件夹名称
EXPORT_FOLDER = 'export_data'

# 静态文件夹名称
STATIC_FOLDER = 'static'
ASSETS_FOLDER = 'assets'
PUBLIC_FOLDER = 'public'
# 私有目录
PRIVATE_FOLDER = 'private'
# 上传文件夹
UPLOAD_FOLDER = 'upload'
# 备份文件夹
DATA_BACKUP_FOLDER = 'backup'
# 前端栏目文件夹
CATEGORY_TEMPLATES_FOLDER = 'category_templates'
# 图片文件夹名称
IMAGES_FOLDER = 'images'
# 图片类型限制
IMAGES_TYPES = ['.png', '.jpeg', '.jpg', '.svg', 'gif']
# 文件类型格式
FIEL_TYPES = ['.txt', '.xlsx', '.csv', '.word']

class UrlPrefix:
    """URL前缀"""
    FRONT_PREFIX = '/'
    API_PREFIX = '/api'
    COMMON_PREFIX = '/common'
    CMS_PREFIX = '/site_admin'


class PermissionType:
    """权限类型"""
    SUPERADMIN = 'superadmin'
    ACCESS = 'access'
    DELETE = 'delete'
    ADD = 'add'
    EDIT = 'edit'
    EXPORT_DATA = 'exportAata'
    UPLOAD_DATA = 'uploadAata'
    name_arr = (ACCESS, DELETE, ADD, EDIT, EXPORT_DATA, UPLOAD_DATA, SUPERADMIN)
    naem_dict = {
        ACCESS: '访问权限', DELETE: '删除数据权限', ADD: '添加数据权限', EDIT: '编辑数据权限', UPLOAD_DATA: '上传数据权限', EXPORT_DATA: '导出数据权限', SUPERADMIN:'最高管理员'
    }


class OnClick:
    """点击类型"""
    JUMP_HREF = 'jump_href'
    SHOW_IMAGES = 'show_images'
    SHOW_CONTENT = 'show_content'
    name_dict = {
        JUMP_HREF: '跳转链接', SHOW_CONTENT: '显示内容', SHOW_IMAGES: '显示图片',
    }


class ClientType:
    """客户端类型"""
    PC = 'pc'
    WAP = 'wap'
    name_arr = (PC, WAP)
    name_dict = { PC: 'pc端', WAP: '移动端'}


class EventType:
    """事件类型"""
    ACCESS = 'access'
    DELETE = 'delete'
    ADD = 'add'
    EDIT = 'edit'
    OUTLOG = 'outlogin'
    LOGIN_SUCCESS = 'login_success'
    LOGIN_FAILED = 'login_failed'
    EXPORT_DATA = 'export_data'
    UPLOAD_DATA = 'upload_data'
    name_arr = (ACCESS, DELETE, ADD, EDIT, LOGIN_SUCCESS,LOGIN_FAILED, EXPORT_DATA, UPLOAD_DATA, OUTLOG)
    name_dict = {
        ACCESS: '访问页面', DELETE: '删除数据', ADD: '添加数据', EDIT: '编辑数据', LOGIN_SUCCESS: '登录成功', LOGIN_FAILED: '登录失败', EXPORT_DATA: '导出数据', UPLOAD_DATA:'上传数据', OUTLOG:'退出登录',
    }
    class_dict = {
        ACCESS: 'btn-default', DELETE: 'btn-danger', ADD: 'btn-success', EDIT: 'btn-default', LOGIN_SUCCESS: 'btn-success', LOGIN_FAILED: 'btn-danger', UPLOAD_DATA: 'btn-success', OUTLOG:'btn-danger',
    }



class CommentAuditStatu:
    is_audit = 'is_audit'
    not_audit = 'not_audit'
    not_through = 'not_through'
    name_arr = (is_audit, not_audit, not_through)
    name_dict = {is_audit: '已审核', not_audit: '未审核', not_through: '未通过'}
    class_dict = {not_audit: 'btn-info',is_audit: 'btn-success',not_through: 'btn-danger',}


class SpiderType:
    """蜘蛛类型"""
    baidu_spider = 'baidu_spider'
    googlebot = 'googlebot'
    spider_360 = 'spider_360'
    soso_spider = 'soso_spider'
    sogou = 'sogou'
    byte_spider = 'byte_spider'
    name_arr = (baidu_spider, googlebot, spider_360, soso_spider, sogou, byte_spider)
    name_dict = {
        baidu_spider: u'百度蜘蛛', googlebot: u'谷歌蜘蛛', spider_360: u'360蜘蛛', soso_spider: u'SOSO蜘蛛', sogou: u'搜狗蜘蛛', byte_spider: u'字节蜘蛛',
    }
    spider_mark = {
        baidu_spider: ['Baiduspider'], googlebot: ['Googlebot'], spider_360: ['360Spider'], soso_spider: ['Sosospider'], sogou: ['Sogou'], byte_spider: ['Bytespider'],
    }


class ExportStatu:
    """导出状态"""
    successed = 'successed'
    failed = 'failed'
    ongoing = 'ongoing'
    name_arr = (successed, failed, ongoing,)
    name_dict = {
        successed: '导出成功', failed: '导出失败', ongoing: '导出中',
    }
    class_dict = {
        successed: 'btn-success', failed: 'btn-danger', ongoing: 'btn-warning',
    }


class CodingType:
    """编码类型"""
    UTF8 = 'UTF-8'
    GB2312 = 'GB2312'
    GBK = 'GBK'
    GB18030 = 'GB18030'
    name_arr = (UTF8, GB2312, GBK, GB18030,)
    name_dict = {UTF8: 'UTF-8', GB2312: 'GB2312', GBK: 'GBK', GB18030: 'GB18030',}



class PermissionCls:
    SUPERADMIN = 'superadmin'
    systemManage = 'systemManage'
    systemManage_edit = 'systemManage_edit'
    adminManage = 'adminManage'
    adminManage_del = 'adminManage_del'
    adminManage_add = 'adminManage_add'
    adminManage_edit = 'adminManage_edit'
    zhudanFenxi = 'zhudanFenxi'
    zhudanFenxi_import = 'zhudanFenxi_import'
    zhudanData = 'zhudanData'
    exportLog = 'exportLog'
    customerManager = 'customerManager'
    exportDataManager = 'exportDataManager'
    # bettingSy = 'bettingSy'
    customerAnalysis = 'customerAnalysis'

    # 平台系统分析
    customCpForms = 'customCpForms'
    customDsfForms = 'customDsfForms'
    customZjForms = 'customZjForms'
    agencyCpForms = 'agencyCpForms'
    agencyDsfForms = 'agencyDsfForms'
    agencyTzForms = 'agencyTzForms'
    agencyZjForms = 'agencyZjForms'

    # 充值分析
    chongzhiFenxi = 'chongzhiFenxi'

    # 域名
    domainAnalysis = 'domainAnalysis'
    domainManager = 'domainManager'

    # 卡商
    CardMerchantManage = 'CardMerchantManage'

    # 报表分析
    fromdataAnalysis = 'fromdataAnalysis'

    # 备份
    backupDataManager = 'backupDataManager'

    name_arr = (
        SUPERADMIN,
        systemManage, systemManage_edit,
        adminManage, adminManage_add, adminManage_del, adminManage_edit,
        zhudanFenxi, zhudanFenxi_import,
        zhudanData,
        exportLog,
        customerManager,
        exportDataManager,
        # bettingSy,
        customerAnalysis,

        domainAnalysis,
        domainManager,

        CardMerchantManage,

        chongzhiFenxi,

        customCpForms,
        customDsfForms,
        customZjForms,
        agencyCpForms,
        agencyDsfForms,
        agencyTzForms,
        agencyZjForms,

        fromdataAnalysis,

        backupDataManager,
    )

    name_dict = {
        "ROOT": {
            SUPERADMIN: '超级管理员权限'
        },
        "系统设置":{
            systemManage: '系统设置权限',
            systemManage_edit: '系统设置-编辑权限',
        },
        "账户管理":{
            adminManage: '账户管理权限',
            adminManage_add: '账户管理-添加权限',
            adminManage_del: '账户管理-删除权限',
            adminManage_edit: '账户管理-编辑权限',
        },
        "注单分析":{
            zhudanFenxi: '注单分析-管理权限',
        },
        "注单数据":{
            zhudanData: '注单数据-管理权限',
        },
        "导入日志":{
            exportLog: '导入日志-管理权限',
        },
        "客户管理":{
            customerManager: '客户管理权限',
        },
        "导出数据": {
            exportDataManager: '导出数据管理',
        },
        "域名分析": {
            domainAnalysis: '域名分析-管理权限',
        },
        "域名管理": {
            domainManager: '域名管理权限',
        },
        "卡商管理": {
            CardMerchantManage: "卡商管理权限",
        },
        # "输赢分层": {
        #     bettingSy: "输赢分层分析权限",
        # },
        "充值分析": {
            chongzhiFenxi: "充值分析权限",
        },
        "客户分析": {
            customerAnalysis: "分析客户注单数据权限",
        },
        "会员报表": {
            customCpForms: "会员彩票报表管理权限",
            customDsfForms: "会员第三方游戏报表管理权限",
            customZjForms: "会员资金报表管理权限",
        },
        "代理报表": {
            agencyCpForms: "代理彩票报表管理权限",
            agencyDsfForms: "代理第三方游戏报表管理权限",
            agencyTzForms: "代理投注报表管理权限",
            agencyZjForms: "代理资金报表管理权限",
        },
        "报表分析": {
            fromdataAnalysis: '报表分析权限'
        },
        "数据备份": {
            backupDataManager: "数据备份管理权限"
        }
    }



class PLAY_NAMES:
    ONE = [
        'Đầu', 'Đuôi',
        'Tài', 'Xỉu', 'Lẻ', 'Chẵn', '0', '1', '3', '2', '4', '5', '6', '7', '8', '9'
    ]
    TWO = [
        'Lô 2 Số', 'Lô 2 Số 1K', 'Xiên 2', 'Đề đầu', 'Đề đặc biệt', 'Đề đầu đuôi', 'Đề Giải Nhất', 'Đề đầu giải nhất', 'Đề Giải 7',
        'Đề đầu đặc biệt', 'Lô 2 Số Đầu',

        'Trượt Xiên 8', 'Trượt Xiên 10',

        '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    ]
    THREE = [
        'Lô 3 Số', 'Xiên 3','3 Càng Đầu', '3 Càng Đặc Biệt', '3 Càng Giải Nhất', '3 Càng Đầu Đuôi'
    ]
    FOUR = [
        'Lô 4 Số', 'Xiên 4', '4 Càng Đặc Biệt', 'Trượt Xiên 4'
    ]

    YINCANG = [
        'Xỉu', 'Lẻ', 'Tài', 'Chẵn',
        '1', '0', '3', '2', '4', '5', '6', '7', '8', '9','10',
        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    ]


WF_ZH_DICT = {
    "Đề đặc biệt": "特码后二中二",
    "3 Càng Đặc Biệt": "特码后三中三",
    "Lô 3 Số": "平特三中三",
    "Xiên 2": "平特二连",
    "3 Càng Giải Nhất": "一等奖的后三中三",
    "Đề Giải Nhất": "一等奖",
    "Xiên 4": "平特四连",
    "Lô 2 Số": "后面二全包",
    "Xiên 3": "平特三连",
    "Lô 2 Số 1K": "后二全包低倍",
    "4 Càng Đặc Biệt": "特码四全中",
    "Đề Giải 7": "七等奖二中二",
    "Đề đầu giải nhất": "一等奖前二中二",
    "Đề đầu đặc biệt": "特码前两二中二",
    "3 Càng Đầu Đuôi": "特六三中三",
    "Lô 4 Số": "平特后四中四",
    "3 Càng Đầu": "六等奖三中三",
    "Đầu": "特等奖后二单码",
    "Đuôi": "特等奖后一单码",
    "Trượt Xiên 4": "平特后二四不中",
    "TRƯỢT XIÊN 8": "平特后二八不中",
    "TRƯỢT XIÊN 10": "平特后二十不中",
    "Đề đầu đuôi": "特八双位二中二",
    "Đề đầu": "八等奖后二中二",
    "Lô 2 Số Đầu": "平特前二",
    "Trượt Xiên 8": "后二全包八不中",
    "Trượt Xiên 10": "后二全包十不中",
}


class backupTypes:
    LOCAL = 'local'
    REMOTE = 'remote'
    name_arr = (LOCAL, REMOTE)
    name_dict = {
        LOCAL: '本地',
        REMOTE: '远程',
    }

# admin_Sodo  Sodo_admin@123

