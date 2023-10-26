# -*- coding: UTF-8 -*-
import time, shortuuid, datetime
from random import randint
from flask import session, request, abort
from constants import SITE_CONFIG_CACHE, SpiderType, ClientType, CMS_USER_SESSION_KEY, SITE_SETTING_CACHE, PermissionType, WF_ZH_DICT
from models.cms_user import CmsUserModel
from common_utils.utils_funcs import get_ip, is_wap, RC4CLS
from common_utils.lqredis import SiteRedis


def current_admin_data_dict():
    uuid = session.get(CMS_USER_SESSION_KEY)
    if CMS_USER_SESSION_KEY in session:
        uuid = session[CMS_USER_SESSION_KEY]
    if not uuid:
        return {}
    user_dict = CmsUserModel.find_one({'uuid': uuid})
    return user_dict

def add_admin_log(event_type, content='', ip='', admin_uuid='', look_over=True, **kwargs):
    if not admin_uuid:
        admin_data = current_admin_data_dict()
        admin_uuid = admin_data.get('uuid')
    log_dict = {
        'ip': ip or get_ip(),
        'referer': str(request.referrer),
        'request_url': str(request.url),
        'user_agent': str(request.user_agent),
        'content': content,
        'event_type': event_type,
        'admin_uuid': admin_uuid,
        'look_over': look_over,
    }
    if kwargs:
        log_dict.update(kwargs)
    return

def get_front_domain():
    if not hasattr(SITE_CONFIG_CACHE, 'front_domain'):
        return False, '网站前端域名未设置!'
    front_domain = getattr(SITE_CONFIG_CACHE, 'front_domain')
    if not front_domain:
        return False, '网站前端域名未设置'
    return True, front_domain

def check_front_site_statu():
    if not hasattr(SITE_CONFIG_CACHE, 'site_statu'):
        return False
    if not getattr(SITE_CONFIG_CACHE, 'site_statu'):
        return False
    return True

def spider_ident():
    ua = str(request.user_agent)
    if ua:
        for k,v in SpiderType.spider_mark.items():
            for u in v:
                if u in ua:
                    return getattr(SpiderType, k)
    return ''

def front_access_log(**kwargs):
    res = spider_ident()
    client_type = ClientType.PC
    if is_wap():
        client_type = ClientType.WAP
    log_dict = {
        'ip': get_ip(),
        'look_over': False,
        'spider_type': res,
        'client_type': client_type,
        'request_url': request.url,
        'user_agent': str(request.user_agent),
        'referer': request.referrer or '',
    }
    if kwargs:
        log_dict.update(kwargs)

def check_black():
    """检测黑名单"""
    if not hasattr(SITE_CONFIG_CACHE, 'ip_black'):
        return
    ip_black = getattr(SITE_CONFIG_CACHE, 'ip_black')
    if not ip_black or not ip_black.strip():
        return
    crr_ip = get_ip()
    for _ip in crr_ip.split():
        if _ip in crr_ip:
            return True
    return


def front_risk_control():
    # if not check_front_site_statu():
    #     return False, '网站维护中...暂时关闭对外开放!'
    # statu, front_domain = get_front_domain()
    # if not statu:
    #     return False, '网站维护中...暂时关闭对外开放!'
    # if request.host not in front_domain:
    #     return False, abort(404)
    # if check_black():
    #     return False, abort(404)
    # front_access_log()
    return True, None


def check_cms_domain():
    crr_user = current_admin_data_dict()
    if not crr_user:
        return True, ''
    if crr_user and crr_user.get('permissions') == [PermissionType.SUPERADMIN]:
        return True, ''
    if not hasattr(SITE_SETTING_CACHE, 'blacklistIp'):
        return True, ''
    blacklistIp = getattr(SITE_SETTING_CACHE, 'blacklistIp')
    if not blacklistIp:
        return True, ''
    if get_ip() in blacklistIp:
        return True, ''
    session.pop(CMS_USER_SESSION_KEY)
    return False, ''

def cms_risk_control():
    statu, res = check_cms_domain()
    if not statu:
        return abort(404)


