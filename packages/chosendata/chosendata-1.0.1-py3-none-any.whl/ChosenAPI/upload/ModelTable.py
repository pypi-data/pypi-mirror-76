

class Table(object):
    def __init__(self):
        pass

    def table_title(self, modelname, tablename):
        # 财务模块
        if modelname == "Finance":
            if tablename == "SampleFinanceRatio":
                Title = ['指标名称', '本期值', '上期值', '行业中值', '变动比率', '与行业差异']
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 1, 2, 3
            elif tablename == "SampleFinance":
                Title = ['科目', '本期金额', '上期金额', '本期比例', '上期比例', '金额变动', '比例变动']
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 1, 2, 3
            elif tablename == "BussinessComposition":
                Title = ['名称', '报告期', '本期收入', '本期毛利率', '上期收入', '上期毛利率', '毛利率变动', '行业毛利率', '行业差异', '参老毛利率']
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 1, 2, 3
            elif tablename == "FinanceReportAssociateOfExpenses": # 财务附注费用类
                Title = ['名称', '报告期', '本期金额', '本期比例', '上期金额', '上期比例', '金额变动', '内部比例变动', "参考说明"]
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 1, 2, 3
            elif tablename == "FinanceReportAssociateOfAccountReceivable":  # 财务附注往来账户:应收账款、其他应收款
                Title = ["帐龄", "本期金额", "坏帐准备", "计提比例(%)", "上期金额", "坏帐准备", "计提比例(%)", "金额变动(%)", "坏帐变动(%)"]
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 1, 2, 3
            elif tablename == "FinanceReportAssociateOfCashEquivalents":  # 财务附注:货币资金
                Title = ["科目", "本期金额", "本期比例", "上期金额", "上期比例", "金额变动", "比例变动"]
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 1, 2, 3

            elif tablename == "FinanceReportAssociateOfInventory":  # 财务附注:存货
                Title = ["项目", "本期金额", "跌价准备", "本期比例", "上期金额", "跌价准备", "上期比例", "金额变动(%)", "比例变动(%)"]
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 1, 2, 3

            elif tablename == "FinanceReportAssociateOfFixAsset":  # 财务附注:固定资产
                Title = ["项目", "期末原值", "累计折旧", "期初原值", "累计折旧", "原值变动", "折旧率", "标准折旧率"]
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 1, 2, 3
            elif tablename == "FinanceReportAssociateOfIntangibleAssets":  # 财务附注:无形资产
                Title = ["项目", "期末原值", "累计摊销", "期初原值", "累计摊销", "原值变动", "摊销率", "标准摊销率"]
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 1, 2, 3
            elif tablename == "FinanceReportAssociateOfPA":  # 财务附注:预付账款,预收账款,其他应付款,应付账款, 短期借款,长期借款
                Title = ["项目", "本期金额", "比例(%)", "期初金额", "比例(%)", "金额变动(%)", "比例变动(%)"]
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 1, 2, 3
            elif tablename == "PolicyAndRegulation":  # 财务附注:无形资产
                Title = ['类别', '文号', "文件名称", '地区', '行业', '发布日期', '状态', '内容']
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 1, 2, 3


            else:
                return None
            return Title, nameIndex, valueIndex, unitIndex, dateIndex

        # 经营分析模块
        elif modelname == "Operation":
            if tablename == "Production":
                Title = ['类别', '产品', '指标', '来源', '单位', '日期', '数据']
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 3, 4, 5
            elif tablename == "ManageBoard":
                Title = ['代码', '报告期', '姓名', '年龄', '性别', '学历','任职时间',  '职务', '人员简历']
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 3, 4, 5
            elif tablename == "HumanResource":
                Title = ['项目', '实例', '对比1', '对比2', '对比3', '对比4','对比5']
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 3, 4, 5
            elif tablename == "HumanResourceInformation":
                Title = ['公司名称', '岗位名称', '发布时间', '信息状态', '岗位地点', '月薪上限','月薪下限','工作职责']
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 3, 4, 5
            elif tablename == "VipOperation_JobData":
                Title = ['城市', '日期', '累计在招数量', '累计就业数量', '新增在招数量', '新增就业数量', "当日指数"]
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 3, 4, 5
            elif tablename == "IndustryIndex":
                Title = ["行业", "细分行业", "指标名称", "日期", "计算周期", "指标值"]
                nameIndex, valueIndex, unitIndex, dateIndex = 0, 1, 2, 3

            else:
                return None
            return Title, nameIndex, valueIndex, unitIndex, dateIndex

        # 舆情模块
        elif modelname == "PublicOpinion":
            if tablename == "AssociateReport":
                Title = ['代码', '公司名称', '标题', '来源', '日期', '内容']
                nameIndex, valueIndex, dateIndex = 0, 5, 7
            elif tablename == "PublicOpinionScore":
                Title = ['代码', '公司名称', '日期', '新闻数', '正面数', '中性数', '负面数', '舆情分值']
                nameIndex, valueIndex, dateIndex = 0, 5, 7
            elif tablename == "HotResearch":
                Title = ["事件名称", "事件类型", "入榜时间", "出榜时间", "热搜峰值", "维持时间(小时)"]
                nameIndex, valueIndex, dateIndex = 0, 1, 2
            else:
                return None
            return Title, nameIndex, valueIndex, dateIndex
        # 研究报告模块
        elif modelname == "ResearchReport":
            if tablename == "CompanyResearch":
                Title = ['代码', '公司名称', '标题', '机构', '作者', '日期', '内容']
                nameIndex, valueIndex, dateIndex = 0, 4, 6
            elif tablename == "IndustryResearch":
                Title = ['行业', '标题', '研究机构', '作者', '日期', '内容']
                nameIndex, valueIndex, dateIndex = 0, 4, 5
            elif tablename == "MacroResearch":
                Title = ['标题', '研究机构', '作者', '日期', '内容']
                nameIndex, valueIndex, dateIndex = 0, 3, 4

            elif tablename == "ListCompanyRate":
                Title = ['代码', '公司名称', '研究机构', '研究人员', "发布日期", '最新评级', '上次评级', '调整方向', '目标价格', '研究标题']
                nameIndex, valueIndex, dateIndex = 0, 7, 4
            elif tablename == "IndustryRate":
                Title = ["行业名称", "报告标题", "日期", "评级", "评级变动", "研究机构", "内容"]
                nameIndex, valueIndex, dateIndex = 0, 3, 4

            else:
                return None
            return Title, nameIndex, valueIndex, dateIndex
        # 导入数据模块
        elif modelname == "ImportData":
            if tablename == "SampleCheck":
                Title = ['实例编码', '报告期', '行业', '风险值', '总资产', '营业收入', '分析标记', '风险评价']
                nameIndex, valueIndex, dateIndex = 0, 1, 2

            else:
                return None
            return Title, nameIndex, valueIndex, dateIndex

        else:
            return None


