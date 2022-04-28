To calcualte the OSD sheets of ZM format:
	* Execute the query given in osd_query.txt file but change the ccc_code accordingly
	* Save the output in file in C:\Python34\zm_format\master.csv
	* Execute the query given in billing_query.txt file but change the ccc_code accordingly.
	* Save the output in file in C:\Python34\zm_format\billing.csv
	* Execute the query given in osd2.txt file but change the ccc_code accordingly
	* Save the output in file in C:\Python34\zm_format\osd2.csv
	* update the ccc.txt file with your desired ccc codes.
	* Execute the zm_osd.py 
	* check the output in <todays_date>-zm-osd.xlsx file