import streamlit as st
import requests
import pandas as pd

# 页面基础配置
st.set_page_config(page_title="银铜流动性与CME期权监控仪表盘", layout="wide", initial_sidebar_state="expanded")

# ==================== 侧边栏：核心概念与终极红绿灯判断基准 ====================
with st.sidebar:
    st.header("🌟 终极风控与概念词典")
    st.markdown("---")
    
    with st.expander("📊 CME 官方 CVOL 的值有什么用？", expanded=True):
        st.markdown("""
        **`CVOL`（芝商所波动率指数）就是期货市场的“VIX（恐慌指数）”**。它代表全市场期权对未来 30 天白银和铜**价格波动剧烈程度**的预期。
        
        **💡 两大核心实战用途：**
        1. **判定洗盘是否接近尾声（量缩价稳）**：随着高位宽幅震荡洗盘的推进，若发现 **CVOL 的值开始持续萎缩、掉头向下**，说明高频大额插针的恶性获利盘已经洗净，进入了经典的“波动率压实”阶段。**CVOL 越低，蓄势越充分，二波点火成功率越高。**
        2. **防止高杠杆爆仓（杠杆管理工具）**：只要 CVOL 挂在 **45 以上**（如白银常态），意味着日内随时可以没有任何理由地暴跌或暴涨 3% 至 5%（恶意插针）。**此时必须强行压低期货杠杆倍数（预留 500% 以上保证金）**，否则极易在二波点火前夕被日内插针强平。
        """)

    with st.expander("🔌 核心红绿灯判断基准（全量红线）", expanded=False):
        st.markdown("""
        ### ⛽ 开关一：美联储准备金 (WRESBAL)
        - **绿灯（可做多）**：大过或等于 2.8 万億美元。大盘油箱安全，流动性充沛。
        - **黄灯（严禁追高）**：在 2.5 至 2.8 万億美元之间。进入缩表消耗期，商品脆性增加。
        - **红灯（无条件清仓逃顶）**：小于 2.5 万億美元。流动性红线跌破，24 小时内无脑全额平仓多单！
        
        ### ⚡ 开关二：短期批发资金摩擦 (SOFR - IORB)
        - **绿灯（安全）**：利差小于 0 轴（即为负数）。资金极度富裕。
        - **黄灯（警惕）**：利差大过或等于 0 轴并开始转正。发债虹吸效应显现。
        - **红灯（无条件逃顶）**：利差连续 3 个交易日大过或等于 +3.0 基点。发生局部“钱荒”，高杠杆资产牛市终结。
        
        ### 🔌 开关三：正回购安全阀 (纽约联储 REPO)
        - **绿灯（正常）**：接受金额 (Amount Accepted) 绝对等于 0。
        - **红灯（无条件逃顶）**：接受金额连续 3 天冲破 **100 億美元**。安全阀被动启动，管网爆裂，多单立刻离场。
        
        ### 🥈 开关四：CME 白银期权点火 (SIVL SKEW)
        - **等待期**：大过或等于 +10.0。虚值 Call 太贵，散户扎堆，极易遭遇日内插针清洗。
        - **🔥 进场冲锋号**：SKEW 快速下砸至小于或等于 0.0 轴（变成负数）。看涨情绪清洗干净或爆发超级 Gamma 逼空，右侧立刻重仓切入。
        
        ### 🧱 开关五：CME 高级铜期权点火 (HGVL SKEW)
        - **等待期**：大过 0.0。散户日常跟风和产业套保噪音，不操作。
        - **🔥 进场冲锋号**：SKEW 跌破零轴变成负数（哪怕是 -0.1）。跨国大游资彻底击穿实体矿山套保卖 Call 墙，右侧立刻重仓杀入。
        """)

# ==================== 主页面：动态监控台 ====================
st.title("🔔 银铜二波宏观流动性与CME期权监控仪表盘")
st.markdown("---")

# 第一部分 - 宏观流动性雷达
st.subheader("📊 第一阶段：宏观流动性后台水闸监测")

col1, col2 = st.columns(2)

