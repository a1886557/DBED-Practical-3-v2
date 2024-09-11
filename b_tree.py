# adapted from https://www.programiz.com/dsa/b-tree
import random
import time

class BTreeNode:
    def __init__(self):
        self.key_vals = []  # each element is a key-value pair
        self.children = []  # each element is a node

class BTree:
    def __init__(self, t = 4):
        self.root = BTreeNode()
        self.t = t  # in any node, maximum number of keys is 2*t-1

    # Print the tree, starting from node x at level l
    def print_tree(self, x = None, l = 0):
        if x is None:
            x = self.root
        print("Level ", l, end = ": ")
        for data in x.key_vals:
            print(data[0], end = " ")
        print()
        for y in x.children:
            self.print_tree(y, l + 1)

    # Search for key, starting from node x
    def search_key(self, k, x = None):
        # k is a value to find
        # if not found, returns None
        # otherwise, returns a tuple with two values:
        # node and key index in that node
        if x is None:
            x = self.root

        i = 0
        while (i < len(x.key_vals)):
            if (k == x.key_vals[i][0]):
                return (x, i)
            elif (k < x.key_vals[i][0]):
                break
            i += 1

        if len(x.children) == 0:
            return None

        return self.search_key(k, x.children[i])

    # Insert value at key
    def insert_key(self, key, value):
        result = self.search_key(key)
        if result is None:
            self.insert_new_key((key, [value]))
        else:
            x = result[0]
            i = result[1]
            values = x.key_vals[i][1]
            values.append(value)

    # Insert the key that didn't exist
    def insert_new_key(self, k):
        root = self.root
        if len(root.key_vals) == (2 * self.t) - 1:
            new_root = BTreeNode()
            self.root = new_root
            new_root.children.insert(0, root)
            self.split(new_root, 0)
            self.insert_non_full(new_root, k)
        else:
            self.insert_non_full(root, k)

    # Insert non full condition
    def insert_non_full(self, x, k):
        i = len(x.key_vals) - 1
        if len(x.children) == 0:
            x.key_vals.append((None, None))
            while i >= 0 and k[0] < x.key_vals[i][0]:
                x.key_vals[i + 1] = x.key_vals[i]
                i -= 1
            x.key_vals[i + 1] = k
        else:
            while i >= 0 and k[0] < x.key_vals[i][0]:
                i -= 1
            i += 1
            if len(x.children[i].key_vals) == (2 * self.t) - 1:
                self.split(x, i)
                if k[0] > x.key_vals[i][0]:
                    i += 1
            self.insert_non_full(x.children[i], k)

    # Split
    def split(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode()
        x.children.insert(i + 1, z)
        x.key_vals.insert(i, y.key_vals[t - 1])
        z.key_vals = y.key_vals[t: (2 * t) - 1]
        y.key_vals = y.key_vals[0: t - 1]
        if len(y.children) > 0:
            z.children = y.children[t: 2 * t]
            y.children = y.children[0: t]


def construct_b_tree(array, t = 3):
    b_tree = BTree(t)
    for i, x in enumerate(array):
        b_tree.insert_key(x, i)
    return b_tree

def linear_search(array, query_value):
    # input: list of numbers and a value to find
    # output: list of indices of elements equal to the desired value
    # example: if array = [1, 3, 3, 0] and query_value = 3, result should be [1, 2]
    # don't use any data structures, except lists
    found_indices = []
    for i, value in enumerate(array):
        if (query_value == value):
            found_indices.append(i)
    return found_indices

def generate_data(data_size, max_value):
    array = random.choices(range(max_value), k=data_size)
    verification = {}
    for i, value in enumerate(array):
        values = verification.get(value, [])
        values.append(i)
        verification[value] = values

    return array, verification

def evaluation(rand_seed = None, max_value = 1000, num_queries = 1000):
    data_sizes = [100, 1000, 10000, 100000];

    random.seed(a=rand_seed)
    for data_size in data_sizes:
        array, verification = generate_data(data_size, max_value = max_value)
        b_tree = construct_b_tree(array)

        b_tree_time = 0
        linear_time = 0
        for i in range(num_queries):
            query_value = random.randrange(max_value)

            start = time.time()
            result = b_tree.search_key(query_value)
            end = time.time()
            b_tree_time += (end - start)

            start = time.time()
            linear_indices = linear_search(array, query_value)
            end = time.time()
            linear_time += (end - start)

            correct_indices = verification.get(query_value, [])
            b_tree_indices = []
            if result is not None:
                x = result[0]
                i = result[1]
                b_tree_indices = x.key_vals[i][1]

            if (correct_indices != b_tree_indices):
                print(correct_indices)
                print(b_tree_indices)
                print("error")
                return

        print("Array size: ", data_size, "; num. queries: ", num_queries)
        print("\tB-tree time: ", round(1000*b_tree_time), " ms")
        print("\tLinear time: ", round(1000*linear_time), " ms")

if __name__ == '__main__':
    evaluation()
