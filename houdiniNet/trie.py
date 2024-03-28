"""
--------------------------------------------------------------------------------------
This Python script comprises four classes designed for specific functionalities:

1. `EnvVariable`: This class is responsible for managing environmental variables, 
    facilitating both the setting and reading of their values. Notably, in this specific 
    Houdini Digital Asset (HDA), the script reads the cached data location from the environmental 
    variable `$CACHE_DATASET_PATH`. This variable contains the path where the cached data will be stored.
    if the variable is not set. The cached data is stored in the same folder as $HIP
    The set_env_var() function has the feature to overide_existing flag this is to allow the user to overide 
    even if the variable is already set. This is the ensure safety. 

2. `DataUtil`: This class is dedicated to managing the retrieval of a CSV file and then saving 
    the object as cached data. It plays a crucial role in handling data operations within the script.

3. `TrieNode` and `Trie`: These classes are exactly the same from the tutorial. 
    Although, at preset, my errort is to make this a case-insensitive search.

Please note that the HDA file is provided in the zip folder along with the 
corresponding .py file. 
---------------------------------------------------------------------------------------
"""
import hou
import pandas as pd
import pickle
import os

class EnvVariable:
    def __init__(self, variable=None, value=None):
        self.variable = variable or 'CACHE_DATASET_PATH'
        self.value = value or '/'.join([hou.getenv('HIP'), 'dataset'])
    
    def set_env_var(self, value, overide_existing=False):
        self.value = value
        if overide_existing:
            hou.putenv(self.variable, self.value)
        else:
            value = hou.getenv(self.variable)
            if not value:
                hou.putenv(self.variable, self.value)
            else:
                self.value = value
        return self.value

    def get_env_var(self):
        value = hou.getenv(self.variable)
        if value:
            return value
        else:
            return self.value


class DataUtil:
    def __init__(self, path=None):
        self.path = path
        self.dataset = None
        if self.path and not self._is_csv_file():
            raise ValueError("Invalid file type. The file must be a '.csv' extension")
    
    def set_path(self, path):
        self.path = path
        if not self._is_csv_file():
            raise ValueError("Invalid file type. The file must be a '.csv' extension")



    def _is_csv_file(self):
        _, file_extension = os.path.splitext(self.path)
        return file_extension.lower() == '.csv'

    def read_csv(self):
        if self.path:
            try:
                self.dataset = pd.read_csv(self.path)
                print("CSV data loaded successfully.")
            except FileNotFoundError:
                print(f"Error: File '{self.path}' not found.")
            except pd.errors.EmptyDataError:
                print(f"Error: File '{self.path}' is empty.")
            except pd.errors.ParserError as e:
                print(f"Error parsing CSV in file '{self.path}': {e}")
        else:
            print('Path is not set, please set the path using set_path()')


    def cache_data(self, cache_file, dataset=None):
        if dataset:
            self.dataset = dataset
        if self.dataset is not None:
            try:
                with open(cache_file, 'wb') as file:
                    pickle.dump(self.dataset, file)
                print(f"Data cached successfully to {cache_file}.")
            except Exception as e:
                print(f'Error caching data: {e}')
        else:
            print("No data to cache. use 'read_csv()' method first")

    def load_cached_data(self, cache_file):
        try:
            with open(cache_file, 'rb') as file:
                self.dataset = pickle.load(file)
        except FileNotFoundError:
            print(f"Error: Cache file '{cache_file}' not found.")
        except Exception as e:
            print(f"Error loading cached data: {e}")

    def testprint(self):
        print('this is working')


class TrieNode:
    def __init__(self, char):
        self.char = char
        self.is_end = False
        self.children = {}

class Trie(object):
    def __init__(self):
        self.root = TrieNode('')
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char]=new_node
                node = new_node
        node.is_end = True

    def _dfs(self, node, prefix):
        if node.is_end:
            self.output.append((prefix+node.char))

        for child in node.children.values():
            self._dfs(child, prefix+node.char)

    def query(self, x):
        self.output = []
        node = self.root

        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                return []

        self._dfs(node, x[:-1])
        return sorted(self.output, key=lambda x:x[1], reverse=True)

"""
------------------------------------------------------------------------------------------------
If you choose not to open the HDA, here is the code that gets embedded within the HDA itself. 
The HDA features a 'fetch()' functionality that loads the .csv file, builds a trie data structure 
using the Trie() class, and caches the data. This module includes 'fetch()' and 'search()' functions.
-----------------------------------------------------------------------------------------------------

import hou
from houdiniNet import trie
from importlib import reload
import os

reload(trie)

def fetch():
    dataset_file = hou.pwd().evalParm('dataset_file')
    if not dataset_file:
        return
    data = trie.DataUtil(dataset_file)
    data.read_csv()
    tr = trie.Trie()
    for title in data.dataset['title']:
        tr.insert(title)
    env = trie.EnvVariable('CACHE_DATASET_PATH')
    path=env.set_env_var('/Users/suhail/Documents/PyHub/cache')
    if not os.path.exists(path):
        os.makedirs(path)
    cache_file = '/'.join([path, 'cached_titles.pkl'])
    data.cache_data(cache_file, tr)
    
def search():
    word = hou.pwd().evalParm('searchfield')
    if not word:
        return
    else:
        env = trie.EnvVariable('CACHE_DATASET_PATH')
        cache_file = '/'.join([env.get_env_var(), 'cached_titles.pkl'])
        if not os.path.exists(cache_file):
            fetch()
        data = trie.DataUtil()
        data.load_cached_data(cache_file)
        res = data.dataset.query(word)
        for item in res:
            print(item)
        
"""