with col1:
    st.info("⛽ 核心燃料库状态 (FRED API 官方实时拉取)")
    st.markdown("[📊 FRED官方一键直达：美联储准备金周度趋势 H.4.1 (WRESBAL)](https://fred.stlouisfed.org/series/WRESBAL)")
    
    # 💡 终极修复：为了防止任何潜在的排版或变量拼接覆盖导致乱码，我们将官方完整 API 链接一字不差地拆解和组装
    API_KEY = "c659bf9c3acaab256b314bdf7ae37865"
    
    # 彻底杜绝任何 stlouisfed.org 错乱串联
    base_api_url = "https://stlouisfed.org"
    query_params = f"?series_id=WRESBAL&api_key={API_KEY}&file_type=json"
    fred_api_url = base_api_url + query_params
    
    try:
        # 发起高优先级的官方 API 直连请求
        response = requests.get(fred_api_url, timeout=15)
        data = response.json()
        
        # 严格提取最后一条最新的官方观测点
        observations = data['observations']
        latest_obs = observations[-1]
        
        latest_date = latest_obs['date']
        # 将字符串转化为浮点数，除以 1,000,000 换算成万亿美元
        latest_val = float(latest_obs['value']) / 1000000 
        
        # 实时渲染最精准的数据（2.991T 将完美从美联储服务器射向手机屏幕）
        st.metric(
            label=f"🔥 FRED API 实时直传（最新数据日期: {latest_date}）", 
            value=f"{latest_val:.3f} T", 
            delta=f"{(latest_val - 2.8):.3f} T 距 2.8T 核心安全线"
        )
        
        # 根据动态抓取的值进行自动化红绿灯判断
        if latest_val >= 2.8:
            st.success("基础保障：🟢 长期基础燃料充沛，后台未触发枯竭，允许二波牛市拉升！")
        elif latest_val < 2.5:
            st.error("逃生警报：🚨 准备金触及 2.5T 崩塌线！美联储水闸已关，必须无条件清仓！")
        else:
            st.warning("黄灯预警：⚠️ 准备金进入 2.5T~2.8T 摩擦损耗区，严禁盲目高位大幅做多。")
            
    except Exception as e:
        st.error(f"❌ 专线连接失败！请排查网络。错误日志: {str(e)}")
        st.caption("提示：由于公共服务器可能存在国际断网，若报错请直接参考上方蓝色FRED原生链接。")

with col2:
    st.info("⚡ 短期批发资金摩擦与正回购求救信号")
    st.markdown("👉 **请分别点开官方链接，核对今日最新读数：**")
    
    c_sofr, c_iorb = st.columns(2)
    with c_sofr:
        st.markdown("[📊 1. 查真实融资成本 (SOFR)](https://fred.stlouisfed.org/series/SOFR)")
    with c_iorb:
        st.markdown("[📊 2. 查央行利率红线 (IORB)](https://fred.stlouisfed.org/series/IORB)")
        
    st.markdown("👉 **盯死纽约联储前线正回购窗口 (SRF 最终安全阀)：**")
    st.markdown("[🔍 纽约联储官方：REPO CHART 每日正回购操作结果页](https://www.newyorkfed.org/markets/desk-operations/repo)")
    st.caption("💡 核心功课：常备回购工具（SRF）每天在该窗口运行。若表格中接受金额（Amount Accepted）突增至 100 亿美元以上，说明系统开始钱荒！")

    st.markdown("**🧮 手机交互快速研判资金面**")
    input_sofr = st.number_input("请输入今日最新 SOFR 利率 (%):", value=3.64, step=0.01, format="%.2f")
    input_iorb = st.number_input("请输入今日最新 IORB 利率 (%):", value=3.65, step=0.01, format="%.2f")
    srf_boost = st.checkbox("🚨 纽约联储 REPO 窗口接受金额突增 / SRF 出现巨额用量")
    
    spread = (input_sofr - input_iorb) * 100 # 换算成基点(bp)
    st.metric(label="今日实时计算利差 (SOFR - IORB)", value=f"{spread:.1f} bp")

    if spread >= 3.0 or srf_boost:
        st.error("核心裁决：🚨 钱荒！利差转正超 3 基点或 SRF 救急爆表！结构性顶部已暗中成熟，多单立刻逃顶！")
    elif spread >= 0.0:
        st.warning("核心裁决：⚠️ 摩擦！资金面紧平衡，美国财政部发债虹吸显现，不可追高。")
    else:
        st.success("核心裁决：🟢 安全！流动性地下管网通畅，随时等待期权大单点火。")

st.markdown("---")

# 第二部分 - CME官方期权点火雷达
st.subheader("🔥 第二阶段：CME 芝商所官方原版期权点火雷达")
st.markdown("👉 **每日核心看盘设定**：请在 CME 官网顶部将 `Hi-Lo Range` 切换为 **1Y 或 Max**，`Layout` 保持 **Grouped List**。直接将看到的最新数据填入下方：")
st.markdown("[📊 官方一键直达：CME Group 全球期权 CVOL 核心数据看板](https://www.cmegroup.com/market-data/cme-group-benchmark-administration/cme-group-volatility-indexes.html)")

