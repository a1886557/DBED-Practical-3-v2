import os

from b_tree import BTree


class SimpleDatabase:
    def __init__(self):
        # before an actual table is loaded, class members are set to None

        # a header is a list of column names
        # e.g., ['name', 'id', 'grade']
        self.header = None

        # map column name to column index in the header
        self.columns = None

        # None if table is not loaded
        # otherwise list b-tree indices corresponding to columns
        self.b_trees = None

        # rows contains actual data; this is a list of lists
        # specifically, this is a list of rows, where each row
        # is a list of values for each column
        # e.g., if a table with the above header has two rows
        # self.rows can be [['Alice', 'a1234', 'HD'], ['Bob', 'a7654', 'D']]
        self.rows = None

        # name of the loaded table
        self.table_name = None

    def get_table_name(self):
        return self.table_name

    def load_table(self, table_name, file_name):
        # note our DBMS only supports loading one table at a time
        # as we load new table, the old one will be lost
        print(f"loading {table_name} from {file_name} ...")

        if not os.path.isfile(file_name):
            print("File not found")
            return

        # note, you could use a CSV module here, also we don't check
        # correctness of file
        with open(file_name) as f:
            self.header = f.readline().rstrip().split(",")
            self.rows = [line.rstrip().split(",") for line in f]
        self.table_name = table_name

        self.columns = {}
        for i, column_name in enumerate(self.header):
            self.columns[column_name] = i

        self.b_trees = [None] * len(self.header)
        print("... done!")

    ## Include create_index and drop_index functions
    def create_index(self, column_name):
        if self.columns is None:
            print("No table loaded.")
            return

        if column_name not in self.columns:
            print(f'Error: No such column {column_name} exists.')
            return

        col_id = self.columns[column_name]
        if self.b_trees[col_id] is not None:
            print(f'Error: Index already exists on column {column_name}.')
            return

        print(f'Creating index on column {column_name}')
        self.b_trees[col_id] = BTree()
        for row in self.rows:
            self.b_trees[col_id].insert_key(row[col_id], row)

        print(f'Index on {column_name} created successfully')

    def drop_index(self, column_name):
        if column_name not in self.columns:
            print(f'Error: No such column {column_name} exists.')
            return

        col_id = self.columns[column_name]
        if self.b_trees[col_id] is None:
            print(f'Error: No Index exists on column {column_name}.')
            return

        print(f'Dropping index on Column {column_name}')
        self.b_trees[col_id] = None
        print(f'Index on {column_name} succesfully dropped')


    def select_rows(self, table_name, column_name, column_value):
        # modify this code such that row selection uses index if it exists
        # note that our DBMS only supports loading one table at a time
        if table_name != self.table_name:
            # no such table
            return [], []

        if column_name not in self.columns:
            # no such column
            return self.header, []

        col_id = self.columns[column_name]

        # Added Code
        if self.b_trees[col_id] is not None:
            result = self.b_trees[col_id].search_key(column_value)
            if not result:
                return self.header, []


            btree_node, key_index = result
            indexed_rows = btree_node.key_vals[key_index][1]
            return self.header, indexed_rows

        selected_rows = []
        for row in self.rows:
            if row[col_id] == column_value:
                selected_rows.append(row)

        return self.header, selected_rows

    def get_indexed_columns(self):
        if self.columns is None:
            return []

        # Find column names that have non-None B-trees
        indexed_columns = []
        for i in range(len(self.header)):
            if self.b_trees[i] is not None:
                indexed_columns.append(self.header[i])

        return indexed_columns
