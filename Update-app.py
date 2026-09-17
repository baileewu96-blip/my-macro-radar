import streamlit as st
import pandas as pd
import requests

# 页面基础配置
st.set_page_config(page_title="银铜二波流动性指挥部V2", layout="wide", initial_sidebar_state="expanded")

st.title("🔔 银铜二波宏观流动性雷达指挥部 V2.0")
st.markdown("---")

# 1. 核心自动化决策红绿灯组件
st.subheader("🚦 宏观流动性自动裁决系统")

col1, col2 = st.columns(2)

with col1:
    st.info("⛽ 核心燃料库状态 (周更)")
    st.markdown("👉 **请通过下方 FRED 官方链接检查最新的准备金规模：**")
    st.markdown("[📊 FRED官方一键直达：美联储准备金周度趋势 H.4.1 (WRESBAL)](https://stlouisfed.org)")
    
    # 获取免密公共源
    try:
        url = "https://yahoo.com"
        df = pd.read_csv(url)
        latest_val = df['Close'].iloc[-1] / 1000000000000 # 换算成万亿美元
        st.metric(label="当前测算准备金规模 (Reserve Balances)", value=f"{latest_val:.2f} T", delta=f"{(latest_val - 2.8):.2f} T 距安全线")
    except:
        latest_val = 2.95
        st.metric(label="当前测算准备金规模 (网络缓冲)", value="2.95 T", delta="0.15 T 距安全线")

    if latest_val >= 2.8:
        st.success("基础保障：🟢 长期基础燃料充沛，二波暴涨环境具备。")
    elif latest_val < 2.5:
        st.error("逃生警报：🚨 准备金彻底跌破 2.5T 生命线！无条件全额清仓逃顶！")
    else:
        st.warning("黄灯预警：⚠️ 进入消耗期，严禁高位重仓。")

with col2:
    st.info("⚡ 短期批发资金摩擦与正回购求救信号")
    st.markdown("👉 **请分别打开以下官方数据，计算最新一天的利差 (SOFR - IORB)：**")
    
    c_sofr, c_iorb = st.columns(2)
    with c_sofr:
        st.markdown("[📊 1. 查真实融资成本 (SOFR)](https://stlouisfed.org)")
    with c_iorb:
        st.markdown("[📊 2. 查央行利率红线 (IORB)](https://stlouisfed.org)")
        
    st.markdown("👉 **盯死纽约联储前线正回购窗口 (SRF 用量探测器)：**")
    st.markdown("[🔍 纽约联储官方：REPO CHART 每日正回购操作结果公告页](https://newyorkfed.org)")
    st.caption("💡 核心功课：常备回购工具（SRF）每天在该窗口运行。若表格中接受金额（Amount Accepted）突增至 100 亿美元以上，说明系统缺钱！")

    # 手机交互计算器
    st.markdown("**🧮 手机交互快速研判盘面**")
    input_sofr = st.number_input("请输入今日最新 SOFR 利率 (%):", value=5.30, step=0.01, format="%.2f")
    input_iorb = st.number_input("请输入今日最新 IORB 利率 (%):", value=5.40, step=0.01, format="%.2f")
    srf_boost = st.checkbox("🚨 纽约联储 REPO 窗口接受金额突增 / SRF 用量过百亿")
    
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
    st.markdown("[👉 一键跳转：SLV 期权偏度图](https://marketchameleon.com)")

with c2:
    st.markdown("### 🧱 CMX高级铜 (HG)")
    st.markdown("[👉 一键跳转：CPER 铜期权偏度图](https://marketchameleon.com)")

with c3:
    st.markdown("### ⛏️ 铜业强手池 (FCX)")
    st.markdown("[👉 一键跳转：FCX 巨头期权偏度](https://marketchameleon.com)")

st.markdown("---")
st.markdown("💡 **系统风控红线**：在大盘未出现期权偏度（Skew）转负的数学铁证前，任何高位震荡期的反弹都可能是“假突破”。严禁使用超高杠杆在第一阶段洗盘期盲目猜底，防止在主升浪开启前半小时被插针强平。")

