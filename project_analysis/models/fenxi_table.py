from . import dbModel
from constants import SITE_SETTING_CACHE


class SiteSettingTable(dbModel):
    """ 系统设置 """
    __tablename__ = 'site_setting_table'
    uuid = dbModel.UUIDField()
    blacklistIp = dbModel.StringField('ip黑名单')
    restore_data_pwd = dbModel.StringField('数据恢复密码')
    @classmethod
    def update_site_config(cls, config={}):
        if not config:
            config = cls.find_one({}) or {}
        SITE_SETTING_CACHE.__dict__.update(config)



class ZhuDanTable(dbModel):
    __tablename__ = 'zhu_dan_table'
    uuid = dbModel.UUIDField()
    order_number = dbModel.StringField('订单号', is_index=True)
    member_account = dbModel.StringField('会员账户', is_index=True)
    create_time = dbModel.DateTimeField('下注时间')
    game_name = dbModel.StringField('游戏', is_index=True)
    date_number = dbModel.StringField('期号', is_index=True)
    play_type = dbModel.StringField('玩法分类', is_index=True)
    play_name = dbModel.StringField('玩法名称')
    zhudan_info = dbModel.StringField('注单信息')
    money = dbModel.IntegerField('下注金额')
    win_lose = dbModel.IntegerField('会员输赢')

    @classmethod
    def field_search(cls):
        return ['order_number', 'member_account', 'game_name', 'date_number', 'play_type', 'play_name', 'zhudan_info', 'create_time']



class ImportLogTable(dbModel):
    __tablename__ = 'import_log_table'
    uuid = dbModel.UUIDField()
    file_name = dbModel.StringField('导入文件名称')
    file_path = dbModel.StringField('文件路径')
    data_count = dbModel.IntegerField('数据量')
    create_time = dbModel.DateTimeField('导入时间', nullable=False)
    note = dbModel.StringField('备注')

    @classmethod
    def field_search(cls):
        return ['file_name', 'file_path', 'data_count', 'create_time']



class BettingDataTable(dbModel):
    ''' 输赢分层功能 '''
    __tablename__ = 'betting_data_table'
    uuid = dbModel.UUIDField()
    account = dbModel.StringField('账号', is_index=True)
    parent_agent = dbModel.StringField('上级代理', is_index=True)
    betting_count = dbModel.IntegerField('下注笔数', is_index=True)
    betting_money = dbModel.FloatField('投注金额')
    profit_money = dbModel.FloatField('盈利投注（金额）')
    agent_odds = dbModel.FloatField('代理赔率(金额)')
    agent_backwater = dbModel.FloatField('代理返水(金额)')
    vip_winlose_money = dbModel.FloatField('会员输赢（不含退水）')
    actual_backwater = dbModel.FloatField('实际退水', is_index=True)
    actual_winlose_money = dbModel.FloatField('实际输赢（含退水）', is_index=True)
    create_tiem = dbModel.DateTimeField('时间', nullable=False)
    batch_code = dbModel.IntegerField('批号')
    blacklistState = dbModel.BooleanField('黑名单状态', default=False)
    new_quota = dbModel.IntegerField('新限额')
    low_quota = dbModel.IntegerField('原限额')
    promotion_state = dbModel.BooleanField('晋级状态', default=False)

    @classmethod
    def field_search(cls):
        return ['account', 'blacklistState']



class ChongZhiFenXiTable(dbModel):
    ''' 充值分析结果 '''
    __tablename__ = 'cz_fenxi_table'
    account = dbModel.StringField('账户', is_index=True)
    money = dbModel.FloatField('金额差值')

    @classmethod
    def field_search(cls):
        return ['account']



# 会员彩票报表
class hy_caipiao_form_tabl(dbModel):
    __tablename__ = 'hy_caipiao_form_tabl'
    uuid = dbModel.UUIDField()
    account = dbModel.StringField('账号', is_index=True)
    name = dbModel.StringField('姓名', is_index=True)
    parent_agent = dbModel.StringField('上级代理', is_index=True)
    betting_count = dbModel.IntegerField('下注笔数', is_index=True)
    betting_money = dbModel.FloatField('投注金额')
    profit_money = dbModel.FloatField('盈利投注（金额）')
    agent_odds = dbModel.FloatField('代理赔率(金额)')
    agent_backwater = dbModel.FloatField('代理返水(金额)')
    vip_winlose_money = dbModel.FloatField('会员输赢（不含退水）')
    actual_backwater = dbModel.FloatField('实际退水', is_index=True)
    actual_winlose_money = dbModel.FloatField('实际输赢（含退水）', is_index=True)
    form_date = dbModel.DateTimeField('报表时间')
    upload_log_id = dbModel.StringField('上传日志id', is_index=True)

    @classmethod
    def field_search(cls):
        return [
            'account',
            'name',
            'parent_agent',
            'form_date',
        ]



