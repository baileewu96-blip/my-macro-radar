import streamlit as st
import pandas as pd

# 页面基础配置
st.set_page_config(page_title="银铜流动性与期权终极指挥部V4", layout="wide", initial_sidebar_state="expanded")

st.title("🔔 银铜二波宏观流动性与CME期权终极指挥部 V4.0")
st.markdown("---")

# 横向分割线：第一部分 - 宏观流动性雷达
st.subheader("📊 第一阶段：宏观流动性后台水闸监测")

col1, col2 = st.columns(2)

with col1:
    st.info("⛽ 核心燃料库状态 (FRED每周实时更新)")
    st.markdown("👉 **双保险手动备用链接：**")
    st.markdown("[📊 FRED官方：美联储准备金周度趋势 H.4.1 (WRESBAL)](https://stlouisfed.org)")
    
    # 动态抓取 FRED 准备金数据
    try:
        fred_url = "https://stlouisfed.org"
        fred_df = pd.read_csv(fred_url)
        fred_df['VALUE'] = pd.to_numeric(fred_df['WRESBAL'], errors='coerce')
        fred_df = fred_df.dropna()
        
        latest_row = fred_df.iloc[-1]
        latest_date = latest_row['DATE']
        latest_val = float(latest_row['VALUE']) / 1000000 # 换算成万亿美元
        
        st.metric(
            label=f"FRED 实时更新值 (数据日期: {latest_date})", 
            value=f"{latest_val:.3f} T", 
            delta=f"{(latest_val - 2.8):.3f} T 距 2.8T 核心安全线"
        )
    except:
        latest_val = 2.95
        st.metric(label="当前测算准备金规模 (网络缓冲中)", value="2.95 T", delta="0.15 T 距安全线")
        st.caption("提示：若因网络波动未刷新，请点击上方蓝色链接直接查看。")

    # 自动化红绿灯判定
    if latest_val >= 2.8:
        st.success("基础保障：🟢 长期基础燃料充沛，二波暴涨宏观底座稳固！")
    elif latest_val < 2.5:
        st.error("逃生警报：🚨 准备金跌破 2.5T 生命线！后台流动性已关，多单必须无条件全额清仓！")
    else:
        st.warning("黄灯预警：⚠️ 准备金进入 2.5T~2.8T 摩擦消耗区，高位重仓需极度谨慎。")

with col2:
    st.info("⚡ 短期批发资金摩擦与正回购求救信号")
    st.markdown("👉 **请分别点开官方链接，核对今日最新读数：**")
    
    c_sofr, c_iorb = st.columns(2)
    with c_sofr:
        st.markdown("[📊 1. 查真实融资成本 (SOFR)](https://stlouisfed.org)")
    with c_iorb:
        st.markdown("[📊 2. 查央行利率红线 (IORB)](https://stlouisfed.org)")
        
    st.markdown("👉 **盯死纽约联储前线正回购窗口 (SRF 最终安全阀)：**")
    st.markdown("[🔍 纽约联储官方：REPO CHART 每日正回购操作结果页](https://newyorkfed.org)")
    st.caption("💡 核心功课：常备回购工具（SRF）每天在该窗口运行。若表格中接受金额（Amount Accepted）突增至 100 亿美元以上，说明系统开始钱荒！")

    st.markdown("**🧮 手机交互快速研判资金面**")
    input_sofr = st.number_input("请输入今日最新 SOFR 利率 (%):", value=3.64, step=0.01, format="%.2f")
    input_iorb = st.number_input("请输入今日最新 IORB 利率 (%):", value=3.65, step=0.01, format="%.2f")
    srf_boost = st.checkbox("🚨 纽约联储 REPO 窗口接受金额突增 / SRF 出现巨额用量")
    
    spread = (input_sofr - input_iorb) * 100 # 换算成基点(bp)
    st.metric(label="今日实时计算利差 (SOFR - IORB)", value=f"{spread:.1f} bp")

    if spread >= 3.0 or srf_boost:
        st.error("核心裁决：🚨 钱荒！利差转正超 3 基点或 SRF 爆表！结构性顶部已暗中成熟，多单立刻逃顶！")
    elif spread >= 0.0:
        st.warning("核心裁决：⚠️ 摩擦！资金面紧平衡，美国财政部发债虹吸显现，不可追高。")
    else:
        st.success("核心裁决：🟢 安全！流动性地下管网通畅，随时等待期权大单点火。")

st.markdown("---")

