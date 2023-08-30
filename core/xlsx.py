# -*- coding: UTF-8 -*-

import os
import re
import time

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, Side, borders, colors
from openpyxl.utils import get_column_letter


class Aclmat:
    """
        The format when recoding 'aclfile' to the '.xlsx' file
    """

    def __init__(self, lang='ch'):

        self.lang = lang
        return

    def get_title_map(self):
        """
            The specific contents in the advanced security settings of the folder.
        """
        _map = {}
        if self.lang == 'ch':
            _map = {
                'path': '查询路径',
                'domain': '所属组/域',
                'user': '用户名称',
                'fullAccessMask': '完整的权限掩码',
                'accessMask': '不包含继承关系的权限掩码',
                'inherit': '继承关系',
                'parentInherit': '从父对象继承',
                'propagateInherit': '传播继承',
                'inheritRight': '权限的应用场景',
                'isAllow': '是否允许的权限',
                'fullControl': '完全控制',
                'readData_listDir': '列出文件夹/读取数据',
                'readAttr': '读取属性',
                'readExtAttr': '读取扩展属性',
                'readPermiss': '读取权限',
                'execute_traverse': '遍历文件夹/执行文件',
                'writeData_addFile': '创建文件/写入数据',
                'appendData_addSubdir': '创建文件夹/附加数据',
                'writeAttr': '写入属性',
                'delete': '删除',
                'deleteChild': '删除子文件夹及文件',
                'changePermiss': '更改权限',
                'takeOwner': '取得所有权',
                'sync': '同步'
            }

        return _map

    def get_inheritRight_int_map(self):
        """
            The permissions applied.
        """
        _map = {}
        if self.lang == 'ch':
            _map = {
                0: '只有该文件夹',
                1: '只有子文件夹',
                2: '只有文件',
                3: '此文件夹和子文件夹',
                4: '此文件夹和文件',
                5: '仅子文件夹和文件',
                6: '此文件夹、子文件夹和文件'
            }

        return _map

    def get_inheritRight_mask_map(self):
        """
            The permissions applied.
        """
        _map = {}
        if self.lang == 'ch':
            _map = {
                '': '只有该文件夹',
                '(CI)(IO)': '只有子文件夹',
                '(OI)(IO)': '只有文件',
                '(CI)': '此文件夹和子文件夹',
                '(OI)': '此文件夹和文件',
                '(OI)(CI)(IO)': '仅子文件夹和文件',
                '(OI)(CI)': '此文件夹、子文件夹和文件'
            }

        return _map

    def get_progagateInherit_map(self):
        """
            The permission propagation.
        """
        _map = {}
        if self.lang == 'ch':
            _map = {
                0: '不传播继承',
                1: '传播继承'
            }

        return _map

    def get_parentInherit_map(self):
        """
             Inherit from parent node.
        """
        _map = {}
        if self.lang == 'ch':
            _map = {
                0: '不继承',
                1: '继承'
            }

        return _map

    def AuthsExport(self, acl_map: dict, output: str, *args, **kwargs):

        if not acl_map or not output:
            return False

        self.W2Xlsx(acl_map, output)

        return True

    def W2Xlsx(self, acl_map: dict, output: str, *args, **kwargs):
        """
            Write the ACL contents to the .xlsx FILE.
        """
        wb = Workbook()
        ws = wb.active

        n_rows = 0
        n_cols = 0

        # setting columns title
        # A1,A2  B1,B2
        for col_i, col_j in self.get_title_map().items():
            n_cols += 1
            ws[get_column_letter(n_cols) + str(1)] = col_i
            ws[get_column_letter(n_cols) + str(2)] = col_j
        n_rows += 2

        # TODO: CONTENTS

        wb.save(output)
        return True