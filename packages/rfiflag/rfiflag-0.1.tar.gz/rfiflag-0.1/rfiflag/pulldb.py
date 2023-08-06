import pandas as pd
import psycopg2 as pg


def extractDB(password, output):
	''' Extract RFI DB into CSV to be used in dataframes. Password from A. Erickson'''

	# Connection info
	connection = pg.connect(user="rfi_ro", password=password, host="sssproddb", dbname="rfi")

	# SQL Query
	sql = ('''
		SELECT * FROM features_peak AS fp
		JOIN observations AS o ON fp.observation=o.id
		JOIN evla_rf_observations AS eo ON eo.observation=o.id
		'''
		)

	# Read and save to csv to be used in pandas dataframe
	data = pd.read_sql_query(sql, connection)
	data.to_csv(output)

	# Close connection
	connection.close()

	# Load csv into dataframe with correct time formatting
	df = pd.read_csv(output, parse_dates=[10], date_parser=lambda col: pd.to_datetime(col, utc=True))
	return df
