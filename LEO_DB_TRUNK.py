#   Name: trunk
#   Description: This file is written for the purpose that it can be conneced to other programs
#   Author: Malay Bhavsar
#   Year: 2020
#   Started: 14-09-2020 {This program & its design}
#   Version: 1.0
# Importing the modules.
import os

# Defining the main class.


class leodb:

    def __init__(self, file_name="data", path="./"):
        self.db_file_name = file_name + ".leodb"
        self.db_path = path
        self.temp_index = -1
        self.temp_data = ""

    def __read_file(self, file_name):
        # Read data from the file.
        if os.path.exists(f"{self.db_path}{file_name}"):
            file = open(f"{self.db_path}{file_name}", "r")
            data = file.read()
            file.close()
            return data

    def __write_file(self, file_name, data=""):
        # Write data to the file.
        file = open(f"{self.db_path}{file_name}", "w")
        data = file.write(data)
        file.close()

    def __list_to_string(self, data, join_with=""):
        # This function convert list to string.
        return join_with.join(element for element in data)

    def __string_to_list(self, data, split_with=" "):
        # This function convert string to list.
        data_ls = data.split(split_with)
        return [element.strip() for element in data_ls]

    ### ESSENTIAL FUNCTION ###
    def table(self, table_name, col_ls=[]):
        if self.temp_index != -1:
            self.close()
        self.data = self.__read_file(self.db_file_name)
        if self.data == None:
            self.__write_file(self.db_file_name, "")
            self.data = self.__read_file(self.db_file_name)
        n_data = self.__string_to_list(self.data, "#BREAK$")
        while "" in n_data:
            n_data.pop(n_data.index(""))
        is_exist = False
        for i in range(len(n_data)):
            nn_data = self.__string_to_list(n_data[i], "#TABLENEXT$")
            if nn_data[0] == table_name:
                is_exist = True
                self.temp_data = n_data[i]
                self.temp_index = i
                break
        if is_exist == False:
            if len(col_ls) == 0:
                print(
                    "[ERROR]: PLEASE GIVE A COLUMN NAME LIST FOR ADDITITON OF NEW TABLE.")
            self.__add_table(table_name, col_ls)

    def __add_table(self, table_name, col_ls):
        # If table doesnt exist then this function inserts a table.
        if self.data == None:
            print("[ERROR]: NO SUCH DATABASE FILE FOUND")
        else:
            n_data = self.__string_to_list(self.data, "#BREAK$")
            new_str = table_name + "#TABLENEXT$" + \
                self.__list_to_string(
                    [sub.upper() for sub in col_ls], ",") + "#TABLENEXT$"
            n_data.append(new_str)
            n_data = self.__list_to_string(n_data, "#BREAK$")
            self.data = n_data
            self.__write_file(self.db_file_name, self.data)
            self.table(table_name)

    def close(self):
        n_data = self.__string_to_list(self.data, "#BREAK$")
        while "" in n_data:
            n_data.pop(n_data.index(""))
        n_data[self.temp_index] = self.temp_data
        self.temp_data = ''
        self.temp_index = -1
        self.data = self.__list_to_string(n_data, "#BREAK$")
        self.__write_file(self.db_file_name, self.data)

    ### RECORD FUNCTION ###
    def insert(self, data_ls):
        # This function is used for inserting the record to the table.
        # Processing data given as input.
        in_col_ls = []
        in_data_ls = []
        for i in range(len(data_ls)):
            n_data = self.__string_to_list(data_ls[i], "=")
            in_col_ls.append(n_data[0].upper())
            in_data_ls.append(n_data[1])
        # Processing data from the disk.
        data = self.__string_to_list(self.temp_data, "#TABLENEXT$")
        ds_col_list = self.__string_to_list(data[1], ",")
        ds_data_list = self.__string_to_list(data[2], "#END$")
        while "" in ds_data_list:
            ds_data_list.pop(ds_data_list.index(""))
        # Inserting the data.
        record_ls = []
        for col in ds_col_list:
            if col in in_col_ls:
                record_ls.append(in_data_ls[in_col_ls.index(col)])
            else:
                record_ls.append("NULL")
        record_ls = self.__list_to_string(record_ls, "#NEXT$")
        ds_data_list.append(record_ls)
        data[2] = self.__list_to_string(ds_data_list, "#END$")
        self.temp_data = self.__list_to_string(data, "#TABLENEXT$")

    def search(self, data_ls, option=0):
        # This function is used to Search specific entries form the table.
        # Process the input data.
        in_col_ls = []
        in_data_ls = []
        for i in range(len(data_ls)):
            n_data = self.__string_to_list(data_ls[i], "=")
            in_col_ls.append(n_data[0].upper())
            in_data_ls.append(n_data[1])
        # Processing the data from the disk.
        data = self.__string_to_list(self.temp_data, "#TABLENEXT$")
        ds_col_list = self.__string_to_list(data[1], ",")
        ds_data_list = self.__string_to_list(data[2], "#END$")
        while "" in ds_data_list:
            ds_data_list.pop(ds_data_list.index(""))
        # Generating the output.
        return_ls = []
        for i in range(len(ds_data_list)):
            count = 0
            for col in in_col_ls:
                nn_data = self.__string_to_list(ds_data_list[i], "#NEXT$")
                if col in ds_col_list:
                    if nn_data[ds_col_list.index(col)] == in_data_ls[in_col_ls.index(col)]:
                        count += 1
            if count == len(in_col_ls):
                return_ls.append(ds_data_list[i])
        if option == 1:
            self.search_result = return_ls
        elif option == 0:
            new_return_ls = []
            for record in return_ls:
                new_return_ls.append(self.__string_to_list(record, "#NEXT$"))
            return new_return_ls

    def delete(self, data_ls):
        # Deletes the data from table searched using provided data..
        self.search(data_ls, 1)
        data = self.__string_to_list(self.temp_data, "#TABLENEXT$")
        ds_data_list = self.__string_to_list(data[2], "#END$")
        while "" in ds_data_list:
            ds_data_list.pop(ds_data_list.index(""))
        for value in self.search_result:
            if value in ds_data_list:
                ds_data_list.pop(ds_data_list.index(value))
        data[2] = self.__list_to_string(ds_data_list, "#END$")
        self.temp_data = self.__list_to_string(data, "#TABLENEXT$")

    def update(self, search_ls, value_ls):
        # Search old data and replace the new values with the old once.
        self.search(search_ls, 1)
        # Processing data from values_ls.
        in_col_ls = []
        in_data_ls = []
        for i in range(len(value_ls)):
            n_data = self.__string_to_list(value_ls[i], "=")
            in_col_ls.append(n_data[0].upper())
            in_data_ls.append(n_data[1])
        # Processing data from the disk.
        data = self.__string_to_list(self.temp_data, "#TABLENEXT$")
        ds_col_list = self.__string_to_list(data[1], ",")
        # preparing the new_list.
        n_data = self.__string_to_list(data[2], "#END$")
        for i in range(len(self.search_result)):
            for col in in_col_ls:
                if col in ds_col_list:
                    nn_data = self.__string_to_list(
                        n_data[n_data.index(self.search_result[i])], "#NEXT$")
                    nn_data[ds_col_list.index(
                        col)] = in_data_ls[in_col_ls.index(col)]
                    n_data[n_data.index(self.search_result[i])] = self.__list_to_string(
                        nn_data, "#NEXT$")
        data[2] = self.__list_to_string(n_data, "#END$")
        self.temp_data = self.__list_to_string(data, "#TABLENEXT$")

    # Export & Import functions.
    def export_(self):
        # This function is used for exporting the data to CSV file.
        # Processing the data form the disk.
        data = self.__string_to_list(self.temp_data, "#TABLENEXT$")
        file_name = data[0] + ".csv"
        # columns.
        ds_col_list = data[1]
        # records.
        new_data_ls = []
        ds_data_list = self.__string_to_list(data[2], "#END$")
        while "" in ds_data_list:
            ds_data_list.pop(ds_data_list.index(""))
        for record in ds_data_list:
            n_record = self.__string_to_list(record, "#NEXT$")
            for i in range(len(n_record)):
                if "," in n_record[i]:
                    n_record[i] = f'"{n_record[i]}"'
            n_record = self.__list_to_string(n_record, ",")
            new_data_ls.append(n_record)
        new_data = self.__list_to_string(new_data_ls, "\n")
        # Data to be written in file.
        file_data = ds_col_list + "\n" + new_data
        self.__write_file(file_name, file_data)