def fenxi_func(dsl, header, name_dict, PROJECT_NAME):
    _crr_datas = []
    for row in dsl:
        _dict_data = {}
        for index, col in enumerate(row.split(',')):
            if index >= len(header):
                continue
            _h = header[index].replace(' ', '').replace('=', '').replace('"', '')
            _k = name_dict.get(_h)
            if not _k:
                continue
            if _k in ['new_time', 'create_time', 'login_time']:
                try:
                    _dict_data[_k] = datetime.datetime.strptime(col.strip().strip('=').strip('"'), '%Y-%m-%d %H:%M:%S')
                except:
                    try:
                        _dict_data[_k] = datetime.datetime.strptime(col.strip().strip('=').strip('"'), '%m/%d/%Y %H:%M')
                    except:
                        _dict_data[_k] = col.strip().strip('=').strip('"')
            elif _k == 'user_tele':
                _dict_data[_k] = RC4CLS.encrypt(col.strip().strip('=').strip('"'), secret_key=PROJECT_NAME).decode()
            else:
                _dict_data[_k] = col.strip().strip('=').strip('"')
        _crr_datas.append(_dict_data)
    return _crr_datas


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
                    if _v == 'new_time':
                        if not v:
                            _dict_data['new_time'] = ''
                        else:
                            try:
                                _dict_data['new_time'] = datetime.datetime.strptime(v, '%m/%d/%Y %H:%M')
                            except:
                                _dict_data['new_time'] = datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S')

                    elif _v == 'money':
                        _dict_data[_v] = int(float(v or 0))
                    elif _v == 'win_lose':
                        _dict_data[_v] = int(float(v or 0))
                    else:
                        _dict_data[_v] = v.strip().strip('=').strip('"')
        datas.append(_dict_data)
    return datas



from models.fenxi_table import ZhuDanTable, BettingDataTable
from constants import PLAY_NAMES

def format_money(data):
    try:
        return format(int(data), ",")
    except:
        return data

def prve_date_number(game_name, date_number):
    datas = ZhuDanTable.distinct('date_number', filter={'game_name': game_name})
    dls = []
    for d in datas:
        dls.append(datetime.datetime.strptime(d, '%d/%m/%Y'))
    dls.sort()
    date_number = datetime.datetime.strptime(date_number, '%d/%m/%Y')
    if date_number not in dls:
        return
    crr_index = dls.index(date_number)
    return dls[crr_index - 1].strftime('%d/%m/%Y')

def contrast1_func(game_name, wf, danShu, renShu, zongE, prve_date_number_data, datas):
    if not prve_date_number_data:
        return {'db_danShu': '', 'db_renShu': '', 'db_zongE': ''}

    _das = ZhuDanTable.find_many({'date_number': prve_date_number_data, 'game_name': game_name, 'play_name': wf})
    db_danShu_z = 0
    if _das:
        db_danShu_z = len(_das)
    db_renShu_ls = []
    db_zongE_z = 0
    for _fd in _das:
        if _fd.get('member_account') not in db_renShu_ls:
            db_renShu_ls.append(_fd.get('member_account'))
        db_zongE_z += _fd.get('money')

    if db_danShu_z:
        db_danShu = str(round((abs(danShu - db_danShu_z))*100 / db_danShu_z, 2)) + '%'
        if danShu - db_danShu_z < 0:
            db_danShu = '-' + db_danShu
    else:
        db_danShu = '100%'

    if db_renShu_ls:
        db_renShu = str(round(((abs(renShu - len(db_renShu_ls)))*100 / len(db_renShu_ls)), 2)) + '%'
        if renShu - len(db_renShu_ls) < 0:
            db_renShu = '-' + db_renShu
    else:
        db_renShu = '100%'

    if db_zongE_z:
        db_zongE = str(round((abs(zongE - db_zongE_z) / db_zongE_z) * 100, 2)) + '%'
        if zongE - db_zongE_z < 0:
            db_zongE = '-' + db_zongE
    else:
        db_zongE = '100%'

    return {
        'db_danShu': db_danShu,
        'db_renShu': db_renShu,
        'db_zongE': db_zongE
    }

