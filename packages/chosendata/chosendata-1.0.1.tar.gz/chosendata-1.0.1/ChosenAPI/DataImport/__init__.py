"""
本程序用于开发数据导入模块，大家需要事先安装xlrd模块和pandas模块

程序开发规范：

1、 命名规范：
按照EXCEL 的模板表格，增加文件，文件起名规范：表名按照模板里各张表的英文名称，使用驼峰命名法：
例如：
基本资料：BaseInformation.py
资产负债表：BalanceSheet
利润表：IncomeStatement
现金流量表：CashFlow
货币资金：MonetaryFunds
应收账款：AccountReceivable
......
具体不记得的可以查询网络进行翻译，


2、 程序写法和格式
参考BaseInformation的结构，使用面向对象的类开发方式：
class名称使用：Get+文件名称，驼峰命名法。__init__初始化统一pass表示
主函数统一使用get_data作为函数名，里面的形参也是固定的：data, username, identify
dic表示字典对象，ID，username，reportdate是每张表必须写的字段，且写法与样式表BaseInformation一致，其他字段名称按照实际模板的情况添加：
1)、财务报表科目名称与数据库里财务报表英文字段名称保持一致，可以查询以前发在群里的excel表格。附注里面的数据名称自己用英文命名，要求是简洁明了。
2)、cell_value里面的参数表示几行几列，但是从0开始表示第1个，所以5行5列应该是（4,4）表示E5，注释按照样例里写，写明：几行几列，格子，字段中文名称
3)、数据如果分为本期数和上期数，需要在名称后面加标志，本期数就加_this,上期数就加_last
4）、以下代码是固定格式，不要动：
        df = pd.DataFrame(dic, index=[0])  # 打包成DataFram
        return df



"""