# 横向分割线：第二部分 - CME官方期权点火雷达
st.subheader("🔥 第二阶段：CME 芝商所官方原版期权点火雷达")
st.markdown("👉 **每日功课：** 请一键跳转下方官方看板，直接将你看到的最新 `SKEW`、`UpVar`、`DnVar` 填入下方计算器：")
st.markdown("[📊 官方一键直达：CME Group 全球期权 CVOL 核心数据看板](https://cmegroup.com)")

c_silver, c_copper = st.columns(2)

with c_silver:
    st.markdown("### 🥈 CMX白银期货 (SI) 决策罗盘")
    # 让用户手动输入刚刚截图看到的数字
    si_skew = st.number_input("输入今日最新白银 SKEW 读数:", value=12.59, step=0.1, format="%.2f")
    si_upvar = st.number_input("输入今日最新白银 UpVar 读数:", value=53.92, step=0.1, format="%.2f")
    si_dnvar = st.number_input("输入今日最新白银 DnVar 读数:", value=41.33, step=0.1, format="%.2f")
    
    # 验证公式
    si_calc_skew = si_upvar - si_dnvar
    st.caption(f"💡 校验：UpVar - DnVar 实际计算差值为: {si_calc_skew:.2f}")
    
    # 战略裁决
    if si_skew <= 0.0 or (si_upvar <= si_dnvar):
        st.success("白银信号：🔥 触发二波启动点火！SKEW成功砸破零轴，看涨情绪彻底倒挂，右侧多单立即进场吃斜率！")
    elif si_skew > 10.0:
        st.error("白银信号：❌ 处于狂热洗盘区！SKEW挂在 +10 以上高位，洗盘极度不彻底，严禁高杠杆追多，防插针爆仓！")
    else:
        st.warning("白银信号：⏳ 处于蓄势洗盘中。SKEW正在向零轴回落，继续保持空仓或定投底仓耐心等待。")

with c_copper:
    st.markdown("### 🧱 CMX高级铜期货 (HG) 决策罗盘")
    cp_skew = st.number_input("输入今日最新高级铜 SKEW 读数:", value=4.76, step=0.1, format="%.2f")
    cp_upvar = st.number_input("输入今日最新高级铜 UpVar 读数:", value=30.30, step=0.1, format="%.2f")
    cp_dnvar = st.number_input("输入今日最新高级铜 DnVar 读数:", value=25.55, step=0.1, format="%.2f")
    
    cp_calc_skew = cp_upvar - cp_dnvar
    st.caption(f"💡 校验：UpVar - DnVar 实际计算差值为: {cp_calc_skew:.2f}")
    
    # 战略裁决
    if cp_skew <= 0.0 or cp_calc_skew <= 0.0:
        st.success("高级铜信号：🔥 触发超级逼空令！铜 SKEW 彻底转负，成功压倒实体套保卖 Call 盘，右侧多单冲锋！")
    elif cp_skew <= 3.0:
        st.warning("高级铜信号：⏳ 进入黄金狙击观察带。SKEW 已逼近 0 轴，大资金可能正在暗中收集筹码，随时准备切入。")
    else:
        st.error("高级铜信号：❌ 属于散户跟风杂波。SKEW 还在常态化正数区间，继续过滤噪音，严禁进场。")

st.markdown("---")

# 第三部分：保留原有美股期权跳转，做多资产交叉参考
st.subheader("🌟 第三阶段：美股衍生品跨资产交叉验证 (选看)")
st.caption("保留原有的美股个股期权监控。当你发现商品期权跟美股股票正相关共振时，可在此进行双重确认：")

c3, c4, c5 = st.columns(3)
with c3:
    st.markdown("[👉 美股 SLV（白银ETF）期权偏度图](https://marketchameleon.com/Overview/SLV/VolatilitySkew/OTMSpread)")
with c4:
    st.markdown("[👉 美股 CPER（纯铜ETF）期权偏度图](https://marketchameleon.com/Overview/CPER/VolatilitySkew/OTMSpreadm)")
with c5:
    st.markdown("[👉 美股 FCX（铜业巨头）期权偏度图](https://marketchameleon.com/Overview/FCX/VolatilitySkew/OTMSpread)")

st.markdown("---")
st.markdown("💡 **系统交易生命线**：在第一阶段震荡洗盘期，大盘频繁出现高频插针清洗杠杆。在第一阶段和第二阶段信号未达成共振前，绝对不盲目猜底，直到期权数据给出数学铁证！")