# 会员三方游戏报表
class hy_sanfang_form_table(dbModel):
    __tablename__ = 'hy_sanfang_form_table'
    uuid = dbModel.UUIDField()
    account = dbModel.StringField('账号', is_index=True)
    name = dbModel.StringField('姓名', is_index=True)
    parent_agent = dbModel.StringField('上级代理', is_index=True)
    bs_number = dbModel.StringField('笔数')
    betting_money = dbModel.FloatField('投注金额')
    yx_betting_money = dbModel.FloatField('有效投注金额')
    sf_jackpot_yc_money = dbModel.FloatField('第三方Jackpot预抽金额')
    sf_jackpot_pj_money = dbModel.FloatField('第三方Jackpot派彩金额')
    sy_money = dbModel.FloatField('输赢金额')
    fs_money = dbModel.FloatField('反水金额') # 会员返水金额
    sy_fs_money = dbModel.FloatField('输赢金额(含反水)')
    other_money = dbModel.FloatField('其他费用')
    form_date = dbModel.DateTimeField('报表时间')
    actual_winlose_money = dbModel.FloatField('实际输赢（含退水）', is_index=True)
    upload_log_id = dbModel.StringField('上传日志id', is_index=True)

    @classmethod
    def field_search(cls):
        return [
            'account',
            'name',
            'parent_agent',
            'form_date',
        ]



# 会员资金报表
class hy_zijing_form_table(dbModel):
    __tablename__ = 'hy_zijing_form_table'
    uuid = dbModel.UUIDField()
    account = dbModel.StringField('账号', is_index=True)
    parent_agent = dbModel.StringField('上级代理', is_index=True)
    chongzhi_money = dbModel.FloatField('充值金额')
    xscz_money = dbModel.FloatField('线上充值')
    xxcz_money = dbModel.FloatField('线下充值')
    hdjq_money = dbModel.FloatField('后台加钱')
    tixian_money = dbModel.FloatField('提现金额')
    hdkq_money = dbModel.FloatField('后台扣钱')
    hd_money = dbModel.FloatField('活动金额')
    hb_money = dbModel.FloatField('红包金额')
    czyh_money = dbModel.FloatField('充值优惠/手续费')
    form_date = dbModel.DateTimeField('报表时间')
    upload_log_id = dbModel.StringField('上传日志id', is_index=True)

    @classmethod
    def field_search(cls):
        return [
            'account',
            'parent_agent',
            'form_date',
        ]



# 代理-彩票报表
class agency_caipiao_form_table(dbModel):
    __tablename__ = 'agency_caipiao_form_table'
    uuid = dbModel.UUIDField()
    account = dbModel.StringField('账号', is_index=True)
    name = dbModel.StringField('姓名', is_index=True)
    xzhy_count = dbModel.IntegerField('下注会员数')
    betting_count = dbModel.IntegerField('下注笔数', is_index=True)
    betting_money = dbModel.FloatField('投注金额')
    profit_money = dbModel.FloatField('盈利投注（金额）')
    agent_odds = dbModel.FloatField('代理赔率(金额)')
    agent_backwater = dbModel.FloatField('代理返水(金额)')
    vip_winlose_money = dbModel.FloatField('会员输赢（不含退水）')
    actual_backwater = dbModel.FloatField('实际退水', is_index=True)
    actual_winlose_money = dbModel.FloatField('实际输赢（含退水）', is_index=True)
    form_date = dbModel.DateTimeField('报表时间')
    upload_log_id = dbModel.StringField('上传日志id', is_index=True)

    @classmethod
    def field_search(cls):
        return [
            'account',
            'name',
            'form_date',
        ]



# 代理-第三方游戏报表
class agency_sanfang_form_table(dbModel):
    __tablename__ = 'agency_sanfang_form_table'
    uuid = dbModel.UUIDField()
    account = dbModel.StringField('账号', is_index=True)
    name = dbModel.StringField('姓名', is_index=True)
    parent_agent = dbModel.StringField('上级代理', is_index=True)
    hy_count = dbModel.IntegerField('会员数')
    bs_number = dbModel.IntegerField('笔数')
    betting_money = dbModel.FloatField('投注金额')
    yx_betting_money = dbModel.FloatField('有效投注金额')
    sf_jackpot_yc_money = dbModel.FloatField('第三方Jackpot预抽金额')
    sf_jackpot_pj_money = dbModel.FloatField('第三方Jackpot派彩金额')
    sy_money = dbModel.FloatField('输赢金额')
    hyfs_money = dbModel.FloatField('会员反水金额')
    dlfs_money = dbModel.FloatField('代理反水金额')
    sjsy_money = dbModel.FloatField('实际输赢（含反水）')
    form_date = dbModel.DateTimeField('报表时间')
    upload_log_id = dbModel.StringField('上传日志id', is_index=True)

    @classmethod
    def field_search(cls):
        return [
            'account',
            'name',
            'form_date',
            'parent_agent',
        ]



