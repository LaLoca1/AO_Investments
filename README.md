# AO Investments Application
AO Investments is a web application that allows users to create a stock and crypto portfolio to keep track of their investments. I coded this for my dissertation in my final year of university. 
* Front-End: React
* Back-End: Django (Python)
* Database: Postgresql
<img src="screenshots/StockPortfolio.PNG" width="500">

# Table of Contents
- [Introduction](https://github.com/LaLoca1/AO_Investments#Introduction)
- [Features](https://github.com/LaLoca1/AO_Investments#Features)
- [How it Works](https://github.com/LaLoca1/AO_Investments#Installation)
- [Credits](https://github.com/LaLoca1/AO_Investments#Credit)
- [Screenshots](https://github.com/LaLoca1/AO_Investments#Screenshots)

# Introduction
AO Investments allows users to keep track of any investment they make in stocks or crypto, they are able to monitor potential or current performance and gain different insights. Users have a choice of over 1500+ equities from 10 different countries.

# Features
Features include: 
* Time-series Performance charts 
* Stock Portfolio include any dividend or stock splits that has occured and will update any data based on this.
* Perform CRUD operations on their portfolios
* Statistical graphics to help visualise portfolio exposure.

These are shown in the screenshots folder in the repo. 

# How it Works
After Registration and logging in, A user can create a stock or crypto portfolio. The user can then start adding securities to the portfolio and enter the economics of the trade. The site will then display the various features based on the information entered by the user. If the security does not yet have a prices stored in the database, an api call will be made to Alpha Vantage and the last 100 End of Day (EOD) prices will be stored to the database. EOD prices are updated before midnight on every weekday.

# Screenshots
<img src="screenshots/StockBreakdown.PNG" width="500">
<img src="screenshots/StockChart.PNG" width="500">