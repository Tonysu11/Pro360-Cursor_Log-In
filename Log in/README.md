# Pro360 Login Automation Test

這是一個用於測試 Pro360 網站登入功能的自動化測試腳本。

## 環境需求

- Python 3.7+
- Chrome 瀏覽器
- pip（Python包管理器）

## 安裝步驟

1. 安裝所需的Python套件：
```bash
pip install -r requirements.txt
```

2. 確保你的系統已安裝最新版本的Chrome瀏覽器。

3. 設置環境變數：
   - 複製 `.env.example` 文件為 `.env`
   - 在 `.env` 文件中填入您的登入憑證：
     ```
     EMAIL=your-email@example.com
     PASSWORD=your-password
     BASE_URL=https://staging.pro360.com.tw
     ```

## 執行測試

運行以下命令來執行測試：
```bash
python test_pro360_login.py
```

## 測試說明

這個測試腳本會：
1. 啟動Chrome瀏覽器
2. 訪問Pro360測試網站
3. 使用環境變數中的帳號密碼進行登入
4. 驗證登入狀態
5. 自動關閉瀏覽器

## 安全性說明

- **重要**：`.env` 文件包含敏感資訊，已被加入 `.gitignore` 確保不會被提交到版本控制
- 登入憑證從環境變數讀取，避免在程式碼中暴露敏感資訊
- 可以安全地將專案推送到 GitHub，不會洩露帳號密碼

## 注意事項

- 測試執行過程中會打開Chrome瀏覽器
- 如果需要無頭模式（不顯示瀏覽器界面），可以在代碼中取消註釋 `--headless` 選項
- 確保在 `.env` 文件中提供有效的登入憑證