# 代理-资金报表
class agency_zijing_form_table(dbModel):
    __tablename__ = 'agency_zijing_form_table'
    uuid = dbModel.UUIDField()
    account = dbModel.StringField('账号', is_index=True)
    chongzhi_money = dbModel.FloatField('充值金额')
    hdjq_money = dbModel.FloatField('后台加钱')
    tixian_money = dbModel.FloatField('提现金额')
    hdkq_money = dbModel.FloatField('后台扣钱')
    hd_money = dbModel.FloatField('活动金额')
    hb_money = dbModel.FloatField('红包金额')
    czyh_money = dbModel.FloatField('充值优惠/手续费')
    form_date = dbModel.DateTimeField('报表时间')
    upload_log_id = dbModel.StringField('上传日志id', is_index=True)

    @classmethod
    def field_search(cls):
        return [
            'account',
            'form_date',
        ]



# 代理-投注报表
class agency_touzhu_form_table(dbModel):
    __tablename__ = 'agency_touzhu_form_table'
    uuid = dbModel.UUIDField()
    account = dbModel.StringField('账号', is_index=True)
    customer_count = dbModel.IntegerField('用户数', is_index=True)
    tzbs_count = dbModel.IntegerField('投注笔数')
    betting_money = dbModel.FloatField('投注金额')
    yx_betting_money = dbModel.FloatField('有效投注金额')
    sy_money = dbModel.FloatField('输赢金额')
    form_date = dbModel.DateTimeField('报表时间')
    upload_log_id = dbModel.StringField('上传日志id', is_index=True)

    @classmethod
    def field_search(cls):
        return [
            'account',
            'form_date',
        ]



# 游戏统计-游戏统计表
class game_yxtj_form_table(dbModel):
    __tablename__ = 'game_yxtj_form_table'
    uuid = dbModel.UUIDField()
    game_name = dbModel.StringField('游戏', is_index=True)
    bs_number = dbModel.IntegerField('笔数', is_index=True)
    betting_money = dbModel.FloatField('投注金额')
    profit_money = dbModel.FloatField('盈利投注金额')
    agent_odds = dbModel.FloatField('代理赔率金额')
    agent_backwater = dbModel.FloatField('代理返水金额')
    vip_winlose_money = dbModel.FloatField('会员输赢（不含退水）')
    actual_backwater = dbModel.FloatField('实际退水', is_index=True)
    actual_winlose_money = dbModel.FloatField('实际输赢（含退水）', is_index=True)
    xzhy_count = dbModel.IntegerField('下注会员数', is_index=True)
    form_date = dbModel.DateTimeField('报表时间')
    upload_log_id = dbModel.StringField('上传日志id', is_index=True)
    @classmethod
    def field_search(cls):
        return [
            'game_name',
            'form_date',
        ]



# 游戏统计-第三方游戏
class game_sfyx_form_table(dbModel):
    __tablename__ = 'game_yztj_form_table'
    uuid = dbModel.UUIDField()
    platform = dbModel.StringField('平台', is_index=True)
    yx_betting_money = dbModel.FloatField('有效投注金额', is_index=True)
    sf_jackpot_yc_money = dbModel.FloatField('第三方Jackpot预抽金额')
    sf_jackpot_pj_money = dbModel.FloatField('第三方Jackpot派彩金额')
    sy_money = dbModel.FloatField('输赢金额')
    fs_money = dbModel.FloatField('返水金额')
    sjsy_money = dbModel.FloatField('实际输赢(含返水)')
    form_date = dbModel.DateTimeField('报表时间')
    upload_log_id = dbModel.StringField('上传日志id', is_index=True)

    @classmethod
    def field_search(cls):
        return [
            'platform',
            'form_date',
        ]



