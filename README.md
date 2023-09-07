# WACL
windows acl command
    @ https://github.com/yalisandsoso/WACL

# Test
from sample import test

test.test_save_excel_PER2()

# Use
    from core.report import AclGt
    aclGt = AclGt()
    #path 查看权限的文件夹 \ depthLevel 遍历文件夹深度 \ output 输出保存文件路径 \ mode 保存的文件格式
    aclGt.getacl(path="T:\\", depthLevel=1, output=".\\output2.xlsx", mode=2)
