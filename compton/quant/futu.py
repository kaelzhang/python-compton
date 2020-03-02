# -*- coding: utf-8 -*-

# matplotlib

# 导入futu-api
import futu as ft
# import matplotlib.pyplot as plt

class FutuContext:
    def __init__(self, host, port):
        self._ctx = ft.OpenQuoteContext(host=host, port=port)

    def subscribe(self, codes):
        ctx.subscribe([code], [
            # ft.SubType.QUOTE,
            # ft.SubType.TICKER,
            ft.SubType.K_DAY,
            # ft.SubType.ORDER_BOOK,
            # ft.SubType.RT_DATA,
            # ft.SubType.BROKER
        ])



# 实例化行情上下文对象
# ctx =

# 上下文控制
# ctx.start()              # 开启异步数据接收

# RET_OK = ft.RET_OK

# class TickerTest(ft.TickerHandlerBase):
#     def on_recv_rsp(self, rsp_str):
#         ret_code, data = super(TickerTest,self).on_recv_rsp(rsp_str)
#         if ret_code != RET_OK:
#             print("CurKlineTest: error, msg: %s" % data)
#             return RET_ERROR, data

#         print("TickerTest ", data) # TickerTest自己的处理逻辑

#         return RET_OK, None

# ctx.set_handler(TickerTest())  # 设置用于异步处理数据的回调对象(可派生支持自定义)

# 低频数据接口
# market = ft.Market.HK
# code = 'HK.00700'
# code_list = [code]
# plate = 'HK.BK1107'
# print(ctx.get_trading_days(market, start=None, end=None))   # 获取交易日

# print(ctx.get_stock_basicinfo(market, stock_type=ft.SecurityType.STOCK))   # 获取股票信息
# print(ctx.get_autype_list(code_list))                                  # 获取复权因子
# print(ctx.get_market_snapshot(code_list))                              # 获取市场快照
# print(ctx.get_plate_list(market, ft.Plate.ALL))                         # 获取板块集合下的子板块列表
# print(ctx.get_plate_stock(plate))                         # 获取板块下的股票列表

# 高频数据接口

# ret, kline_df = ctx.get_cur_kline(code, 100)

# print('df', kline_df)
# print('index', kline_df.index)
# print('columns', kline_df.columns)
# print('dtypes', kline_df.dtypes)
# print('values', kline_df.values)

# stock = StockDataFrame.retype(kline_df)

# print(stock['kdjk'])
# print(stock['boll'])

# print(ctx.get_stock_quote(code))  # 获取报价
# print(ctx.get_rt_ticker(code))   # 获取逐笔
# print(ctx.get_cur_kline(code, num=100, ktype=ft.KLType.K_DAY))   #获取当前K线
# print(ctx.get_order_book(code))       # 获取摆盘
# print(ctx.get_rt_data(code))          # 获取分时数据
# print(ctx.get_broker_queue(code))     # 获取经纪队列

# # 停止异步数据接收
# ctx.stop()

# # 关闭对象
# ctx.close()

# # 实例化港股交易上下文对象
# trade_hk_ctx = ft.OpenHKTradeContext(host="127.0.0.1", port=11111)

# # 交易接口列表
# print(trade_hk_ctx.unlock_trade(password='123456'))                # 解锁接口
# print(trade_hk_ctx.accinfo_query(trd_env=ft.TrdEnv.SIMULATE))      # 查询账户信息
# print(trade_hk_ctx.place_order(price=1.1, qty=2000, code=code, trd_side=ft.TrdSide.BUY, order_type=ft.OrderType.NORMAL, trd_env=ft.TrdEnv.SIMULATE))  # 下单接口
# print(trade_hk_ctx.order_list_query(trd_env=ft.TrdEnv.SIMULATE))      # 查询订单列表
# print(trade_hk_ctx.position_list_query(trd_env=ft.TrdEnv.SIMULATE))    # 查询持仓列表

# trade_hk_ctx.close()
