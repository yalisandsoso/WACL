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
                    self.deep_walk(walks, dir, depthLevel, rootDepth)
            return

    def deep_walk(self, path: str, depthLevel: int = 1, rootDepth: int = -1):
        walks = []
        self.__deep_walk__(walks, path, depthLevel, rootDepth)
        return walks

    def list_acl(self, path: str, depthLevel: int = 1, rootDepth: int = -1):
        """
            Query the specified ACL infos.
        """
        if not os.path.exists(path):
            return 4004, ['query path not exits, please try again', '查询路径不存在，请重新输入']
        elif int != type(depthLevel) or not str(depthLevel).isdecimal() or not 0 <= depthLevel < 6:
            return 4011, ['depth format error, please enter number 0-5', 'depthLevel格式错误，请输入数字 0-5']


    def __get_autority__(self, path: str):
        """
            Get permission info.
        :param path:
        :return: dict. ACL object
        """
        if not os.path.exists(path):
            return {4004: ['query path not exists, please try again', '查询路径不存在，请重新输入']}
        computerName = os.environ.get('computername')

        auth_id = 0
        auths_list = []






