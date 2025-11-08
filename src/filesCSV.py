import csv
import re

class FilesCSV:
    def read_csv(self, filename):
                if(filename == ""):
                    print("Filename is empty")
                    return None

                try:
                    data = []
                    header = None
                    WRAP_RX = re.compile(r'(\[.*?\])')

                    with open(filename, "r", newline="") as csvfile:
                        lines = (
                            WRAP_RX.sub(r'"\1"', raw)
                            for raw in csvfile
                            if raw.strip() and not raw.lstrip().startswith("#")
                        )
                        reader = csv.reader(lines)
                        for row in reader:
                            if row and row[0].startswith("#"):
                                continue

                            if header is None:
                                header = row
                            else:
                                if(len(row) != len(header)):
                                    print(f"Row length mismatch: {len(row)} != {len(header)}")
                                    return None
                                data.append(row)

                    return {"header": header, "data": data}
                except Exception as e:
                    print(f"Error reading CSV file: {str(e)}")
                    return None
                
    def write_csv(self, filename, data):
         if filename == "":
            print("Filename is empty")
            return None
         
         try:
            with open(filename, mode= 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data["header"])
                for row in data["data"]:
                    writer.writerow(row)
                return True
         except Exception as e:
            print(f"Error writing CSV file: {str(e)}")
            return None