def get_new_zhudan_info_func(zhudan_info, play_name):
    new_zhudan_info_ls = []
    for zi in zhudan_info:
        if '|' not in zi:
            for zd in zi.strip().split(','):
                new_zhudan_info_ls.append(zd)
            continue

        # 1位数
        if play_name in PLAY_NAMES.ONE:
            for vhz_s1 in zi.split('|'):
                new_zhudan_info_ls.append(vhz_s1)
            continue

        # 2位数
        if play_name in PLAY_NAMES.TWO:
            if zi.count('|') == 1:
                hz_s = zi.split('|')
                for vhz_s1 in hz_s[0].split(','):
                    for xhz_s2 in hz_s[1].split(','):
                        new_zhudan_info_ls.append(vhz_s1 + xhz_s2)
                continue
            if zi.count('|') >= 2 and ',' not in zi:
                for vhz_s1 in zi.split('|'):
                    new_zhudan_info_ls.append(vhz_s1)
                continue
            if zi.count('|') >= 2:
                continue
        # 3位数
        if play_name in PLAY_NAMES.THREE:
            if zi.count('|') < 2:
                continue
            elif zi.count('|') == 2:
                hz_s = zi.split('|')
                for vhz_s1 in hz_s[0].split(','):
                    for xhz_s2 in hz_s[1].split(','):
                        for xhz_s3 in hz_s[2].split(','):
                            new_zhudan_info_ls.append(vhz_s1 + xhz_s2 + xhz_s3)
                continue
            elif zi.count('|') >= 2 and ',' not in zi:
                for vhz_s1 in zi.split('|'):
                    new_zhudan_info_ls.append(vhz_s1)
                continue
        # 4位数
        if play_name in PLAY_NAMES.FOUR:
            if zi.count('|') < 3:
                continue
            elif zi.count('|') == 3:
                hz_s = zi.split('|')
                for vhz_s1 in hz_s[0].split(','):
                    for xhz_s2 in hz_s[1].split(','):
                        for xhz_s3 in hz_s[2].split(','):
                            for xhz_s4 in hz_s[3].split(','):
                                new_zhudan_info_ls.append(vhz_s1 + xhz_s2 + xhz_s3 + xhz_s4)
                continue
            elif zi.count('|') >= 3 and ',' not in zi:
                for vhz_s1 in zi.split('|'):
                    new_zhudan_info_ls.append(vhz_s1)
                continue

    return new_zhudan_info_ls

