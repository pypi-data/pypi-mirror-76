## pgabc为数据分析提供各种帮助

## 需要安装pandas numpy talib 


##类内容：
##class Indicator():
##    """数据指数函数 可变列host_nv ,user_wm,passwd_wm,db_wm,chareset_wm来适应不同要求"""
##    period = 6    #系数
##    weight = 0.2
##    k = 12
##    ts_code = '000001.SZ'
##    time_temp = datetime.datetime.now() - datetime.timedelta(days=0)
##    given_dt = time_temp.strftime('%Y%m%d')
##    def __init__(self,df_wm,start_dt,end_dt):   
##        self.df_wm = df_wm
##        self.start_dt = start_dt
##        self.end_dt = end_dt
##        #self.cho_dt = self.cho_dt

##    def ma(self):
##        #返回是的DATA 可以用data.iloc[-1].ma_5等方式获得数据,可以直接用ma_wm[1]来得到最后一个数据
##        data = self.df_wm[(self.df_wm['ts_code']==self.ts_code)&(self.df_wm['trade_date']>=self.start_dt)&(self.df_wm['trade_date']<=self.given_dt)] 
##        data.drop_duplicates(subset=['ts_code','trade_date'],keep='first',inplace=True)  #去重
##        data = data.reset_index()   #重新排
##        data['ma_{}'.format(str(self.k))] = data.close.rolling(self.k).mean()    #5日收盘价均值
##        print(data.tail())
##        ma_wm = data.iloc[-1]['ma_{}'.format(str(self.k))]
##        return data,ma_wm
##   ...


