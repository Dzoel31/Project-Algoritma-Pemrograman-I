import os
import pandas as pd
from pandas import DataFrame
from prettytable import PrettyTable


class Controller:
    """
    A class that provides methods for controlling data in a database.

    Attributes:
        - _current_path (str): The current path of the file.
        - _data_path (str): The path to the data directory.
        - filename (str): The name of the data file.

    Methods:
        - is_dir_exists(): Check if the data directory exists.
        - is_file_exists(): Check if any files exist in the data directory.
        - is_data_exists(): Check if the data file exists in the data directory.
        - is_data_empty(): Check if the data file is empty.
        - get_data_path(): Get the path to the data directory.
        - create_dir(): Create the data directory if it doesn't exist.
        - create_file(): Create a new file in the data directory.
        - save_data(data: DataFrame | list): Save data to the data file.
        - dataframe_to_list(dataframe: DataFrame): Convert a DataFrame to a list.
        - list_to_dataframe(list_data: list, columns_name: list): Convert a list to a DataFrame.
        - get_data(): Get data from the data file.
        - read_data(): Read data from the data file.
        - delete_data(index: int): Delete data from the data file.
        - update_data(index: int, newdata: list): Update data in the data file.
        - add_data(newdata: list): Add data to the data file.
        - show_data(): Display data from the data file.
        - is_convert_types(data: str, data_type: type): Check if the data can be converted to the specified data type.
    """

    def __init__(self, data_filename: str) -> None:
        """
        Initialize the Controller class.

        Args:
            - data_filename (str): The name of the data file.
        """
        self._current_path = os.path.split(os.path.dirname(__file__))[0]
        self._data_path = os.path.join(self._current_path, "data")
        self.filename = data_filename + ".csv"

    def is_dir_exists(self) -> bool:
        """
        Check if the data directory exists.

        Returns:
            bool: True if the data directory exists, False otherwise.
        """
        return os.path.isdir(f"{self._data_path}")

    def is_file_exists(self) -> bool:
        """
        Check if the data file exists in the data directory.

        Returns:
            bool: True if the data file exists, False otherwise.
        """
        if not self.is_dir_exists():
            self.create_dir()

        return self.filename in os.listdir(f"{self._data_path}")

    def is_data_empty(self) -> bool:
        """
        Check if the data file is empty.

        Returns:
            bool: True if the data file is empty, False otherwise.
        """

        if self.is_file_exists():
            return pd.read_csv(f"{self._data_path}\\{self.filename}").empty

    def get_data_path(self) -> str:
        """
        Get the path to the data directory.

        Returns:
            str: The path to the data directory.
        """
        return self._data_path

    def create_dir(self) -> None:
        """
        Create the data directory if it doesn't exist.
        """
        if not self.is_dir_exists():
            print("Making directory...")
            os.mkdir(f"{self._data_path}")
        else:
            print("Directory is already exists!")

    def create_file(self, columns_name: list | None = ...) -> None:
        """
        Create a new file in the data directory.
        """
        if not self.is_file_exists():
            print(f"Making {self.filename} at {self._data_path} directory...")
            f = open(f"{self._data_path}\\{self.filename}", "w+")
            if columns_name:
                f.write(",".join(columns_name))
            f.close()

    def dataframe_to_list(self, dataframe: DataFrame) -> list:
        """
        Convert a DataFrame to a list.

        Args:
            - dataframe (DataFrame): The DataFrame to be converted.

        Returns:
            list: The converted list.
        """
        return dataframe.values.tolist()

    def list_to_dataframe(
            self,
            list_data: list,
            columns_name: list) -> DataFrame:
        """
        Convert a list to a DataFrame.

        Args:
            - list_data (list): The list to be converted.
            - columns_name (list): The names of the columns in the DataFrame.

        Returns:
            DataFrame: The converted DataFrame.
        """
        return DataFrame(data=list_data, columns=columns_name)

    def get_data(self) -> DataFrame:
        """
        Get data from the data file.

        Returns:
            DataFrame: The data from the data file.
        """
        data = pd.read_csv(f"{self._data_path}\\{self.filename}")
        return data

    def read_data(self, columns_name: list = ...) -> DataFrame:
        """
        Read data from the data file.

        Args:
        - columns_name (list): The names of the columns in the DataFrame.

        Returns:
            DataFrame: The data from the data file.
        """
        if self.is_file_exists():
            return self.get_data()
        else:
            print("File tidak ditemukan!\nMembuat file baru...")
            self.create_file(columns_name)
            return self.get_data()

    def delete_data(self, index: int) -> None:
        """
        Delete data from the data file.

        Args:
            - index (int): The index of the data to be deleted.
        """
        data = self.read_data()
        data.drop(index=index, inplace=True)
        self.save_data(data)

    def update_data(
            self,
            index: int,
            newdata: list | str | int,
            columns: str = ...) -> None:
        """
        Update data in the data file.

        Args:
            - index (int): The index of the data to be updated.
            - newdata (list): The new data to replace the existing data.
        """
        data = self.read_data()
        if columns != ...:
            data.loc[index, columns] = newdata
        else:
            data.loc[index] = newdata
        self.save_data(data)

    def add_data(self, newdata: list | list[list]) -> None:
        """
        Add data to the data file.

        Args:
            - newdata (list): The new data to be added.
        """
        data = self.read_data()
        if self.is_nested_lists(newdata):
            for item in newdata:
                new_series = pd.Series(item, index=data.columns)
                data = data._append(new_series, ignore_index=True)
        else:
            new_series = pd.Series(newdata, index=data.columns)
            data = data._append(new_series, ignore_index=True)
        self.save_data(data)

    def save_data(
            self,
            data: DataFrame | list[list],
            columns_name: list = ...) -> None:
        """
        Save data to the data file.

        Args:
            - data (DataFrame | list): The data to be saved.
        """
        if isinstance(data, list):
            data = self.list_to_dataframe(data, columns_name)

        if self.is_file_exists():
            data.to_csv(f"{self._data_path}\\{self.filename}", index=False)
        else:
            print("File tidak ditemukan!\n Membuat file baru...")
            self.create_file()
            data.to_csv(f"{self._data_path}\\{self.filename}", index=False)

    def show_data(self) -> None:
        """
        Display data from the data file.
        """
        data = self.read_data().reset_index(names=["No."])

        data_list = self.dataframe_to_list(data)

        table = PrettyTable()
        table.field_names = data.columns

        for row in data_list:
            table.add_row(row)
        print(table)

    def convert_types(self, data: str, data_type: type) -> bool:
        """
        Check if the data can be converted to the specified data type.

        Args:
            - data (str): The data to be checked.
            - data_type (type): The data type to check against.

        Returns:
            bool: True if the data can be converted, False otherwise.
        """
        try:
            return data_type(data)
        except ValueError:
            raise ValueError(f"Data harus berupa {data_type.__name__}!")

    def is_nested_lists(self, data: list) -> bool:
        """
        Check if the data is a nested list.

        Args:
            - data (list): The data to be checked.

        Returns:
            bool: True if the data is a nested list, False otherwise.
        """
        return any(isinstance(i, list) for i in data)
