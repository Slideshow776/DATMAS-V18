import csv

trafikkregistreringsstasjonsett = ['rådata\_stavanger.csv',
                                    'rådata\_oslo.csv',
                                    'rådata\_bergen.csv',
                                    'rådata\_norge.csv']

# Read CSV file
with open(trafikkregistreringsstasjonsett[3], 'r') as fp:
    reader = csv.reader(fp, delimiter=',')
    next(reader, None)  # skip the headers
    data_read = [row for row in reader]

# Print data in right format
for data in data_read:
    print(data[0].split(';')[5].strip('"'))