## 主要指标
     ma(self,k:int = 10):
        #index_1

     ema(self,k:int = 10):
        #index_2

     rsi_wm(self,period:int = 6):
        #index_3  不推荐
        #RSI相对强弱指标
        #相对强弱指数（RSI）是通过比较一段时期内的平均收盘涨数和平均收盘跌数来分析市场买沽盘的意向和实力，从而作出未来市场的走势
    
     sma(self,k:int = 5):
        #index_4
        #计算PRICE_WM K天的简单平均数

     wma(self,timeperiod:int=30):
        #index_5 wma     
    
     ewma(self,period:int = 5,exponential:float = 0.2):
        #index_6
        # 计算PRICE_WM 期数为PERIOD天,EXPONENTIAL权数的指数加权平均数
    
     momentum(self,period:int = 19):
        #index_7
        #momentum trading strategy 动量交易策略 现价比PERIOND_WM前的价差

     macd(self,period1:int = 12,period2:int = 26,period3:int=9):
        #index_8

     kdj(self,n:int = 9,m1:int = 3,m2:int = 3):
        #index_9
        #kdj 9,3,3 数据

     bias(self,n1:int = 6,n2:int = 12,n3:int = 24):
        #index_10
        #bias指标  6,12,24
        #N期BIAS=(当日收盘价-N期平均收盘价)/N期平均收盘价*100%

     wr(self,n1:int = 10,n2:int = 6):
        #index_11
        #威廉指标

     obv(self,n:int = 30):
        #index_12

     boll(self):
        #index_13 
        #布林线指标，即BOLL指标，其英文全称是“Bollinger Bands”

     sun_moon(self):
        #index_14
        #生成阳线阴线标志，阳线为True ,阴线为False 

     k_form(self):
        #index_15
        #生成K线实体占HIGH-LOW的比重*100

     ma_group(self):
        #index_16 ma
        #生成数据的

     sma_ta(self,timeperiod:int = 30):
        #index_17 sma
        #SMA （简单移动平均线）（参数1：收盘价序列，参数2：时间周期（均线的计算长度 即 几日均线））

     atr(self,timeperiod:int = 14):
        #index_18
        #ATR（平均真实波幅）
        #（参数1：最高价序列，参数2：最低价序列，参数3：收盘价序列，参数4：时间周期）

     ht_trendline(self):
        #inex_19 ht_trendline
        #HT_TRENDLINE - Hilbert Transform - Instantaneous Trendline

     kama(self,timeperiod:int=30):
        #index_20 kama
        #KAMA - Kaufman Adaptive Moving Average

     var(self,timeperiod:int = 5,nbdev:int = 1):
        #index_21 var
        #MAMA - MESA Adaptive Moving Average

     tsf(self,timeperiod:int=14):
        #index_22 var
        #TSF - Time Series Forecast

     dema(self,timeperiod:int = 30):
        #index_23 dema
        #DEMA - Double Exponential Moving Average

     midpoint(self,timeperiod:int=14):
        #MIDPOINT - MidPoint over period
        #index_26 minpoint

     midprice(self,timeperiod:int=14):
        #index_27 midprice
        #MIDPRICE - Midpoint Price over period

     sar(self):
        #index_28 sar
        #SAR - Parabolic SAR

     sarext(self):
        #index_29 sarext
        #SAREXT - Parabolic SAR - Extended

     t3(self,timeperiod:int = 5):
        #index_30 t3
        #T3 - Triple Exponential Moving Average (T3)

     tema(self,timeperiod:int=30):
        #index_31 tema
        #TEMA - Triple Exponential Moving Average

     trima(self,timeperiod:int=30):
        #index_32 tirma
        #TRIMA - Triangular Moving Average

     wma1(self,timeperiod:int = 30):
        #index_33 wma
        #WMA - Weighted Moving Average

     adx(self,timeperiod:int = 14):
        #index_34 adx
        #ADX - Average Directional Movement Index
        #NOTE: The ADX function has an unstable period.

     adxr(self,timeperiod:int=14):
        #index_35 adxr
        #ADXR - Average Directional Movement Index Rating
        #NOTE: The ADXR function has an unstable period.

     apo(self,fastperiod:int=12,slowperiod:int=26):
        #index_36 apo
        #APO - Absolute Price Oscillator

     aroon(self,timeperiod:int=14):
        #index_37 aroon
        #AROON - Aroon

     aroonosc(self,timeperiod:int=14):
        #index_38 aroonosc
        #AROONOSC - Aroon Oscillator

     bop(self):
        #index_39 bop
        #BOP - Balance Of Power

     cci(self,timeperiod:int = 14):
        #index_40 cci
        #CCI - Commodity Channel Index

     cmo(self,timeperiod:int=14):
        #index_41 cmo
        #CMO - Chande Momentum Oscillator

     dx(self,timeperiod:int=14):
        #index_42 dx 
        #DX - Directional Movement Index

     macd_t(self,fastperiod:int=12,slowperiod:int=26,signalperiod:int=9):
        #index_43 macd
        #MACD - Moving Average Convergence/Divergence

     macdext(self,fastperiod:int=12,slowperiod:int=26,signalperiod:int=9):
        #index_44 macdext
        #MACDEXT - MACD with controllable MA type

     macdfix(self,signalperiod:int=9):
        #index_45 macdfix
        #MACDFIX - Moving Average Convergence/Divergence Fix 12/26

     mfi(self,timeperiod:int=14):
        #index_46 mfi
        #MFI - Money Flow Index

     minus_di(self,timeperiod:int=14):
        #index_47 minus_di
        #MINUS_DI - Minus Directional Indicator

     minus_dm(self,timeperiod:int=14):
        #index_48 minus_dm
        #MINUS_DM - Minus Directional Movement

     mom(self,timeperiod:int=10):
        #index_49 mom
        #MOM - Momentum

     plus_di(self,timeperiod:int=14):
        #index_50 plus_di
        #PLUS_DI - Plus Directional Indicator

     plus_dm(self,timeperiod:int=14):
        #index_51 plus_dm
        #PLUS_DM - Plus Directional Movement

     ppo(self,fastperiod:int=12,slowperiod:int=26):
        #index_52 ppo
        #PPO - Percentage Price Oscillator

     roc(self,timeperiod:int=10):
        #index_53 roc
        #ROC - Rate of change : ((price/prevPrice)-1)*100

     rocp(self,timeperiod:int=10):
        #index_54 rocp
        #ROCP - Rate of change Percentage: (price-prevPrice)/prevPrice

     rocr(self,timeperiod:int=10):
        #index_55 rocr
        #ROCP - Rate of change Percentage: (price-prevPrice)/prevPrice

     rocr100(self,timeperiod:int=10):
        #index_56 rocr100
        #ROCR100 - Rate of change ratio 100 scale: (price/prevPrice)*100

     rsi(self,timeperiod:int=14):
        #index_57 rsi
    
     stoch(self,fastk_period:int=5,slowk_period:int=3,slowd_period:int=3):
        #index_58 stoch
        #STOCH - Stochastic

     stochf(self,fastk_period:int=5,fastd_period:int=3):
        #index_59 stochf
        #STOCHF - Stochastic Fast

     stochrsi(self,timeperiod:int=14,fastk_period:int=5,fastd_period:int=3):
        #index_60 stochrsi
        #STOCHRSI - Stochastic Relative Strength Index

     trix(self,timeperiod:int=30):
        #index_61 trix
        #TRIX - 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA

     ultosc(self,timeperiod1:int=7,timeperiod2:int=14,timeperiod3:int=28):
        #index_62 stochf
        #ULTOSC - Ultimate Oscillator  

     willr(self,timeperiod:int=14):
        #index_63 stochf
        #WILLR - Williams' %R 

     ad(self):
        #index_64 ad
        #AD - Chaikin A/D Line

     ad(self,fastperiod:int=3,slowperiod:int=10):
        #index_65 adosc
        #ADOSC - Chaikin A/D Oscillator

     obv_ta(self):
        #index_66 obv
        #OBV - On Balance Volume

     ht_dcperiod(self):
        #index_67 ht_dcperiod
        #HT_DCPERIOD - Hilbert Transform - Dominant Cycle Period

     ht_dcphase(self):
        #index_68 ht_dcphase    NNN
        #HT_DCPHASE - Hilbert Transform - Dominant Cycle Phase

     ht_phasor(self):
        #index_69 ht_phasor  NNNN
        #HT_PHASOR - Hilbert Transform - Phasor Components

     ht_sine(self):
        #index_70 ht_sine  NNN
        #HT_SINE - Hilbert Transform - SineWave

     ht_trendmode(self):
        #index_71 ht_trendmode
        #HT_TRENDMODE - Hilbert Transform - Trend vs Cycle Mode

     avgprice(self):
        #index_72 AVGPRICE
        #AVGPRICE - Average Price

     medprice(self):
        #index_73 MEDPRICE
        #MEDPRICE - Median Price

     typprice(self):
        #index_74 TYPPRICE
        #TYPPRICE - Typical Price

     wclprice(self):
        #index_75 WCLPRICE
        #WCLPRICE - Weighted Close Price

     atr(self,timeperiod:int=14):
        #index_76 atr
        #ATR - Average True Range

     natr(self,timeperiod:int=14):
        #index_77 aatr
        #NATR - Normalized Average True Range

     trange(self):
        #index_78 trange
        #TRANGE - True Range

     cdl2crows(self):
        #index_79 cdl2crows 

     cdl3blackcrows(self):
        #index_80 cdl3blackcrows
        #CDL3BLACKCROWS - Three Black Crows

     cdl3inside(self):
        #index_81 cdl3blackcrows
        #CDL3INSIDE - Three Inside Up/Down 

     cdl3linestrike(self):
        #index_82 cdl3cdl3linestrike
        #CDL3INSIDE - Three Inside Up/Down  

     cdl3outside(self):
        #index_83 cdl3outside

     cdl3starstinsouth(self):
        #index_84 CDL3STARSINSOUTH
        #CDL3STARSINSOUTH - Three Stars In The South

     cdl3whitesoldiers(self):
        #index_85  CDL3WHITESOLDIERS
        #CDL3WHITESOLDIERS - Three Advancing White Soldiers

     cdlabandonedbaby(self):
        #index_86  CDLABANDONEDBABY
        #CDLABANDONEDBABY - Abandoned Baby

     cdladvanceblock(self):
        #index_87 CDLADVANCEBLOCK
        #CDLADVANCEBLOCK - Advance Block

     cdlbelthold(self):
        #index_88 CDLBELTHOLD
        #CDLBELTHOLD - Belt-hold

     cdlbreakaway(self):
        #index_89 CDLBREAKAWAY
        #CDLBREAKAWAY - Breakaway

     cdlclosingmarubozu(self):
        #index_90 CDLCLOSINGMARUBOZU
        #CDLCLOSINGMARUBOZU - Closing Marubozu

     cdlconcealbabyswall(self):
        #index_91 CDLCLOSINGMARUBOZU
        #CDLCONCEALBABYSWALL - Concealing Baby Swallow

     cdlcounterattack(self):
        #index_92 CDLCOUNTERATTACK
        #CDLCOUNTERATTACK - Counterattack

     cdldarkcloundcover(self):
        #index_93 CDLDARKCLOUDCOVER
        #CDLDARKCLOUDCOVER - Dark Cloud Cover

     cdldoji(self):
        #index_94 CDLDOJI 
        #CDLDOJI - Doji
    
     cdldojistar(self):
        #index_95 CDLDOJI 
        #CDLDOJISTAR - Doji Star

     cdldragonflydoji(self):
        #index_96 CDLDRAGONFLYDOJI
        #CDLDRAGONFLYDOJI - Dragonfly Doji

     cdlengulfing(self):
        #index_97 CDLDRAGONFLYDOJI
        #CDLENGULFING - Engulfing Pattern

     cdleveningdojistar(self):
        #index_98 CDLEVENINGDOJISTAR
        #CDLEVENINGDOJISTAR - Evening Doji Star

     cdleveningstar(self):
        #index_99 CDLEVENINGSTAR 
        #CDLEVENINGSTAR - Evening Star

     cdlgapsidesidewhite(self):
        #index_100 CDLGAPSIDESIDEWHITE 
        #CDLGAPSIDESIDEWHITE - Up/Down-gap side-by-side white lines

     cdlgravestonedoji(self):
        #index_101 CDLGRAVESTONEDOJI - Gravestone Doji
        #CDLGRAVESTONEDOJI - Gravestone Doji

     cdlhammer(self):
        #index_102 CDLHAMMER  
        #CDLHAMMER - Hammer

     cdlhangingman(self):
        #index_103 CDLHANGINGMAN  
        #CDLHANGINGMAN - Hanging Man

     cdlharami(self):
        #index_104 CDLHARAMI 
        #CDLHARAMI - Harami Pattern

     cdlharamicross(self):
        #index_105 CDLHARAMICROSS 
        #CDLHARAMICROSS - Harami Cross Pattern

     cdlhighwave(self):
        #index_106 CDLHIGHWAVE 
        #CDLHIGHWAVE - High-Wave Candle

     cdlhikkake(self):
        #index_107 CDLHIKKAKE
        #CDLHIKKAKE - Hikkake Pattern

     cdlhikkakemod(self):
        #index_108 CDLHIKKAKEMOD 
        #CDLHIKKAKEMOD - Modified Hikkake Pattern

     cdlhomingpigeon(self):
        #index_109 CDLHOMINGPIGEON  
        #CDLHOMINGPIGEON - Homing Pigeon

     cdlidentical3crows(self):
        #index_110 CDLIDENTICAL3CROWS  
        #CDLIDENTICAL3CROWS - Identical Three Crows

     cdlinneck(self):
        #index_111 CDLINNECK 
        #CDLINNECK - In-Neck Pattern

     cdlinvertedhammer(self):
        #index_112 CDLINVERTEDHAMMER  
        #CDLINVERTEDHAMMER - Inverted Hammer

     cdlkicking(self):
        #index_113 CDLKICKING - Kicking
        #CDLKICKING - Kicking

     cdlkickingbylegngth(self):
        #index_114 CDLKICKINGBYLENGTH   
        #CDLKICKINGBYLENGTH - Kicking - bull/bear determined by the longer marubozu

     cdlladderbottom(self):
        #index_115 CDLLADDERBOTTOM  
        #CDLLADDERBOTTOM - Ladder Bottom

     cdllongleggeddoji(self):
        #index_116 CDLLONGLEGGEDDOJI  
        #CDLLONGLEGGEDDOJI - Long Legged Doji

     cdllongline(self):
        #index_117 CDLLONGLINE  
        #CDLLONGLINE - Long Line Candle

     cdlmarubozu(self):
        #index_118 CDLMARUBOZU  
        #CDLMARUBOZU - Marubozu

     cdlmatchinglow(self):
        #index_119 CDLMATCHINGLOW - Matching Low
        #CDLMARUBOZU - Marubozu

     cdlmathold(self):
        #index_119 CDLMATCHINGLOW - Matching Low
        #CDLMATHOLD - Mat Hold

     cdlmorningdojistar(self):
        #index_120 CDLMORNINGDOJISTAR 
        #CDLMORNINGDOJISTAR - Morning Doji Star

     cdlmorningstar(self):
        #index_121 CDLMORNINGSTAR 
        #CDLMORNINGSTAR - Morning Star

     cdlonneck(self):
        #index_122 CDLONNECK - On-Neck Pattern
        #CDLONNECK - On-Neck Pattern

     cdlpiercting(self):
        #index_123 CDLPIERCING - Piercing Pattern
        #CDLPIERCING - Piercing Pattern

     cdlrickshawman(self):
        #index_124 CDLRICKSHAWMAN 
        #CDLRICKSHAWMAN - Rickshaw Man

     cdlrisefall3methods(self):
        #index_125 CDLRISEFALL3METHODS  
        #CDLRISEFALL3METHODS - Rising/Falling Three Methods

     cdlseparatinglines(self):
        #index_126 CDLSEPARATINGLINES  
        #CDLSEPARATINGLINES - Separating Lines

     cdlshootingstar(self):
        #index_127 CDLSHOOTINGSTAR  
        #CDLSHOOTINGSTAR - Shooting Star

     cdlshortline(self):
        #index_128 CDLSHORTLINE - Short Line Candle
        #CDLSHORTLINE - Short Line Candle

     cdlspinningtop(self):
        #index_129 CDLSPINNINGTOP - Spinning Top
        #CDLSPINNINGTOP - Spinning Top

     cdlstalledpattern(self):
        #index_130 CDLSTALLEDPATTERN - Stalled Pattern
        #CDLSTALLEDPATTERN - Stalled Pattern

     cdlsticksandwich(self):
        #index_131 CDLSTICKSANDWICH  
        #CDLSTICKSANDWICH - Stick Sandwich

     cdltakuri(self):
        #index_132 CDLTAKURI
        #CDLTAKURI - Takuri (Dragonfly Doji with very long lower shadow)

     cdltasukigap(self):
        #index_132 CDLTASUKIGAP  
        #CDLTASUKIGAP - Tasuki Gap

     cdlthrusting(self):
        #index_133 CDLTHRUSTING  
        #CDLTHRUSTING - Thrusting Pattern

     cdltristar(self):
        #index_134 CDLTRISTAR  
        #CDLTRISTAR - Tristar Pattern

     cdlunique3river(self):
        #index_135 CDLUNIQUE3RIVER  
        #CDLUNIQUE3RIVER - Unique 3 River

     cdlupsidegap2crows(self):
        #index_136 CDLUPSIDEGAP2CROWS  
        #CDLUPSIDEGAP2CROWS - Upside Gap Two Crows

     cdlxsidegap3methods(self):
        #index_137 CDLXSIDEGAP3METHODS  
        #CDLXSIDEGAP3METHODS - Upside/Downside Gap Three Methods

     beta(self,timeperiod:int=5):
        #index_138 BETA 
        #BETA - Beta

     correl(self,timeperiod:int=30):
        #index_139 CORREL            
        #CORREL - Pearson's Correlation Coefficient (r)

     linearreg(self,timeperiod:int=14):
        #index_140 LINEARREG
        #LINEARREG - Linear Regression

     linearreg_angle(self,timeperiod:int=14):
        #index_141 LINEARREG_ANGLE
        #LINEARREG_ANGLE - Linear Regression Angle

     linearreg_intercept(self,timeperiod:int=14):
        #index_142 LINEARREG_INTERCEPT 
        #LINEARREG_INTERCEPT - Linear Regression Intercept

     linearreg_slope(self,timeperiod:int=14):
        #index_143 LINEARREG_SLOPE 
        #LINEARREG_SLOPE - Linear Regression Slope

     stddev(self,timeperiod:int=5,nbdev:int=1):
        #index_144 STDDEV
        #STDDEV - Standard Deviation

     tsf(self,timeperiod:int=14):
        #index_145 TSF 
        #TSF - Time Series Forecast

     var_ta(self,timeperiod:int=5,nbdev:int=1):
        #index_146 VAR 
        #VAR - Variance

     acos(self):
        #index_147 ACOS 
        #ACOS - Vector Trigonometric ACos

     asin(self):
        #index_148 ASIN 
        #ASIN - Vector Trigonometric ASin

     atan(self):
        #index_149 ATAN 
        #ATAN - Vector Trigonometric ATan

     ceil(self):
        #index_150 CEIL
        #CEIL - Vector Ceil

     cos(self):
        #index_151 COS
        #COS - Vector Trigonometric Cos

     cosh(self):
        #index_152 COSH 
        #COSH - Vector Trigonometric Cosh

     exp(self):
        #index_152 EXP
        #EXP

     floor(self):
        #index_153 FLOOR 
        #FLOOR - Vector Floor

     ln(self):
        #index_154 LN 
        #LN - Vector Log Natural

     log10(self):
        #index_155 LOG10 
        #LOG10 - Vector Log10

     sin(self):
        #index_156 SIN
        #SIN - Vector Trigonometric Sin

     sinh(self):
        #index_157 SINH 
        #SINH - Vector Trigonometric Sinh

     sqrt(self):
        #index_158 SQRT 
        #SQRT - Vector Square Root

     tan(self):
        #index_159 TAN 
        #TAN - Vector Trigonometric Tan

     tanh(self):
        #index_160 TANH 
        #TANH - Vector Trigonometric Tanh

     add(self):
        #index_161  ADD 
        #ADD - Vector Arithmetic Add

     div(self):
        #index_162 DIV 
        #DIV - Vector Arithmetic Div

     max(self,timeperiod:int=30):
        #index_163 MAX 

     maxindex(self,timeperiod:int=30):
        #index_164 MAXINDEX 
        #MAXINDEX - Index of highest value over a specified period

     min(self,timeperiod:int=30):
        #index_165 MIN 
        #MIN - Lowest value over a specified period

     minindex(self,timeperiod:int=30):
        #index_166 MININDEX 
        #MININDEX - Index of lowest value over a specified period

     minmax(self,timeperiod:int=30):
        #index_167 MINMAX 
        #MINMAX - Lowest and highest values over a specified period

     minmaxindex(self,timeperiod:int=30):
        #index_168 MINMAXINDEX 
        #MINMAXINDEX - Indexes of lowest and highest values over a specified period

     mult(self):
        #index_169 MULT - Vector Arithmetic Mult
        #MULT - Vector Arithmetic Mult

     sub(self):
        #index_170 SUB 
        #SUB - Vector Arithmetic Substraction

     sum(self,timeperiod:int=30):
        #index_171 SUM 
        #SUM - Summation

## 应用

##安装 pip install pgabc

##使用举例

##  import pgabc.indicator as pg_indicator
## pg = pg_indicator.Indicator(df,start_dt,end_dt)     #引入类  df 是数据pandas格式 ， 一般有 trade_date,ts_code,open,high,low,close,vol 等内容
## pg.ts_code = '600999.SH'                            #选定股票
## pg.given_dt = '20200701'                            #设定指定日期，默认是当前日期
## df = pg.ema(k=12)                                   #生成12日ema数据              

