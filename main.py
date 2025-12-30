import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime
import hashlib

# --- 1. 資料庫基礎設定 ---
def init_db():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    # 建立交易紀錄表
    c.execute('''CREATE TABLE IF NOT EXISTS transactions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, date TEXT, type TEXT, category TEXT, amount REAL)''')
    # 建立使用者目標表
    c.execute('''CREATE TABLE IF NOT EXISTS goals 
                 (user TEXT PRIMARY KEY, monthly_goal REAL)''')
    # 建立簡單使用者表 (密碼以 Hash 儲存)
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# --- 2. 系統配置 ---
st.set_page_config(page_title="個人財務管理系統", layout="wide")
init_db()

# --- 3. 登入邏輯 ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.title("🔐 歡迎使用財務管理系統")
    menu = ["登入", "註冊"]
    choice = st.sidebar.selectbox("選單", menu)

    if choice == "註冊":
        new_user = st.text_input("使用者名稱")
        new_pw = st.text_input("密碼", type='password')
        if st.button("註冊"):
            conn = sqlite3.connect('finance.db')
            c = conn.cursor()
            try:
                c.execute('INSERT INTO users VALUES (?,?)', (new_user, make_hashes(new_pw)))
                conn.commit()
                st.success("帳號建立成功！請切換至登入。")
            except:
                st.error("此名稱已被註冊。")
            conn.close()

    else:
        username = st.sidebar.text_input("使用者名稱")
        password = st.sidebar.text_input("密碼", type='password')
        if st.sidebar.button("登入"):
            conn = sqlite3.connect('finance.db')
            c = conn.cursor()
            c.execute('SELECT password FROM users WHERE username =?', (username,))
            data = c.fetchone()
            conn.close()
            if data and check_hashes(password, data[0]):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("帳號或密碼錯誤")
    st.stop()

# --- 4. 登入後的內容 ---
st.title(f"💰 {st.session_state.username} 的個人財務看板")

# 登出按鈕
if st.sidebar.button("登出"):
    st.session_state.logged_in = False
    st.rerun()

# --- 5. 資料庫讀取功能 ---
def get_data(user):
    conn = sqlite3.connect('finance.db')
    df = pd.read_sql_query("SELECT * FROM transactions WHERE user=?", conn, params=(user,))
    conn.close()
    return df

def save_goal(user, goal):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO goals (user, monthly_goal) VALUES (?,?)', (user, goal))
    conn.commit()
    conn.close()

def get_goal(user):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('SELECT monthly_goal FROM goals WHERE user=?', (user,))
    data = c.fetchone()
    conn.close()
    return data[0] if data else 10000.0

# --- 6. 介面佈局 ---
tab1, tab2, tab3 = st.tabs(["📝 收支記錄", "📊 分析報表", "🎯 財務目標"])

with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("新增紀錄")
        date = st.date_input("日期", datetime.now())
        t_type = st.selectbox("類型", ["支出", "收入"])
        if t_type == "支出":
            cat = st.selectbox("類別", ["食", "衣", "住", "行", "育", "樂", "其他"])
        else:
            cat = st.selectbox("類別", ["獎助金", "薪資", "投資", "其他"])
        amount = st.number_input("金額", min_value=0.0, step=10.0)
        
        if st.button("確認新增"):
            conn = sqlite3.connect('finance.db')
            c = conn.cursor()
            c.execute('INSERT INTO transactions (user, date, type, category, amount) VALUES (?,?,?,?,?)',
                      (st.session_state.username, date.strftime('%Y-%m-%d'), t_type, cat, amount))
            conn.commit()
            conn.close()
            st.success("紀錄已儲存！")
            st.rerun()

    with col2:
        st.subheader("最近的紀錄")
        df = get_data(st.session_state.username)
        if not df.empty:
            st.dataframe(df.sort_values('date', ascending=False), use_container_width=True)
            if st.button("清除所有歷史紀錄 (危險)"):
                conn = sqlite3.connect('finance.db')
                c = conn.cursor()
                c.execute('DELETE FROM transactions WHERE user=?', (st.session_state.username,))
                conn.commit()
                conn.close()
                st.rerun()

with tab2:
    st.subheader("財務視覺化分析")
    df = get_data(st.session_state.username)
    if not df.empty:
        # 計算總覽
        income = df[df['type'] == '收入']['amount'].sum()
        expense = df[df['type'] == '支出']['amount'].sum()
        savings = income - expense
        
        c1, c2, c3 = st.columns(3)
        c1.metric("本月總收入", f"${income:,.0f}")
        c2.metric("本月總支出", f"${expense:,.0f}")
        c3.metric("本月淨儲蓄", f"${savings:,.0f}")

        # 圖表展示
        col_fig1, col_fig2 = st.columns(2)
        with col_fig1:
            exp_df = df[df['type'] == '支出']
            if not exp_df.empty:
                fig_pie = px.pie(exp_df, values='amount', names='category', title="支出類別分佈")
                st.plotly_chart(fig_pie)
        
        with col_fig2:
            fig_bar = px.bar(df, x='date', y='amount', color='type', title="每日收支趨勢", barmode='group')
            st.plotly_chart(fig_bar)

        # 建議分析
        st.divider()
        st.subheader("💡 財務建議")
        if savings < 0:
            st.error("⚠️ 您目前處於入不敷出的狀態！建議檢視「樂」或「衣」類別是否過高。")
        elif expense > (income * 0.8):
            st.warning("🧐 支出已超過收入的 80%，建議增加儲蓄比例。")
        else:
            st.success("✅ 財務狀況良好，繼續保持！")
    else:
        st.info("尚無資料可供分析。")

with tab3:
    st.subheader("財務目標進度")
    user_goal = get_goal(st.session_state.username)
    new_goal = st.number_input("設定每月儲蓄目標", value=user_goal)
    if st.button("更新目標"):
        save_goal(st.session_state.username, new_goal)
        st.success("目標已更新！")
    
    df = get_data(st.session_state.username)
    income = df[df['type'] == '收入']['amount'].sum()
    expense = df[df['type'] == '支出']['amount'].sum()
    actual_savings = income - expense
    
    # 修正進度條 Bug (範圍 0.0 ~ 1.0)
    progress_val = max(0.0, min(actual_savings / new_goal, 1.0)) if new_goal > 0 else 0.0
    st.write(f"當前儲蓄進度: {actual_savings:,.0f} / {new_goal:,.0f}")
    st.progress(progress_val)