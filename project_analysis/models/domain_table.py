from . import dbModel


class DomainTable(dbModel):
    __tablename__ = 'domain_table'
    uuid = dbModel.UUIDField()
    domain = dbModel.StringField('域名', is_index=True)
    account = dbModel.StringField('账户', is_index=True)
    end_time = dbModel.DateTimeField('到期时间')
    is_top = dbModel.BooleanField('置顶', default=False)
    note = dbModel.StringField('备注')
    _create_time = dbModel.DateTimeField('创建时间', nullable=False)

    @classmethod
    def field_search(cls):
        return [
            'domain',
            'account',
            'end_time'
        ]



class CardMerchantTable(dbModel):
    __tablename__ = 'CardMerchant_table'
    uuid = dbModel.UUIDField()
    cardMerchant_name = dbModel.StringField('卡商', is_index=True)
    username = dbModel.StringField('姓名', is_index=True)
    cardNo = dbModel.StringField('卡号', is_index=True)
    end_time = dbModel.DateTimeField('到期时间')
    is_top = dbModel.BooleanField('置顶', default=False)
    department = dbModel.StringField('部门')
    note = dbModel.StringField('备注')
    _create_time = dbModel.DateTimeField('创建时间', nullable=False)
    cmd_note = dbModel.StringField('后台备注')

    @classmethod
    def field_search(cls):
        return [
            'cardMerchant_name',
            'username',
            'cardNo',
            'department',
            'end_time'
        ]


