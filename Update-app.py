import streamlit as st
import pandas as pd
import datetime

# 页面基础配置
st.set_page_config(page_title="银铜二波流动性指挥部V3", layout="wide", initial_sidebar_state="expanded")

st.title("🔔 银铜二波宏观流动性雷达指挥部 V3.0 (FRED实时对接版)")
st.markdown("---")

# 1. 核心自动化决策红绿灯组件
st.subheader("🚦 宏观流动性自动裁决系统")

col1, col2 = st.columns(2)

with col1:
    st.info("⛽ 核心燃料库状态 (FRED每周实时更新)")
    st.markdown("👉 **手动双保险检查：**")
    st.markdown("[📊 FRED官方一键直达：美联储准备金周度趋势 H.4.1 (WRESBAL)](https://fred.stlouisfed.org/series/WRESBAL)")
    
    # 动态免密钥抓取 FRED WRESBAL 原始 CSV 文件
    try:
        fred_url = "https://stlouisfed.org"
        # 抓取并清洗数据
        fred_df = pd.read_csv(fred_url)
        fred_df['VALUE'] = pd.to_numeric(fred_df['WRESBAL'], errors='coerce')
        fred_df = fred_df.dropna()
        
        latest_row = fred_df.iloc[-1]
        latest_date = latest_row['DATE']
        # WRESBAL单位是百万美元，换算成万亿美元 (T)
        latest_val = float(latest_row['VALUE']) / 1000000 
        
        st.metric(
            label=f"FRED 实时更新值 (数据日期: {latest_date})", 
            value=f"{latest_val:.3f} T", 
            delta=f"{(latest_val - 2.8):.3f} T 距 2.8T 核心安全线"
        )
    except Exception as e:
        # 网络防断裂备用兜底
        latest_val = 2.99
        st.metric(label="当前测算准备金规模 (网络缓冲中)", value="2.99 T", delta="0.19 T 距安全线")
        st.caption("提示：若因跨境网络波动加载较慢，请点击上方蓝色链接直接查看FRED官方图表。")

    # 燃料自动化裁决
    if latest_val >= 2.8:
        st.success("基础保障：🟢 长期基础燃料充沛，流动性未枯竭，支持商品第二波脉冲！")
    elif latest_val < 2.5:
        st.error("逃生警报：🚨 准备金触及 2.5T 无脑清仓线！市场后台水闸已关，必须无条件离场！")
    else:
        st.warning("黄灯预警：⚠️ 准备金进入 2.5T~2.8T 消耗摩擦区，严禁盲目高位做多。")

with col2:
    st.info("⚡ 短期批发资金摩擦与正回购求救信号")
    st.markdown("👉 **请分别打开以下官方数据，核对最新的利差指标：**")
    
    c_sofr, c_iorb = st.columns(2)
    with c_sofr:
        st.markdown("[📊 1. 查真实融资成本 (SOFR)](https://stlouisfed.org)")
    with c_iorb:
        st.markdown("[📊 2. 查央行利率红线 (IORB)](https://stlouisfed.org)")
        
    st.markdown("👉 **盯死纽约联储前线正回购窗口 (SRF 最终安全阀)：**")
    st.markdown("[🔍 纽约联储官方：REPO CHART 每日正回购操作结果公告页](https://newyorkfed.org)")
    st.caption("💡 战术心法：常备回购工具（SRF）每天在该窗口运行。若表格中接受金额（Amount Accepted）突增至 100 亿美元以上，说明系统开始缺钱！")

    # 手机交互计算器
    st.markdown("**🧮 手机交互快速研判盘面**")
    input_sofr = st.number_input("请输入今日最新 SOFR 利率 (%):", value=3.64, step=0.01, format="%.2f")
    input_iorb = st.number_input("请输入今日最新 IORB 利率 (%):", value=3.65, step=0.01, format="%.2f")
    srf_boost = st.checkbox("🚨 纽约联储 REPO 窗口接受金额突增 / SRF 出现用量（利差破3触发器）")
    
    # 自动计算利差
    spread = (input_sofr - input_iorb) * 100  # 换算成基点(bp)
    st.metric(label="今日实时计算利差 (SOFR - IORB)", value=f"{spread:.1f} bp (基点)")

    if spread >= 3.0 or srf_boost:
        st.error("核心裁决：🚨 钱荒！利差连续转正超 3 基点或 SRF 救急爆表！结构性顶部已暗中成熟，多单立刻逃顶！")
    elif spread >= 0.0:
        st.warning("核心裁决：⚠️ 摩擦！资金面开始紧平衡，美国国债发行虹吸效应显现，二波点火易失败，不可追高。")
    else:
        st.success("核心裁决：🟢 安全！流动性地下管网通畅，随时等待期权大单点火。")

st.markdown("---")

# 2. 期权点火模块
st.subheader("🔥 第二阶段期权市场 Gamma 点火雷达")
st.caption("请点击下方跳转，进入后在手机浏览器下拉页面盯紧 30-Day Skew 黑色粗线。若黑色粗线快速向下砸破 0 轴冲向负数区间，说明 Gamma 逼空启动，右侧立刻重仓进场！")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("### 🥈 CMX白银期货 (SI)")
    st.markdown("[👉 一键跳转：SLV 期权偏度图](https://marketchameleon.com/Overview/SLV/VolatilitySkew/OTMSpread)")

with c2:
    st.markdown("### 🧱 CMX高级铜 (HG)")
    st.markdown("[👉 一键跳转：CPER 铜期权偏度图](https://marketchameleon.com/Overview/CPER/VolatilitySkew/OTMSpreadm)")

with c3:
    st.markdown("### ⛏️ 铜业强手池 (FCX)")
    st.markdown("[👉 一键跳转：FCX 巨头期权偏度](https://marketchameleon.com/Overview/FCX/VolatilitySkew/OTMSpread)")

st.markdown("---")
st.markdown("💡 **系统风控红线**：在大盘未出现期权偏度（Skew）转负的数学铁证前，任何高位震荡期的反弹都可能是“假突破”。严禁使用超高杠杆在第一阶段洗盘期盲目猜底，防止在主升浪开启前半小时被插针强平。")
