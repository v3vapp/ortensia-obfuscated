## Genetic Backtest and Auto-Pilot Trading Algorithm 
__This repository is a mock.__
### Data Flow Diagram
<img src="https://github.com/v3vapp/storage/blob/main/img/ortensia_data_flow2.png" width="100%" height="100%">  

## Blue Print

### Strategy Logic Provider ๐
This API provides a consistent trading strategy logic for the backtest engine and trading system by handling post requests. By using the same logic, the backtest engine and trading system will operate under the same conditions.    
  
ใใใฏใในใใจใใฌใผใใฃใณใฐใทในใใ ใใ่ฆๆฑใใใๅฃฒ่ฒทใญใธใใฏใๆไพใใพใใ

### Backtest Engine ๐งฌ
This algorithm runs genetic backtesting using the submitted strategy, and parameters and returns the most profitable parameter set. The results are stored in a central database or storage, such as Supabase or Google Cloud Storage (GCS), and can also be used to start trading by sending a post request to the Trading Algo API.   
  
็ทๅฝใใใใฏใในใใๆ็ณปๅใซๆฒฟใฃใฆ้บไผ็ใซๅฎ่กใใๆใๅชใใใใฉใกใผใฟใผใ็ฎๅบใใพใใ

### Order System ๐ฑ
This algorithm runs automatic trading based on the submitted strategy and parameters. It stores the parameters in the database, starts a trading session, and manages multiple processes and trading information. The trading system is complex, and further changes to the structure may be necessary.   
  
ใใใฏใในใใซใใฃใฆ็ฎๅบใใใใญใธใใฏใฎใใฉใกใผใฟใผใซๅบใฅใใฆใๅๅผใๅฎ่กใใพใใ็ฎๅบใใใๆๅนๆ้ใ่ถ้ใใใใๆณๅฎๅคใฎๆๅคฑใๅบใใจๅผทๅถ็ตไบใใพใใ

### Account Manager ๐ถ
This service collects account data from all exchanges and bank accounts, such as trading history, balance/profit and loss, and position information, and stores it in a central location. 
    
ๅฎๆ็ใซๅๅผๆใใใขใซใฆใณใๆๅ ฑใๅๅพใใไฟๅญใใพใใ

### Centralized Database ๐
This stores all backtest results, trading data, active session information, account balance data, exception data, and backups.  
  
ใใใฏใในใ็ตๆใปๅๅผๆๅ ฑใปๅฃๅบงๆๅ ฑใชใฉใฎใใฌใผใใทในใใ ใซ้ขใใใใผใฟใๅจใฆไธ็ฎๆใซ้ใไฟ็ฎกใใพใใ

### Interface ๐ฎ

This provides a centralized control and monitoring interface for all the services.  
  
ใใใฏใในใใฎๆกไปถๆ็คบใป่ชๅใใฌใผใใฎๅถๅพกใปๅฃๅบงๆๅ ฑใฎ็ฎ่ฆใชใฉใใทในใใ ๅจไฝใฎๆไฝใใขใใฟใชใณใฐใ่กใใฆใผใถใผใคใณใฟใผใใงใคในใงใใ


