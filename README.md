個人財務管理系統 (Personal Finance System)
此專案為一個使用 Python + Streamlit 開發的個人財務管理系統，旨在提供使用者一個私密、安全且具備視覺化分析功能的理財工具。

專案亮點（Key Features）
本系統完全符合「程式設計概念與方法」專案需求，包含以下核心功能：

使用者驗證系統：實作帳號註冊與登入功能，使用 SHA-256 加密技術確保使用者密碼安全。

收支分類管理：允許使用者輸入每日收支，並提供預設類別（食、衣、住、行、育、樂、薪資、獎助金等）。

資料持久化儲存：使用 SQLite 資料庫 儲存交易紀錄與個人設定，即使關閉網頁或重啟程式，資料也不會遺失。

財務目標追蹤：使用者可設定每月儲蓄目標，系統會自動計算目前進度並以進度條（Progress Bar）呈現。

視覺化報表：

圓餅圖：分析各類別支出佔比。

互動式長條圖：追蹤每日收支趨勢。

智慧分析與建議：系統會根據使用者的收支比率，自動給予財務狀況評估與消費建議。

技術棧（Tech Stack）
Language: Python 3.9+

Web Framework: Streamlit

Data Processing: Pandas

Visualization: Plotly Express

Database: SQLite (內建於 Python)

Security: Hashlib (SHA-256 加密)

安裝與啟動指南
Windows 環境
安裝 Python: 確保已安裝 Python 並勾選 Add Python to PATH。

建立虛擬環境:

PowerShell

python -m venv venv
.\venv\Scripts\Activate.ps1
安裝套件:

PowerShell

pip install streamlit pandas plotly
啟動系統:

PowerShell

streamlit run main.py
資料庫結構說明 (Database Schema)
本專案包含三個核心資料表：

users: 儲存使用者帳號與加密密碼。

transactions: 儲存每筆收入與支出的詳細資料。

goals: 儲存每個使用者設定的每月儲蓄目標。

版本紀錄（Changelog）
v1.0.0 (當前版本)
完成 SQLite 資料庫串接，支援多使用者資料隔離。

實作 Plotly 互動式圖表。

修正進度條數值超出範圍導致的錯誤 (Clamping logic)。

新增登入登出邏輯。