def data_fenxi_func(datas, daten, game_name):
    """
    注单分析
    :param datas: 数据列表
    :param daten: 期号
    :param game_name: 游戏/城市名称
    :return:
    """
    biShu = len(datas)
    zongE = 0
    zongShuYing = 0
    renShu_ls = []
    wanFa_ls = []
    wfxz_zongE = {}
    prve_date_number_data = prve_date_number(game_name, daten) # 获取上期期数
    for d in datas:
        zongE += d.get('money')
        zongShuYing += d.get('win_lose')
        if d.get('member_account') not in renShu_ls:
            renShu_ls.append(d.get('member_account'))
        if d.get('play_name') not in wanFa_ls:
            wanFa_ls.append(d.get('play_name'))
        if d.get('play_name') not in wfxz_zongE:
            wfxz_zongE[d.get('play_name')] = 0
        else:
            _v = wfxz_zongE.get(d.get('play_name')) or 0
            wfxz_zongE[d.get('play_name')] = _v + (d.get('money') or 0)

    new_wfxz_zongE = []
    for k, v in wfxz_zongE.items():
        new_wfxz_zongE.append({
            'value': v,
            'name': k,
        })

    low_duiBi1 = []
    wanFaTop5_list = []
    da_number, xiao_number, shuang_number, dan_number = 0, 0, 0, 0

    paiXu = {}
    for w in wanFa_ls:
        if w not in PLAY_NAMES.ONE and w not in PLAY_NAMES.TWO and w not in PLAY_NAMES.THREE and w not in PLAY_NAMES.FOUR:
            continue
        wdatas = ZhuDanTable.find_many({'play_name': w, 'date_number': daten, 'game_name': game_name})
        num_dict = {}
        _bresult = {
            'name': w,
            'danShu': len(wdatas),
        }
        _renShu = []
        _zongE = 0
        win_lose_total = 0

        for wd in wdatas:
            if wd.get('member_account') not in _renShu:
                _renShu.append(wd.get('member_account'))
            win_lose_total += wd.get('win_lose')
            _zongE += wd.get('money')
            play_name = wd.get('play_name') or ''
            if not play_name:
                continue
            zhudan_info = wd.get('zhudan_info') or ''
            zhudan_info = zhudan_info.strip().split(' ')
            new_zhudan_info_ls = get_new_zhudan_info_func(zhudan_info, play_name)

            pj = round(wd.get('money') / len(new_zhudan_info_ls), 2)
            for zi in new_zhudan_info_ls:
                if 'Tài' in zi:
                    da_number += pj
                    continue
                if 'Xỉu' in zi:
                    xiao_number += pj
                    continue
                if 'Chẵn' in zi:
                    dan_number += pj
                    continue
                if 'Lẻ' in zi:
                    shuang_number += pj
                    continue
                _v = num_dict.get(zi) or 0
                _vv = _v + pj
                num_dict[zi] = _vv

        _bresult['_renShu'] = len(_renShu)
        _bresult['_zongE'] = _zongE
        _bresult['win_lose_total'] = win_lose_total

        _bresult.update(contrast1_func(game_name, w, len(wdatas), len(_renShu), _zongE, prve_date_number_data, datas))

        if w not in ['Tài', 'Xỉu', 'Chẵn', 'Lẻ'] and not w.isdigit():
            wanFaTop5_list.append({
                'wanFa': w,
                'allData': num_dict
            })
        paiXu[str(len(low_duiBi1))] = _zongE
        low_duiBi1.append(_bresult)

    duiBi1 = []
    student_tuplelist_sorted = sorted(paiXu.items(), key=lambda x: x[1], reverse=True)
    for df in student_tuplelist_sorted:
        duiBi1.append(low_duiBi1[int(df[0])])

    new_wanFaTop5_list = []
    da_total, xiao_total, dan_total, shuang_total = 0, 0, 0, 0
    for wn in wanFaTop5_list:
        for wk, wv in wn.get('allData').items():
            if int(str(wk)[-1]) >= 5:
                da_total += 1
            else:
                xiao_total += 1

            if int(str(wk)[-1]) % 2 == 0:
                shuang_total += 1
            else:
                dan_total += 1

    n_total = da_total + xiao_total + dan_total + shuang_total
    if n_total:
        if da_total:
            da_pj = round(da_number / 5 / da_total, 2)
        else:
            da_pj = 0
        if xiao_total:
            xiao_pj = round(da_number / 5 / xiao_total, 2)
        else:
            xiao_pj = 0
        if dan_total:
            dan_pj = round(da_number / 5 / dan_total, 2)
        else:
            dan_pj = 0
        if shuang_total:
            shuang_pj = round(da_number / 5 / shuang_total, 2)
        else:
            shuang_pj = 0
        for wn2 in wanFaTop5_list:
            _new_dict = {
                'wanFa': wn2.get('wanFa'),
            }
            num_dict = {}
            for nk, nv in wn2.get('allData').items():
                if int(str(nk)[-1]) >= 5:
                    nv += da_pj
                else:
                    nv += xiao_pj

                if int(str(nk)[-1]) % 2 == 0:
                    nv += shuang_pj
                else:
                    nv += dan_pj

                num_dict[nk] = nv
            a1 = sorted(num_dict.items(), key=lambda x: x[1], reverse=True)
            _new_dict['top5'] = a1[:5]
            new_wanFaTop5_list.append(_new_dict)

    wanFenTop5_html = ''
    for wan in new_wanFaTop5_list:
        wanFenTop5_html += '<li class="list-group-item mt-3"><h4 class="text-center" style="margin-bottom: 15px; font-size: 15px; font-weight: bold;">玩法名称:%s</h4>' % wan.get('wanFa')
        wanFenTop5_html += '<table class="table table-bordered" style="width: 80%; margin: auto;"><tbody>'
        top5 = wan.get('top5')
        wanFenTop5_html += '<tr>'
        wanFenTop5_html += '<td>号码</td>'
        for ln in top5:
            wanFenTop5_html += '<td>%s</td>' % ln[0]
        wanFenTop5_html += '</tr>'
        wanFenTop5_html += '<tr>'
        wanFenTop5_html += '<td>金额</td>'
        for ln in top5:
            wanFenTop5_html += '<td>%s</td>' % format_money(ln[1])
        wanFenTop5_html += '</tr>'
        wanFenTop5_html += '''
                        </tbody>
                    </table>
                </li>            
        '''

    duiBi1_html = ''
    duiBi1_html += '<li class="list-group-item mt-3"><h4 class="text-center" style="margin-bottom: 15px; font-size: 15px; font-weight: bold;">上一期各细化玩法数据增减百分比</h4>'
    duiBi1_html += '<table class="table table-bordered" style="width: 80%; margin: auto;"><tbody>'
    duiBi1_html += '<tr>'
    duiBi1_html += '<td>玩法</td>'
    duiBi1_html += '<td>中文名称</td>'
    duiBi1_html += '<td>下注人数</td>'
    duiBi1_html += '<td>下注金额</td>'
    duiBi1_html += '<td>下注单数</td>'
    duiBi1_html += '<td>会员输赢</td>'
    duiBi1_html += '<td>对比上期-下注人数</td>'
    duiBi1_html += '<td>对比上期-下注金额</td>'
    duiBi1_html += '<td>对比上期-下注单数</td>'
    duiBi1_html += '</tr>'
    total_renshu = 0
    total_bishu = 0
    total_jine = 0
    total_win_lose_total = 0
    for duiBi in duiBi1:
        total_renshu += int(duiBi.get('_renShu') or 0)
        total_jine += int(duiBi.get('_zongE') or 0)
        total_bishu += int(duiBi.get('danShu') or 0)
        total_win_lose_total += int(duiBi.get('win_lose_total') or 0)

        if duiBi.get('name') in PLAY_NAMES.YINCANG:
            continue

        duiBi1_html += '<tr>'
        duiBi1_html += '<td>%s</td>' % duiBi.get('name')
        duiBi1_html += '<td>%s</td>' % (WF_ZH_DICT.get((duiBi.get('name') or '').strip()) or '')

        duiBi1_html += '<td>%s</td>' % duiBi.get('_renShu')

        duiBi1_html += '<td>%s</td>' % format_money(duiBi.get('_zongE'))

        duiBi1_html += '<td>%s</td>' % duiBi.get('danShu')

        duiBi1_html += '<td>%s</td>' % format_money(duiBi.get('win_lose_total'))

        duiBi1_html += f'<td>{duiBi.get("db_renShu")}</td>'
        duiBi1_html += f'<td>{duiBi.get("db_zongE")}</td>'
        duiBi1_html += f'<td>{duiBi.get("db_danShu")}</td>'
        duiBi1_html += '</tr>'
    duiBi1_html += f'''
        <tr>
            <td>总计</td>
            <td></td>
            <td>{ format_money(len(renShu_ls)) }</td>
            <td>{ format_money(total_jine) }</td>
            <td>{ format_money(total_bishu) }</td>
            <td><a name="total_win_lose_total_bottom" href="#zongShuYing_top">{ format_money(total_win_lose_total) }</a></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
    '''

    duiBi1_html += '''
                    </tbody>
                </table>
            </li> 
    '''

    dxds_html = ''
    for play_type in ['Lô 2 Số Giải ĐB[Tổng Giá Trị]', 'Lô 2 Số Giải ĐB[Lớn Nhỏ Chẵn Lẻ]']:
        dd = ZhuDanTable.collection().aggregate([
            {"$match": {'game_name': game_name, 'play_type': play_type, 'date_number': daten}},
            {"$group": {"_id": "$play_name", "count": {"$sum": "$money"}, "win_lose": {"$sum": "$win_lose"}}}
        ])
        total_renShu_ls = ZhuDanTable.distinct('member_account', {'game_name': game_name, 'play_type': play_type, 'date_number': daten})
        total_renShu = len(total_renShu_ls)
        da, xiao, shuang, dan, win_lose = 0, 0, 0, 0, 0
        for fd in list(dd):
            if fd.get('_id') == 'Tài':
                da = fd.get('count')
            if fd.get('_id') == 'Xỉu':
                xiao = fd.get('count')
            if fd.get('_id') == 'Chẵn':
                shuang = fd.get('count')
            if fd.get('_id') == 'Lẻ':
                dan = fd.get('count')
            win_lose += fd.get('win_lose')
        if not da and not xiao and not shuang and not dan:
            continue
        dxds_html += '<li class="list-group-item mt-3"><h4 class="text-center" style="margin-bottom: 15px; font-size: 15px; font-weight: bold;">玩法分类:%s</h4>' % play_type
        dxds_html += '<table class="table table-bordered" style="width: 80%; margin: auto;"><tbody>'
        dxds_html += '<tr>'
        dxds_html += '<td>玩法名称</td>'
        dxds_html += '<td>Tài</td>'
        dxds_html += '<td>Xỉu</td>'
        dxds_html += '<td>Chẵn</td>'
        dxds_html += '<td>Lẻ</td>'
        dxds_html += '<td>会员输赢</td>'
        dxds_html += '<td>下注人数</td>'
        dxds_html += '</tr>'
        dxds_html += '<tr>'
        dxds_html += '<td>金额</td>'
        dxds_html += f'<td>{ format_money(da) }</td>'
        dxds_html += f'<td>{ format_money(xiao) }</td>'
        dxds_html += f'<td>{ format_money(shuang) }</td>'
        dxds_html += f'<td>{ format_money(dan) }</td>'
        dxds_html += f'<td>{ format_money(win_lose) }</td>'
        dxds_html += f'<td>{ format_money(total_renShu) }</td>'
        dxds_html += '</tr>'
        dxds_html += '''
                        </tbody>
                    </table>
                </li>            
        '''

    _result = {
        "biShu": biShu,
        "dxds_html": dxds_html,
        "zongE": format_money(zongE),
        "zongShuYing": format_money(zongShuYing),
        "renShu": len(renShu_ls),
        "wanFaTop5_list": new_wanFaTop5_list,
        "wanFenTop5_html": wanFenTop5_html,
        "new_wfxz_zongE": new_wfxz_zongE,
        "duiBi1_html": duiBi1_html,
        "daten": daten,
        "game_name": game_name,
    }
    return _result

