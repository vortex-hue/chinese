# -*- coding: utf-8 -*-
from create_app import create_app
from project_analysis import ProjectConfig
from flask import request

app = create_app(ProjectConfig)


@app.route('/jlx')
def jlx():
    print('test:', request.args)
    return '666'


if __name__ == '__main__':
    app.run('0.0.0.0', port=80)
