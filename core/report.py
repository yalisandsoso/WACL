# -*- coding: UTF-8 -*-

from core.xlsx import Aclmat
from core.icacls import AclSupport

class AclGt:
    _aclmat = Aclmat()
    _aclsupport = AclSupport()

    def __init__(self):
        pass
    def __repr__(self):
        print("Get Win. ACL and save to excel.")

    def __help__(self):
        print("*")

    def getacl(self, path: str, depthLevel:1, output: str, mode: int = 2):
        try:
            result = self._aclsupport.list_acl(path, depthLevel)
            self._aclmat.AuthsExport(result, output, mode)
            print('Save Successfully.')
            return True
        except Exception as e:
            print("Error:" + str(e))
            exit(-1)