# 平台报表
class platform_form_table(dbModel):
    __tablename__ = 'platform_form_table'
    uuid = dbModel.UUIDField()
    form_date = dbModel.DateTimeField('报表时间')
    data_date = dbModel.StringField('日期')
    app_regist = dbModel.IntegerField('APP注册')
    shou_chong = dbModel.FloatField('首充')
    xzyxhy_cp = dbModel.FloatField('新增有效会员(彩票)')
    xzyxhy_dsfyx = dbModel.FloatField('新增有效会员(第三方游戏)')
    yxyh_count = dbModel.IntegerField('有效用户总数')
    yxyh_cp_count = dbModel.IntegerField('有效用户-彩票')
    yxyh_sfyx_count = dbModel.IntegerField('有效用户-第三方')
    cpye_money = dbModel.FloatField('彩票余额')
    sfye_money = dbModel.FloatField('三方余额')
    recharge_money = dbModel.FloatField('充值金额')
    withdraw_money = dbModel.FloatField('提现金额')
    touzhu_money = dbModel.FloatField('投注总额')
    tsze_money = dbModel.FloatField('退水总额')
    sjsy_money = dbModel.FloatField('实际输赢(含退水)')
    agent_odds = dbModel.FloatField('代理赔率(金额)')
    tuishui_money = dbModel.FloatField('退水金额')
    jackpot = dbModel.FloatField('jackpot')
    jackBonus = dbModel.FloatField('jackBonus')
    sfyx_money = dbModel.FloatField('三方有效')
    sy_money = dbModel.FloatField('输赢金额')
    fs_money = dbModel.FloatField('反水金额')
    sfqtfy_money = dbModel.FloatField('三方其他费用')
    czyh_money = dbModel.FloatField('充值优惠&手续费')
    hd_money = dbModel.FloatField('活动金额')
    hb_money = dbModel.FloatField('红包金额')
    yk_mongey = dbModel.FloatField('平台盈亏')



class RechargeTable(dbModel):
    __tablename__ = 'recharge_table'
    uuid = dbModel.UUIDField()
    bill_time = dbModel.DateTimeField('订单日期')
    cl_time = dbModel.DateTimeField('处理日期')
    account = dbModel.StringField('会员', is_index=True)
    parent_agent = dbModel.StringField('上级代理', is_index=True)
    username = dbModel.StringField('真实姓名', is_index=True)
    over_money = dbModel.FloatField('余额')
    order_number = dbModel.StringField('订单号')
    pay_way = dbModel.StringField('付款方式')
    jy_money = dbModel.FloatField('交易金额')
    operator_user = dbModel.StringField('操作人')
    collect_money_info = dbModel.StringField('收款信息')
    deposit_money_info = dbModel.StringField('入款信息')
    state = dbModel.StringField('状态')
    cz_level = dbModel.StringField('充值层级')
    note = dbModel.StringField('备注')
    scdd = dbModel.StringField('首充订单')
    form_date = dbModel.DateTimeField('报表时间')

    @classmethod
    def field_search(cls):
        return ['account', 'parent_agent', 'form_date']



class FtpTable(dbModel):
    ''' ftp服务器配置 '''
    __tablename__ = 'ftp_table'
    uuid = dbModel.UUIDField()
    ftp_host = dbModel.StringField('ftp Host')
    ftp_username = dbModel.StringField('ftp 用户名')
    ftp_password = dbModel.StringField('ftp 密码')
    server_path = dbModel.StringField('ftp上传位置')



class BackupTable(dbModel):
    ' 备份 '
    __tablename__ = 'backup_table'
    uuid = dbModel.UUIDField()
    name = dbModel.StringField('名称')
    data_count = dbModel.IntegerField('数据量')
    _create_time = dbModel.DateTimeField('备份时间', nullable=False)
    note = dbModel.StringField('备注')
    dataCode = dbModel.StringField('日期Code')
    path = dbModel.StringField('文件访问路径')
    backup_type = dbModel.StringField('备份类型')
    is_automatic = dbModel.BooleanField('是否自动备份')

    @classmethod
    def field_search(cls):
        return ['backup_type']



class UploadlogTable(dbModel):
    '上传日志'
    __tablename__ = 'upload_log_table'
    uuid = dbModel.UUIDField()
    table_code = dbModel.StringField('表Code', is_index=True)
    statu = dbModel.BooleanField('是否恢复之前', is_index=True)
    low_data = {}
    log_type = dbModel.StringField('日志类型', is_index=True)
    data_uuid = dbModel.StringField('data_uuid', is_index=True)



class agencyConfigTable(dbModel):
    __tablename__ = 'agency_config_table'
    uuid = dbModel.UUIDField()
    create_time = dbModel.DateTimeField('时间', nullable=False)
    main_agency = dbModel.StringField('主代理', is_index=True)
    child_agency = dbModel.StringField('子代理', is_index=True)

    @classmethod
    def field_search(cls):
        return ['main_agency', 'child_agency']

