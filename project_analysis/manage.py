# -*- coding: utf-8 -*-
import os, datetime, click, time, shortuuid, stat
from app_analysis2 import app, ProjectConfig
from common_utils.lqredis import SiteRedis
from common_utils.mongodb.mongo_admin import MongoManage, CONFIG
from constants import PermissionType, backupTypes
from models.cms_table import SiteConfigModel
from models.domain_table import DomainTable, CardMerchantTable
from models.cms_user import CmsUserModel
from models.customer_table import CustomerTable, ExportDataModel
from models.fenxi_table import SiteSettingTable,ZhuDanTable,ImportLogTable,BettingDataTable,ChongZhiFenXiTable,hy_caipiao_form_tabl,hy_sanfang_form_table,hy_zijing_form_table,agency_caipiao_form_table,agency_sanfang_form_table,agency_zijing_form_table,agency_touzhu_form_table,game_yxtj_form_table,game_sfyx_form_table,platform_form_table,RechargeTable,FtpTable,BackupTable,agencyConfigTable
from modules.ftp_cls import FtpCls



@click.group()
def mainFunc():
    pass


@mainFunc.command()
@click.option('--login_account', '-t')
def init_admin(login_account):
    """ 初始化admin用户 """
    if not login_account.strip():
        return '请输入手机号!'
    CmsUserModel.delete_many({})
    user_data = {
        'login_account': login_account.strip(),
        'password': CmsUserModel.encry_password('admin123'),
        'username': 'superadmin',
        'statu': True,
        'permissions': [PermissionType.SUPERADMIN],
        '_current_login': '',
    }
    CmsUserModel.insert_one(user_data)
    print('%s: 用户添加成功!'%login_account)
    return '%s: 用户添加成功!'%login_account


@mainFunc.command()
def init_index():
    """创建索引"""
    tables = [
        SiteConfigModel,
        DomainTable, CardMerchantTable,
        CmsUserModel,
        CustomerTable, ExportDataModel,
        SiteSettingTable, ZhuDanTable, ImportLogTable, BettingDataTable, ChongZhiFenXiTable, hy_caipiao_form_tabl,
        hy_sanfang_form_table, hy_zijing_form_table, agency_caipiao_form_table, agency_sanfang_form_table,
        agency_zijing_form_table, agency_touzhu_form_table, game_yxtj_form_table, game_sfyx_form_table,
        platform_form_table, RechargeTable, FtpTable, BackupTable, agencyConfigTable
    ]
    for MCLS in tables:
        indexs = MCLS.index_information()
        for k, v in MCLS.fields().items():
            if not hasattr(v, 'is_index'):
                continue
            if not getattr(v, 'is_index'):
                continue
            if not indexs.get('%s_1' % k) and v.is_index:
                print(k, MCLS.create_index(k))


@mainFunc.command()
def remove_project_data():
    """清空整个项目所有数据库内的数据"""
    instruction = input('该操作会清除当前项目下所有的数据,指令（Y/N），回复确认操作Y，其它拒绝操作!')
    if instruction.strip() != 'Y':
        exit()
    for key in SiteRedis.get_keys():
        if key.decode().startswith(ProjectConfig.PROJECT_NAME):
            SiteRedis.dele(key)
    p_db = MongoManage(username=CONFIG.root_username, password=CONFIG.root_password)
    print(p_db.drop_database(ProjectConfig.MONGODB_DB))
    return '操作成功!'


@mainFunc.command()
def update_primary_key():
    """更细项目字段主键"""
    print('更新项目字段主键KEY')
    for _k in SiteRedis.get_keys():
        _k = _k.decode()
        if ProjectConfig.PROJECT_NAME in _k and '_field' in _k:
            SiteRedis.dele(_k)
    import models
    for n in dir(models):
        if n.startswith('__') or n == 'db' or n == 'dbModel' or n == 'MongoBase':
            continue
        n_f = getattr(models, n)
        for c in dir(n_f):
            if c == 'dbModel':
                continue
            MCLS = getattr(n_f, c)
            if not hasattr(MCLS, '__tablename__') or not getattr(MCLS, '__tablename__'):
                continue
            table_name = getattr(MCLS, '__tablename__')
            for db_field, v_Cls in MCLS.fields().items():
                if not hasattr(v_Cls, 'field_type'):
                    continue
                if v_Cls.primary_key:
                    v_dict = MCLS.find_one({}, sort=[[db_field, -1]])
                    if v_dict:
                        kk_v = v_dict.get(db_field) or 0
                        _redis_check_key = '%s_%s_%s_%s_field' % (ProjectConfig.PROJECT_NAME, ProjectConfig.MONGODB_DB, table_name, db_field)
                        SiteRedis.set(_redis_check_key, kk_v)
                        print(table_name, db_field, kk_v)
    print('项目字段主键KEY更新完毕！')



