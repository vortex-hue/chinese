# -*- coding: utf-8 -*-
import os, datetime, threading, json

import shortuuid
from flask import render_template, request, current_app
from .cms_base import CmsFormViewBase
from common_utils.utils_funcs import PagingCLS
from models.cms_table import SiteConfigModel
from models.domain_table import DomainTable, CardMerchantTable
from models.cms_user import CmsUserModel
from models.customer_table import CustomerTable, ExportDataModel
from models.fenxi_table import SiteSettingTable,ZhuDanTable,ImportLogTable,BettingDataTable,ChongZhiFenXiTable,hy_caipiao_form_tabl,hy_sanfang_form_table,hy_zijing_form_table,agency_caipiao_form_table,agency_sanfang_form_table,agency_zijing_form_table,agency_touzhu_form_table,game_yxtj_form_table,game_sfyx_form_table,platform_form_table,RechargeTable,FtpTable,BackupTable
from werkzeug.security import generate_password_hash, check_password_hash
from constants import backupTypes
from modules.ftp_cls import FtpCls
from common_utils.lqredis import SiteRedis


class CmsIndexView(CmsFormViewBase):
    title = '注单分析'
    show_menu = False
    add_url_rules = [['/', 'cms_index']]
    template = 'fenXi/index.html'

    def view_get(self):
        print("Dashboard Page")
        self.context['title'] = self.title
        return render_template(self.template, **self.context)



