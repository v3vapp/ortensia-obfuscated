## Genetic Backtest and Auto-Pilot Trading Algorithm 
__This repository is a mock.__
### Data Flow Diagram
<img src="https://github.com/v3vapp/storage/blob/main/ortensia_data_flow2.png" width="100%" height="100%">  

## Blue Print

### Strategy Logic Provider 📈
This API provides a consistent trading strategy logic for the backtest engine and trading system by handling post requests. By using the same logic, the backtest engine and trading system will operate under the same conditions.    
  
バックテストとトレーディングシステムから要求された売買ロジックを提供します。

### Backtest Engine 🧬
This algorithm runs genetic backtesting using the submitted strategy, and parameters and returns the most profitable parameter set. The results are stored in a central database or storage, such as Supabase or Google Cloud Storage (GCS), and can also be used to start trading by sending a post request to the Trading Algo API.   
  
総当りバックテストを時系列に沿って遺伝的に実行し、最も優れたパラメーターを算出します。

### Order System 💱
This algorithm runs automatic trading based on the submitted strategy and parameters. It stores the parameters in the database, starts a trading session, and manages multiple processes and trading information. The trading system is complex, and further changes to the structure may be necessary.   
  
バックテストによって算出されたロジックのパラメーターに基づいて、取引を実行します。算出された有効期限を超過するか、想定外の損失が出ると強制終了します。

### Account Manager 🔶
This service collects account data from all exchanges and bank accounts, such as trading history, balance/profit and loss, and position information, and stores it in a central location. 
    
定期的に取引所からアカウント情報を取得し、保存します。

### Centralized Database 🕋
This stores all backtest results, trading data, active session information, account balance data, exception data, and backups.  
  
バックテスト結果・取引情報・口座情報などのトレードシステムに関するデータを全て一箇所に集め保管します。

### Interface 🔮

This provides a centralized control and monitoring interface for all the services.  
  
バックテストの条件指示・自動トレードの制御・口座情報の目視など、システム全体の操作やモニタリングを行うユーザーインターフェイスです。


