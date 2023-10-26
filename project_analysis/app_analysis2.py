# -*- coding: utf-8 -*-
from create_app import create_app
from project_analysis2 import ProjectConfig


app = create_app(ProjectConfig)

if __name__ == '__main__':
    app.run('0.0.0.0', port=80)