def generate_html(cs_name, html_data, _crrKey):
    html = f'''
    <div class="panel">
        <h3>
            <svg style="color: #1E9FFF;" viewBox="64 64 896 896" focusable="false" data-icon="hourglass" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M742 318V184h86c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8H196c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8h86v134c0 81.5 42.4 153.2 106.4 194-64 40.8-106.4 112.5-106.4 194v134h-86c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8h632c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8h-86V706c0-81.5-42.4-153.2-106.4-194 64-40.8 106.4-112.5 106.4-194zm-72 388v134H354V706c0-42.2 16.4-81.9 46.3-111.7C430.1 564.4 469.8 548 512 548s81.9 16.4 111.7 46.3C653.6 624.1 670 663.8 670 706zm0-388c0 42.2-16.4 81.9-46.3 111.7C593.9 459.6 554.2 476 512 476s-81.9-16.4-111.7-46.3A156.63 156.63 0 01354 318V184h316v134z"></path></svg>
            【<b>{cs_name}</b>】：数据分析结果
        </h3>
        <div class="panel-body">
            <ul class="list-group">
                <li class="list-group-item">
                    <a name="zongShuYing_top"></a>
                    <span style="width: 200px; text-align: right; font-weight: bold;">下注人数：</span>
                    <span class="renShu">{ html_data.get('renShu') }</span>
                </li>
                <li class="list-group-item">
                    <span style="width: 200px; text-align: right; font-weight: bold;">下注笔数：</span>
                    <span class="biShu">{ html_data.get('biShu') }</span>
                </li>
                <li class="list-group-item">
                    <span style="width: 200px; text-align: right; font-weight: bold;">总下注额：</span>
                    <span class="zongE">{ html_data.get('zongE') }</span>
                </li>
                <li class="list-group-item">
                    <span style="width: 200px; text-align: right; font-weight: bold;">总会员输赢：</span>
                    <span class="zongE"><a href="#total_win_lose_total_bottom">{ html_data.get('zongShuYing') }</a></span>
                </li>

                <div style="width: 100%; background: #e3e3e3; height: 1px; margin: 5px 0 20px; display: block;"></div>
                <li class="list-group-item">
                    <b style="font-size: 15px; color: #1E9FFF;">玩法下注额前五：</b>
                </li>
                <div id="wanFanTop">{ html_data.get('wanFenTop5_html') }</div>

                <div style="width: 100%; background: #e3e3e3; height: 1px; margin: 5px 0 20px; display: block;"></div>
                <li class="list-group-item">
                    <b style="font-size: 15px; color: #1E9FFF;">细化玩法总下注额：</b>
                </li>
                <li class="list-group-item">
                    <div id="fenXiZXZE{_crrKey}" style="height: 300px;"></div>
                </li>

                <div style="width: 100%; background: #e3e3e3; height: 1px; margin: 5px 0 20px; display: block;"></div>
                <li class="list-group-item">
                    <b style="font-size: 15px; color: #1E9FFF;">上一期各细化玩法数据增减百分比：</b>
                </li>
                <div id="duiBiTop1">{ html_data.get('duiBi1_html') }</div>

                <div style="width: 100%; background: #e3e3e3; height: 1px; margin: 5px 0 20px; display: block;"></div>
                <li class="list-group-item">
                    <b style="font-size: 15px; color: #1E9FFF;">大、小、双、单注单数据统计：</b>
                </li>
                <div id="duiBiTop1">{ html_data.get('dxds_html') }</div>
                
            </ul>
        </div>
    </div>        
    '''
    return html

