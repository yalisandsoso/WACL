# import sys
# from PyQt5 import QtCore, QtGui, QtWidgets
# from app.main import Ui_MainWindow
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     Ui = Ui_MainWindow()
#     Ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
import os.path

# from core.icacls import AclSupport
#
# walks = []
# paths = "D:\\共享测试"
# acls = AclSupport()
# # acls.deep_walk(walks=walks, path=paths, depthLevel=3)
# print(walks)

from core.icacls import  AclSupport
from core.xlsx import Aclmat

acl = AclSupport()
result = acl.list_acl("T:\\", 1)

xlsx = Aclmat()
xlsx.AuthsExport(result, "D:\\WACL\\t.xlsx")


# print(result)
