import csv
from parser import Parser
from filesCSV import FilesCSV

class Interpreter:
    """
    The Interpreter class runs parsed commands and manages in-memory tables read from CSV files.
    Attributes:
        parser (Parser): The YACC parser for interpreting CQL commands.
        filesCSV (FilesCSV): Utility for reading and writing CSV files.
        tablesData (dict): In-memory storage of tables keyed by table name.
        filePath (str): Default directory path for CSV files.
    """
    def __init__(self):
        """
        Initialize the Interpreter with a Parser, FilesCSV utility,
        and empty tablesData storage.
        """
        self.parser = Parser()
        self.filesCSV = FilesCSV()
        self.tablesData = {}
        self.filePath = "data/"
        self.exportPath = "output/"
        self.procedures = {}

    def run(self, data, is_test):
        """
        Parse and execute a block of CQL commands.
        Args:
            data (str): The raw CQL commands string to run.
        Returns:
            None
        """
        result = self.parser.parse(data)
        if result is None:
            print("No result from parser")
            return None
        for cmd in result:
            if(is_test == True):
                return self.execute(cmd, is_test)
            else:
                self.execute(cmd, is_test)

    def execute(self, command, is_test):
        """
        Dispatch and execute a single parsed command tuple.
        Args:
            command (tuple): Parsed command in the form (CMD_TYPE, ...).
        Returns:
            None
        """
        cmd = command[0]
        if cmd == "IMPORT":
            x = self.import_table(command[1], command[2])
            if is_test == False: print(x)
            return x
        elif cmd == "EXPORT":
            x = self.export_table(command[1], command[2])
            if is_test == False: print(x)
            return x
        elif cmd == "RENAME":
            x = self.rename_table(command[1], command[2])
            if is_test == False: print(x)
            return x
        elif cmd == "PRINT":
            x = self.print_table(command[1])
            if is_test == False: print(x)
            return x
        elif cmd == "DISCARD":
            x = self.discard_table(command[1])
            if is_test == False: print(x)
            return x
        elif cmd == "SELECT_NO_LIMIT":
            x = self.select_table(command[1], 0)
            if is_test == False: print(x)
            return x
        elif cmd == "SELECT_LIMIT":
            x = self.select_table(command[1], command[2])
            if is_test == False: print(x)
            return x
        elif cmd == "SELECT_SPECIFIC_NO_LIMIT":
            x = self.select_specific(command[2], command[1], 0)
            if is_test == False: print(x)
            return x
        elif cmd == "SELECT_SPECIFIC_LIMIT":
            x = self.select_specific(command[2], command[1], command[3])
            if is_test == False: print(x)
            return x
        elif cmd == "SELECT_WHERE_NO_LIMIT":
            x = self.select_where(command[1], command[2], 0)
            if is_test == False: print(x)
            return x
        elif cmd == "SELECT_WHERE_LIMIT":
            x = self.select_where(command[1], command[2], command[3])
            if is_test == False: print(x)
            return x
        elif cmd == "CREATE_TABLE_SELECT_NO_LIMIT":
            x = self.create_table_select(command[1], command[2], 0)
            if is_test == False: print(x)
            return x
        elif cmd == "CREATE_TABLE_SELECT_LIMIT":
            x = self.create_table_select(command[1], command[2], command[3])
            if is_test == False: print(x)
            return x
        elif cmd == "CREATE_TABLE_SELECT_WHERE_NO_LIMIT":
            x = self.create_table_select_where(command[1],command[2], command[3], 0)
            if is_test == False: print(x)
            return x
        elif cmd == "CREATE_TABLE_SELECT_WHERE_LIMIT":
            x = self.create_table_select_where(command[1], command[2], command[3], command[4])
            if is_test == False: print(x)
            return x
        elif cmd == "PROCEDURE":
            x = self.store_procedure(command[1], command[2])
            if is_test == False: print(x)
            return x
        elif cmd == "CREATE_TABLE_FROM_JOIN":
            x = self.create_table_from_join(command[1], command[2], command[3], command[4])
            if is_test == False: print(x)
            return x
        elif cmd == "CALL":
            x = self.call_procedure(command[1])
            if is_test == False: print(x)
            return x

    def import_table(self, table_name, filename):
        """
        Import a CSV file into memory as a table.
        Args:
            table_name (str): Name to assign to the imported table.
            filename (str): CSV filename to read (relative to filePath).
        Returns:
            str: Result
        """
        data = self.filesCSV.read_csv(self.filePath + filename)
        if data:
            self.tablesData[table_name] = data
            return f"Table '{table_name}' imported successfully"
        else:
            return f"Table {table_name} was not imported"

    def export_table(self, table_name, filename):
        """
        Export an in-memory table to a CSV file.
        Args:
            table_name (str): Name of the table to export.
            filename (str): Destination CSV filename.
        Returns:
            str: Result
        """
        if table_name not in self.tablesData:
            return f"Table {table_name} does not exist."
        
        result = self.filesCSV.write_csv(self.exportPath + filename, self.tablesData[table_name])
        if(result):
            return f"Table '{table_name}' exported successfully"
        else:
            return f"Table '{table_name}' was not exported successfully"


    def rename_table(self, table_name, new_name):
        """
        Rename a table stored in memory.
        Args:
            table_name (str): Current name of the table.
            new_name (str): New name for the table.
        Returns:
            str: Result
        """
        if table_name in self.tablesData:
            self.tablesData[new_name] = self.tablesData.pop(table_name)
            return(f"Table {table_name} renamed to {new_name}.")
        else:
            return(f"Table {table_name} does not exist.")

    def print_table(self, table_name):
        """
        Print the contents of a table.
        Args:
            table_name (str): Name of the table to print.
        Returns:
            str: Result
        """
        print(f"Table {table_name}:")
        if table_name in self.tablesData:
            
            data = self.tablesData[table_name]
            header = data.get("header")
            rows = data.get("data")
            print(header)
            for row in rows:
                print(row)
            return(f"Table {table_name} was printed.")
        else:
            return(f"Table {table_name} was not printed.")

    def discard_table(self, table_name):
        """
        Remove a table from memory.
        Args:
            table_name (str): Name of the table to discard.
        Returns:
            str: Result
        """
        if table_name in self.tablesData:
            self.tablesData.pop(table_name)
            return(f"Table {table_name} was discarded.")
        else:
            return(f"Table {table_name} not found.")

    def select_table(self, table_name, limit):
        """
        Print all rows (up to optional limit) of a table.
        Args:
            table_name (str): Name of the table to select from.
            limit (int, optional): Maximum number of rows to display.
        Returns:
            dict: A dictionary with keys 'header' (list of column names) and
                'data' (list of rows), or None if invalid.
        """
        if not table_name:
                print("Table name is empty")
                return None
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return None

        selectedTable = self.get_table_data(table_name, limit)
        if selectedTable is None:
            return(f"Table {table_name} not found.")

        header = selectedTable.get("header")
        data = selectedTable.get("data")
        self.print_data(header, data)
        return(f"Table {table_name} was selected.")



    def select_specific(self, table_name, columns, limit):
        """
        Return selected rows from a table based on one or more numerical conditions.

        Args:
            table_name (str): Name of the table to query.
            condition (list of tuples): Each tuple describes a filter in the form
                (column_name, operator, value)
            limit (int, optional): Maximum number of rows to scan from the table.

        Returns:
            dict: A dictionary with keys 'header' (list of column names) and
                'data' (list of rows matching all conditions), or None if invalid.
        """
        if not table_name:
            print("Table name is empty")
            return None
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return None

        selectedTable = []
        selectedTable = self.get_table_data_specific(table_name, columns, limit)
        if selectedTable is None:
            return(f"{columns} was not selected from table {table_name}.")

        self.print_data(selectedTable["header"], selectedTable["data"])
        return(f"{columns} was selected from table {table_name}.")

    def select_where(self, table_name, condition, limit):
        if table_name == "":
            return("Table name is empty")
        if table_name not in self.tablesData:
            return(f"Table {table_name} does not exist.")
        selectedTable = []
        selectedTable = self.get_table_data_where(table_name, condition, limit)
        if selectedTable is None:
            return(f"Table {table_name} was not selected with the condition {condition}.")
        
        self.print_data(selectedTable["header"], selectedTable["data"])
        return(f"Table {table_name} was selected with the condition {condition}.")

        
    def create_table_select(self, new_table, table_name, limit):
        if table_name == "":
            print("Table name is empty")
            return None
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return None
        if new_table in self.tablesData:
            print(f"Table {new_table} already exists.")
            return None
        
        newTable = self.get_table_data(table_name, limit)
        if newTable is None:
            return(f"Failed to retrieve data from table {table_name}.")
        self.tablesData[new_table] = newTable
        return(f"Table {new_table} created from {table_name}.")
    
    def create_table_select_where(self, new_table, table_name, condition, limit):
        if table_name == "":
            print("Table name is empty")
            return None
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return None
        if new_table in self.tablesData:
            print(f"Table {new_table} already exists.")
            return None
        newTable = self.get_table_data_where(table_name, condition, limit)
        if newTable is None:
            return(f"Failed to retrieve data from table {table_name}.")
        self.tablesData[new_table] = newTable
        return(f"Table {new_table} created from {table_name} with condition {condition}")


    def store_procedure(self, name, command):
        """
        Create a procedure with the given name and command.
        Args:
            name (str): Name of the procedure.
            command (str): Command to execute when the procedure is called.
        Returns:
            None
        """
        if name in self.procedures:
            return(f"Procedure {name} already exists.")
        if not command:
            return("Command is empty")
        self.procedures[name] = command
        return(f"Procedure '{name}' stored successfully.")

    def call_procedure(self, name):
        """
        Execute a stored procedure by its name.
        Args:
            name (str): Name of the procedure to call.
        Returns:
            None
        """
        if name not in self.procedures:
            return(f"Procedure {name} does not exist.")
        
        for cmd in self.procedures[name]:
            self.execute(cmd, False)
        return(f"Procedure {name} was called.")

    
    def create_table_from_join(self, new_table, table_name1, table_name2, id):
        if table_name1 == "":
            print("Table name is empty")
            return None
        if table_name1 not in self.tablesData:
            print(f"Table {table_name1} does not exist.")
            return None
        if table_name2 == "":
            print("Table name is empty")
            return None
        if table_name2 not in self.tablesData:
            print(f"Table {table_name2} does not exist.")
            return None
        if new_table in self.tablesData:
            print(f"Table {new_table} already exists.")
            return None
        
        data1 = self.tablesData[table_name1]
        data2 = self.tablesData[table_name2]
        header1 = data1.get("header")
        header2 = data2.get("header")

        if id not in header1 or id not in header2:
            print(f"Column {id} does not exist in one of the tables.")
            return None
        
        index1 = header1.index(id)
        index2 = header2.index(id)
        new_header = header1 + [col for col in header2 if col != id]
        new_tableData = []
        for row1 in data1["data"]:
            join_val = row1[index1]
            for row2 in data2["data"]:
                if row2[index2] == join_val:
                    new_row = row1 + [
                        row2[i] for i in range(len(row2)) if header2[i] != id
                    ]
                    new_tableData.append(new_row)
                    
        self.tablesData[new_table] = {"header": new_header, "data": new_tableData}
        print(f"Table {new_table} created from join of {table_name1} and {table_name2} using the column {id}.")

    def print_data(self, header, data):
        """
        Print the contents of a data object.
        Args:
            data (dict): Data object to print.
        Returns:
            None
        """
        print(header)
        for row in data:
            print(row)
    
    
    def get_table_data(self, table_name, limit):
        """
        Retrieves data from an in-memory table, optionally limited to a number of rows.

        Parameters:
            table_name (str): Name of the table to retrieve.
            limit (int): Maximum number of rows to return. If 0, return all rows.

        Returns:
            dict: A array with 'header' and 'data' keys, or a message if the table doesn't exist.
        """
        if not table_name:
            return None
        if table_name not in self.tablesData:
            return None

        selectedTable = []
        data = self.tablesData[table_name]
        dataLimit = int(limit) if limit != 0 else None
        header = data.get("header")
        rows = data.get("data")
        for row in rows[:dataLimit]:
            selectedTable.append(row)
        return {"header": header, "data": selectedTable}

    def get_table_data_specific(self, table_name, columns, limit):
        """
        Return selected rows from a table based on one or more numerical conditions.

        Args:
            table_name (str): Name of the table to query.
            condition (list of tuples): Each tuple describes a filter in the form
                (column_name, operator, value)
            limit (int, optional): Maximum number of rows to scan from the table.

        Returns:
            dict: A dictionary with keys 'header' (list of column names) and
                'data' (list of rows matching all conditions), or None if invalid.
        """
        data = self.tablesData[table_name]
        header = data.get("header")
        rows = data.get("data")

        for col in columns:
            if col not in header:
                return None

        selectedTable = []
        column_indices = [header.index(col) for col in columns]
        dataLimit = int(limit) if limit != 0 else None
        for row in rows[:dataLimit]:
            selected_row = [row[i] for i in column_indices]
            selectedTable.append(selected_row)

        return {"header": columns, "data": selectedTable}

    def get_table_data_where(self, table_name, condition, limit):
        """
        Filters table rows by specified conditions, optionally limited to a number of rows.

        Parameters:
            table_name (str): Name of the table to query.
            conditions (list): List of conditions in the form (CONDITION, column, operator, value).
            limit (int): Max number of rows to consider (0 means no limit).

        Returns:
            dict: A dictionary with 'header' and 'data' keys.
        """
        data = self.tablesData.get(table_name)
        dataLimit = int(limit) if limit != 0 else None
        intermediate = {}

        index = 0
        header = data.get("header")
        rows = data.get("data")
        for c in condition: 
            filtered = []
            for row in rows[:dataLimit]:
                cell = row[header.index(c[1])]
                cond = c[2]
                value = c[3]
                if cond == "=" and cell == value:
                    filtered.append(row)
                elif cond == "!=" and cell != value:
                    filtered.append(row)
                elif cond == "<" and cell < value:
                    filtered.append(row)
                elif cond == ">" and cell > value:
                    filtered.append(row)
                elif cond == "<=" and cell <= value:
                    filtered.append(row)
                elif cond == ">=" and cell >= value:
                    filtered.append(row)
            intermediate[index] = filtered
            index += 1
  
        parsed_data = []
        index = 0
        dictLenght = len(intermediate)
        if(dictLenght != 1):
            for i in intermediate:
                for j in intermediate[i]:
                    if(i+1 > dictLenght):
                        break
                    for k in intermediate[i+1]:
                        if(j[0] == k[0]):
                            parsed_data.append(k)
                break
        else:
            parsed_data = intermediate[0]

        return {"header": header, "data": parsed_data}    