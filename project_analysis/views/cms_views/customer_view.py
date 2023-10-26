# -*- coding: utf-8 -*-
import datetime, csv, os, shortuuid, threading, random, multiprocessing
from flask import abort, request, render_template, current_app
from .cms_base import CmsFormViewBase
from models.customer_table import CustomerTable, ExportDataModel
from common_utils.utils_funcs import PagingCLS, RC4CLS
from constants import ASSETS_FOLDER, EXPORT_FOLDER, ExportStatu
from views.view_func import fenxi_func



class CustomerManager(CmsFormViewBase):
    title = '客户信息管理'
    MCLS = CustomerTable
    add_url_rules = [['/customer/', 'customer']]
    template = 'fenXi/customer.html'
    per_page = 100
    sort = [['new_time', -1]]

    def export_csv(self, uuid, datas, export_folder, filename, project_name):
        name_dict = {
            '用户账号': 'user_account',
            '用户姓名': 'user_name',
            '会员等级': 'vip_level',
            '支付层级': 'pay_level',
            '上级代理ID': 'upper_id',
            '上级代理': 'agency',
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

            '用户帐号': 'user_account',
            '用户等级': 'vip_level',
            '充值层级': 'pay_level',
            '提款次数': 'withdrawal_count',
        }

        export_data = ExportDataModel.find_one({'uuid': uuid})
        if not export_data:
            return
        try:
            if not os.path.exists(export_folder):
                os.makedirs(export_folder)
            header, datas_ls = [], []
            crr_count = 0
            for k, v  in name_dict.items():
                header.append(k)
            for data_dict in datas:
                data_l = []
                for db_field in name_dict.values():
                    field_cls = self.MCLS.fields().get(db_field)
                    data = data_dict.get(db_field)
                    data = field_cls.transform(data)
                    _v = data or ''
                    if field_cls.field_type == 'DictField':
                        _v = field_cls.dict_cls.name_dict.get(data)
                    elif field_cls.field_type == 'BooleanField':
                        if data:
                            _v = field_cls.true_text
                        else:
                            _v = field_cls.false_text
                    elif db_field == 'user_tele':
                        _v = RC4CLS.decrypt(_v, project_name)
                    data_l.append(_v)
                datas_ls.append(data_l)
                crr_count += 1
                if crr_count % 100 == 0:
                    export_data['out_count'] = crr_count
                    ExportDataModel.save(export_data)
            file_path = os.path.join(export_folder, filename)
            with open(file_path, 'w', encoding='gbk') as fw:
                wr = csv.writer(fw)
                wr.writerow(header)
                wr.writerows(datas_ls)
            export_data['out_count'] = crr_count
            export_data['statu'] = ExportStatu.successed
            ExportDataModel.save(export_data)
            return True
        except Exception as e:
            export_data['note'] = str(e)
            export_data['statu'] = ExportStatu.failed
            ExportDataModel.save(export_data)
            return

    def out_data_func(self):
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        if not fext.endswith('csv'):
            return self.xtjson.json_params_error('文件格式错误，只支持CSV文件上传！')
        absolute_folter = os.path.join(current_app.root_path, self.project_static_folder)
        export_folder = os.path.join(absolute_folter, ASSETS_FOLDER, EXPORT_FOLDER)
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)
        filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S_') + str(random.choice(range(100, 999))) + '.csv'
        filePath = export_folder + '/' + filename
        fileobj.save(filePath)

        try:
            f = open(filePath, 'r', encoding='gbk').read()
        except:
            try:
                f = open(filePath, 'r', encoding='utf8').read()
            except:
                f = open(filePath, 'r', encoding='gb18030').read()
        file_text = f.replace('\r', '').replace('"', '').replace('=', '').replace('\ufeff', '').split('\n')

        user_accunts = []
        for ft in file_text[1:]:
            user_accunts.append(ft.replace('"','').replace('=','').replace('\r', '').split(',')[0])

        if len(user_accunts) > 65535:
            return self.xtjson.json_params_error(f'导出文件数量过大(csv，单个文件最大量为65535)')

        datas = []
        for d in user_accunts:
            _d = self.MCLS.find_one({'user_account': d})
            if not _d:
                print("d:", d)
                continue
            datas.append(_d)

        absolute_folter = os.path.join(current_app.root_path, self.project_static_folder)
        export_folder = os.path.join(absolute_folter, ASSETS_FOLDER, EXPORT_FOLDER)
        filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S_') + str(random.choice(range(100, 999))) + '.csv'
        _out_data_dict = {
            'filename': filename,
            'statu': ExportStatu.ongoing,
            'path': os.path.join(export_folder, filename).replace(absolute_folter, ''),
            'total': len(datas),
            'out_count': 0,
        }
        uuid = ExportDataModel.insert_one(_out_data_dict)

        threading.Thread(target=self.export_csv, args=(uuid, datas, export_folder, filename, current_app.config.get('PROJECT_NAME'))).start()
        return self.xtjson.json_result(message='后台导出中，请稍后到导出数据管理中进行下载！')

    def format_datetime(self, data):
        if isinstance(data, datetime.datetime):
            return data.strftime('%Y-%m-%d %H:%M:%S')
        return data

    def del_all(self):
        self.MCLS.delete_many({})

    def duplicateRemoval_func(self):
        ''' 检测去重 '''
        d_ls = []
        for da in self.MCLS.find_many({}):
            user_account = da.get('user_account')
            if user_account not in d_ls:
                d_ls.append(user_account)
                continue
            self.MCLS.delete_one({'uuid': da.get('uuid')})

    def fenXi_csv(self, filePath):
        name_dict = {
            '用户账号': 'user_account',
            '用户姓名': 'user_name',
            '会员等级': 'vip_level',
            '支付层级': 'pay_level',
            '上级代理ID': 'upper_id',
            '上级代理': 'agency',
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

            '用户帐号': 'user_account',
            '用户等级': 'vip_level',
            '充值层级': 'pay_level',
            '提款次数': 'withdrawal_count',
        }

        try:
            f = open(filePath, 'r', encoding='gbk').read()
        except:
            try:
                f = open(filePath, 'r', encoding='utf8').read()
            except:
                f = open(filePath, 'r', encoding='gb18030').read()
        ds = f.replace('\r', '').replace('"', '').replace('=', '').replace('\ufeff', '').split('\n')
        header = ds[0].split(',')

        pool = multiprocessing.Pool(25)
        datas = ds[1:]
        multi_result = []
        while datas:
            crr_datas = datas[:5000]
            if not crr_datas:
                break
            del datas[:5000]
            multi_result.append(pool.apply_async(func=fenxi_func, args=(crr_datas, header, name_dict, current_app.config.get('PROJECT_NAME'))))
        pool.close()
        pool.join()
        total_datas = []
        for m in multi_result:
            total_datas += m.get(0)

        return total_datas

    def import_data(self, datas):
        for da in datas:
            user_account = da.get('user_account')
            self.MCLS.update_one({'user_account': user_account}, {'$set': da},upsert=True)

    def view_get(self):
        if 'customerManager' not in self.current_admin_user.permissions and not self.current_admin_user.is_superadmin:
            return abort(404)

        self.context['title'] = self.title
        self.context['format_datetime'] = self.format_datetime
        page = request.args.get('page', 1, int)
        skip = (page - 1) * self.per_page
        self.context['title'] = self.title
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
        dd = CustomerTable.collection().aggregate([
            {"$match": {}},
            {"$group": {"_id": "$user_name", "count": {"$sum": 1}}}
        ])
        dddddd = {dl.get('_id'): dl.get('count') for dl in list(dd)}
        _datas = []
        for dll in all_datas:
            dll['tm_count'] = dddddd.get(dll.get('user_name') or '') or ''
            _datas.append(dll)

        pagination = PagingCLS.pagination(page, self.per_page, total)
        self.context['total'] = total
        self.context['all_datas'] = _datas
        self.context['pagination'] = pagination
        self.context['search_res'] = context_res
        return render_template(self.template, **self.context)

    def post_other_way(self):
        if self.action == 'importData':
            fileobj = request.files['upload']
            fname, fext = os.path.splitext(fileobj.filename)
            if not fext.endswith('csv'):
                return self.xtjson.json_params_error('文件格式错误，只支持CSV文件上传！')
            import_folder = current_app.root_path + '/' + self.project_static_folder + '/importFile/'
            if not os.path.exists(import_folder):
                os.makedirs(import_folder)

            new_filename = shortuuid.uuid()
            fileobj.save(import_folder + new_filename + fext)
            filePath = import_folder + new_filename + fext

            datas = self.fenXi_csv(filePath)
            if not datas:
                return self.xtjson.json_params_error('文件无数据！')

            threading.Thread(target=self.import_data, args=(datas,)).start()
            return self.xtjson.json_result(message=f'数据提交成功 后台储存中，请稍后刷新查看！')
        if self.action == 'exportData':
            return self.out_data_func()
        if self.action == 'del_all':
            threading.Thread(target=self.del_all).start()
            return self.xtjson.json_result(message='删除中， 请稍后刷新查看！')
        if self.action == 'duplicateRemoval':
            threading.Thread(target=self.duplicateRemoval_func).start()
            return self.xtjson.json_result(message='后台检测去重中...')

    def post_data_other_way(self):
        if self.action == 'del':
            self.MCLS.delete_one({'uuid': self.data_uuid})
            return self.xtjson.json_result()



class ExportManager(CustomerManager):
    title = '文件下载'
    MCLS = ExportDataModel
    add_url_rules = [['/exportManager/', 'exportManager']]
    template = 'fenXi/exportManager.html'
    per_page = 20
    sort = [['_create_time', -1]]

    def view_get(self):
        if 'exportDataManager' not in self.current_admin_user.permissions and not self.current_admin_user.is_superadmin:
            return abort(404)

        self.context['title'] = self.title
        self.context['format_datetime'] = self.format_datetime
        page = request.args.get('page', 1, int)
        skip = (page - 1) * self.per_page
        self.context['title'] = self.title
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
        return render_template(self.template, **self.context)

    def post_other_way(self):
        if self.action == 'del_all':
            self.MCLS.delete_many({})
            return self.xtjson.json_result()

    def post_data_other_way(self):
        if self.action == 'del':
            try:
                filePath = current_app.static_folder + '/' + current_app.config.get(
                    'PROJECT_NAME') + self.data_dict.get('path')
                os.remove(filePath)
            except:
                pass
            self.MCLS.delete_one({'uuid': self.data_uuid})
            return self.xtjson.json_result(message='数据删除成功！')

