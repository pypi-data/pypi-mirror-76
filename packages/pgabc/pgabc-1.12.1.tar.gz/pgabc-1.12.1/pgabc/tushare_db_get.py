"""
1.stock_daily(ts_code:str=ts_code, start_date='', end_date=''):
    #获取各大交易所交易日历数据,默认提取的是上交所
2.trade_cal(start_date='', end_date='')
    #获取各大交易所交易日历数据,默认提取的是上交所
3.namechange(ts_code:str=ts_code)
    #  历史名称变更记录
4.hs_const(hs_type='')
    #获取沪股通、深股通成分数据,hs_type类型SH沪股通SZ深股通
5.stock_company(exchange='')
    获取上市公司基础信息exchange交易所代码 ，SSE上交所 SZSE深交所 ，默认SSE
6.new_share(self,start_date:str=start_date,end_date:str=end_date)
    获取新股上市列表数据
7.stock_basic(ts_code:str=ts_code, start_date='', end_date='')
    #获取基础信息数据，包括股票代码、名称、上市日期、退市日期等
8.stock_weekly(ts_code:str=ts_code, start_date='', end_date=''):
    获取A股周线行情
9.stock_monthly(ts_code:str=ts_code, start_date='', end_date='')
    获取A股月线行情
10.bar(ts_code:str=ts_code,freq='',adj='', start_date='', end_date='')
    #复权行情通过通用行情接口实现，利用Tushare Pro提供的复权因子进行计算，目前暂时只在SDK中提
    #freq = 'D','W','M' 日、周、月  adj ='qfq','hfq'前复权，后复权
11.suspend(ts_code:str=ts_code)
    获取股票每日停复牌信息suspend_date停牌日期(三选一)resume_date复牌日期(三选一)
12.daily_basic(self,trade_date:str=trade_date):
    #获取全部股票每日重要的基本面指标，可用于选股分析、报表展示等
13.moneyflow(ts_code:str=ts_code,start_date='',end_date=''):
    #获取沪深A股票资金流向数据，分析大单小单成交情况，用于判别资金动向
14.stk_limit(self,trade_date:str=trade_date):
    获取全市场（包含A/B股和基金）每日涨跌停价格，包括涨停价格，跌停价格等
15.hk_hold(self,trade_date:str=trade_date):
    获取沪深港股通持股明细，数据来源港交所
16.income(ts_code:str=ts_code,start_date='',end_date=''):
    #获取上市公司财务利润表数据
17.balancesheet(ts_code:str=ts_code,start_date='',end_date=''):
    #获取上市公司资产负债表
18.cashflow(ts_code:str=ts_code,start_date='',end_date=''):
    #获取上市公司现金流量表
19.forecast(self,ann_date:str=ann_date):
    获取业绩预告数据
20.express(ts_code:str=ts_code,start_date='',end_date=''):
    获取上市公司业绩快报
21.dividend(ts_code:str=ts_code):
    分红送股数据
22.fina_indicator(ts_code:str=ts_code, start_date:str=start_date,end_date:str=end_date):
    获取上市公司财务指标数据，为避免服务器压力，现阶段每次请求最多返回60条记录，可通过设置日期多次请求获取更多数据
23.fina_audit(ts_code:str=ts_code, start_date:str=start_date,end_date:str=end_date):
    获取上市公司定期财务审计意见数据
24.disclosure_date(self,end_date:str=end_date):
    获取财报披露计划日期
25.moneyflow_hsgt(self,start_date:str=start_date,end_date:str=end_date):
    获取沪股通、深股通、港股通每日资金流向数据，每次最多返回300条记录，总量不限制
26.hsgt_top10(trade_date='',market_type=''):
    获取沪股通、深股通每日前十大成交详细数据市场类型（1：沪市 3：深市）
27.ggt_top10(self,trade_date:str=trade_date):
    获取港股通每日成交数据，其中包括沪市、深市详细数据市场类型 2：港股通（沪） 4：港股通（深）
28.margin(self,trade_date:str=trade_date):
    获取融资融券每日交易汇总数据
29. margin_detail(self,trade_date:str=trade_date)
    获取沪深两市每日融资融券明细
30.top10_holders(ts_code:str=ts_code,start_date='',end_date='')
    获取上市公司前十大股东数据，包括持有数量和比例等信息。
31.top10_floatholders(ts_code:str=ts_code,start_date='',end_date='')
    获取上市公司前十大流通股东数据。
32.top_list(self,trade_date:str=trade_date)
    龙虎榜每日交易明细
33.top_inst(self,trade_date:str=trade_date)
    龙虎榜机构成交明细
34. pledge_start(ts_code:str=ts_code)
    获取股权质押统计数据
35.pledge_detail(ts_code:str=ts_code):
    获取股权质押明细数据
36.repurchase(self,start_date:str=start_date,end_date:str=end_date):
    获取上市公司回购股票数据
37.concept(self):
    获取概念股分类，目前只有ts一个来源，未来将逐步增加来源
38.concept_detail(id=''):
    获取概念股分类明细数据
39.share_float(self,ann_date:str=ann_date):
    获取限售股解禁
40.block_trade(self,trade_date:str=trade_date):
    大宗交易
41.stk_account(self,start_date:str=start_date,end_date:str=end_date)
    获取股票账户开户数据，统计周期为一周
42.stk_account_old(self,start_date:str=start_date,end_date:str=end_date)
    获取股票账户开户数据，统计周期为一周(old)
43.stk_holdernumber(ts_code:str=ts_code,start_date='',end_date=''):
    获取上市公司股东户数数据，数据不定期公布
44.stk_holdertrade(self,ann_date:str=ann_date):
    #：获取上市公司增减持数据，了解重要股东近期及历史上的股份增减变化
45.index_basic(market='',start_date='',end_date=''):
    获取指数基础信息
46. index_daily(ts_code:str=ts_code,start_date='',end_date=''):
    #：获取指数每日行情，还可以通过bar接口获取
47.index_weekly(trade_date='',start_date='',end_date=''):
    #：获取指数周线行情
48.index_monthly(trade_date='',start_date='',end_date=''):
    #：获取指数月线行情,每月更新一次
49.index_weight(index_code='',start_date='',end_date=''):
    #：获取各类指数成分和权重，月度数据 ，如需日度指数成分和权重，请联系 waditu@163.com
50.index_dailybasic(self,trade_date:str=trade_date):
    #：目前只提供上证综指，深证成指，上证50，中证500，中小板指，创业板指的每日指标数据
51.index_classify(level=''):
    #：获取申万行业分类，包括申万28个一级分类，104个二级分类，227个三级分类的列表信息
52.index_member(level=''):
    #：申万行业成分
53.fund_basic(market=''):
    #：获取公募基金数据列表，包括场内和场外基金 场内O场外
54.fund_company(self):
    #：获取公募基金管理人列表
55. fund_nav(ts_code:str=ts_code):
    #：获取公募基金净值数据
56. fund_div(self,ann_date:str=ann_date):
    #：获取公募基金分红数据
57.fund_portfolio(ts_code:str=ts_code):
    #：获取公募基金持仓数据，季度更新
58.fut_basic(exchange=''):
    #：获取期货合约列表数据交易所代码 CFFEX-中金所 DCE-大商所 CZCE-郑商所 SHFE-上期所 INE-上海国际能源交易中心
59.trade_cal(exchange='',start_date='',end_date=''):
    #：获取各大期货交易所交易日历数据
60.fut_daily(exchange='',trade_date=''):
    #：期货日线行情数据
61.fut_holding(exchange='',trade_date=''):
    #：获取每日成交持仓排名数据
62.fut_wsr(exchange='',symbol=''):
    #：获取仓单日报数据，了解各仓库/厂库的仓单变化
63.fut_settle(exchange='',trade_date=''):
    #：获取每日结算参数数据，包括交易和交割费率等
64.opt_basic(exchange=''):
    # ：获取期权合约信息
65.opt_daily(self,trade_date:str=trade_date):
    # ：获取期权日线行情
66.cb_basic(self):
    # ：获取可转债基本信息
67.cb_issue(self,ann_date:str=ann_date):
    # ：获取可转债发行数据
68. cb_daily(self,trade_date:str=trade_date):
    # ：获取可转债行情
69.fx_obasic(exchange='',classify=''):
    # 获取海外外汇基础信息，目前只有FXCM交易商的数据
70.fx_daily(ts_code:str=ts_code,start_date='',end_date=''):
    # 获取外汇日线行情
71.shibor(self,start_date:str=start_date,end_date:str=end_date):
    # shibor利率
72.shibor_quote(self,start_date:str=start_date,end_date:str=end_date):
    # ：Shibor报价数据
73.shibor_lpr(self,start_date:str=start_date,end_date:str=end_date):
    # LPR贷款基础利率
74.libor(curr_type='',start_date='',end_date=''):
    # Libor拆借利率 货币代码 (USD美元 EUR欧元 JPY日元 GBP英镑 CHF瑞郎，默认是USD)
75.hibor(self,start_date:str=start_date,end_date:str=end_date):
    #Hibor利率
76.wz_index(self,start_date:str=start_date,end_date:str=end_date):
    #温州民间借贷利率，即温州指数
77.def gz_index(self,start_date:str=start_date,end_date:str=end_date):
    #广州民间借贷利率
78.news(self,start_date:str=start_date,end_date:str=end_date):
    #获取主流新闻网站的快讯新闻数据
79.cctv_news(date=''):
    #获取新闻联播文字稿数据，数据开始于2006年6月，超过12年历史
80. anns(ts_code:str=ts_code,start_date='',end_date='',year=''):
    #获取上市公司公告数据及原文文本，数据从2000年开始，内容很大，请注意数据调取节奏。
81.coinlist(start_date='',end_date='',year=''):
    #获取全球数字货币基本信息，包括发行日期、规模、所基于的公链和算法等。
82.coinpair(exchange='',trade_date=''):
    #获取全球数字货币基本信息，包括发行日期、规模、所基于的公链和算法等。
83.coinexchanges(area_code=''):
    #：获取全球数字货币交易所基本信息。
84.coinbar(exchange='',symbol='',frep='',start_date='',end_date=''):
    #获取数字货币行情数据，目前支持币币交易和期货合约交易。如果是币币交易，exchange参数请输入huobi,okex,binance,bitfinex等。
85.coincap(self,trade_date:str=trade_date):
    #获取数字货币每日市值数据，该接口每隔6小时采集一次数据，所以当日每个品种可能有多条数据，用户可根据实际情况过滤截取使用。
86.coinfree(exchange=''):
    #获取交易所当前和历史交易费率，目前支持的有huobi、okex、binance和bitfinex。
87. marketcap(self,start_date:str=start_date,end_date:str=end_date):
    #获取比特币历史以来每日市值数据
88.btc_pricevol(self,start_date:str=start_date,end_date:str=end_date):
    #获取比特币历史每日的价格和成交量数据。
89. ubindex_constituents(index_name='',start_date='',end_date=''):
    #获取优币指数成分所对应的流通市值、权重以及指数调仓日价格等数据。
90.btc8(self,start_date:str=start_date,end_date:str=end_date):
    #：获取巴比特即时和历史资讯数据（5分钟更新一次，未来根据服务器压力再做调整）
91.bishijie(self,start_date:str=start_date,end_date:str=end_date):
    #：获取币世界即时和历史资讯数据（5分钟更新一次，未来根据服务器压力再做调整）
92. exchange_ann(self,start_date:str=start_date,end_date:str=end_date):
    #：获取各个交易所公告的即时和历史资讯数据（5分钟更新一次，未来根据服务器压力再做调整）
93.def exchange_twitter(self,start_date:str=start_date,end_date:str=end_date):
    #：获取Twitter上数字货币交易所发布的消息（5分钟更新一次，未来根据服务器压力再做调整）
94.twitter_kol(self,start_date:str=start_date,end_date:str=end_date):
    #：获取Twitter上数字货币领域大V的消息（5分钟更新一次，未来根据服务器压力再做调整）
95.tmt_twincome(self,start_date:str=start_date,end_date:str=end_date):
    #：获取台湾TMT电子产业领域各类产品月度营收数据。
96. tmt_twincomedetail(self):
    #：获取台湾TMT行业上市公司各类产品月度营收情况。
97.bo_mothly(date=''):
    #：获取电影月度票房数据
98.bo_weekly(date=''):
    #：获取周度票房数据
99.bo_daily(date=''):
    #：获取电影日度票房
100.bo_cinema(date=''):
    #：获取每日各影院的票房数据
101. film_record(self,start_date:str=start_date,end_date:str=end_date):
    #获取全国电影剧本备案的公示数据
102.teleplay_record(self,start_date:str=start_date,end_date:str=end_date):
    #获取2009年以来全国拍摄制作电视剧备案公示数据
103.def deposit_rate(self):
    #获取获取存款利率
104. loan_rate(self):
    #获取贷款利率
105.rrr(self):
    #获取存款准备金利率
106.money_supply(self):
    #获取货币供应量
107.money_supply_ball(self):
    #获取货币供应量年底余额
108.gdp_year(self):
    #获取国民生产总值
109.gdp_quarter(self):
    #获取国内生产总值(季度）
110.gdp_for(self):
    #获取三大需求对GDP贡献
111.gdp_pull(self):
    # 获取三产业对GDP拉动
112.gdp_contrib(self):
    #获取三产业对GDP贡献率
113.cpi(self):
    #获取居民消费指数 CPI
114.ppi(self):
    #获取工业品出厂价格指数 PPI
115.today_all(self):
    #一次性获取当前交易所有股票的行情数据（如果是节假日，即为上一交易日，结果显示速度取决于网速）
116.today_all(ts_code:str=ts_code,date=''):
    #获取个股以往交易历史的分笔数据明细，
117.realtime_quotes(ts_code:str=ts_code):
    #获取实时分笔数据，可以实时取得股票当前报价和成交信息
118.today_ticks(ts_code:str=ts_code):
    #获取当前交易日（交易进行中使用）已经产生的分笔明细数据
119.industry_classified(self):
    #获取行业分类
120.concept_classified(self):
    #获取概念分类
121.area_classified(self):
    #获取地域分类
122.sme_classified(self):
    #获取中小板分类
123.gem_classified(self):
    #获取创业板分类
124.hs300s(self):
    # 获取沪深300成分及权重
125.sz50(self):
    # 获取上证50成分
126.zz500(self):
    #获取中证500
127.report_data(year,querter):
    #获取业绩报告主表
128.profit_data(year,querter):
    #获取盈利能力
129.operation_data(year,querter):
    #获取运营能力
130.growth_data(year,querter):
    #获取成长能力
131.debtpaving_data(year,querter):
    #获取偿债能力
132.cashflow_data(year,querter):
    #获取现金流量数据
133.latest_news(top=''):
    #获取最新消息条数
134.notices(top=''):
    #获取信息地雷
135.guba_sina(top=''):
    #获取新浪股吧数据前17条
136.guba_sina(self):
    #获取新浪股吧数据前17条
137.hk_basic(self):
    #获取港股数据
138.hk_daily(ts_code:str=ts_code,start_dt='',end_dt=''):
    #获取港股每日增量和历史行情
139.fut_mapping(ts_code:str=ts_code,start_dt='',end_dt=''):
    #获取期货主力（或连续）合约与月合约映射数据
140.major_news(start_dt='',end_dt=''):
    #获取长篇通讯信息，覆盖主要新闻资讯网站
141.stk_rewards(end_date='',ts_code:str=ts_code)
    #获取上市公司管理层薪酬和持股
142.anns(end_date='',ts_code:str=ts_code):
    #上市公司公告(信息地雷)
143.news(end_date='',src='',ts_code:str=ts_code):
    #新闻快讯
144.cctv_news(self,end_date:str=end_date):
    #接口：cctv_news   144.
145.stock_basic(self):
    #获取基础信息数据，包括股票代码、名称、上市日期、退市日期等  145.
146.stk_managers(ts_code=code_list):
    #接口：stk_managers    #描述：获取上市公司管理层   146

147.stk_rewards(ts_code:str=ts_code,end_date=''):
    # db_ts_0007_stk_rewards     # 管理层薪酬和持股     # 接口：stk_rewards
    # 描述：获取上市公司管理层薪酬和持股   147

148.adj_factor(ts_code:str=ts_code,trade_date=''):
    #接口：adj_factor
    #更新时间：早上9点30分
    #描述：获取股票复权因子，可提取单只股票全部历史复权因子，也可以提取单日全部股票的复权因子。 148
149.fina_mainbz(ts_code:str=ts_code,period='',type=''):
    # 试3次下载数据，如不成功，每次暂停2钞    149
    #：获得上市公司主营业务构成，分地区和产品,两种方式类型：P按产品 D按地区
150. fund_daily(ts_code:str=ts_code,start_date='',end_date=''):
    #：获取场内基金日线行情，类似股票日行情   150
    # 试3次下载数据，如不成功，每次暂停2钞市场代码
151.index_daily(ts_code:str=ts_code,start_date='',end_date=''):
    #     #：获取南华指数每日行情，指数行情也可以通过通用行情接口获取数据．
    #     # 试3次下载数据，如不成功，每次暂停2钞          151
    for g in range(self.retry_count):
152.jinse(self,start_date:str=start_date,end_date:str=end_date):
    #：获取金色采集即时和历史资讯数据（5分钟更新一次）  152
    # 试3次下载数据，如不成功，每次暂停2钞

153.limit_list(start_date='', end_date=''):
    #接口：limit_list    153
    #描述：获取每日涨跌停股票统计，包括封闭时间和打开次数等数据，帮助用户快速定位近期强（弱）势股，以及研究超短线策略。
154.ggt_daily(self,trade_date:str=trade_date):
    #接口：ggt_daily                    154
    #描述：获取港股通每日成交信息，数据从2014年开始

155. ggt_monthly(self,trade_date:str=trade_date):
    #接口：ggt_daily                   155
    #描述：获取港股通每日成交信息，数据从2014年开始

156.fund_adj(ts_code:str=ts_code,start_date='', end_date=''):
    #接口：fund_adj     156    ok
    #描述：获取基金复权因子，用于计算基金复权行情
157. fut_mapping(ts_code:str=ts_code):
    #接口：fut_mapping    157   ok
    #描述：获取期货主力（或连续）合约与月合约映射数据

158.yc_cb(self,trade_date:str=trade_date):
    #接口：yc_cb
    #描述：获取中债收益率曲线，目前可获取中债国债收益率曲线即期和到期收益率曲线数据   158  ok


159. fund_share(ts_code:str=ts_code):
    #接口：fund_share
    #描述：获取基金规模数据，包含上海和深圳ETF基金   159  ok
    
160.fund_manager(ts_code:str=ts_code):
    #接口：fund_manager
    #描述：获取公募基金经理数据，包括基金经理简历等数据  160  ok

161.cn_gdp(start_q,end_q):
    #接口：cn_gdp
    #描述：获取国民经济之GDP数据      No. 161

162.cn_cpi(start_m,end_m):
    #接口：cn_cpi
    #描述：获取CPI居民消费价格数据，包括全国、城市和农村的数据   NO.162

163.def eco_cal(item_dt,country_wm):
    #接口：eco_cal
    #描述：获取全球财经日历、包括经济事件数据更新  NO.163


164.def bak_daily(self,ts_code:str=ts_code,start_date:str=start_date,end_date:str=end_date):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #接口：bak_daily
        #描述：获取备用行情，包括特定的行情指标


165. def index_global(self,index_global:str=index_global,start_date:str=start_date,end_date:str=end_date):    
        #接口：bak_daily     #165
        #描述：获取备用行情，包括

 
166. def ft_tick(self,ft_symbol:str=ft_symbol,start_date:str=start_date,end_date:str=end_date):    
        #接口：ft_tick       #166     #需要公司交易账号
        #描述：获取期权和期货的tick数据   


167.    def eco_cal_a(self,trade_date:str=trade_date):     #not use !!!!!!!!!!!!!!!!!!!!!!         
        #接口：eco_cal     #167     
        #描述：获取全球财经日历、包括经济事件数据更新




169.   def us_basic(self):                                  
        #接口：us_basic    #169
        #描述：获取美股列表信息

170.   def us_tradecal(self,start_date:str=start_date,end_date:str=end_date):                                  
        #接口：us_tradecal    #170
        #描述：获取美股交易日历信息
        import time


171.    def us_daily(self,us_code:str=us_code,start_date:str=start_date,end_date:str=end_date):                                  
        #接口：us_daily   #171
        #描述：获取美股行情，包括全部股票全历史行情，以及重要的市场和估值指标



172.    def us_daily_a(self,trade_date:str=trade_date):                                  
        #接口：us_daily   #172
        #描述：获取美股行情，包括全部股票全历史行情，以及重要的市场和估值指标



173.   def cn_ppi(self,start_date:str=start_date,end_date:str=end_date):                                  
        #接口：cn_ppi   #173
        #描述：获取PPI工业生产者出厂价格指数数据


174.    def cn_m(self,start_date:str=start_date,end_date:str=end_date):                                  
        #接口：cn_m    #174
        #描述：获取货币供应量之月度数据


175.   def us_tycr(self,start_date:str=start_date,end_date:str=end_date):                                  
        #接口：us_tycr    #175
        #描述：获取美国每日国债收益率曲线利率



176.    def us_trycr(self,start_date:str=start_date,end_date:str=end_date):                                  
        #接口：us_trycr    #176
        #描述：国债实际收益率曲线利率


177.   def us_tbr(self,start_date:str=start_date,end_date:str=end_date):                                   
        #接口：us_tbr  #177
        #描述：获取美国短期国债利率数据



178.   def us_tbr_a(self,start_date:str=start_date,end_date:str=end_date):                                  
        #接口：us_tbr  #178
        #描述：获取美国短期国债利率数据


179. def us_tltr(self,start_date:str=start_date,end_date:str=end_date):                                   
        #接口：us_tltr    #179
        #描述：国债长期利率



180.   def us_trltr(self,start_date:str=start_date,end_date:str=end_date):                                    
        #接口：us_trltr    #180
        #描述：国债实际长期利率平均值



"""
import time
import datetime
class TushareDbGet():
    """
    通过https://tushare.pro 获得各种经济数据，需要登录官网注册，取得接中TOKEN，
    import tushare as ts
    ts.set_token('your token')
    pro = ts.pro_api()
    """
    import tushare as ts
    retry_count = 3   #在系统、网络连接错误时重试次数
    pause = 2         #重新连接间暂停时间
    ts_code = '000001.SZ'
    time_temp = datetime.datetime.now() - datetime.timedelta(days=365)
    start_date = time_temp.strftime('%Y%m%d')                                   #开始日期设为当前日期前365日期
    time_temp = datetime.datetime.now() - datetime.timedelta(days=0)
    end_date = time_temp.strftime('%Y%m%d')                                     #终止日期设为当前日期前365日期
    exchange_stock = 'SSE'                                                      #exchange交易所 SSE上交所 SZSE深交所
    hs_type = 'SH'                                                              #沪股通、深股通成分数据,hs_type类型SH沪股通SZ深股通
    freq = 'D'                                                                  #'D','W','M' 日、周、月  
    adj =  'qfq'                                                                #'qfq','hfq'前复权，后复权
    asset ='E'                                                                  #资产类别：E股票 I沪深指数 C数字货币 F期货 FD基金 O期权，默认E
    suspend_date = end_date                                                     #停牌日期(三选一)
    resume_date = end_date                                                      #复牌日期(三选一)    
    trade_date = end_date                                                       #交易日期
    ann_date = end_date                                                         #公告日期
    period = '20200331'                                                         #str	N	报告期(每个季度最后一天的日期,比如20171231表示年报)
    type = 'P'                                                                  #STR	N	类型：P按产品 D按地区（请输入大写字母P或者D）
    market_type = 1                                                             #获取沪股通、深股通每日前十大成交详细数据市场类型（1：沪市 3：深市）
    market_index = 'SSE'                                                        #MSCI	MSCI指数 # CSI	中证指数 SSE上交所指数 SZSE	深交所指数 CICC	中金所指数 SW	申万指数  OTH	其他指数
    index_code='399300.SZ'  
    level = 'L3'                                                                #申万行业分类，包括申万28个一级分类，104个二级分类，227个三级分类（L1/L2/L3）
    market_fund = 'E'                                                           #	str	N	交易市场: E场内 O场外（默认E）
    status_fund = 'N'                                                           #	str	N	存续状态 D摘牌 I发行 L上市中
    fund_code='165509.SZ'
    exchange_fut= 'SHFE'                                                        #交易所代码 CFFEX-中金所 DCE-大商所 CZCE-郑商所 SHFE-上期所 INE-上海国际能源交易中心
    symbol_fut = 'ZN'                                                           #期货代码
    exchange_opt= 'DCE'                                                        #交易所代码 CFFEX-中金所 DCE-大商所 CZCE-郑商所 SHFE-上期所 INE-上海国际能源交易中心
    exchange_fx = 'FXCM'                                                       # 获取海外外汇基础信息，目前只有FXCM交易商的数据         69  ok 
    classify_fx = 'FX'
    """
        classify分类说明
        序号    分类代码    分类名称    样例
        1    FX    外汇货币对    USDCNH（美元人民币对）
        2    INDEX    指数    US30（美国道琼斯工业平均指数）
        3    COMMODITY    大宗商品    SOYF（大豆）
        4    METAL    金属    XAUUSD （黄金）
        5    BUND    国库债券   Bund（长期欧元债券）
        6    CRYPTO    加密数字货币    BTCUSD(比特币)
        7    FX_BASKET    外汇篮子    USDOLLAR （美元指数）
    """
    code_fx = 'USDCNH.FXCM'                                                 #外汇代码
    curr_type='USD'                                                         # Libor拆借利率 货币代码 (USD美元 EUR欧元 JPY日元 GBP英镑 CHF瑞郎，默认是USD)   74   ok
    exchange_coin = 'huobi'
    area_code  = 'us'
    symbol_coin = 'btcusdt'  
    freq_coin = 'weekly'      # perpetual / biquarterly / quarterly / monthly / weekly
    index_name = 'UBI7'     #UBI7    平台类TOP7项目指数   #UBI0    平台类TOP10项目指数   #UBI20    平台类TOP20项目指数   #UBC7    币类TOP7项目指数    #UB7    市场整体类TOP7项目指数        #UB20    市场整体类TOP20项目指数
    fut_code = 'I'
    src = 'sina'                                           #               ['sina','wallstreetcn','10jqka','eastmoney','yuncaijing']
    country_wm = '美国'
    index_global =  'DJI' 
        #接口：index_global
        #描述：获取国际主要指数日线行情
        #TS指数代码	指数名称
        #XIN9	富时中国A50指数 (富时A50)
        #HSI	恒生指数
        #DJI	道琼斯工业指数
        #SPX	标普500指数
        #IXIC	纳斯达克指数
        #FTSE	富时100指数
        #FCHI	法国CAC40指数
        #GDAXI	德国DAX指数
        #N225	日经225指数
        #KS11	韩国综合指数
        #AS51	澳大利亚标普200指数
        #SENSEX	印度孟买SENSEX指数
        #IBOVESPA	巴西IBOVESPA指数
        #RTS	俄罗斯RTS指数
        #TWII	台湾加权指数
        #CKLSE	马来西亚指数
        #SPTSX	加拿大S&P/TSX指数
        #CSX5P	STOXX欧洲50指数
    ft_symbol = 'DCE'
    us_code = 'AAPL'



    def __init__(self,pro):
        self.pro = pro


    def stock_basic(self):
        #获取基础信息数据，包括股票代码、名称、上市日期、退市日期等   ok     145/7
        #上市状态： L上市 D退市 P暂停上市
        for g in range(self.retry_count):
            try:
                df = self.pro.stock_basic(exchange='', list_status='L',fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
            except:
                time.sleep(self.pause)
            else:
                #print(df)
                return df

    
    def trade_cal(self,start_date:str = start_date,end_date:str = end_date):
        #获取各大交易所交易日历数据,默认提取的是上交所  ok   2
        #exchange交易所 SSE上交所 SZSE深交所
        for g in range(self.retry_count):
            try:
                df = self.pro.trade_cal(exchange=self.exchange_stock, start_date=start_date, end_date=end_date,
                                fields='exchange,cal_date,is_open,pretrade_date')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    
    def namechange(self,ts_code:str=ts_code,start_date:str=start_date,end_date:str=end_date):
        #历史名称变更记录   ok     3
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.namechange(ts_code=ts_code, start_date=start_date, end_date=end_date, fields='ts_code,name,start_date,end_date,ann_date,change_reason')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df
    
    def hs_const(self,hs_type:str=hs_type):
        #获取沪股通、深股通成分数据,hs_type类型SH沪股通SZ深股通  ok    4
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.hs_const(hs_type=hs_type)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df
    
    def stock_company(self,exchange_stock:str=exchange_stock):
        #获取上市公司基础信息exchange交易所代码 ，SSE上交所 SZSE深交所 ，默认SSE  ok  5
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.stock_company(exchange=exchange_stock, list_status='L', fields='ts_code,exchange,chairman,manager,secretary,reg_capital,setup_date,province,city,introduction,website,email,office,employees,main_business,business_scope')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def new_share(self,start_date:str=start_date,end_date:str=end_date):
        #获取新股上市列表数据
        # 试3次下载数据，如不成功，每次暂停2钞  ok   6
        for g in range(self.retry_count):
            try:
                df = self.pro.new_share(start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def stock_daily(self,ts_code:str=ts_code, start_date:str=start_date, end_date:str=end_date):
        # 试3次下载数据，如不成功，每次暂停2钞  ok  1
        #交易日每天15点～16点之间
        for g in range(self.retry_count):
            try:
                df = self.pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date, fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def stock_weekly(self,ts_code:str=ts_code, start_date:str=start_date, end_date:str=end_date):
        # 试3次下载数据，如不成功，每次暂停2钞  ok    8
        #获取A股周线行情
        for g in range(self.retry_count):
            try:
                df = self.pro.weekly(ts_code=ts_code, start_date=start_date, end_date=end_date,fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def stock_monthly(self,ts_code:str=ts_code, start_date:str=start_date, end_date:str=end_date):
        # 试3次下载数据，如不成功，每次暂停2钞  ok   9
        #获取A股月线行情
        for g in range(self.retry_count):
            try:
                df = self.pro.monthly(ts_code=ts_code, start_date=start_date, end_date=end_date,
                            fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def bar(self,ts_code:str=ts_code,freq:str=freq,adj:str=adj, start_date:str=start_date, end_date:str=end_date):
        # 试3次下载数据，如不成功，每次暂停2钞  ok   10
        #复权行情通过通用行情接口实现，利用Tushare Pro提供的复权因子进行计算，目前暂时只在SDK中提
        #freq = 'D','W','M' 日、周、月  adj ='qfq','hfq'前复权，后复权
        for g in range(self.retry_count):
            try:
                df = self.ts.pro_bar(ts_code=ts_code, freq=freq,adj=adj, start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def pro_bar(self,ts_code:str=ts_code,freq:str=freq,adj:str=adj, start_date:str=start_date, end_date:str=end_date, asset:str=asset):
        # 试3次下载数据，如不成功，每次暂停2钞  ok
        #复权行情通过通用行情接口实现，利用Tushare Pro提供的复权因子进行计算，目前暂时只在SDK中提
        #freq = 'D','W','M','1MIN','5MIN','15MIN','30MIN','60MIN',日、周、月
        # adj ='qfq','hfq','None'前复权，后复权
        #asset =''资产类别：E股票 I沪深指数 C数字货币 F期货 FD基金 O期权，默认E
        #ma = 均线，支持任意周期的均价和均量，输入任意合理int数值
        for g in range(self.retry_count):
            try:
                df = self.ts.pro_bar(ts_code=ts_code, freq=freq,adj=adj, start_date=start_date, end_date=end_date,asset=asset)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def adj_factor(self,ts_code:str=ts_code,trade_date:str=trade_date):
        # 试3次下载数据，如不成功，每次暂停2钞  ok   148
        #获取股票复权因子，可提取单只股票全部历史复权因子，也可以提取单日全部股票的复权因子。
        for g in range(self.retry_count):
            try:
                #df = self.pro.adj_factor(ts_code='000001.SZ', trade_date='')
                #df = self.pro.adj_factor(ts_code:str=ts_code, trade_date='20180718')
                df = self.pro.adj_factor(ts_code=ts_code, trade_date=trade_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def suspend(self,suspend_date:str=suspend_date):
        # 试3次下载数据，如不成功，每次暂停2钞  ok   11
        #获取股票每日停复牌信息suspend_date停牌日期(三选一)resume_date复牌日期(三选一)
        for g in range(self.retry_count):
            try:
                df = self.pro.query('suspend', ts_code=ts_code, suspend_date=suspend_date, resume_date='', fields='ts_code,suspend_date,resume_date,ann_date,suspend_reason,reason_type')
                #df = self.pro.suspend(ts_code=ts_code, suspend_date='', resume_date='', fields='ts_code,suspend_date,resume_date,ann_date,suspend_reason,reason_type')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def daily_basic(self,trade_date:str=trade_date):
        # 试3次下载数据，如不成功，每次暂停2钞 ok  12
        #获取全部股票每日重要的基本面指标，可用于选股分析、报表展示等
        for g in range(self.retry_count):
            try:
                #df = self.pro.query('daily_basic', ts_code:str=ts_code, trade_date='20180726',fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb')
                df = self.pro.daily_basic(ts_code=ts_code, trade_date=trade_date, fields='ts_code,trade_date,close,turnover_rate,turnover_rate_f,volume_ratio,pe,pe_ttm,pb,ps,ps_ttm,total_share,float_share,free_share,total_mv,circ_mv')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def moneyflow(self,trade_date:str=trade_date):
        #：moneyflow   OK
        #描述：获取沪深A股票资金流向数据，分析大单小单成交情况，用于判别资金动向
        for g in range(self.retry_count):
            try:
                #df = self.pro.moneyflow(trade_date=trade_date, fields='ts_code，trade_date，buy_sm_vol，buy_sm_amount，sell_sm_vol，sell_sm_amount，buy_md_vol，buy_md_amount，sell_md_vol，sell_md_amount，buy_lg_vol，buy_lg_amount，sell_lg_vol，sell_lg_amount，buy_elg_vol，buy_elg_amount，sell_elg_vol，sell_elg_amount，net_mf_vol，net_mf_amount')
                #df = self.pro.moneyflow(ts_code=ts_code, start_date=start_date, end_date=end_date)
                df = self.pro.moneyflow(trade_date=trade_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def stk_limit(self,trade_date:str=trade_date):
        # 试3次下载数据，如不成功，每次暂停2钞    14  OK
        #获取全市场（包含A/B股和基金）每日涨跌停价格，包括涨停价格，跌停价格等
        for g in range(self.retry_count):
            try:
                df = self.pro.stk_limit(trade_date=trade_date)
                #df = self.pro.stk_limit(ts_code='002149.SZ', start_date='20190115', end_date='20190615')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def hk_hold(self,trade_date:str=trade_date):
        # 试3次下载数据，如不成功，每次暂停2钞     15  ok
        #获取沪深港股通持股明细，数据来源港交所。exchange：SH沪股通SZ深港通HK港股通
        for g in range(self.retry_count):
            try:
                df = self.pro.hk_hold(trade_date=trade_date)
                #df = self.pro.hk_hold(trade_date='20190625', exchange='SH')
            except:
                time.sleep(self.pause)
            else:
                # print(df)     
                return df


    def income(self,ts_code:str=ts_code,start_date:str=start_date,end_date:str=end_date):
        # 试3次下载数据，如不成功，每次暂停2钞    16  ok
        #获取上市公司财务利润表数据
        #income(ts_code:str=ts_code,start_date='',end_date=''):
        #income(period=''):
        for g in range(self.retry_count):
            try:
                fiel1 = 'ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,basic_eps,'
                fiel2 = 'diluted_eps,total_revenue,revenue,int_income,prem_earned,comm_income,'
                fiel3 = 'n_commis_income,n_oth_income,n_oth_income,n_oth_b_income,prem_income,'
                fiel4 = 'out_prem,une_prem_reser,reins_income,n_sec_tb_income,n_sec_uw_income,'
                fiel5 = 'n_asset_mg_income,oth_b_income,fv_value_chg_gain,invest_income,'
                fiel6 = 'ass_invest_income,forex_gain,total_cogs,oper_cost,int_exp,comm_exp,'
                fiel7 = 'biz_tax_surchg,sell_exp,int_exp,assets_impair_loss,prem_refund,'
                fiel8 = 'compens_payout,reser_insur_liab,div_payt,reins_exp,oper_exp,'
                fiel9 = 'compens_payout_refu,insur_reser_refu,reins_cost_refund,other_bus_cost,'
                fiel10 = 'operate_profit,non_oper_income,non_oper_exp,nca_disploss,total_profit,'
                fiel11 = 'income_tax,n_income,n_income_attr_p,minority_gain,oth_compr_income,'
                fiel12 = 't_compr_income,compr_inc_attr_p,compr_inc_attr_m_s,ebit,ebitda,'
                fiel13 = 'insurance_exp,undist_profit,distable_profit'
                fiel0 = fiel1 + fiel2 + fiel3 + fiel4 + fiel5 + fiel6 + fiel7 + fiel8 + fiel9 + fiel10 + fiel11 + fiel12 + fiel13

                df = self.pro.income(ts_code=ts_code, start_date=start_date, end_date=end_date, fields=fiel0)
                #df = self.pro.income_vip(period=period,fields=fiel0)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def balancesheet(self,ts_code:str=ts_code,start_date:str=start_date,end_date:str=end_date):
        # 试3次下载数据，如不成功，每次暂停2钞
        #获取上市公司资产负债表    17  ok
        for g in range(self.retry_count):
            try:
                df = self.pro.balancesheet(ts_code=ts_code, start_date=start_date, end_date=end_date, fields='ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,total_share,cap_rese,undistr_porfit,surplus_rese,special_rese,money_cap,trad_asset,notes_receiv,accounts_receiv,oth_receiv,prepayment,div_receiv,int_receiv,inventories,amor_exp,nca_within_1y,sett_rsrv,loanto_oth_bank_fi,premium_receiv,reinsur_receiv,reinsur_res_receiv,pur_resale_fa,oth_cur_assets,total_cur_assets,fa_avail_for_sale,htm_invest,lt_eqt_invest,invest_real_estate,time_deposits,oth_assets,lt_rec,fix_assets,cip,const_materials,fixed_assets_disp,produc_bio_assets,oil_and_gas_assets,intan_assets,r_and_d,goodwill,lt_amor_exp,defer_tax_assets,decr_in_disbur,oth_nca,total_nca,cash_reser_cb,depos_in_oth_bfi,prec_metals,deriv_assets,rr_reins_une_prem,rr_reins_outstd_cla,rr_reins_lins_liab,rr_reins_lthins_liab,refund_depos,ph_pledge_loans,refund_cap_depos,indep_acct_assets,client_depos,client_prov,transac_seat_fee,invest_as_receiv,total_assets,lt_borr,st_borr,cb_borr,depos_ib_deposits,loan_oth_bank,trading_fl,notes_payable,acct_payable,adv_receipts,sold_for_repur_fa,comm_payable,payroll_payable,taxes_payable,int_payable,div_payable,oth_payable,acc_exp,deferred_inc,st_bonds_payable,payable_to_reinsurer,rsrv_insur_cont,acting_trading_sec,acting_uw_sec,non_cur_liab_due_1y,oth_cur_liab,total_cur_liab,bond_payable,lt_payable,specific_payables,estimated_liab,defer_tax_liab,defer_inc_non_cur_liab,oth_ncl,total_ncl,depos_oth_bfi,deriv_liab,depos,agency_bus_liab,oth_liab,prem_receiv_adva,depos_received,ph_invest,reser_une_prem,reser_outstd_claims,reser_lins_liab,reser_lthins_liab,indept_acc_liab,pledge_borr,indem_payable,policy_div_payable,total_liab,treasury_share,ordin_risk_reser,forex_differ,invest_loss_unconf,minority_int,total_hldr_eqy_exc_min_int,total_hldr_eqy_inc_min_int,total_liab_hldr_eqy,lt_payroll_payable,oth_comp_income,oth_eqt_tools,oth_eqt_tools_p_shr,lending_funds,acc_receivable,st_fin_payable,payables,hfs_assets,hfs_sales')
                #df2 = pro.balancesheet_vip(period='20181231',fields='ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,cap_rese')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def cashflow(self,ts_code:str=ts_code,start_date:str=start_date,end_date:str=end_date):
        # 试3次下载数据，如不成功，每次暂停2钞   18    ok
        #获取上市公司现金流量表
        for g in range(self.retry_count):
            try:
                #df = self.pro.query('cashflow',ts_code='600000.SH', start_date='20180101', end_date='20181231')
                df = self.pro.cashflow(ts_code=ts_code, start_date=start_date, end_date=end_date,fields='')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def forecast(self,ann_date:str=ann_date):
        # 试3次下载数据，如不成功，每次暂停2钞   19  ok
        #获取业绩预告数据
        for g in range(self.retry_count):
            try:
                #df = self.pro.forecast_vip(period='20181231',fields='ts_code,ann_date,end_date,type,p_change_min,p_change_max,net_profit_min')
                #df = self.pro.query('forecast', ts_code='600000.SH',fields='ts_code,ann_date,end_date,type,p_change_min,p_change_max,net_profit_min,net_profit_max,last_parent_net,first_ann_date,summary,change_reason')
                df = self.pro.forecast(ann_date=ann_date, fields='ts_code,ann_date,end_date,type,p_change_min,p_change_max,net_profit_min,net_profit_max,last_parent_net,first_ann_date,summary,change_reason')

            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def express(self,ts_code:str=ts_code,start_date:str=start_date,end_date:str=end_date):  
        # 试3次下载数据，如不成功，每次暂停2钞
        #获取上市公司业绩快报      20  ok
        for g in range(self.retry_count):
            try:
                df = self.pro.express(ts_code=ts_code, start_date=start_date, end_date=end_date,
                                fields='ts_code,ann_date,end_date,revenue,operate_profit,total_profit,n_income,total_assets,total_hldr_eqy_exc_min_int,diluted_eps,diluted_roe,yoy_net_profit,bps,yoy_sales,yoy_op,yoy_tp,yoy_dedu_np,yoy_eps,yoy_roe,growth_assets,yoy_equity,growth_bps,or_last_year,op_last_year,tp_last_year,np_last_year,eps_last_year,open_net_assets,open_bps,perf_summary,is_audit,remark')
                # df = self.pro.query('express', ts_code='600000.SH', start_date='20180101', end_date='20180701', fields='ts_code,ann_date,end_date,revenue,operate_profit,total_profit,n_income,total_assets')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def dividend(self,ts_code:str=ts_code):
        # 试3次下载数据，如不成功，每次暂停2钞   21  ok
        #分红送股数据
        for g in range(self.retry_count):
            try:
                df = self.pro.dividend(ts_code=ts_code, fields='ts_code, end_date, ann_date, div_proc, stk_div, stk_bo_rate, stk_co_rate, cash_div, cash_div_tax, record_date, ex_date, pay_date, div_listdate, imp_ann_date, base_date, base_share')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def fina_indicator(self,ts_code:str=ts_code, start_date:str=start_date,end_date:str=end_date):
        # 试3次下载数据，如不成功，每次暂停2钞    22    OK
        #：获取上市公司财务指标数据，为避免服务器压力，现阶段每次请求最多返回60条记录，可通过设置日期多次请求获取更多数据。
        for g in range(self.retry_count):
            try:
                df = self.pro.query('fina_indicator', ts_code=ts_code, start_date=start_date, end_date=end_date,fields='ts_code, ann_date, end_date, eps, dt_eps, total_revenue_ps, revenue_ps, capital_rese_ps, surplus_rese_ps, undist_profit_ps, extra_item, profit_dedt, gross_margin, current_ratio, quick_ratio, cash_ratio, invturn_days, arturn_days, inv_turn, ar_turn, ca_turn, fa_turn, assets_turn, op_income, valuechange_income, interst_income, daa, ebit, ebitda, fcff, fcfe, current_exint, noncurrent_exint, interestdebt, netdebt, tangible_asset, working_capital, networking_capital, invest_capital, retained_earnings, diluted2_eps, bps, ocfps, retainedps, cfps, ebit_ps, fcff_ps, fcfe_ps, netprofit_margin, grossprofit_margin, cogs_of_sales, expense_of_sales, profit_to_gr, saleexp_to_gr, adminexp_of_gr, finaexp_of_gr, impai_ttm, gc_of_gr, op_of_gr, ebit_of_gr, roe, roe_waa, roe_dt, roa, npta, roic, roe_yearly, roa2_yearly, roe_avg, opincome_of_ebt, investincome_of_ebt, n_op_profit_of_ebt, tax_to_ebt, dtprofit_to_profit, salescash_to_or, ocf_to_or, ocf_to_opincome, capitalized_to_da, debt_to_assets, assets_to_eqt, dp_assets_to_eqt, ca_to_assets, nca_to_assets, tbassets_to_totalassets, int_to_talcap, eqt_to_talcapital, currentdebt_to_debt, longdeb_to_debt, ocf_to_shortdebt, debt_to_eqt, eqt_to_debt, eqt_to_interestdebt, tangibleasset_to_debt, tangasset_to_intdebt, tangibleasset_to_netdebt, ocf_to_debt, ocf_to_interestdebt, ocf_to_netdebt, ebit_to_interest, longdebt_to_workingcapital, ebitda_to_debt, turn_days, roa_yearly, roa_dp, fixed_assets, profit_prefin_exp, non_op_profit, op_to_ebt, nop_to_ebt, ocf_to_profit, cash_to_liqdebt, cash_to_liqdebt_withinterest, op_to_liqdebt, op_to_debt, roic_yearly, profit_to_op, q_opincome, q_investincome, q_dtprofit, q_eps, q_netprofit_margin, q_gsprofit_margin, q_exp_to_sales, q_profit_to_gr, q_saleexp_to_gr, q_adminexp_to_gr, q_finaexp_to_gr, q_impair_to_gr_ttm, q_gc_to_gr, q_op_to_gr, q_roe, q_dt_roe, q_npta, q_opincome_to_ebt, q_investincome_to_ebt, q_dtprofit_to_profit, q_salescash_to_or, q_ocf_to_sales, q_ocf_to_or, basic_eps_yoy, dt_eps_yoy, cfps_yoy, op_yoy, ebt_yoy, netprofit_yoy, dt_netprofit_yoy, ocf_yoy, roe_yoy, bps_yoy, assets_yoy, eqt_yoy, tr_yoy, or_yoy, q_gr_yoy, q_gr_qoq, q_sales_yoy, q_sales_qoq, q_op_yoy, q_op_qoq, q_profit_yoy, q_profit_qoq, q_netprofit_yoy, q_netprofit_qoq, equity_yoy, rd_exp')
                #df = self.pro.fina_indicator(ts_code='600000.SH')
                #df = self.pro.query('fina_indicator', ts_code=ts_code, start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def fina_audit(self,ts_code:str=ts_code, start_date:str=start_date,end_date:str=end_date):
        # 试3次下载数据，如不成功，每次暂停2钞   23   ok
        #：获取上市公司定期财务审计意见数据
        for g in range(self.retry_count):
            try:
                df = self.pro.fina_audit(ts_code=ts_code, start_date=start_date, end_date=end_date,fields='ts_code,ann_date,end_date,audit_result,audit_fees,audit_agency,audit_sign')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def fina_mainbz(self,period:str=period,type:str=type):
        # 试3次下载数据，如不成功，每次暂停2钞    149  ok
        #period 是季末的最后一天 ‘20200630’
        #获得上市公司主营业务构成，分地区和产品,两种方式类型：P按产品 D按地区
        for g in range(self.retry_count):
            try:
                #df = self.pro.fina_mainbz(ts_code='000627.SZ', period='20171231', type='P',fields='ts_code, end_date, bz_item, bz_sales, bz_profit, bz_cost, curr_type,update_flag')
                #df = self.pro.fina_mainbz(ts_code='000627.SZ', type='P')
                #df = self.pro.fina_mainbz(ts_code=ts_code, period=period, type=type,fields='ts_code, end_date, bz_item, bz_sales, bz_profit, bz_cost, curr_type,update_flag')
                df = self.pro.fina_mainbz_vip(period=period, type=type ,fields='ts_code, end_date, bz_item, bz_sales, bz_profit, bz_cost, curr_type,update_flag')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def disclosure_date(self,end_date:str=end_date):
        # 试3次下载数据，如不成功，每次暂停2钞   24 ok 
        #：获取财报披露计划日期
        for g in range(self.retry_count):
            try:
                #df = self.pro.disclosure_date(end_date='20181231')
                df = self.pro.disclosure_date(end_date='20181231')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def moneyflow_hsgt(self,start_date:str=start_date,end_date:str=end_date):
        # 试3次下载数据，如不成功，每次暂停2钞   25  ok
        #：获取沪股通、深股通、港股通每日资金流向数据，每次最多返回300条记录，总量不限制
        for g in range(self.retry_count):
            try:
                #pro.query('moneyflow_hsgt', trade_date='20180725')
                df = self.pro.moneyflow_hsgt(start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def hsgt_top10(self,trade_date:str=trade_date,market_type:str=market_type):
        # 试3次下载数据，如不成功，每次暂停2钞    26  ok
        #：获取沪股通、深股通每日前十大成交详细数据市场类型（1：沪市 3：深市）
        for g in range(self.retry_count):
            try:
                #pro.query('hsgt_top10', ts_code='600519.SH', start_date='20180701', end_date='20180725')
                #pro.hsgt_top10(trade_date='20180725', market_type='1')
                df = self.pro.hsgt_top10(trade_date=trade_date, market_type=market_type)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def ggt_top10(self,trade_date:str=trade_date):
        # 试3次下载数据，如不成功，每次暂停2钞    27  ok
        #：获取港股通每日成交数据，其中包括沪市、深市详细数据市场类型 2：港股通（沪） 4：港股通（深）
        for g in range(self.retry_count):
            try:
                #pro.query('ggt_top10', ts_code='00700', start_date='20180701', end_date='20180727')
                #pro.ggt_top10(trade_date='20180727')
                df = self.pro.ggt_top10(trade_date=trade_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def ggt_daily(self,trade_date:str=trade_date):
        #接口：ggt_daily                    154
        #描述：获取港股通每日成交信息，数据从2014年开始
        for g in range(self.retry_count):
            try:           
                #获取单日全部统计
                df = self.pro.ggt_daily(trade_date=trade_date)
                #获取多日统计信息
                #df = self.pro.ggt_daily(trade_date='20190925,20180924,20170925')
                #获取时间段统计信息
                #df = self.pro.ggt_daily(start_date='20180925', end_date='20190925)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def ggt_monthly(self,start_date:str=start_date,end_date:str=end_date):
        #接口：ggt_daily                   155
        #描述：获取港股通每日成交信息，数据从2014年开始
        for g in range(self.retry_count):
            try:           
                #获取单月全部统计
                #df = self.pro.ggt_monthly(trade_date='201906')
                #获取多月统计信息
                #df = self.pro.ggt_monthly(trade_date='201906,201907,201709')
                #获取时间段统计信息
                df = self.pro.ggt_monthly(start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def margin(self,trade_date:str=trade_date):
        # 试3次下载数据，如不成功，每次暂停2钞    28  ok
        #：获取融资融券每日交易汇总数据
        for g in range(self.retry_count):
            try:
                df = self.pro.margin(trade_date=trade_date)
                #df = self.pro.query('margin', trade_date=trade_date, exchange_id='SSE')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def margin_detail(self,trade_date:str=trade_date):
        # 试3次下载数据，如不成功，每次暂停2钞  29  ok
        #：获取沪深两市每日融资融券明细
        for g in range(self.retry_count):
            try:
                df = self.pro.margin_detail(trade_date='20180802')
                #df = self.pro.query('margin_detail', trade_date='20180802')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def top10_holders(self,ts_code:str=ts_code,start_date='',end_date=''):
        # 试3次下载数据，如不成功，每次暂停2钞   30  OK
        #：获取上市公司前十大股东数据，包括持有数量和比例等信息。
        for g in range(self.retry_count):
            try:
                df = self.pro.top10_holders(ts_code=ts_code, start_date=start_date, end_date=end_date)
                #df = self.pro.query('top10_holders', ts_code='600000.SH', start_date='20170101', end_date='20171231')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def top10_floatholders(self,ts_code:str=ts_code,start_date:str=start_date,end_date:str=end_date):
        # 试3次下载数据，如不成功，每次暂停2钞     31    OK
        #：：获取上市公司前十大流通股东数据。
        for g in range(self.retry_count):
            try:
                df = self.pro.top10_floatholders(ts_code=ts_code, start_date=start_date, end_date=end_date)
                #df = self.pro.query('top10_floatholders', ts_code='600000.SH', start_date='20170101', end_date='20171231')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def top_list(self,trade_date:str=trade_date):
        # 试3次下载数据，如不成功，每次暂停2钞   32   ok
        #：龙虎榜每日交易明细
        for g in range(self.retry_count):
            try:
                df  = self.pro.top_list(trade_date=trade_date)
                #df = self.pro.query('top_list', trade_date='20180928', ts_code='002219.SZ')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def top_inst(self,trade_date:str=trade_date):
        # 试3次下载数据，如不成功，每次暂停2钞    33   ok
        #：龙虎榜机构成交明细
        for g in range(self.retry_count):
            try:
                df = self.pro.top_inst(trade_date=trade_date)
                #df = self.pro.query('top_inst', trade_date='20180928', ts_code='002219.SZ')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def pledge_start(self,ts_code:str=ts_code):
        # 试3次下载数据，如不成功，每次暂停2钞   34   ok
        #：获取股权质押统计数据
        for g in range(self.retry_count):
            try:
                df = self.pro.pledge_stat(ts_code=ts_code)
                #df = self.pro.query('pledge_stat', ts_code='000014.SZ')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def pledge_detail(self,ts_code:str=ts_code):
        # 试3次下载数据，如不成功，每次暂停2钞   35  ok 
        #：获取股权质押明细数据
        for g in range(self.retry_count):
            try:
                df = self.pro.pledge_detail(ts_code=ts_code)
                #df = self.pro.query('pledge_detail', ts_code='000014.SZ')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def repurchase(self,ann_date:str=ann_date):
        # 试3次下载数据，如不成功，每次暂停2钞   36 ok 
        #：获取上市公司回购股票数据
        for g in range(self.retry_count):
            try:
                #df = self.pro.repurchase(ann_date='', start_date=start_date, end_date=end_date)
                df = self.pro.repurchase(ann_date=ann_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def concept(self):
        # 试3次下载数据，如不成功，每次暂停2钞   37  ok 
        #：获取概念股分类，目前只有ts一个来源，未来将逐步增加来源
        for g in range(self.retry_count):
            try:
                #df = self.pro.concept()
                df = self.pro.concept(src='ts')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def concept_detail(self,ts_code:str=ts_code):
        # 试3次下载数据，如不成功，每次暂停2钞   38   ok
        #：获取概念股分类明细数据
        for g in range(self.retry_count):
            try:
                df = self.pro.concept_detail(ts_code = ts_code)
                #df = self.pro.concept_detail(id='TS2', fields='ts_code,name')
                #df = self.pro.concept_detail(id=id, fields='ts_code,name')
                #df = self.pro.concept(src='ts')先通过概念股分类接口获取具体分类
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def share_float(self,ann_date:str=ann_date):
        # 试3次下载数据，如不成功，每次暂停2钞   39  ok
        #：获取限售股解禁
        for g in range(self.retry_count):
            try:
                df = self.pro.share_float(ann_date=ann_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def block_trade(self,trade_date:str=trade_date):
        # 试3次下载数据，如不成功，每次暂停2钞   40   ok
        #：大宗交易
        for g in range(self.retry_count):
            try:
                df = self.pro.block_trade(trade_date=trade_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def stk_account(self,start_date:str=start_date,end_date:str=end_date):
        # 试3次下载数据，如不成功，每次暂停2钞   41  ok
        #：获取股票账户开户数据，统计周期为一周
        for g in range(self.retry_count):
            try:
                df = self.pro.stk_account(start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def stk_account_old(self,start_date:str=start_date,end_date:str=end_date):
        # 试3次下载数据，如不成功，每次暂停2钞  42      ok 
        #：获取股票账户开户数据，统计周期为一周(old)
        for g in range(self.retry_count):
            try:
                df = self.pro.stk_account_old(start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def stk_holdernumber(self,ts_code:str=ts_code,start_date='',end_date=''):
        # 试3次下载数据，如不成功，每次暂停2钞    43   ok 
        #：获取上市公司股东户数数据，数据不定期公布
        for g in range(self.retry_count):
            try:
                df = self.pro.stk_holdernumber(ts_code=ts_code, start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def stk_holdertrade(self,ann_date:str=ann_date):
        #：获取上市公司增减持数据，了解重要股东近期及历史上的股份增减变化   44    ok
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                # 获取单日全部增减持数据
                df = self.pro.stk_holdertrade(ann_date=ann_date)
                # 获取单个股票数据
                #df = self.pro.stk_holdertrade(ts_code='002149.SZ')
                # 获取当日增持数据
                #df = self.pro.stk_holdertrade(ann_date='20190426', trade_type='IN')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def index_basic(self,market_index:str=market_index):
        #：获取指数基础信息   45   ok
        # 试3次下载数据，如不成功，每次暂停2钞市场代码	说明
        # MSCI	MSCI指数 # CSI	中证指数 SSE上交所指数 SZSE	深交所指数 CICC	中金所指数 SW	申万指数  OTH	其他指数
        for g in range(self.retry_count):
            try:
                #df = self.pro.index_basic(market='SW')
                df = self.pro.index_basic(market=market_index)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def index_daily(self,index_code:str=index_code,start_date:str=start_date,end_date:str=end_date):
        #：获取指数每日行情，还可以通过bar接口获取   46     ok
        # 试3次下载数据，如不成功，每次暂停2钞市场代码	说明
        for g in range(self.retry_count):
            try:
                #df = self.pro.index_daily(ts_code='399300.SZ')
                df = self.pro.index_daily(ts_code=index_code, start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def index_weekly(self,trade_date:str=trade_date):
        #：获取指数周线行情  47       ok
        # 试3次下载数据，如不成功，每次暂停2钞市场代码	说明
        for g in range(self.retry_count):
            try:
                #df = self.pro.index_weekly(ts_code='000001.SH', start_date='20180101', end_date='20190329', fields='ts_code,trade_date,open,high,low,close,vol,amount')
                df = self.pro.index_weekly(trade_date=trade_date, fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def index_monthly(self,trade_date:str=trade_date):
        #：获取指数月线行情,每月更新一次   48   ok 
        # 试3次下载数据，如不成功，每次暂停2钞市场代码	说明
        for g in range(self.retry_count):
            try:
                #df = self.pro.index_monthly(ts_code='000001.SH', start_date='20180101', end_date='20190330', fields='ts_code,trade_date,open,high,low,close,vol,amount')
                df = self.pro.index_monthly(trade_date=trade_date, fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def index_weight(self,index_code:str=index_code,start_date:str=start_date,end_date:str=end_date):
        #：获取各类指数成分和权重，月度数据 ，如需日度指数成分和权重，请联系 waditu@163.com
        # 试3次下载数据，如不成功，每次暂停2钞市场代码	说明   49   ok
        for g in range(self.retry_count):
            try:
                df = self.pro.index_weight(index_code=index_code, start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df




    def index_dailybasic(self,trade_date:str=trade_date):
        #：目前只提供上证综指，深证成指，上证50，中证500，中小板指，创业板指的每日指标数据   50   ok
        # 试3次下载数据，如不成功，每次暂停2钞市场代码	说明
        for g in range(self.retry_count):
            try:
                df = self.pro.index_dailybasic(trade_date=trade_date, fields='ts_code,trade_date,total_mv,total_share,free_share,turnover_rate,turnover_rate_f,pe,pe_ttm,pb')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def index_classify(self,level:str=level):
        #：获取申万行业分类，包括申万28个一级分类，104个二级分类，227个三级分类的列表信息  51  ok
        # 试3次下载数据，如不成功，每次暂停2钞市场代码	说明行业分级（L1/L2/L3）
        for g in range(self.retry_count):
            try:
                # 获取申万一级行业列表
                #df = self.pro.index_classify(level='L1', src='SW')
                # 获取申万二级行业列表
                #df = self.pro.index_classify(level='L2', src='SW')
                # 获取申万三级级行业列表
                #df = self.pro.index_classify(level='L3', src='SW')
                df = self.pro.index_classify(level=level, src='SW')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def index_member(self,ts_code:str=ts_code):
        #：申万行业成分    52    ok
        # 试3次下载数据，如不成功，每次暂停2钞市场代码
        for g in range(self.retry_count):
            try:
                # 获取黄金分类的成份股
                #df = self.pro.index_member(index_code='850531.SI')
                # 获取000001.SZ所属行业
                #df = self.pro.index_member(ts_code='000001.SZ')
                df = df = self.pro.index_member(ts_code=ts_code)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def fund_basic(self,market_fund:str=market_fund):
        #：获取公募基金数据列表，包括场内和场外基金 场内O场外   53  ok
        # 试3次下载数据，如不成功，每次暂停2钞市场代码
        for g in range(self.retry_count):
            try:
                #df = self.pro.fund_basic(market='E')
                df = self.pro.fund_basic(market=market_fund)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def fund_company(self):
        #：获取公募基金管理人列表
        # 试3次下载数据，如不成功，每次暂停2钞市场代码   54    ok
        for g in range(self.retry_count):
            try:
                df = self.pro.fund_company()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def fund_nav(self,fund_code:str=fund_code):
        #：获取公募基金净值数据
        # 试3次下载数据，如不成功，每次暂停2钞市场代码  55   ok
        for g in range(self.retry_count):
            try:
                #df = self.pro.fund_nav(end_date=end_date)
                df = self.pro.fund_nav(ts_code=fund_code)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def fund_div(self,ann_date:str=ann_date):
        #：获取公募基金分红数据
        # 试3次下载数据，如不成功，每次暂停2钞市场代码  56    ok
        for g in range(self.retry_count):
            try:
                df = self.pro.fund_div(ann_date=ann_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def fund_portfolio(self,fund_code:str=fund_code):
        #：获取公募基金持仓数据，季度更新
        # 试3次下载数据，如不成功，每次暂停2钞市场代码  57   ok
        for g in range(self.retry_count):
            try:
                df = self.pro.fund_portfolio(ts_code=fund_code)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def fund_daily(self,fund_code:str=fund_code,start_date:str=start_date,end_date:str=end_date):
        #：获取场内基金日线行情，类似股票日行情   150     ok
        # 试3次下载数据，如不成功，每次暂停2钞市场代码
        for g in range(self.retry_count):
            try:
                df = self.pro.fund_daily(ts_code=fund_code, start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def fut_basic(self,exchange_fut:str=exchange_fut):
        #：获取期货合约列表数据交易所代码 CFFEX-中金所 DCE-大商所 CZCE-郑商所 SHFE-上期所 INE-上海国际能源交易中心
        # 试3次下载数据，如不成功，每次暂停2钞市场代码   58   ok
            try:
                #df = self.pro.fut_basic(exchange=exchange, fut_type='', fields='ts_code,symbol,exchange,name,fut_code,muliplier,trade_unit,pre_unit,quote_unit,quote_unit_desc,d_mode_desc,list_date,delist_date,d_moth,last_ddate')
                df = self.pro.fut_basic(exchange=exchange_fut,fut_type='',fields='ts_code,symbol,exchange,name,fut_code,multiplier,trade_unit,per_unit,quote_unit,quote_unit_desc,d_mode_desc,list_date,delist_date,d_month,last_ddate,trade_time_desc')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def fut_basic_a(self,exchange_fut:str=exchange_fut):
        #：获取期货合约列表数据交易所代码 CFFEX-中金所 DCE-大商所 CZCE-郑商所 SHFE-上期所 INE-上海国际能源交易中心
        # 试3次下载数据，如不成功，每次暂停2钞市场代码   58   ok
            try:
                #df = self.pro.fut_basic(exchange=exchange, fut_type='', fields='ts_code,symbol,exchange,name,fut_code,muliplier,trade_unit,pre_unit,quote_unit,quote_unit_desc,d_mode_desc,list_date,delist_date,d_moth,last_ddate')
                df = self.pro.fut_basic(exchange=exchange_fut,fut_type='1',fields='ts_code,symbol,exchange,name,fut_code,multiplier,trade_unit,per_unit,quote_unit,quote_unit_desc,d_mode_desc,list_date,delist_date,d_month,last_ddate,trade_time_desc')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def trade_cal_fut(self,exchange_fut:str=exchange_fut,start_date:str=start_date,end_date:str=end_date):
        #：获取各大期货交易所交易日历数据             59   ok
        # 试3次下载数据，如不成功，每次暂停2钞市场代码
        for g in range(self.retry_count):
            try:
                df = self.pro.trade_cal(exchange=exchange_fut, start_date=start_date, end_date=end_date)
                #df = self.pro.trade_cal(exchange='DCE', start_date='20180101', end_date='20181231')
                #df = self.pro.query('trade_cal', exchange='DCE', start_date='20180101', end_date='20181231')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def fut_daily(self,exchange_fut:str=exchange_fut,trade_date:str=trade_date):
        #：期货日线行情数据           60    ok
        # 试3次下载数据，如不成功，每次暂停2钞市场代码
        for g in range(self.retry_count):
            try:
                # 获取CU1811合约20180101～20181113期间的行情
                #df = self.pro.fut_daily(ts_code='CU1811.SHF', start_date='20180101', end_date='20181113')
                # 获取2018年11月13日大商所全部合约行情数据
                #df = self.pro.fut_daily(trade_date='20181113', exchange='DCE',fields='ts_code,trade_date,pre_close,pre_settle,open,high,low,close,settle,vol')
                df = self.pro.fut_daily(trade_date=trade_date, exchange=exchange_fut,
                                fields='ts_code,trade_date,pre_close,pre_settle,open,high,low,close,settle,change1,change2,vol,amount,oi,oi_chg,delv_settle')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def fut_holding(self,exchange_fut:str=exchange_fut,trade_date:str=trade_date):
        #：获取每日成交持仓排名数据          61   ok 
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #df = self.pro.fut_holding(trade_date='20181113', symbol='C', exchange='DCE')
                df = self.pro.fut_holding(trade_date=trade_date, symbol='C', exchange=exchange_fut)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def fut_wsr(self,trade_date:str=trade_date,symbol_fut:str=symbol_fut):
        #：获取仓单日报数据，了解各仓库/厂库的仓单变化   62  ok
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #df = self.pro.fut_wsr(trade_date='20181113', symbol='ZN')
                df = self.pro.fut_wsr(trade_date=trade_date, symbol=symbol_fut)
            except:
                time.sleep(self.pause)            
            else:
                # print(df)
                return df


    def fut_settle(self,exchange_fut:str=exchange_fut,trade_date:str=trade_date):
        #：获取每日结算参数数据，包括交易和交割费率等   63   ok
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #df = self.pro.fut_settle(trade_date='20181114', exchange='SHFE')
                df = self.pro.fut_settle(trade_date=trade_date, exchange=exchange_fut)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    """
    def index_daily(self,ts_code:str=ts_code,start_date='',end_date=''):
        #     #：获取南华指数每日行情，指数行情也可以通过通用行情接口获取数据．
        #     # 试3次下载数据，如不成功，每次暂停2钞          151   ok
        for g in range(self.retry_count):
            try:
                #df = self.pro.index_daily(ts_code='CU.NH', start_date='20180101', end_date='20181201')
                df = self.pro.index_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df
    """



    def opt_basic(self,exchange_opt:str=exchange_opt):
        #：获取期权合约信息
        # 试3次下载数据，如不成功，每次暂停2钞            64   ok
        for g in range(self.retry_count):
            try:
                #df = self.pro.opt_basic(exchange='DCE', fields='ts_code,exchange,name,per_unit,opt_code,opt_type,call_put,exercise_type,exercise_price,s_month,maturity_date,list_price,list_date,delist_date,last_edate,last_ddate,quote_unit,min_price_chg')
                df = self.pro.opt_basic(exchange=exchange_opt,
                                fields='ts_code,exchange,name,per_unit,opt_code,opt_type,call_put,exercise_type,exercise_price,s_month,maturity_date,list_price,list_date,delist_date,last_edate,last_ddate,quote_unit,min_price_chg')

            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def opt_daily(self,trade_date:str=trade_date):
        # ：获取期权日线行情              65  ok
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.opt_daily(trade_date=trade_date,fields='ts_code,trade_date,exchange,pre_settle,pre_close,open,high,low,close,settle,vol,amount,oi')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def cb_basic(self):
        # ：获取可转债基本信息       66   OK
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.cb_basic()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def cb_issue(self,ann_date:str=ann_date):
        # ：获取可转债发行数据         67  ok
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                # 获取可转债发行数据
                df = self.pro.cb_issue(ann_date=ann_date)
                # 获取可转债发行数据，自定义字段
                #df = self.pro.cb_issue(ann_date='20190612', fields='ts_code,ann_date,offl_deposit')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def cb_daily(self,trade_date:str=trade_date):
        # ：获取可转债行情         68  ok
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.cb_daily(trade_date=trade_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def fx_obasic(self,exchange_fx:str=exchange_fx,classify_fx:str=classify_fx):
        # 获取海外外汇基础信息，目前只有FXCM交易商的数据         69  ok 
 
        """
        classify分类说明
        序号    分类代码    分类名称    样例
        1    FX    外汇货币对    USDCNH（美元人民币对）
        2    INDEX    指数    US30（美国道琼斯工业平均指数）
        3    COMMODITY    大宗商品    SOYF（大豆）
        4    METAL    金属    XAUUSD （黄金）
        5    BUND    国库债券   Bund（长期欧元债券）
        6    CRYPTO    加密数字货币    BTCUSD(比特币)
        7    FX_BASKET    外汇篮子    USDOLLAR （美元指数）
        """
    
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                # 获取差价合约(CFD)中指数产的基础信息
                #df = self.pro.fx_obasic(exchange='FXCM', classify='INDEX', fields='ts_code,name,classify,min_unit,max_unit,pip,pip_cost,traget_spread,min_stop_distance,trading_hours,break_time')
                df = self.pro.fx_obasic(exchange=exchange_fx, classify=classify_fx,
                                fields='ts_code,name,classify,min_unit,max_unit,pip,pip_cost,traget_spread,min_stop_distance,trading_hours,break_time')

            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def fx_daily(self,code_fx:str=code_fx,start_date:str=start_date,end_date:str=end_date):
        # 获取外汇日线行情             70   ok 
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                # 获取差价合约(CFD)中指数产的基础信息
                #df = self.pro.fx_daily(ts_code='USDCNH.FXCM', start_date='20190101', end_date='20190524')
                df = self.pro.fx_daily(ts_code=code_fx, start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def shibor(self,start_date:str=start_date,end_date:str=end_date):
        # shibor利率            71   ok
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.shibor(start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def shibor_quote(self,start_date:str=start_date,end_date:str=end_date):          #not successful   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # ：Shibor报价数据            72   ok
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.shibor_quote(start_date=start_date, end_date=end_date)
                #pro.shibor_quote(start_date='20180101', end_date='20181101')
            except:
                time.sleep(self.pause)
                # print(df)
                return df

    def shibor_lpr(self,start_date:str=start_date,end_date:str=end_date):
        # LPR贷款基础利率   73    ok
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.shibor_lpr(start_date=start_date, end_date=end_date)
                #df = pro.shibor_lpr(start_date='20180101', end_date='20181130')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def libor(self,curr_type:str=curr_type,start_date:str=start_date,end_date:str=end_date):
        # Libor拆借利率 货币代码 (USD美元 EUR欧元 JPY日元 GBP英镑 CHF瑞郎，默认是USD)   74   ok
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #df = self.pro.libor(curr_type='USD', start_date='20180101', end_date='20181130')
                df = self.pro.libor(curr_type=curr_type, start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def hibor(self,start_date:str=start_date,end_date:str=end_date):
        #Hibor利率          75   ok
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.hibor(start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def wz_index(self,start_date:str=start_date,end_date:str=end_date):
        #温州民间借贷利率，即温州指数      76
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.wz_index(start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def gz_index(self,start_date:str=start_date,end_date:str=end_date):
        #广州民间借贷利率      77  ok
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.gz_index(start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def cctv_news(self,trade_date:str=trade_date):
        #获取新闻联播文字稿数据，数据开始于2006年6月，超过12年历史  79
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.cctv_news(date=trade_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def anns(self,ts_code:str=ts_code,start_date:str=start_date,end_date:str=end_date):
        #获取上市公司公告数据及原文文本，数据从2000年开始，内容很大，请注意数据调取节奏。
        # 试3次下载数据，如不成功，每次暂停2钞           80   ok
        for g in range(self.retry_count):
            try:
                # 获取单个股票公告数据
                df = self.pro.anns(ts_code=ts_code, start_date=start_date, end_date=end_date)
                # 获取2019年最新的50条公告数据
                #df = self.pro.anns(year='2019')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def coinlist(self,start_date:str=start_date,end_date:str=end_date):          #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取全球数字货币基本信息，包括发行日期、规模、所基于的公链和算法等。
        # 试3次下载数据，如不成功，每次暂停2钞          81
        for g in range(self.retry_count):
            try:
                #df = self.pro.coinlist(start_date=start_date, end_date=end_date,fields='coin,en_name,cn_name,issue_date,issue_price,amount,supply,algo,area,desc,labels')
                df = self.pro.query('coinlist', start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def coinpair(self,exchange_coin:str=exchange_coin,trade_date:str=trade_date):     #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取全球数字货币基本信息，包括发行日期、规模、所基于的公链和算法等。          82
        # 试3次下载数据，如不成功，每次暂停2钞
    
        """    交易所列表
        序号    交易所名称
        1    allcoin
        2    bcex
        3    bibox
        4    bigone
        5    binance
        6    bitbank
        7    bitfinex
        8    bitflyer
        9    bitflyex
        10    bithumb
        11    bitmex
        12    bitstamp
        13    bitstar
        14    bittrex
        15    bitvc
        16    bitz
        17    bleutrade
        18    btcbox
        19    btcc
        20    btccp
        21    btcturk
        22    btc_usd_index
        23    bter
        24    chbtc
        25    cobinhood
        26    coinbase
        27    coinbene
        28    coincheck
        29    coinegg
        30    coinex
        31    coinone
        32    coinsuper
        33    combine
        34    currency
        35    dextop
        36    digifinex
        37    exmo
        38    exx
        39    fcoin
        40    fisco
        41    future_bitmex
        42    gate
        43    gateio
        44    gdax
        45    gemini
        46    hadax
        47    hbus
        48    hft
        49    hitbtc
        50    huobi
        51   huobiotc
        52    huobip
        53    huobix
        54    idax
        55    idex
        56    index
        57    itbit
        58    jubi
        59    korbit
        60    kraken
        61    kucoin
        62    lbank
        63    lbc
        64    liqui
        65    okcn
        66    okcom
        67    okef
        68    okex
        69    okotc
        70    okusd
        71    poloniex
        72    quoine
        73    quoinex
        74    rightbtc
        75    shuzibi
        76    simex
        77    topbtc
        78    upbit
        79    viabtc
        80    yobit
        81    yuanbao
        82    yunbi
        83    zaif
        84    zb
        """
  
        for g in range(self.retry_count):
            try:
                df = self.pro.coinpair(exchange=exchange_coin, trade_date=trade_date)
                # df = self.pro.query('coinpair', exchange='huobi', trade_date='20180802')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def  coinexchanges(self,area_code:str=area_code):
        #：获取全球数字货币交易所基本信息。          83
        # 试3次下载数据，如不成功，每次暂停2钞
        
        """    交易所地区说明

        地区代码	地区名称
        ae	阿联酋
        au	澳大利亚
        br	巴西
        by	白俄罗斯
        bz	伯利兹
        ca	加拿大
        cbb	加勒比
        ch	瑞士
        cl	智利
        cn	中国
        cy	塞浦路斯
        dk	丹麦
        ee	爱沙尼亚
        es	西班牙
        hk	中国香港
        id	印度尼西亚
        il	以色列
        in	印度
        jp	日本
        kh	柬埔寨
        kr	韩国
        ky	开曼群岛
        la	老挝
        mn	蒙古国
        mt	马耳他
        mx	墨西哥
        my	马来西亚
        nl	荷兰
        nz	新西兰
        ph	菲律宾
        pl	波兰
        ru	俄罗斯
        sc	塞舌尔
        sg	新加坡
        th	泰国
        tr	土耳其
        tz	坦桑尼亚
        ua	乌克兰
        uk	英国
        us	美国
        vn	越南
        ws	萨摩亚
        za	南非
        """
      
        for g in range(self.retry_count):
            try:
                df = self.pro.coinexchanges(area_code=area_code)
                # 按交易对数量排序
                #df = df.sort('pairs', ascending=False)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def coinbar(self,exchange_coin:str=exchange_coin,symbol_coin:str=symbol_coin,freq_coin:str=freq_coin,start_date:str=start_date,end_date:str=end_date):     #not use  !!!!!!!!!!!!!!!!!!
        #获取数字货币行情数据，目前支持币币交易和期货合约交易。如果是币币交易，exchange参数请输入huobi,okex,binance,bitfinex等。
        # 如果是期货，exchange参数请输入future_xxx，比如future_okex，future_bitmex。  84
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #future_okex的contract_type有三种: this_week / next_week / quarter
                #future_bitmex的contract_type有五种: perpetual / biquarterly / quarterly / monthly / weekly
                #df = self.pro.coinbar(exchange='huobi', symbol='btcusdt', freq='15min', start_date='20180801',end_date='20180802')
                df = self.pro.coinbar(exchange=exchange_coin, symbol=symbol_coin, freq=freq_coin, start_date=start_date,end_date =end_date)
                #df = self.pro.query('coinbar', exchange='huobi', symbol='btcusdt', freq='15min', start_date='20180801', end_date='20180802')
                #df = self.pro.coinlist(start_date=start_date, end_date=end_date)
                #df = self.pro.query('coinlist', start_date='20170101', end_date='20171231')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def coincap(self,trade_date:str=trade_date):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取数字货币每日市值数据，该接口每隔6小时采集一次数据，所以当日每个品种可能有多条数据，用户可根据实际情况过滤截取使用。
        # 试3次下载数据，如不成功，每次暂停2钞   85
        for g in range(self.retry_count):
            try:
                df = self.pro.coincap(trade_date=trade_date)
                #df = self.pro.query('coincap', trade_date='20180806', coin='BTC')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def coinfree(self,exchange_coin:str=exchange_coin):
        #获取交易所当前和历史交易费率，目前支持的有huobi、okex、binance和bitfinex。
        # 试3次下载数据，如不成功，每次暂停2钞   86
        
        #xchange	名称	优惠情况
        #huobi	火币	按VIP级别不同有优惠，VIP需购买
        #okex	okex	按成交额度有优惠
        #binance	币安	按年优惠
        #bitfinex	bitfinex	按成交额度大小优惠
        #fcoin	fcoin	交易即挖矿，先收后返
        #coinex	coin	交易即挖矿，先收后返        
        for g in range(self.retry_count):
            try:
                df = self.pro.coinfees(exchange='huobi')
                #df = self.pro.query('coinfees', exchange='okex', asset_type='future')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def marketcap(self,start_date:str=start_date,end_date:str=end_date):
        #获取比特币历史以来每日市值数据  87
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.btc_marketcap(start_date=start_date, end_date=end_date)
                #df = self.pro.query('btc_marketcap', start_date='20180101', end_date='20180801')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def btc_pricevol(self,start_date:str=start_date,end_date:str=end_date):
        #获取比特币历史每日的价格和成交量数据。  88
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.btc_pricevol(start_date=start_date, end_date=end_date)
                #df = self.pro.query('btc_pricevol', start_date='20180101', end_date='20180801')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def ubindex_constituents(self,index_name:str=index_name,start_date:str=start_date,end_date:str=end_date):     #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取优币指数成分所对应的流通市值、权重以及指数调仓日价格等数据。   89
        # 试3次下载数据，如不成功，每次暂停2钞
        #指数名称    说明
        #UBI7    平台类TOP7项目指数
        #UBI0    平台类TOP10项目指数
        #UBI20    平台类TOP20项目指数
        #UBC7    币类TOP7项目指数
        #UB7    市场整体类TOP7项目指数
        #UB20    市场整体类TOP20项目指数
        for g in range(self.retry_count):
            try:
                df = self.pro.ubindex_constituents(index_name=index_name, start_date=start_date, end_date=end_date)
                #df = self.pro.ubindex_constituents(index_name='UBI7', start_date='20180801', end_date='20180901')
                #df =pro.query('ubindex_constituents', index_name='UBI7', start_date='20180801', end_date='20180901')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def jinse(self,start_date:str=start_date,end_date:str=end_date):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #：获取金色采集即时和历史资讯数据（5分钟更新一次）  152
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #start_date 格式'2018-08-17 16:00:00'
                df = self.pro.jinse(start_date=start_date, end_date=end_date,fields='title,content,type,url, datetime')
                #df = self.pro.jinse(start_date='2018-08-17 16:00:00', end_date='2018-08-17 18:00:00', fields='title, type, datetime')
                #df = self.pro.query('jinse', start_date='2018-08-17 16:00:00', end_date='2018-08-17 18:00:00', fields='title, type, datetime')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def btc8(self,start_date:str=start_date,end_date:str=end_date):      #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #：获取巴比特即时和历史资讯数据（5分钟更新一次，未来根据服务器压力再做调整）  90
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #start_date 格式'2018-08-17 16:00:00'
                df = self.pro.btc8(start_date=start_date, end_date=end_date, fields='title, url, datetime')
                #df = self.pro.btc8(start_date='2018-08-17 16:00:00', end_date='2018-08-17 18:00:00', fields='title, url, datetime')
                #df = self.pro.query('btc8', start_date='2018-08-17 16:00:00', end_date='2018-08-17 18:00:00',fields='title, url, datetime')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def bishijie(self,start_date:str=start_date,end_date:str=end_date):      #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #：获取币世界即时和历史资讯数据（5分钟更新一次，未来根据服务器压力再做调整）   91
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #start_date 格式'2018-08-17 16:00:00'
                df = self.pro.bishijie(start_date=start_date, end_date=end_date, fields='title, datetime')
                #df = self.pro.bishijie(start_date='2018-08-17 16:00:00', end_date='2018-08-17 18:00:00', fields='title, datetime')
                #df = self.pro.query('bishijie', start_date='2018-08-17 16:00:00', end_date='2018-08-17 18:00:00', fields='title, datetime')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def exchange_ann(self,start_date:str=start_date,end_date:str=end_date):        #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #：获取各个交易所公告的即时和历史资讯数据（5分钟更新一次，未来根据服务器压力再做调整）  92
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #start_date 格式'2018-08-17 16:00:00'
                df = self.pro.exchange_ann(start_date=start_date, end_date=end_date, fields='title, datetime')
                #df = self.pro.exchange_ann(start_date='2018-08-17 16:00:00', end_date='2018-08-17 18:00:00',fields='title, datetime')
                #df = self.pro.query('exchange_ann', start_date='2018-08-17 16:00:00', end_date='2018-08-17 18:00:00', fields='title, datetime')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def exchange_twitter(self,start_date:str=start_date,end_date:str=end_date):     #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #：获取Twitter上数字货币交易所发布的消息（5分钟更新一次，未来根据服务器压力再做调整）  93
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #start_date 格式'2018-08-17 16:00:00'
                df = self.pro.exchange_twitter(start_date=start_date, end_date=end_date, fields="id,account,nickname,content,retweet_content,media,str_posted_at,create_at")
                #df = self.pro.exchange_twitter(start_date='2018-09-02 03:20:03', end_date='2018-09-02 03:35:03', fields="id,account,nickname,content,retweet_content,media,str_posted_at,create_at")
                #df = self.pro.query('exchange_twitter', start_date='2018-09-02 03:20:03', end_date='2018-09-02 03:35:03', fields="id,account,nickname,content,retweet_content,media,str_posted_at,create_at")
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def twitter_kol(self,start_date:str=start_date,end_date:str=end_date):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #：获取Twitter上数字货币领域大V的消息（5分钟更新一次，未来根据服务器压力再做调整）  94
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #start_date 格式'2018-08-17 16:00:00'
                df = self.pro.twitter_kol(start_date=start_date, end_date=end_date, fields="id,account,nickname,content,retweet_content,media,str_posted_at")
                #df = self.pro.twitter_kol(start_date='2018-09-26 14:15:41', end_date='2018-09-26 16:20:11', fields="id,account,nickname,content,retweet_content,media,str_posted_at")
                #df = self.pro.query('twitter_kol', start_date='2018-09-26 14:15:41', end_date='2018-09-26 16:20:11', fields="id,account,nickname,content,retweet_content,media,str_posted_at")
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def tmt_twincome(self,start_date:str=start_date,end_date:str=end_date):   #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #：获取台湾TMT电子产业领域各类产品月度营收数据。   95
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #df = self.pro.tmt_twincome(item='8')
                df = self.pro.tmt_twincome(item='8', start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def tmt_twincomedetail(self):
        #：获取台湾TMT行业上市公司各类产品月度营收情况。  96
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.tmt_twincomedetail(item='8', symbol='6156')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def bo_monthly(self,trade_date:str=trade_date):        # not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #：获取电影月度票房数据   97
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.bo_monthly(date=trade_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def bo_weekly(self,trade_date:str=trade_date):       #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #：获取周度票房数据   98
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.bo_weekly(date=trade_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def bo_daily(self,trade_date:str=trade_date):      #not use !!!!!!!!!!!!!!!!!!!!!!!!!
        #：获取电影日度票房  99
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df =  pro.bo_daily(date=trade_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def bo_cinema(self,trade_date:str=trade_date):     #not use !!!!!!!!!!!!!!!!!!!!!!!!!
        #：获取每日各影院的票房数据   100
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.bo_cinema(date=trade_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def film_record(self,start_date:str=start_date,end_date:str=end_date):     #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取全国电影剧本备案的公示数据   101
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = self.pro.film_record(start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def teleplay_record(self,start_date:str=start_date,end_date:str=end_date):     #not use !!!!!!!!!!!!!!!!!
        #获取2009年以来全国拍摄制作电视剧备案公示数据  102
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                # 按备案月份查询
                #df = self.pro.teleplay_record(report_date='201905')
                df = self.pro.teleplay_record(start_date=start_date, end_date=end_date)
                # 按备案机构查询
                #df = self.pro.teleplay_record(org='上海新文化传媒集团股份有限公司')
                # 按电视剧名称查询
                #df = self.pro.teleplay_record(name='三体')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def deposit_rate(self):                   #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取存款利率   103
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_deposit_rate()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def loan_rate(self):        #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取贷款利率   104
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_loan_rate()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def rrr(self):                     #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取存款准备金利率   105
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_rrr()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def money_supply(self):                   #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取货币供应量    106
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_money_supply()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def money_supply_ball(self):     #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取货币供应量年底余额   107
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_money_supply_bal()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def gdp_year(self):      #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取国民生产总值   108
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_gdp_year()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def gdp_quarter(self):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   
        #获取国内生产总值(季度）   109
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_gdp_quarter()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def gdp_for(self):       #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取三大需求对GDP贡献   110
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_gdp_for()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def gdp_pull(self):   #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取三产业对GDP拉动  111
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_gdp_pull()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def gdp_contrib(self):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取三产业对GDP贡献率   112
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_gdp_contrib()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def cpi(self):   #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取居民消费指数 CPI   113
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_cpi()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def ppi(self):   #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取工业品出厂价格指数 PPI  114
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_ppi()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def ppi(self):   #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取工业品出厂价格指数 PPI   115
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_ppi()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def today_all(self):  #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #一次性获取当前交易所有股票的行情数据（如果是节假日，即为上一交易日，结果显示速度取决于网速）
        # 试3次下载数据，如不成功，每次暂停2钞   116
        for g in range(self.retry_count):
            try:
                df = ts.get_today_all()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def realtime_quotes(self,ts_code:str=ts_code):   #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取实时分笔数据，可以实时取得股票当前报价和成交信息  117
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #df = ts.get_realtime_quotes('000581')
                df = ts.get_realtime_quotes(ts_code)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def today_ticks(self,ts_code:str=ts_code):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取当前交易日（交易进行中使用）已经产生的分笔明细数据   118
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #df = ts.get_today_ticks('601333')
                df = ts.get_today_ticks(ts_code)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def industry_classified(self):   #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取行业分类   119
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_industry_classified()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def concept_classified(self):   #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取概念分类  120
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_concept_classified()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def area_classified(self):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取地域分类   121
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_area_classified()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def sme_classified(self):   #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取中小板分类  122
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_sme_classified()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def gem_classified(self):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取创业板分类  123
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_gem_classified()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def hs300s(self):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取沪深300成分及权重  124
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_hs300s()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def sz50(self):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取上证50成分   125
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_sz50s()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def zz500(self):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取中证500  126
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                df = ts.get_zz500s()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def report_data(year,querter):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取业绩报告主表  127
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #df = ts.get_report_data(2014,3)
                df = ts.get_report_data(year,querter)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def profit_data(year,querter):     #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取盈利能力   128
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #ts.get_profit_data(2014,3)
                df = ts.get_profit_data(year,querter)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def operation_data(year,querter):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取运营能力  129
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #ts.get_operation_data(2014,3)
                df = ts.get_operation_data(year,querter)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def growth_data(year,querter):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取成长能力  130
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #ts.get_growth_data(2014,3)
                df = ts.get_growth_data(year,querter)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def debtpaving_data(year,querter):     #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取偿债能力  131
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #ts.get_debtpaying_data(2014,3)
                df = ts.get_debtpaving_data(year,querter)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def cashflow_data(year,querter):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取现金流量数据   132
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #ts.get_cashflow_data(2014,3)
                df = ts.get_cashflow_data(year,querter)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def latest_news(top=''):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取最新消息条数  133
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #ts.get_latest_news(top=5,show_content=True) #显示最新5条新闻，并打印出新闻内容
                df = ts.get_latest_news(top=top,show_content=True)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def notices(top=''):     #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取信息地雷  134
        # 试3次下载数据，如不成功，每次暂停2钞
        for g in range(self.retry_count):
            try:
                #ts.get_notices()
                df = ts.get_latest_news(top=top,show_content=True)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def guba_sina(self):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取新浪股吧数据前17条  135
        # 试3次下载数据，如不成功，每次暂停2钞
        import time
        for g in range(self.retry_count):
            try:
                #ts.guba_sina()
                df = ts.guba_sina()
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def hk_basic(self):   
        #获取港股数据  137   ok
        # 试3次下载数据，如不成功，每次暂停2钞
        import time
        for g in range(self.retry_count):
            try:
                #ts.guba_sina()
                df = self.pro.hk_basic(fields='ts_code,name,fullname,enname,cn_spell,market,list_status,list_date,delist_date,trade_unit,isin,curr_type')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def hk_daily(self,trade_date:str=trade_date):   #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取港股每日增量和历史行情  138   ok
        # 试3次下载数据，如不成功，每次暂停2钞
        import time
        for g in range(self.retry_count):
            try:
                #ts.guba_sina()
                #df = self.pro.hk_daily(ts_code=ts_code, start_date=start_dt, end_date=end_dt)
                df = self.pro.hk_daily(trade_date=trade_date,fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def fut_mapping(self,fut_code:str=fut_code,start_date:str=start_date,end_date:str=end_date):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #获取期货主力（或连续）合约与月合约映射数据  139
        # 试3次下载数据，如不成功，每次暂停2钞
        import time
        for g in range(self.retry_count):
            try:
                #ts.guba_sina()
                df =  pro.fut_mapping(ts_code=fut_code, start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def major_news(self,start_date:str=start_date,end_date:str=end_date):
        #获取长篇通讯信息，覆盖主要新闻资讯网站  140
        #major_news(start_dt=date_wm,end_dt=date_wm,retry_count=3, pause=60) #网站下载要求 
        # 试3次下载数据，如不成功，每次暂停2钞
        import time
        
        time_min = ' 00:00:00'
        start_time = start_date[0:4] + '-' + start_date[4:6] + '-' + start_date[6:8] + time_min
        end_time = end_date[0:4] + '-' + end_date[4:6] + '-' + end_date[6:8] + time_min
        print(start_time,end_time)
        
        for g in range(self.retry_count):
            try:
                #ts.guba_sina()
                #df =  pro.major_news(src='', start_date='2018-11-21 00:00:00', end_date='2018-11-22 00:00:00', fields='title,content')
                df = self.pro.major_news(src='', start_date=start_time, end_date=end_time,fields='title,content,pub_time,src')
                #df = self.pro.major_news(src='', start_date=start_date, end_date=end_date,fields='title,content,pub_time,src')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def news(self,src:str=src,start_date:str=start_date, end_date:str=end_date):    
        #新闻快讯  143.   ok
        #src = ['sina','wallstreetcn','10jqka','eastmoney','yuncaijing']
        # 试3次下载数据，如不成功，每次暂停2钞
        import time
        time_min = ' 09:00:00'
        start_date = start_date + time_min
        end_date = end_date + time_min
        #print(start_date,end_date)
        for g in range(self.retry_count):
            try:
                #df = self.pro.news(src='eastmoney', start_date='20181121', end_date='20181122',fields='datetime', 'content', 'title', 'channels')
                df = self.pro.news(src=src, start_date=start_date, end_date=end_date,fields='datetime, content, title, channels')
                #df = pro.news(src='sina', start_date='2018-11-21 09:00:00', end_date='2018-11-22 10:10:00')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def cctv_news(self,trade_date:str=trade_date):   
        #接口：cctv_news   144.  ok
        #描述：获取新闻联播文字稿数据，数据开始于2006年6月，超过12年历史
        # 试3次下载数据，如不成功，每次暂停2钞
        import time
        for g in range(self.retry_count):
            try:
                #df = self.pro.cctv_news(date='20181211',fields='date', 'title', 'content')
                df = self.pro.cctv_news(date=trade_date,fields='date, title, content')
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def stk_managers(self,ts_code:str=ts_code):
        #接口：stk_managers
        #描述：获取上市公司管理层   146
        # 试3次下载数据，如不成功，每次暂停2钞
        import time
        for g in range(self.retry_count):
            try:
                #df = self.pro.cctv_news(date='20181211',fields='date', 'title', 'content')
                #df = self.pro.stk_managers(ts_code='000001.SZ')
                #df = self.pro.stk_managers(ts_code=ts_code,fields='ts_code，ann_date，name，gender，lev，title，edu，national，birthday，begin_date，end_date，resume')
                df = self.pro.stk_managers(ts_code=ts_code)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def stk_rewards(self,ts_code:str=ts_code):
        # db_ts_0007_stk_rewards
        # 管理层薪酬和持股
        # 接口：stk_rewards
        # 描述：获取上市公司管理层薪酬和持股   147   ok
        import time
        for g in range(self.retry_count):
            try:
                #df = self.pro.stk_rewards(ts_code='000001.SZ',end_date=end_date,fields='ts_code,ann_date,holder_name,pledge_amount,start_date,end_date,is_release,release_date,pledgor,holding_amount,pledged_amount,p_total_ratio,h_total_ratio,is_buyback')
                #df = self.pro.stk_rewards(ts_code=ts_code,end_date=end_date,fields='ts_code，ann_date，end_date，name，title，reward，hold_vol')
                #df = self.pro.stk_rewards(ts_code=ts_code, fields='ts_code，ann_date，end_date，name，title，reward，hold_vol')
                df = self.pro.stk_rewards(ts_code=ts_code)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def adj_factor_b(self,trade_date:str=trade_date):     #not use !!!!!!!!!!!!!!!!!!!!!!!!!!
        #接口：adj_factor
        #更新时间：早上9点30分
        #描述：获取股票复权因子，可提取单只股票全部历史复权因子，也可以提取单日全部股票的复权因子。 148
        import time
        for g in range(self.retry_count):
            try:
                # 提取000001全部复权因子
                #df = self.pro.adj_factor(ts_code='000001.SZ', trade_date='')
                # 提取2018年7月18日复权因子
                #df = self.pro.adj_factor(ts_code=ts_code, trade_date=trade_date)
                df = self.pro.query('adj_factor', trade_date=trade_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def limit_list(self,start_date:str=start_date, end_date:str=end_date):
        #接口：limit_list    153
        #描述：获取每日涨跌停股票统计，包括封闭时间和打开次数等数据，帮助用户快速定位近期强（弱）势股，以及研究超短线策略。
        import time
        for g in range(self.retry_count):
            try:
                # 获取单日统计数据
                #df = self.pro.limit_list(trade_date='20190925')
                # 获取某日涨停股票，并指定字段输出
                #df = self.pro.limit_list(trade_date='20190925', limit_type='U', fields='ts_code,close,first_time,last_time')
                # 获取时间段统计信息
                df = self.pro.limit_list(start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df



    def fund_adj(self,ts_code:str=ts_code,start_date:str=start_date, end_date:str=end_date):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #接口：fund_adj      156    ok
        #描述：获取基金复权因子，用于计算基金复权行情
        import time
        for g in range(self.retry_count):
            try:
                df = self.pro.fund_adj(ts_code=ts_code, start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def yc_cb(self,trade_date:str=trade_date):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!
        #接口：yc_cb
        #描述：获取中债收益率曲线，目前可获取中债国债收益率曲线即期和到期收益率曲线数据   158  ok
        import time
        for g in range(self.retry_count):
            try:
                #df = self.pro.yc_cb(ts_code='1001.CB',curve_type='0',trade_date='20200203')
                df = self.pro.yc_cb(ts_code=ts_code,curve_type='',trade_date=trade_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def fund_share(self,fund_code:str=fund_code):
        #接口：fund_share
        #描述：获取基金规模数据，包含上海和深圳ETF基金   159  ok
        import time
        for g in range(self.retry_count):
            try:            
                #df = df = self.pro.fund_share(ts_code='150018.SZ')
                df = self.pro.fund_share(ts_code=fund_code)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def fund_manager(self,fund_code:str=fund_code):
        #接口：fund_manager
        #描述：获取公募基金经理数据，包括基金经理简历等数据  160  ok
        import time
        for g in range(self.retry_count):
            try: 
                #df = df = self.pro.fund_share(ts_code='150018.SZ')
                df = self.pro.fund_manager(ts_code=fund_code)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def cn_gdp(self,start_date:str=start_date,end_date:str=end_date):
        #接口：cn_gdp
        #描述：获取国民经济之GDP数据      No. 161
        import time
        q1 = 'Q1'
        q4 = 'Q4'
        start_q = start_date[0:4] + q1
        end_q = end_date[0:4] + q4
        for g in range(self.retry_count):
            try: 
                #df = self.pro.us_tycr(start_q='2018Q1', end_q='2019Q3', fields='quarter,gdp,gdp_yoy,pi,pi_yoy,si,si_yoy,ti,ti_yoy')
                #df = self.pro.us_tycr(start_q=start_q, end_q=end_q, fields='quarter,gdp,gdp_yoy,pi,pi_yoy,si,si_yoy,ti,ti_yoy')
                df = self.pro.cn_gdp(start_q=start_q, end_q=end_q)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def cn_cpi(self,start_date:str=start_date,end_date:str=end_date):
        #接口：cn_cpi
        #描述：获取CPI居民消费价格数据，包括全国、城市和农村的数据   NO.162
        import time
        start_m = start_date[0:6]
        end_m = end_date[0:6]
        for g in range(self.retry_count):
            try: 
                # df = self.pro.cn_cpi(start_m='201801', end_m='201903')
                #df = self.pro.us_cpi(start_q='201801', end_q='201903', fields='month,nt_val,nt_yoy')
                df = self.pro.cn_cpi(start_m=start_m, end_m=end_m)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def eco_cal(self,trade_date:str=trade_date,country_wm:str=country_wm):
        #接口：eco_cal
        #描述：获取全球财经日历、包括经济事件数据更新  NO.163
        import time
        for g in range(self.retry_count):
            try: 
                # df = self.pro.cn_cpi(start_m='201801', end_m='201903')
                #df = self.pro.us_cpi(start_q='201801', end_q='201903', fields='month,nt_val,nt_yoy')
                df = self.pro.eco_cal(date=trade_date,country=country_wm)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def eco_cal_a(self,trade_date:str=trade_date):    #not use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #接口：eco_cal
        #描述：获取全球财经日历、包括经济事件数据更新  NO.163
        import time
        for g in range(self.retry_count):
            try: 
                # df = self.pro.cn_cpi(start_m='201801', end_m='201903')
                #df = self.pro.us_cpi(start_q='201801', end_q='201903', fields='month,nt_val,nt_yoy')
                df = self.pro.eco_cal(date=trade_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

  
    def bak_daily(self,ts_code:str=ts_code,start_date:str=start_date,end_date:str=end_date):    
        #接口：bak_daily     #164
        #描述：获取备用行情，包括特定的行情指标
        import time
        for g in range(self.retry_count):
            try: 
                df = self.pro.bak_daily(ts_code=ts_code,start_date=start_date,end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df

    def index_global(self,index_global:str=index_global,start_date:str=start_date,end_date:str=end_date):
        #接口：bak_daily     #165
        #描述：获取备用行情，包括特定的行情指标
        #接口：index_global
        #描述：获取国际主要指数日线行情
        #TS指数代码	指数名称
        #XIN9	富时中国A50指数 (富时A50)
        #HSI	恒生指数
        #DJI	道琼斯工业指数
        #SPX	标普500指数
        #IXIC	纳斯达克指数
        #FTSE	富时100指数
        #FCHI	法国CAC40指数
        #GDAXI	德国DAX指数
        #N225	日经225指数
        #KS11	韩国综合指数
        #AS51	澳大利亚标普200指数
        #SENSEX	印度孟买SENSEX指数
        #IBOVESPA	巴西IBOVESPA指数
        #RTS	俄罗斯RTS指数
        #TWII	台湾加权指数
        #CKLSE	马来西亚指数
        #SPTSX	加拿大S&P/TSX指数
        #CSX5P	STOXX欧洲50指数
        import time
        for g in range(self.retry_count):
            try:                
                df = self.pro.index_global(ts_code=index_global, start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                # print(df)
                return df


    def ft_tick(self,ft_symbol:str=ft_symbol,start_date:str=start_date,end_date:str=end_date):    
        #接口：ft_tick       #166     #需要公司交易账号
        #描述：获取期权和期货的tick数据   
        import time
        for g in range(self.retry_count):
            try: 
                df = self.pro.ft_tick(symbol=ft_symbol,start_date=start_date,end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                #print(df)
                return df



    def eco_cal_a(self,trade_date:str=trade_date):     #not use !!!!!!!!!!!!!!!!!!!!!!         
        #接口：eco_cal     #167     
        #描述：获取全球财经日历、包括经济事件数据更新
        import time
        for g in range(self.retry_count):
            try: 
                df = self.pro.eco_cal(date=trade_date)
            except:
                time.sleep(self.pause)
            else:
                #print(df)
                return df


    def eco_cal_b(self):                                    #no use !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!        
        #接口：eco_cal     #168    
        #描述：获取美国非农数据
        import time
        for g in range(self.retry_count):
            try: 
                df = self.pro.eco_cal(event='美国季调后非农*', fields='date,time,country,event,value,pre_value,fore_value')
            except:
                time.sleep(self.pause)
            else:
                #print(df)
                return df

    def us_basic(self):                                  
        #接口：us_basic    #169
        #描述：获取美股列表信息
        import time
        for g in range(self.retry_count):
            try: 
                df = self.pro.us_basic()
            except:
                time.sleep(self.pause)
            else:
                #print(df)
                return df

    def us_tradecal(self,start_date:str=start_date,end_date:str=end_date):                                  
        #接口：us_tradecal    #170
        #描述：获取美股交易日历信息
        import time
        for g in range(self.retry_count):
            try: 
                df = self.pro.us_tradecal(start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                #print(df)
                return df

    def us_daily(self,us_code:str=us_code,start_date:str=start_date,end_date:str=end_date):                                  
        #接口：us_daily   #171
        #描述：获取美股行情，包括全部股票全历史行情，以及重要的市场和估值指标
        import time
        for g in range(self.retry_count):
            try: 
                #df = self.df = pro.us_daily(ts_code='AAPL', start_date='20190101', end_date='20190904')
                df = self.pro.us_daily(ts_code=us_code, start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                #print(df)
                return df


    def us_daily_a(self,trade_date:str=trade_date):                                  
        #接口：us_daily   #172
        #描述：获取美股行情，包括全部股票全历史行情，以及重要的市场和估值指标
        import time
        for g in range(self.retry_count):
            try: 
                #df = self.df = pro.us_daily(ts_code='AAPL', start_date='20190101', end_date='20190904')
                df = self.pro.us_daily(trade_date=trade_date)
            except:
                time.sleep(self.pause)
            else:
                #print(df)
                return df


    def cn_ppi(self,start_date:str=start_date,end_date:str=end_date):                                  
        #接口：cn_ppi   #173
        #描述：获取PPI工业生产者出厂价格指数数据
        import time
        start_m = start_date[0:6]
        end_m = end_date[0:6]
        for g in range(self.retry_count):
            try:                 
                df = self.pro.cn_ppi(start_m=start_m, end_m=end_m)
            except:
                time.sleep(self.pause)
            else:
                #print(df)
                return df

    def cn_m(self,start_date:str=start_date,end_date:str=end_date):                                  
        #接口：cn_m    #174
        #描述：获取货币供应量之月度数据
        import time
        start_m = start_date[0:6]
        end_m = end_date[0:6]
        for g in range(self.retry_count):
            try:                 
                df = self.pro.cn_m(start_m=start_m, end_m=end_m)
            except:
                time.sleep(self.pause)
            else:
                #print(df)
                return df

    def us_tycr(self,start_date:str=start_date,end_date:str=end_date):                                  
        #接口：us_tycr    #175
        #描述：获取美国每日国债收益率曲线利率
        import time
        for g in range(self.retry_count):
            try:                 
                df = self.pro.us_tycr(start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                #print(df)
                return df


    def us_trycr(self,start_date:str=start_date,end_date:str=end_date):                                  
        #接口：us_trycr    #176
        #描述：国债实际收益率曲线利率
        import time
        for g in range(self.retry_count):
            try:                 
                df = self.pro.us_trycr(start_date=start_date, end_date=end_date)
            except:
                time.sleep(self.pause)
            else:
                #print(df)
                return df

    def us_tbr(self,start_date:str=start_date,end_date:str=end_date):                                   
        #接口：us_tbr  #177
        #描述：获取美国短期国债利率数据
        import time
        for g in range(self.retry_count):
            try:                 
                df = self.pro.us_tbr(start_date=start_date, end_date=end_date, fields='w4_bd,w4_ce,w8_bd,w8_ce,w13_bd,w13_ce,w26_bd,w26_ce,w52_bd,w52_ce')
            except:
                time.sleep(self.pause)
            else:
                #print(df)
                return df


    def us_tbr_a(self,start_date:str=start_date,end_date:str=end_date):                                  
        #接口：us_tbr  #178
        #描述：获取美国短期国债利率数据
        import time
        for g in range(self.retry_count):
            try:                 
                df = self.pro.us_tbr(start_date=start_date, end_date=end_date, fields='w4_bd,w4_ce,w8_bd,w8_ce,w13_bd,w13_ce,w26_bd,w26_ce,w52_bd,w52_ce')
            except:
                time.sleep(self.pause)
            else:
                #print(df)
                return df


    def us_tltr(self,start_date:str=start_date,end_date:str=end_date):                                   
        #接口：us_tltr    #179
        #描述：国债长期利率
        import time
        for g in range(self.retry_count):
            try:                 
                df = self.pro.us_tltr(start_date=start_date, end_date=end_date, fields='date,ltc,cmt,e_factor')
            except:
                time.sleep(self.pause)
            else:
                #print(df)
                return df


    def us_trltr(self,start_date:str=start_date,end_date:str=end_date):                                    
        #接口：us_trltr    #180
        #描述：国债实际长期利率平均值
        import time
        for g in range(self.retry_count):
            try:                 
                df = self.pro.us_trltr(start_date=start_date, end_date=end_date, fields='date,ltr_avg')
            except:
                time.sleep(self.pause)
            else:
                #print(df)
                return df

