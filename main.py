CODECS = ['cp932','shift_jis','utf-8','shift_jis','euc_jp','cp932',
          'euc_jis_2004','euc_jisx0213',
          'iso2022_jp','iso2022_jp_1','iso2022_jp_2','iso2022_jp_2004','iso2022_jp_3','iso2022_jp_ext',
          'shift_jis_2004','shift_jisx0213',
          'utf_16','utf_16_be','utf_16_le','utf_7','utf_8_sig']

import os, sys, csv, shapefile, io

def convert_dbf_to_list(dbffile):
	records = []

	#Able to read Any type of encoding
	for codec in CODECS:
		try:
			reader = shapefile.Reader(dbf=io.BytesIO(dbffile),encoding=codec)

			record_headers = []
			fields = reader.fields[1:]
			for field in fields:
				record_headers.append(field[0])
			records.append(record_headers)

			for rec in reader.records():
				records.append(rec)
			
			print(codec + 'encoding is correct.' )
			break
			
		except UnicodeDecodeError:
			print(codec + 'is not suitable for this file.')
			continue

	return records

if __name__ == '__main__':
	files = sys.argv
	dbf_datas = []
	for i in range(len(files)):
		if i == 0:
			continue

		#read dbf as binary
		dbf_file = open(files[i], "rb")
		dbf = dbf_file.read()
		dbf_file.close()
		filename = os.path.basename(files[i])

		#write .csv in same directory with .dbf
		with open(filename[:-4] + '.csv','w') as f:
			csv_writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL, lineterminator="\n")
			records = convert_dbf_to_list(dbf)
			for record in records:
				csv_writer.writerow(record)