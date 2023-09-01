import os
import re


class AclSupport:
    """
        Support the operation of obtaining ACL (win).
    """

    auths_arr = [{
        'id': int,  # 权限条目的序号
        'alias': str,  # 文件夹的别名
        'subDirs': str,  # 遍历当前文件夹的子文件夹.     -1 非文件夹 | -2 拒绝访问
        'subFiles': str,  # 遍历当前文件夹的文件.       -1 非文件夹 | -2 拒绝访问
        'domain': str,  # 所属组/域. 非组/域则为空
        'user': str,  # 用户名称
        'fullAccessMask': str,  # 完整的权限掩码, 包含继承关系.
        'accessMask': str,  # 不包含继承关系的权限掩码.
        'inherit': str,  # 继承关系.
        'isAllow': int,  # 允许或拒绝的权限. 参数: 1允许|0拒绝
        'parentInherit': int,  # 从父对象继承. 参数: 1继承|0不继承
        'propagateInherit': int,  # 递归传播权限. 参数: 1开启|0关闭
        'inheritRight': int,  # 权限的应用场景.
        'fullControl': int,  # 完全控制权限, 参数: 1开启|0关闭
        'modify': int,  # 修改权限, 参数: 1开启|0关闭  (普通权限声明)
        'read_execute': int,  # 读取和执行, 参数: 1开启|0关闭  (普通权限声明)
        'read_only': int,  # 读取权限, 参数: 1开启|0关闭  (普通权限声明)
        'write_only': int,  # 写入权限, 参数: 1开启|0关闭  (普通权限声明)
        'readData_listDir': int,  # 列出文件夹/读取数据, 参数: 1开启|0关闭  (特殊权限声明)
        'readAttr': int,  # 读取属性, 参数: 1开启|0关闭  (特殊权限声明)
        'readExtAttr': int,  # 读取扩展属性, 参数: 1开启|0关闭  (特殊权限声明)
        'readPermiss': int,  # 读取权限, 参数: 1开启|0关闭  (特殊权限声明)
        'execute_traverse': int,  # 遍历文件夹/执行文件, 参数: 1开启|0关闭  (特殊权限声明)
        'writeData_addFile': int,  # 创建文件/写入数据, 参数: 1开启|0关闭  (特殊权限声明)
        'appendData_addSubdir': int,  # 创建文件夹/附加数据, 参数: 1开启|0关闭  (特殊权限声明)
        'writeAttr': int,  # 写入属性, 参数: 1开启|0关闭  (特殊权限声明)
        'writeExtAttr': int,  # 写入扩展属性, 参数: 1开启|0关闭  (特殊权限声明)
        'delete': int,  # 删除, 参数: 1开启|0关闭  (特殊权限声明)
        'deleteChild': int,  # 删除子文件夹及文件, 参数: 1开启|0关闭  (特殊权限声明)
        'changePermiss': int,  # 更改权限, 参数: 1开启|0关闭  (特殊权限声明)
        'takeOwner': int,  # 取得所有权, 参数: 1开启|0关闭  (特殊权限声明)
        'sync': int  # 同步, 参数: 1开启|0关闭  (特殊权限声明)
    }]

    path_auths = {
        'dirs':  # 文件夹的权限ACL列表
            {
                str: auths_arr  # 文件夹的绝对路径和权限ACL
            },
        'files':  # 文件的权限ACL列表
            {
                str: auths_arr  # 文件的绝对路径和权限ACL
            }
    }

    inheritRight_map = {
        0: '',  # 只有该文件夹
        1: '(CI)(IO)',  # 只有子文件夹
        2: '(OI)(IO)',  # 只有文件
        3: '(CI)',  # 此文件夹和子文件夹
        4: '(OI)',  # 此文件夹和文件
        5: '(OI)(CI)(IO)',  # 仅子文件夹和文件
        6: '(OI)(CI)'  # 此文件夹、子文件夹和文件
    }

    def __init__(self, folder_list: list = []):
        # a list for given folder path list to do
        self.folder_list = folder_list
        return

    def __all_walk__(self, walks: list, path: str):
        """
             Deeply recursively traverse all folders.
        """
        for root, dirs, files in os.walk(path):
            if root[-1] != '\\':
                root += '\\'
            walks.append({'root': root, 'dirs': dirs, 'files': files})

        return

    def __deep_walk__(self, walks: list, path: str, depthLevel: int = 1, rootDepth: int = -1):
        """
            Deeply recursively traverse all folders according depthLevel.
        :param depthLevel:
        :param rootDepth:  The number of parent directory levels of the 'path'.
        :return:
                    if:
                       path = "D:\\共享测试"
                       depthLevel = 1
                       rootDepth = 1
                    then:
                       D:\\共享测试\\新媒体\\
                       D:\\共享测试\\编辑\\
                       D:\\共享测试\\资料\\
        """
        if not os.path.isdir(path):
            return

        if path[-1] != '\\':
            path += '\\'
        rootDepth = path.count('\\') - 1 if rootDepth == -1 else rootDepth
        for root, dirs, files in os.walk(path):
            walks.append({'root': root, 'dirs': dirs, 'files': files})
            depth = root.count('\\') if root[-1] == '\\' else root.count('\\') + 1
            if (depth - rootDepth) > depthLevel:
                return

            dirs = [os.path.join(root, cd) for cd in dirs]
            for dir in dirs:
                if os.path.isdir(dir):
                    self.__deep_walk__(walks=walks, path=dir, depthLevel=depthLevel, rootDepth=rootDepth)
            return

    def __print_auth_tree__(self, ):
        pass

    def deep_walk(self, path: str, depthLevel: int = 1, rootDepth: int = -1):
        walks = []
        self.__deep_walk__(walks=walks, path=path, depthLevel=depthLevel, rootDepth=rootDepth)
        return walks

    def list_acl(self, path: str, depthLevel: int = 1, rootDepth: int = -1):
        """
            Query the specified ACL infos.Do not list file perm.
        :param path:  D:\\测试共享
        :return: dict. ACL object
        """
        if not os.path.exists(path):
            return 4004, ['query path not exits, please try again', '查询路径不存在，请重新输入', 'list_acl']
        elif int != type(depthLevel) or not str(depthLevel).isdecimal() or not 0 <= depthLevel < 6:
            return 4011, ['depth format error, please enter number 0-5', 'depthLevel格式错误，请输入数字 0-5']

        pathAuths = dict()
        if depthLevel == 0:
            pathAuths = self.get_autority(path)
        else:
            walks = self.deep_walk(path=path, depthLevel=depthLevel)
            for item in walks:
                pathAuths.update(self.get_autority(item['root'][:-1]))

        return pathAuths

    def get_autority(self, path: str):
        """
            Get permission info.

            line: BUILTIN\Administrators:(F)
                  NT AUTHORITY\SYSTEM:(OI)(CI)(IO)(F)
                  NT AUTHORITY\SYSTEM:(OI)(CI)(DENY)(M)

        :param path:  D:\\测试共享
        :return: dict. ACL object
        """
        if not os.path.exists(path):
            return {4004: ['query path not exists, please try again', '查询路径不存在，请重新输入', 'get_autority']}
        computerName = os.environ.get('computername')

        auth_id = 0
        auths_list = []

        shell_code = 'icacls "%s"' % path

        auth_subDirs = [os.path.join(path, cd) for cd in os.listdir(path) if os.path.isdir(os.path.join(path, cd))] if os.path.isdir(path) else -1
        auth_subFiles = [os.path.join(path, cd) for cd in os.listdir(path) if os.path.isfile(os.path.join(path, cd))] if os.path.isdir(path) else -1

        with os.popen(shell_code, 'r') as auths:
            for line in auths.readlines():
                if path in line:
                    line = line.replace('\n', '').replace(path,'').strip()
                else:
                    line = line.replace('\n', '').strip()

                if '未设置任何权限。所有用户都具有完全控制权限。' in line:
                    line = 'Everyone:(F)'

                if '处理 1 个文件时失败' in line:
                    auths_list = '拒绝访问'
                elif line != '' and '已成功处理' not in line:
                    auth_alias = os.path.basename(path)
                    auth_domain = line[line[:line.rfind('\\')].rfind(' ') + 1:line.rfind('\\')] if line.rfind('\\') > 0 else ''
                    auth_user = line[line.rfind('\\') + 1:line.rfind(':')]

                    # TODO: FIND SID

                    auth_fullAccessMask = line[line.rfind(':') + 1:]
                    auth_isAllow = 0 if '(DENY)' in auth_fullAccessMask or '(N)' in auth_fullAccessMask else 1
                    auth_fullControl = 1 if '(F)' in auth_fullAccessMask or '(N)' in auth_fullAccessMask else 0

                    # 继承关系
                    # (OI)(CI)
                    auth_inherit = ""
                    if not auth_isAllow and auth_fullControl:
                        pass
                    else:
                        auth_inherit = str.join('', [
                            '%s)' % v for v in ((auth_fullAccessMask.split(')')[:-3] if '(DENY)' in auth_fullAccessMask else auth_fullAccessMask.split(')')[:-2])
                                                if len(auth_fullAccessMask.split(')')) > 2 else auth_fullAccessMask.split(')')[:-2])
                        ])

                    # 继承于
                    auth_parentInherit = 1 if '(I)' in auth_inherit else 0
                    # 仅将这些权限应用到此容器中的对象和/或容器（T)
                    auth_propagateInherit = 0 if '(NP)' in auth_inherit else 1
                    # 获取继承关系
                    auth_inheritRight = [k for k, v in self.inheritRight_map.items() if
                                         v == auth_inherit.replace('(I)', '').replace('(NP)', '')][0]

                    if auth_fullControl == 1:
                        auth_simple_modify = 1
                        auth_simple_read_execute = 1
                        auth_simple_read_only = 1
                        auth_simple_write_only = 1
                        auth_special_readData_listDir = 1
                        auth_special_readAttr = 1
                        auth_special_readExtAttr = 1
                        auth_special_readPermiss = 1
                        auth_special_execute_traverse = 1
                        auth_special_writeData_addFile = 1
                        auth_special_appendData_addSubdir = 1
                        auth_special_writeAttr = 1
                        auth_special_writeExtAttr = 1
                        auth_special_delete = 1
                        auth_special_deleteChild = 1
                        auth_special_changePermiss = 1
                        auth_special_takeOwner = 1
                        auth_special_sync = 1
                    else:
                        # 获取权限
                        auth_accessMask = auth_fullAccessMask.split(")")[-2][1:].upper().split(',')

                        # 基本权限
                        auth_simple_modify = 1 if len([v for v in auth_accessMask if 'M' == v]) == 1 else 0
                        auth_simple_read_execute = 1 if auth_simple_modify or len([v for v in auth_accessMask if 'RX' == v]) == 1 else 0
                        auth_simple_read_only = 1 if auth_simple_read_execute or len([v for v in auth_accessMask if 'R' == v]) == 1 else 0
                        auth_simple_write_only = 1 if auth_simple_modify or len([v for v in auth_accessMask if 'W' == v]) == 1 else 0

                        # 高级权限
                        auth_special_readData_listDir = 1 if auth_simple_read_only or len([v for v in auth_accessMask if 'RD' == v]) == 1 else 0
                        auth_special_readAttr = 1 if auth_simple_read_only or len([v for v in auth_accessMask if 'RA' == v]) == 1 else 0
                        auth_special_readExtAttr = 1 if auth_simple_read_only or len([v for v in auth_accessMask if 'REA' == v]) == 1 else 0
                        auth_special_readPermiss = 1 if auth_simple_read_only or len([v for v in auth_accessMask if 'RC' == v]) == 1 else 0
                        auth_special_execute_traverse = 1 if auth_simple_read_execute or len([v for v in auth_accessMask if 'X' == v]) == 1 else 0
                        auth_special_writeData_addFile = 1 if auth_simple_write_only or len([v for v in auth_accessMask if 'WD' == v]) == 1 else 0
                        auth_special_appendData_addSubdir = 1 if auth_simple_write_only or len([v for v in auth_accessMask if 'AD' == v]) == 1 else 0
                        auth_special_writeAttr = 1 if auth_simple_write_only or len([v for v in auth_accessMask if 'WA' == v]) == 1 else 0
                        auth_special_writeExtAttr = 1 if auth_simple_write_only or len([v for v in auth_accessMask if 'WEA' == v]) == 1 else 0
                        auth_special_delete = 1 if auth_simple_modify or len([v for v in auth_accessMask if 'D' == v]) == 1 else 0
                        auth_special_deleteChild = 1 if len([v for v in auth_accessMask if 'DC' == v]) == 1 else 0
                        auth_special_changePermiss = 1 if len([v for v in auth_accessMask if 'WDAC' == v]) == 1 else 0
                        auth_special_takeOwner = 1 if len([v for v in auth_accessMask if 'WO' == v]) == 1 else 0
                        auth_special_sync = 1 if len([v for v in auth_accessMask if 'S' == v]) == 1 else 0

                    auths_list.append({
                        'id': auth_id,
                        'alias': auth_alias,
                        'domain': computerName if auth_domain == 'BUILTIN' else auth_domain,
                        'user': auth_user,
                        'fullAccessMask': auth_fullAccessMask,
                        'accessMask': auth_accessMask,
                        'inherit': auth_inherit,
                        'isAllow': auth_isAllow,
                        'parentInherit': auth_parentInherit,
                        'propagateInherit': auth_propagateInherit,
                        'inheritRight': auth_inheritRight,
                        'fullControl': auth_fullControl,
                        'modify': auth_simple_modify,
                        'read_execute': auth_simple_read_execute,
                        'read_only': auth_simple_read_only,
                        'write_only': auth_simple_write_only,
                        'readData_listDir': auth_special_readData_listDir,
                        'readAttr': auth_special_readAttr,
                        'readExtAttr': auth_special_readExtAttr,
                        'readPermiss': auth_special_readPermiss,
                        'execute_traverse': auth_special_execute_traverse,
                        'writeData_addFile': auth_special_writeData_addFile,
                        'appendData_addSubdir': auth_special_appendData_addSubdir,
                        'writeAttr': auth_special_writeAttr,
                        'writeExtAttr': auth_special_writeExtAttr,
                        'delete': auth_special_delete,
                        'deleteChild': auth_special_deleteChild,
                        'changePermiss': auth_special_changePermiss,
                        'takeOwner': auth_special_takeOwner,
                        'sync': auth_special_sync
                    })
                    auth_id += 1

            auth_usersList = list(set([('{}\\{}'.format(item['domain'], item['user']) if item['domain'] != '' else item['user']) for item in auths_list if auths_list != '拒绝访问']))

        return {path: {'accessState': auths_list, 'subDirs': auth_subDirs, 'subFiles': auth_subFiles,'count_result': [auth_usersList]}}








