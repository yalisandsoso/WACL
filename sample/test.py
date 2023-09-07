from core.report import AclGt

def test_save_excel_PER1():
    aclGt = AclGt()
    aclGt.getacl(path="T:\\", depthLevel=1, output=".\\output1.xlsx", mode=1)

def test_save_excel_PER2():
    aclGt = AclGt()
    aclGt.getacl(path="T:\\", depthLevel=1, output=".\\output2.xlsx", mode=2)