class BackupDataCls(CmsFormViewBase):
    per_page = 50
    sort = [['_create_time', -1]]
    add_url_rules = [['/backupData/', 'backupData']]
    MCLS = BackupTable
    title = '数据备份'
    tables = [
        DomainTable, CardMerchantTable,
        CustomerTable, ExportDataModel,
        ZhuDanTable, ImportLogTable, BettingDataTable, ChongZhiFenXiTable, hy_caipiao_form_tabl,
        hy_sanfang_form_table, hy_zijing_form_table, agency_caipiao_form_table, agency_sanfang_form_table,
        agency_zijing_form_table, agency_touzhu_form_table, game_yxtj_form_table, game_sfyx_form_table,
        platform_form_table, RechargeTable
    ]

    def toBackup_func(self, folder, PROJECT_NAME):
        for c in self.tables:
            c.delete_many({})
            cmd = f'/www/opt/mongodb/bin/mongoimport -h 127.0.0.1:27017 -d {PROJECT_NAME} -c {c.__tablename__} --file {folder}/{c.__tablename__}.json'
            os.system(cmd)

    def toRemoteBackup_func(self, folder, dataCode, total_count, keyId='', PROJECT_NAME=''):
        ftp_data = FtpTable.find_one({}) or {}
        ftpCls = FtpCls(
            host=ftp_data.get('ftp_host'),
            user=ftp_data.get('ftp_username'),
            pwd=ftp_data.get('ftp_password'),
            dataKey=keyId,
            total_count=total_count,
        )
        print('ftp_data:', ftp_data)
        server_path = ftp_data.get('server_path')
        localpath = folder+'.zip'
        if server_path.startswith('/'):
            remotepath = server_path + '/' + dataCode + '.zip'
        else:
            remotepath = '/' + server_path + '/' + dataCode + '.zip'
        if os.path.exists(localpath.replace('.zip', '')):
            cmd = 'rm -rf ' + localpath.replace('.zip', '')
            os.system(cmd)
        if os.path.exists(localpath):
            cmd = 'rm ' + localpath
            os.system(cmd)
        state, res = ftpCls.downLoadFile(localpath, remotepath)
        if not state:
            _pdata = {
                'statu': 'error',
                'total_count': total_count,
                'msg': '备份ftp远程下载失败！'
            }
            SiteRedis.set(keyId, json.dumps(_pdata), expire=60 * 10)
            return

        cmd = f'unzip { localpath } -d {localpath.replace(".zip", "")}'
        os.system(cmd)

        for path, directories, files in os.walk(localpath.replace(".zip", "")):
                for f in files:
                    if '.json' in f:
                        cmd = f'mv {path}/{f} {localpath.replace(".zip", "")}'
                        os.system(cmd)

        _pdata = {
            'statu': 'jxz',
            'total_count': total_count,
            'msg': '原数据删除中！'
        }
        SiteRedis.set(keyId, json.dumps(_pdata), expire=60 * 10)
        for c in self.tables:
            c.delete_many({})
        _pdata = {
            'statu': 'jxz',
            'toBackup': True,
            'total_count': total_count,
            'msg': '备份还原中...',
        }
        SiteRedis.set(keyId, json.dumps(_pdata), expire=60 * 10)
        for c in self.tables:
            print('toto:', c.__tablename__)
            c.delete_many({})
            cmd = f'/www/opt/mongodb/bin/mongoimport -h 127.0.0.1:27017 -d {PROJECT_NAME} -c {c.__tablename__} --file {localpath.replace(".zip", "")}/{c.__tablename__}.json'
            print('cmd:', cmd)
            os.system(cmd)

    def format_datetime(self, data):
        if isinstance(data, datetime.datetime):
            return data.strftime('%Y-%m-%d %H:%M:%S')
        return data

    def check_password(self, pwd, rawpwd):
        """
        :param pwd: 密文
        :param rawpwd: 明文
        """
        return check_password_hash(pwd, rawpwd)

    def selectDelBackup_func(self):
        html = f'''
            <div class="input-group mb-3">
                <div class="input-group-prepend"><span class="input-group-text">备份类型：</span></div>
                <select class="form-control" id="backup_type" aria-label="">
                    <option value="">备份类型</option>
                    <option value="local">本地备份</option>
                    <option value="remote">FTP 远程备份</option>
                </select>                   
            </div>                
            <div class="input-group mb-3">
                <div class="input-group-prepend"><span class="input-group-text">入职日期：</span></div>
                <input type="text" class="form-control pickerdate" onmouseenter="$.picker_YY_HH_DD_HH_MM_SS('.pickerdate');" id="selectBackupDate" placeholder="日期范围" value="">
            </div>                
            <span class="btn btn-primary swal2-styled" onclick="post_select_del()" style="margin: 20px 10px;">确定</span>
            <span class="btn btn-default swal2-styled" onclick="xtalert.close()" style="margin: 20px 10px;">取消</span>                      
        '''
        return self.xtjson.json_result(message=html)

    def view_get(self):
        self.context['title'] = self.title
        self.context['format_datetime'] = self.format_datetime
        page = request.args.get('page', 1, int)
        skip = (page - 1) * self.per_page

        filter_dict, context_res = {}, {}
        fields = self.MCLS.fields()
        self.context['FIELDS'] = fields
        statu, res = self.search_func(fields)
        if not statu:
            return res

        filter_dict.update(res[0])
        context_res.update(res[1])
        self.context.update(self.get_context())
        filter_dict.update(self.get_filter_dict())
        total = self.MCLS.count(filter_dict)
        all_datas = self.MCLS.find_many(filter_dict, limit=self.per_page, skip=skip, sort=self.sort)

        pagination = PagingCLS.pagination(page, self.per_page, total)
        self.context['total'] = total
        self.context['all_datas'] = all_datas
        self.context['pagination'] = pagination
        self.context['search_res'] = context_res
        return render_template('fenXi/backupData.html', **self.context)

    def post_other_way(self):
        if self.action == 'getProgres':
            total_count = 0
            for c in self.tables:
                total_count += c.count({}) or 0
            return self.xtjson.json_result(data={'v': total_count})
        if self.action == 'delAllBackup':
            for data in self.MCLS.find_many({}):
                folder = data.get('folder') or ''
                cmd = 'rm -rf ' + folder
                os.system(cmd)

                cmd = 'rm -rf ' + folder + '.zip'
                os.system(cmd)
                self.MCLS.delete_one(data)
            return self.xtjson.json_result()
        if self.action == 'selectDelBackup_html':
            return self.selectDelBackup_func()
        if self.action == 'selectDel':
            backup_type = self.request_data.get('backup_type')
            selectBackupDate = self.request_data.get('selectBackupDate')
            if not selectBackupDate or not backup_type:
                return self.xtjson.json_params_error()
            start_time, end_time = PagingCLS.by_silce(selectBackupDate)
            crrD = datetime.datetime.now() + datetime.timedelta(days=7)
            if start_time > crrD or crrD < end_time:
                return self.xtjson.json_params_error('七天内备份不允许删除！')

            for data in self.MCLS.find_many({'_create_time': {'$gte': start_time, '$lte': end_time}, 'backup_type': backup_type}):
                folder = data.get('folder') or ''
                cmd = 'rm -rf ' + folder
                os.system(cmd)

                cmd = 'rm -rf ' + folder + '.zip'
                os.system(cmd)
                self.MCLS.delete_one(data)
            return self.xtjson.json_result()
        if self.action == 'toBackup_chack':
            data_value = self.request_data.get('data_value')
            if not data_value:
                return self.xtjson.json_params_error('缺少恢复密码！')
            systemConfig = SiteSettingTable.find_one({}) or {}
            low_pwd = systemConfig.get('restore_data_pwd')
            if not low_pwd:
                return self.xtjson.json_params_error('未设置恢复密码，不可恢复！')
            if not self.check_password(low_pwd, data_value.strip()):
                return self.xtjson.json_params_error('恢复密码不正确！')
            return self.xtjson.json_result()
        if self.action == 'ycyyProgres':
            keyId = self.request_data.get('keyId')
            if not keyId:
                return self.xtjson.json_params_error()
            dataj = SiteRedis.get(keyId)
            if not dataj:
                return self.xtjson.json_params_error()
            data_json = json.loads(dataj.decode())
            print('data_json111:', data_json)
            total_count = data_json.get('total_count')
            if not total_count:
                return self.xtjson.json_result(data={'statu': 'success'})
            if data_json.get('toBackup'):
                crr_total_count = 0
                for c in self.tables:
                    crr_total_count += c.count({}) or 0
                print('crr_total_count:',crr_total_count)
                if crr_total_count >= total_count:
                    statu = 'success'
                    msg = '备份恢复成功！'
                    data_json.update({
                        'msg': msg,
                        'statu': statu,
                    })
                else:
                    cv = crr_total_count / total_count
                    msg = '备份还原中，进度：%.2f' % cv
                    data_json.update({
                        'msg': msg,
                    })
            return self.xtjson.json_result(data=data_json)


    def post_data_other_way(self):
        if self.action == 'toBackup':
            if self.data_dict.get('backup_type') == backupTypes.LOCAL:
                folder = self.data_dict.get('folder') or ''
                threading.Thread(target=self.toBackup_func, args=(folder, current_app.config.get("PROJECT_NAME"))).start()
                return self.xtjson.json_result(data={'total': self.data_dict.get('total_count')})

            return self.xtjson.json_params_error('备份恢复失败！')
        if self.action == 'del':
            folder = self.data_dict.get('folder') or ''
            cmd = 'rm -rf ' + folder
            os.system(cmd)

            cmd = 'rm -rf ' + folder + '.zip'
            os.system(cmd)
            self.MCLS.delete_one(self.data_dict)
            return self.xtjson.json_result(message='备份删除成！')
        if self.action == 'toRemoteBackup':
            if self.data_dict.get('backup_type') == backupTypes.REMOTE:
                keyId = 'toRemoteBackup_'+shortuuid.uuid()
                folder = self.data_dict.get('folder') or ''
                dataCode = self.data_dict.get('dataCode') or ''
                total_count = self.data_dict.get('total_count') or ''
                threading.Thread(target=self.toRemoteBackup_func, args=(folder, dataCode, total_count, keyId, current_app.config.get("PROJECT_NAME"))).start()
                return self.xtjson.json_result(data={'keyId': keyId})
            return self.xtjson.json_params_error('备份恢复失败！')