import datetime, time, multiprocessing
from common_utils.utils_funcs import RC4CLS

def demo(dsl, header, name_dict):
    _crr_datas = []
    for row in dsl:
        _dict_data = {}
        for index, col in enumerate(row.split(',')):
            if index >= len(header):
                continue
            _h = header[index].replace(' ', '').replace('=', '').replace('"', '')
            _k = name_dict.get(_h)
            if _k == 'create_time':
                try:
                    _dict_data[_k] = datetime.datetime.strptime(col.strip().strip('=').strip('"'), '%Y-%m-%d %H:%M:%S')
                except:
                    pass
            elif _k == 'money':
                _dict_data[_k] = int(col or 0)
            elif _k == 'win_lose':
                _dict_data[_k] = int(col or 0)
            else:
                if _k == 'user_tele':
                    _dict_data[_k] = RC4CLS.encrypt(col.strip().strip('=').strip('"'), secret_key=ProjectConfig.PROJECT_NAME).decode()
                else:
                    _dict_data[_k] = col.strip().strip('=').strip('"')
        if len(_crr_datas) % 10 == 0:
            print('_crr_datas：', len(_crr_datas))
        _crr_datas.append(_dict_data)
    return _crr_datas


@mainFunc.command()
def test_func():
    start = time.time()
    name_dict = {
        '用户账号': 'user_account',
        '用户姓名': 'user_name',
        '会员等级': 'vip_level',
        '支付层级': 'pay_level',
        '上级代理ID': 'upper_id',
        'm.user.superAgentName': 'superAgentName',
        '邀请码': 'invite_code',
        '邀请人': 'inviter',
        '用户邮箱': 'user_email',
        '用户手机': 'user_tele',
        '用户QQ': 'user_QQ',
        '登录时间': 'login_time',
        '新增时间': 'new_time',
        '是否存款': 'is_deposit',
        '存款次数': 'deposit_count',
        '存款金额': 'deposit_money',
        '取款次数': 'withdrawal_count',
        '提款金额': 'withdrawal_money',
        'facebook': 'facebook',
        'zalo': 'zalo',
        'whatsapp': 'whatsapp',
        'telegram': 'telegram',
    }
    filePath = './好运.csv'
    try:
        f = open(filePath, encoding='gbk').read()
    except:
        try:
            f = open(filePath, encoding='utf8').read()
        except:
            f = open(filePath, encoding='gb18030').read()
    ds = f.replace('\r', '').split('\n')
    header = ds[0].split(',')
    pool = multiprocessing.Pool(25)
    datas = ds[1:]
    multi_result = []
    while datas:
        crr_datas = datas[:5000]
        if not crr_datas:
            break
        del datas[:5000]
        multi_result.append(pool.apply_async(func=demo, args=(crr_datas, header, name_dict)))
    print('statt...')
    pool.close()
    pool.join()
    datas = []
    for m in multi_result:
        datas += m.get(0)

    print('data：', len(datas), 'total time:', time.time() - start)


def zd_fenxi_func(csv_data, name_dict):
    datas = []
    for row in csv_data:
        _dict_data = {}
        for k, v in row.items():
            for _k, _v in name_dict.items():
                if _k == k.replace('\ufeff', '').replace(' ','').replace('=', '').replace('"', ''):
                    if _v == 'create_time':
                        try:
                            _dict_data[_v] = datetime.datetime.strptime(v.strip().strip('=').strip('"'),'%Y-%m-%d %H:%M:%S')
                        except:
                            pass
                    elif _v == 'money':
                        _dict_data[_v] = int(float(v or 0))
                    elif _v == 'win_lose':
                        _dict_data[_v] = int(float(v or 0))
                    else:
                        _dict_data[_v] = v.strip().strip('=').strip('"')
        datas.append(_dict_data)
    return datas

