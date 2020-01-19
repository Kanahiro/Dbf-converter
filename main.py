import os, sys, csv, shapefile, io
from constants import Constants as CONSTANTS

def convert_dbf_to_list(dbffile):
	records = []

	#Able to read Any type of encoding
	for codec in CONSTANTS.CODECS:
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
	#when argv include no files
	if len(sys.argv) == 1:
		print("No files are included in your argument.")

	else:
		files = sys.argv[1:]

		for fl in files:
			#read dbf as binary
			dbf_file = open(fl, "rb")
			dbf = dbf_file.read()
			dbf_file.close()
			filename = os.path.basename(fl)

			#write .csv in same directory with .dbf
			with open(filename[:-4] + '.csv','w') as f:
				csv_writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL, lineterminator="\n")
				records = convert_dbf_to_list(dbf)
				for record in records:
					csv_writer.writerow(record)

			print(filename[:-4] + '.csv was wroted.')

		print("All files were wroted.")