class ComboxList(object):  # 设置模块和表设置相关下拉菜单
    def __init__(self):
        pass

    def List(self, modelname, tablename):
        # 研究报告模块
        if modelname == "ResearchReport":
            if tablename == "IndustryResearch":
                li = {
                    "农林牧渔": ["种植业", "渔业", "林业", "饲料", "农产品加工", "农业综合", "畜禽养殖", "动物保健"],
                    "采掘": ["石油开采", "煤炭开采", "其他采掘", "采掘服务"],
                    "化工": ["石油化工", "化学原料", "化学制品", "化学纤维", "塑料", "橡胶"],
                    "钢铁": ["钢铁"],
                    "有色金属": ["金属非金属材料", "工业金属", "黄金", "稀有金属"],
                    "电子": ["半导体", "元件", "光学光电子", "其他电子", "电子制造"],
                    "汽车": ["汽车整车", "汽车零部件", "汽车服务", "其他交运设备"],
                    "家用电器": ["白色家电", "视听器材"],
                    "食品饮料": ["饮料制造", "食品加工"],
                    "纺织服饰": ["纺织制造", "服饰家纺"],
                    "轻工制造": ["造纸", "包装印刷", "家用轻工", "其他轻工制造"],
                    "医药生物": ["化学制药", "中药", "生物制品", "医药商业", "医疗器械", "医疗服务"],
                    "公用事业": ["电力", "水务", "燃气", "环保工程及服务", "", ""],
                    "交通运输": ["港口", "高速公路", "公交", "航空运输", "机场", "航运", "铁路运输", "物流"],
                    "房地产": ["房地产开发", "园区开发"],
                    "商业贸易": ["贸易", "一般零售", "专业零售", "商业物业经营"],
                    "休闲服务": ["景点", "酒店", "旅游综合", "餐饮", "其他休闲服务"],
                    "银行": ["银行"],
                    "非银金融": ["证券", "保险", "多元金融"],
                    "综合": ["综合"],
                    "建筑材料": ["水泥制造", "玻璃制造", "其他建材"],
                    "建筑装饰": ["房屋建设", "装修装饰", "基础建设", "专业工程", "园林工程"],
                    "电气设备": ["电机", "电气自动化设备", "电源设备", "高低压设备"],
                    "机械设备": ["通用机械", "专业设备", "仪器仪表", "金属制品", "运输设备"],
                    "国防军工": ["航天装备", "航空装备", "地面兵装", "船舶制造"],
                    "计算机": ["计算机设备", "计算机应用"],
                    "传媒": ["文化传媒", "营销传媒", "互联网传媒"],
                    "通信": ["通信运营", "通信设备"]
                }
            # elif
            else:
                return None
            return li

        elif modelname == "Finance":
            if tablename == "FinanceStatement":
                li = ["错报风险", "持续经营风险"]
            elif tablename == "BalanceSheetAssociate":
                li = ["货币资金", "应收账款", "存货", "固定资产", "无形资产", "短期借款", "应付帐款", "应付职工薪酬"]
            elif tablename == "IncomeStatementAssociate":
                li = ["营业收入", "营业成本", "销售费用", "管理费用", "研发费用", "财务费用", "投资收益", "其他收益"]
            elif tablename == "SampleFinance":
                li = ["全部", "资产负债表", "利润表", "现金流量表", "财务指标"]
            elif tablename == "ForecastFinanceStatement":
                li = ["资产负债表", "利润表", "现金流量表"]
            elif tablename == "ForecastFinanceRatio":
                li = ["盈利能力", "偿债能力", "运营能力"]
            else:
                return None
            return li


        else:
            return None