with col2:
    st.info("⚡ 短期批发资金摩擦与正回购求救信号")
    st.markdown("👉 **请分别打开以下官方数据，计算最新一天的利差 (SOFR - IORB)：**")
    
    c_sofr, c_iorb = st.columns(2)
    with c_sofr:
        st.markdown("[📊 1. 查真实融资成本 (SOFR)](https://stlouisfed.org)")
    with c_iorb:
        st.markdown("[📊 2. 查央行利率红线 (IORB)](https://stlouisfed.org)")
        
    st.markdown("👉 **盯死纽约联储前线正回购窗口 (SRF 用量探测器)：**")
    st.markdown("[🔍 纽约联储官方：REPO CHART 每日正回购操作结果公告页](https://newyorkfed.org)")
    st.caption("💡 核心功课：常备回购工具（SRF）每天在该窗口运行。若表格中接受金额（Amount Accepted）突增至 100 亿美元以上，说明系统缺钱！")

    # 手机交互计算器
    st.markdown("**🧮 手机交互快速研判盘面**")
    input_sofr = st.number_input("请输入今日最新 SOFR 利率 (%):", value=5.30, step=0.01, format="%.2f")
    input_iorb = st.number_input("请输入今日最新 IORB 利率 (%):", value=5.40, step=0.01, format="%.2f")
    srf_boost = st.checkbox("🚨 纽约联储 REPO 窗口接受金额突增 / SRF 用量过百亿")
    
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
    st.markdown("[👉 一键跳转：SLV 期权偏度图](https://marketchameleon.com)")

with c2:
    st.markdown("### 🧱 CMX高级铜 (HG)")
    st.markdown("[👉 一键跳转：CPER 铜期权偏度图](https://marketchameleon.com)")

with c3:
    st.markdown("### ⛏️ 铜业强手池 (FCX)")
    st.markdown("[👉 一键跳转：FCX 巨头期权偏度](https://marketchameleon.com)")

st.markdown("---")
st.markdown("💡 **系统风控红线**：在大盘未出现期权偏度（Skew）转负的数学铁证前，任何高位震荡期的反弹都可能是“假突破”。严禁使用超高杠杆在第一阶段洗盘期盲目猜底，防止在主升浪开启前半小时被插针强平。")
st.markdown("👉 **请点击下方官方一键直达链接查看今日利差曲线：**")
st.markdown("[📊 FRED官方一键直达：SOFR - IORB 实时利差曲线](https://stlouisfed.org)")
    
# 交互滑块：让用户每天扫一眼图表后输入数值，网页在手机端会自动做出研判
user_sofr = st.slider("请根据FRED图表，拖动今日最新的利差数值 (基点 %):", min_value=-0.10, max_value=0.10, value=-0.03, step=0.01)
if user_sofr >= 0.03:
    st.error("研判结果：🚨 钱荒！利差连续突破 3 个基点。商品高杠杆仓位建议立刻清仓逃顶。")
elif user_sofr >= 0.00:
    st.warning("研判结果：⚠️ 警告！批发资金开始紧张，9月财政部发债虹吸效应显现，不宜追高。")
else:
    st.success("研判结果：🟢 安全！后台管网通畅。可以安心执行右侧点火战术。")

st.markdown("---")

# 2. 期权点火模块 (防止爬虫封锁的完美无缝跳转卡片)
st.subheader("🔥 第二阶段期权市场 Gamma 点火雷达")
st.warning("华尔街期权变色龙（Market Chameleon）有高强度的IP防火墙。请直接点击下方卡片，进入后下拉网页盯紧 30-Day Skew 黑色粗线：")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("### 🥈 CMX白银期货 (SI)")
    st.markdown("[👉 点击进入 SLV 期权偏度图](https://marketchameleon.com)")
    st.caption("🚨 信号判定：若黑色粗线砸破 0 轴冲向负数，白银多单右侧立刻进场！")

with c2:
    st.markdown("### 🧱 LME/CMX高级铜 (HG)")
    st.markdown("[👉 点击进入 CPER 铜期权偏度图](https://marketchameleon.com)")
    st.caption("🚨 信号判定：绑定AI电网叙事，30日偏度转负为最终追击令。")

with c3:
    st.markdown("### ⛏️ 铜业游资总舵 (FCX)")
    st.markdown("[👉 点击进入 FCX 自由港期权偏度](https://marketchameleon.com)")
    st.caption("🚨 信号判定：矿业巨头的期权偏度最能反映强手资金的建仓真实意图。")

st.markdown("---")
# 内置风控框架
st.markdown("💡 **系统交易提醒**：白银（SI）与铜（HG）在高位震荡洗盘期（第一阶段）日内频繁剧烈插针，在期权偏度（Skew）未彻底砸向零轴下方前，严禁使用超过 5 倍的高财务杠杆盲目左侧猜底，严防在二波暴涨前半小时被洗出局。")
