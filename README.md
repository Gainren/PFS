#Project Archived

此專案為一個使用 Python + Streamlit 開發的個人財務管理系統，主要作為學習與原型驗證用途。
目前已由更新的系統架構與實作方式取代，因此不再進行功能開發與維護。

專案仍可正常執行，並適合作為以下用途的參考範例：

Streamlit 介面設計

使用 st.session_state 管理狀態

基本財務資料分析與視覺化

Plotly 圖表整合

專案說明（Description）

本系統為一套簡易的 個人財務管理系統，提供使用者記錄收入與支出、分析消費結構，並追蹤每月儲蓄目標。

主要功能包含：

收入 / 支出資料輸入

支出類別分析

圓餅圖視覺化支出比例

每月儲蓄目標設定與進度追蹤

本專案採用 記憶體暫存資料（st.session_state），不使用資料庫，適合課堂作業與展示用途。

相關連結（Links）

Streamlit 官方文件
https://docs.streamlit.io/

Plotly Express 官方文件
https://plotly.com/python/plotly-express/

Pandas 官方文件
https://pandas.pydata.org/docs/

Linux / macOS 安裝方式

請先確認已安裝 Python 3.9 以上版本。

安裝必要套件：

pip install streamlit pandas plotly


進入專案目錄後執行：

streamlit run app.py

Windows 安裝方式

至官方網站下載並安裝 Python
https://www.python.org/downloads/

（安裝時請務必勾選 Add Python to PATH）

開啟「命令提示字元（CMD）」

安裝套件：

pip install streamlit pandas plotly


啟動系統：

streamlit run app.py

系統啟動方式（How to Launch）

在專案目錄中輸入：

streamlit run app.py


啟動後瀏覽器會自動開啟：

http://localhost:8501/

資料儲存說明（Data Storage）

本專案使用 st.session_state 進行資料暫存。

注意事項：

重新整理頁面後資料將會遺失

不需設定資料庫

適合展示、學習與短期測試

建議未來可擴充為：

SQLite

CSV 檔案儲存

MongoDB / Firebase

相依套件（Dependencies）

https://www.python.org/
 — 主要程式語言

https://pypi.org/project/streamlit/
 — Web 介面框架

https://pypi.org/project/pandas/
 — 資料處理

https://pypi.org/project/plotly/
 — 資料視覺化

https://docs.python.org/3/library/datetime.html
 — 日期時間處理

版本紀錄（Changelog）
0.3.0

新增每月儲蓄目標設定

新增目標達成進度條

新增依消費狀況給予建議提示

0.2.0

新增支出類別圓餅圖

新增收入與支出總覽指標

改善介面配置與分頁結構

0.1.0

初始版本

基本收支輸入功能

使用 Session State 管理資料

Streamlit 多分頁介面