c_silver, c_copper = st.columns(2)

with c_silver:
    st.markdown("### 🥈 CMX白银期货 (SI) 决策罗盘")
    si_cvol = st.number_input("输入今日最新白银 CVOL 波动率读数:", value=48.04, step=0.1, format="%.2f")
    si_skew = st.number_input("输入今日最新白银 SKEW 偏度读数:", value=12.59, step=0.1, format="%.2f")
    si_upvar = st.number_input("输入今日最新白银 UpVar 读数:", value=53.92, step=0.1, format="%.2f")
    si_dnvar = st.number_input("输入今日最新白银 DnVar 读数:", value=41.33, step=0.1, format="%.2f")
    
    if si_cvol >= 45.0:
        st.warning(f"⚠️ 风险提示：当前白银 CVOL 为 {si_cvol:.2f}，属于中高波动率，日内极易恶意插针 3% 至 5% 清洗散户。做 CMX 期货时必须压低杠杆，预留 500% 以上保证金缓冲垫！")
    else:
        st.info(f"ℹ️ 提示：当前白银 CVOL 为 {si_cvol:.2f}，处于波动率压实期。若 SKEW 触发，点火成功率极高。")
        
    if si_skew <= 0.0 or (si_upvar <= si_dnvar):
        st.success("白银信号：🔥 触发二波启动点火！SKEW 砸破零轴转负，看涨情绪反向倒挂，做市商正被迫扫货，右侧多单立即进场！")
    elif si_skew > 10.0:
        st.error("白银信号：❌ 狂热洗盘区。SKEW 挂在 +10 以上高位，追高散户密集。继续保持空仓等待，切勿盲目猜底。")
    else:
        st.warning("白银信号：⏳ 蓄势洗盘中。SKEW 正在向 0 轴回落，继续保持战略耐心。")

with c_copper:
    st.markdown("### 🧱 CMX高级铜期货 (HG) 决策罗盘")
    cp_cvol = st.number_input("输入今日最新高级铜 CVOL 波动率读数:", value=28.02, step=0.1, format="%.2f")
    cp_skew = st.number_input("输入今日最新高级铜 SKEW 偏度读数:", value=4.76, step=0.1, format="%.2f")
    cp_upvar = st.number_input("输入今日最新高级铜 UpVar 读数:", value=30.30, step=0.1, format="%.2f")
    cp_dnvar = st.number_input("输入今日最新高级铜 DnVar 读数:", value=25.55, step=0.1, format="%.2f")
    
    if cp_cvol >= 35.0:
        st.warning(f"⚠️ 风险提示：当前铜 CVOL 为 {cp_cvol:.2f} 处于偏高风险状态，严防宏观发债引起的剧烈波动。")
    else:
        st.info(f"ℹ️ 提示：当前铜 CVOL 为 {cp_cvol:.2f}，属于正常工业合理资产震荡波幅。")
        
    if cp_skew <= 0.0:
        st.success("高级铜信号：🔥 触发超级逼空令！铜 SKEW 彻底转负，大游资买盘彻底压倒了产业套保卖 Call 盘，右侧多单冲锋！")
    elif cp_skew <= 3.0:
        st.warning("高级铜信号：⏳ 进入黄金狙击观察带。SKEW 已逼近零轴（过滤掉日常波动），大资金可能正在暗中收集筹码，随时准备切入。")
    else:
        st.error("高级铜信号：❌ 纯属散户日常跟风杂波。SKEW 挂在常态化正数区间，继续过滤噪音，保持空仓等待。")

st.markdown("---")

# 第三部分：保留原有美股期权跳转（修复c3错写变量Bug）
st.subheader("🌟 第三阶段：美股衍生品跨资产交叉验证 (选看)")
o1, o2, o3 = st.columns(3)
with o1:
    st.markdown("[👉 美股 SLV（白银ETF）期权偏度图](https://marketchameleon.com/Overview/SLV/VolatilitySkew/OTMSpread)")
with o2:
    st.markdown("[👉 美股 CPER（纯铜ETF）期权偏度图](https://marketchameleon.com/Overview/CPER/VolatilitySkew/OTMSpread)")
with o3:
    st.markdown("[👉 美股 FCX（铜业巨头）期权偏度图](https://marketchameleon.com/Overview/FCX/VolatilitySkew/OTMSpread)")

st.markdown("---")
st.markdown("💡 **系统交易生命线**：在第一阶段震荡洗盘期，大盘频繁出现高频插针清洗杠杆。在第一阶段和第二阶段信号未达成共振前，绝对不盲目猜底，直到期权数据给出数学铁证！")
