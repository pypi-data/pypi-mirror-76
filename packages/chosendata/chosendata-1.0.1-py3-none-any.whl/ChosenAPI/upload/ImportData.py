
import xlrd
from ChosenAPI.SecuriyIdentify.SampleID import CreateID
from xlrd import open_workbook
from xlutils.copy import copy
from ChosenAPI.DataImport.BaseInformation import GetBaseInformation
from ChosenAPI.Settings.ImportTableSettings import ImportTable
from ChosenAPI.SecuriyIdentify.client import Client
from ChosenAPI.SecuriyIdentify.MachineCode import IdentifyCodeList
from ChosenAPI.Config.Headers import SetHeaders
from ChosenAPI.Settings.IpAndPort import DefineServerIpAndPort


# 端口通信字典：
ip_port = DefineServerIpAndPort().ip_port()



class ImportData(object):

    def __init__(self):
        pass

    def import_table(self, data, reportdate, username, identify, sheetname):
        """
        :param data:
        :param username:
        :param identify:
        :param sheetname:
        :return:
        """
        db_table = ImportTable().db_table()
        object_table = ImportTable().object_table()
        contain = object_table[sheetname]
        df = contain.get_data(data, username, identify)
        if type(df) == tuple:
            df = df[0]
        df, errorlist = contain.CheckError(df)
        df["report_date"] = reportdate
        if errorlist == []:
            data = df.to_dict(orient='records') # 转换成字典传服务器
            id = Client(ip_port["Insert"])  # 定义主机和通信端口,查询端口号
            machinecode = IdentifyCodeList().all()  # 写入机器码
            signalcode = "InsertSampleFinanceData"
            dic = {"ID": "-", "report_date": "-", "machinecode": machinecode, "username": username, "tablename": db_table[sheetname], "signalcode": signalcode, "data": data}
            checkDic = id.client_handler(dic, format='json')
            if checkDic["status"] != "success":
                errorstr = checkDic["status"]
                print("数据导入失败:", errorstr)
                success, unsuccess, error = "-", sheetname, errorstr
                self.successtable.append(success)
                self.unsuccesstable.append(unsuccess)
                self.totalerror.append(error)
            else:
                print("数据导入成功： %s" % sheetname)
                success, unsuccess, error = sheetname, "-", "-"
                self.successtable.append(success)
                self.unsuccesstable.append(unsuccess)
                self.totalerror.append(error)
        else:
            errorstr = ",".join(errorlist)
            print("数据导入失败： %s,原因：%s" % (sheetname, errorstr))
            success, unsuccess, error = "-", sheetname, errorstr
            self.successtable.append(success)
            self.unsuccesstable.append(unsuccess)
            self.totalerror.append(error)

    def import_data(self, filename):  # 实现导入数据的主要逻辑，运用xlrd模块
        self.successtable = []  # 初始化成功列表
        self.unsuccesstable = []  # 初始化不成功列表
        self.totalerror = []  # 错误列表
        rdfile = xlrd.open_workbook(filename)  # 只读方式打开
        tablenames = rdfile.sheet_names()  # 获取所有表名信息
        # 调用用户名与密码：
        username = SetHeaders().set_username()
        # 如果之前已经导入过，会留下实例ID号在文件里：如果有实例ID编码，则使用文件中的编码
        IdGrantee = rdfile.sheet_by_name("基本情况")
        Id = IdGrantee.cell_value(2, 1)  # B3 3行2列
        # 如果选中关联实例checkbox,取LineEdit的ID号：
        if Id == '-':  # 模板中保留‘-’标记,不能乱改
            ID = CreateID()
            identify = ID.creation()
        elif Id != "-":
            identify = Id
        else:
            return
        # 取出所有选中的表名(excel的sheet名称)
        count = len(tablenames)

        # 获取报告期
        contain = GetBaseInformation()
        data = rdfile.sheet_by_name("基本情况")  # 通过表明取得excel数据
        _, reportdate = contain.get_data(data, username, identify)
        if reportdate == "" or reportdate is None:
            print("提示：", "基本信息里报告期未填写,请填写")
            return

        for i in range(count):  # 循环遍历选中的表格进行导入
            sheetname = tablenames[i]
            data = rdfile.sheet_by_name(sheetname) # 通过表明取得excel数据
            """先导入基本情况表"""
            if sheetname == "基本情况":
                contain = GetBaseInformation()
                df, _ = contain.get_data(data, username, identify)
                df, errorlist = contain.CheckError(df)
                if errorlist == []:
                    self.import_table(data, reportdate, username, identify, sheetname)
                    # 回写ID号到excel文件作为标记
                    rb = open_workbook(filename, formatting_info=True)  # 保留excel文件原格式
                    wb = copy(rb)
                    s = wb.get_sheet(0)
                    s.write(2, 1, identify)  # B3 3行2列
                    wb.save(filename)
                    print("成功写入实例ID号： %s" % identify)

                else:
                    errorstr = ",".join(errorlist)
                    print("数据导入失败： %s,原因：%s" % (sheetname, errorstr))
                    return  # 如果出错，直接返回
        db_table = ImportTable().db_table()
        for i in range(count):
            sheetname = tablenames[i]
            if sheetname in db_table.keys() and sheetname != "基本情况":
                data = rdfile.sheet_by_name(sheetname)  # 通过表明取得excel数据
                self.import_table(data, reportdate, username, identify, sheetname)

        print("数据导入结束：%s", filename)