@mainFunc.command()
def test1():
    import csv, datetime
    from models.fenxi_table import ImportLogTable, ZhuDanTable
    crr_date = datetime.datetime.now()
    log_datas = ImportLogTable.find_many({'create_time': {'$gt': datetime.datetime.strptime('2022-10-08 00:00:00', '%Y-%m-%d %H:%M:%S'), '$lt': crr_date}})
    for log_data in log_datas:
        filePath = app.root_path + log_data.get('file_path')
        print(filePath)
        name_dict = {
            '订单号': 'order_number',
            '会员': 'member_account',
            '下注时间': 'create_time',
            '游戏': 'game_name',
            '期号': 'date_number',
            '玩法分类': 'play_type',
            '玩法名称': 'play_name',
            '注单信息': 'zhudan_info',
            '下注金额': 'money',
            '会员输赢': 'win_lose',
        }

        csv_data = []
        try:
            with open(filePath, 'r', encoding='gbk') as fp:
                csv_data = list(csv.DictReader(fp))
        except:
            try:
                with open(filePath, 'r', encoding='utf8') as fp:
                    csv_data = list(csv.DictReader(fp))
            except:
                with open(filePath, 'r', encoding='GB2312') as fp:
                    csv_data = list(csv.DictReader(fp))
        if not csv_data:
            continue

        pool = multiprocessing.Pool(15)
        multi_result = []
        while csv_data:
            crr_datas = csv_data[:5000]
            if not crr_datas:
                break
            del csv_data[:5000]
            multi_result.append(pool.apply_async(func=zd_fenxi_func, args=(crr_datas, name_dict)))
        pool.close()
        pool.join()
        zd_fenxi_func(csv_data, name_dict)

        total_datas = []
        for m in multi_result:
            total_datas += m.get(0)

        for da in total_datas:
            da['log_uuid'] = log_data.get('uuid')
            # self.MCLS.insert_one(da)
            ZhuDanTable.update_one({'order_number': da.get('order_number')}, {'$set': da},upsert=True)


@mainFunc.command()
def update_secret_key():
    import base64
    from models.cms_table import SiteConfigModel
    site_data = SiteConfigModel.find_one({'project_name': app.config.get("PROJECT_NAME")}) or {}
    new_secret_key = base64.b64encode(os.urandom(66)).decode()
    site_data['secret_key'] = new_secret_key
    SiteConfigModel.save(site_data)
    print('success!')


def ftpBackup_func():
    PROJECT_NAME = app.config.get('PROJECT_NAME')
    crrDate = datetime.datetime.now().strftime('%Y%m%d')
    folder = f'/www/{ PROJECT_NAME }/static/{ PROJECT_NAME }/assets/backup/17_{crrDate}'
    if not os.path.exists(folder):
        os.makedirs(folder)
    os.chmod(folder, stat.S_IRWXU)

    tables = [
        SiteConfigModel,
        DomainTable, CardMerchantTable,
        CmsUserModel,
        CustomerTable, ExportDataModel,
        SiteSettingTable, ZhuDanTable, ImportLogTable, BettingDataTable, ChongZhiFenXiTable, hy_caipiao_form_tabl,
        hy_sanfang_form_table, hy_zijing_form_table, agency_caipiao_form_table, agency_sanfang_form_table,
        agency_zijing_form_table, agency_touzhu_form_table, game_yxtj_form_table, game_sfyx_form_table,
        platform_form_table, RechargeTable, FtpTable, BackupTable,
    ]

    total_count = 0
    for index, c in enumerate(tables):
        print('backup:', c.__tablename__)
        total_count += c.count({}) or 0
        file_path = f'{folder}/{c.__tablename__}.json'
        cmd = f'/www/opt/mongodb/bin/mongoexport -h 127.0.0.1:27017 -d { PROJECT_NAME } -c {c.__tablename__} -o ' + file_path
        os.system(cmd)

    cmd = f'zip -r {folder}.zip {folder}'
    os.system(cmd)
    path = (folder + '.zip').replace(f'/www/{PROJECT_NAME}/static/' + PROJECT_NAME, '')

    _backup_log = {
        'name': datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '-' + 'FTP数据备份',
        'dataCode': crrDate,
        'data_count': total_count,
        'note': '',
        '_create_time': datetime.datetime.now(),
        'folder': folder,
        'path': path,
        'total_count': total_count,
        'backup_type': backupTypes.REMOTE,
        'is_automatic': True,
    }
    BackupTable.insert_one(_backup_log)
    print('ftp upload backup...')
    ftp_data = FtpTable.find_one({}) or {}
    ftpCls = FtpCls(
        host=ftp_data.get('ftp_host'),
        user=ftp_data.get('ftp_username'),
        pwd=ftp_data.get('ftp_password')
    )
    localpath = folder + '.zip'
    server_path = ftp_data.get('server_path')
    if server_path.startswith('/'):
        remotepath = server_path + '/' + crrDate + '.zip'
    else:
        remotepath = '/' + server_path + '/' + crrDate + '.zip'

    statu, res = ftpCls.uploadFile(localpath, remotepath)
    print('result', statu, res)

    cmd = 'rm -rf ' + folder
    os.system(cmd)
    cmd = 'rm -rf ' + folder + '.zip'
    os.system(cmd)


