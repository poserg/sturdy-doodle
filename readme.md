Download all tickers
for i in `cat ../tickers.txt `                                                                                                                  ░▒▓ ✔  took 3m 51s  
do
wget https://mfd.ru/export/handler.ashx/mfdexport_1month_17102006_17102022.txt\?TickerGroup\=11\&Tickers\=$i\&Alias\=false\&Period\=9\&timeframeValue\=1\&timeframeDatePart\=day\&StartDate\=17.10.2006\&EndDate\=17.10.2022\&SaveFormat\=0\&SaveMode\=0\&FileName\=mfdexport_1month_$i.txt\&FieldSeparator\=%3b\&DecimalSeparator\=.\&DateFormat\=yyyyMMdd\&TimeFormat\=HHmmss\&DateFormatCustom\=\&TimeFormatCustom\=\&AddHeader\=true\&RecordFormat\=2\&Fill\=false
done