def fenxi_task_func(game_name, daten, _crrKey):
    datas = ZhuDanTable.find_many({'date_number': daten, 'game_name': game_name})
    if not datas:
        return {}
    result = data_fenxi_func(datas, daten, game_name)
    if not result:
        return {}

    res_html = generate_html(game_name, result, _crrKey)
    return {
        'res_html': res_html,
        'result_data': result,
    }



def calculationQuota(crrMoney):
    """ 计算限额 """
    if crrMoney >= 1000000000 and crrMoney < 2000000000:
        return 50000000
    if crrMoney >= 2000000000 and crrMoney < 3000000000:
        return 10000000
    if crrMoney >= 3000000000:
        return 5000000
    if crrMoney > -1000000000 and crrMoney <= -500000000:
        return 200000000
    if crrMoney > -2000000000 and crrMoney <= -1000000000:
        return 300000000
    if crrMoney < -2000000000:
        return 500000000
    return 100000000

def fcFenXiCsv_fucn(csv_data, name_dict, batch_code):
    results = []
    for row in csv_data:
        _dict_data = {
            "batch_code": batch_code
        }
        for k, v in row.items():
            for _k, _v in name_dict.items():
                if _k == k.replace('\ufeff', '').replace(' ', '').replace('=', '').replace('"', ''):
                    if _v in ['betting_money', 'profit_money', 'agent_odds', 'agent_backwater', 'vip_winlose_money', 'actual_backwater', 'actual_winlose_money']:
                        _dict_data[_v] = float(v.strip().strip('=').strip('"') or 0)
                    elif _v == 'betting_count':
                        _dict_data[_v] = int(v.strip().strip('=').strip('"') or 0)
                    else:
                        _dict_data[_v] = v.strip().strip('=').strip('"')

        account = _dict_data.get('account')
        _sk = 'import_' + account
        if SiteRedis.get(_sk):
            while True:
                _data = BettingDataTable.find_one({'account': account})
                if not _data:
                    time.sleep(0.1)
                    continue
                break
            SiteRedis.set(_sk, _sk, expire=20)
        else:
            SiteRedis.set(_sk, _sk, expire=20)
            _data = BettingDataTable.find_one({'account': account}) or {}

        if _data:
            _actual_winlose_money = _data.get('actual_winlose_money')
            actual_winlose_money = _dict_data.get('actual_winlose_money')
            _dict_data['actual_winlose_money'] = actual_winlose_money + _actual_winlose_money

            _new_quota = _data.get('new_quota')
            _low_quota = _data.get('low_quota')
            crr_quota = calculationQuota(_dict_data.get('actual_winlose_money'))
            if _new_quota != crr_quota:
                _dict_data['new_quota'] = crr_quota
                _dict_data['low_quota'] = _new_quota
                _dict_data['promotion_state'] = True
            else:
                _dict_data['promotion_state'] = False
        else:
            _dict_data['uuid'] = shortuuid.uuid()
            _dict_data['blacklistState'] = False
            _dict_data['promotion_state'] = False

            crr_quota = calculationQuota(_dict_data.get('actual_winlose_money'))
            if crr_quota != 100000000:
                _dict_data['new_quota'] = crr_quota
                _dict_data['low_quota'] = 100000000
                _dict_data['promotion_state'] = True
            else:
                _dict_data['new_quota'] = 100000000
                _dict_data['low_quota'] = 0
        results.append(_dict_data)
    return results