@mainFunc.command()
def backup_func():
    while True:
        time.sleep(60)
        crr_date = datetime.datetime.now()
        if crr_date.hour < 17:
            continue

        start_time = datetime.datetime(crr_date.year, crr_date.month, crr_date.day, 0, 0, 0)
        end_time = datetime.datetime(crr_date.year, crr_date.month, crr_date.day, 23, 59, 59)
        if BackupTable.count({'_create_time': {'$gte': start_time, '$lte': end_time}, 'is_automatic': True}):
            continue
        ftpBackup_func()
        print('backup success!')


@mainFunc.command()
def test22():
    c = 0
    from models.customer_table import CustomerTable
    for d in CustomerTable.find_many({}):
        c += 1
        for _k in ['new_time', 'create_time', 'login_time']:
            _v = d.get(_k)
            if not _v:
                continue
            if isinstance(_v, str):
                try:
                    if '/' in _v:
                        d[_k] = datetime.datetime.strptime(_v.strip().strip('=').strip('"'), '%m/%d/%Y %H:%M')
                    else:
                        d[_k] = datetime.datetime.strptime(_v.strip().strip('=').strip('"'), '%Y-%m-%d %H:%M:%S')
                except:
                    print('_v:',_v)
                    continue
                CustomerTable.save(d)
        if c % 10000 == 0:
            print('crr c:', c)


@mainFunc.command()
def demo():
    crrDate = '20230821'
    _backup_log = {
        'name': datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '-' + 'FTP数据备份',
        'dataCode': crrDate,
        'data_count': 999999,
        'note': '',
        '_create_time': datetime.datetime.now(),
        'folder': '/www/project_analysisTest/static/project_analysis/assets/backup/17_20230821',
        'path': '/assets/backup/17_20230821',
        'total_count': 999999,
        'backup_type': backupTypes.REMOTE,
        'is_automatic': True,
    }
    BackupTable.insert_one(_backup_log)
    return

    for data in hy_zijing_form_table.find_many({}):
        total = 0
        for f in ['chongzhi_money', 'xscz_money', 'xxcz_money', 'hdjq_money', 'tixian_money', 'hdkq_money', 'hd_money', 'hb_money', 'czyh_money']:
            total += float(data.get(f) or 0)
        if total <= 0:
            hy_zijing_form_table.delete_one({'uuid': data.get('uuid')})
    return

    now = datetime.datetime.now()
    start_tiem = datetime.datetime(now.year, 7, 28, 0, 0, 0)
    end_time = datetime.datetime(now.year, 7, 28, 23, 59, 59)
    print(start_tiem, type(start_tiem))
    cus_datas2 = hy_zijing_form_table.find_many(
        {'form_date': {'$gte': start_tiem, '$lte': end_time}, 'parent_agent': 'dl'})
    print('elL:', len(cus_datas2))
    return


    import time
    statr_time = time.time()
    now = datetime.datetime.now() - datetime.timedelta(days=1)
    start_tiem = datetime.datetime(now.year, 7, 28, 0, 0, 0)
    end_time = datetime.datetime(now.year, 7, 28, 23, 59, 59)

    account = 'jk0001'
    ddsls = agency_touzhu_form_table.collection().aggregate([
        {"$match": {'form_date': {'$gte': start_tiem, '$lte': end_time}, 'account': 'jk0001'}},
        {"$group": {"_id": "$account", "count": {"$sum": '$customer_count'}}},
    ])
    hbtz_ls = {}
    for df in ddsls:
        print('df:', df)
        hbtz_ls[df.get('_id')] = df.get('count') or 0

    _data = {}
    _data['hbtz_count'] = hbtz_ls.get(account) or 0
    print(_data)
    return

    filter = {}
    filter['form_date'] = {'$gte': start_tiem, '$lte': end_time}

    page = 1
    per_page = 30
    skip = (page - 1) * per_page
    cp_datas = hy_caipiao_form_tabl.find_many(filter, sort=[['form_date', -1]])
    sfyx_datas = hy_sanfang_form_table.find_many(filter, sort=[['form_date', -1]])
    zj_datas = hy_zijing_form_table.find_many(filter, sort=[['form_date', -1]])

    account_ls = []
    ad_dict = {}
    for td in cp_datas:
        account = td.get('account')
        ad_dict[account] = td.get('parent_agent')
        account_ls.append(account)
    for td in sfyx_datas:
        account = td.get('account')
        ad_dict[account] = td.get('parent_agent')
        account_ls.append(account)
    for td in zj_datas:
        account = td.get('account')
        ad_dict[account] = td.get('parent_agent')
        account_ls.append(account)
    account_ls = list(set(account_ls))
    total = len(account_ls)
    print(time.time() - statr_time)


if __name__ == '__main__':
    mainFunc()

