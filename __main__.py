from json import loads as load_json
import requests
import sys

class Fetcher: 
    def get_data(self): pass

class JSONFetch(Fetcher):
    def get_data(self): 
        with open("config.json", 'r') as f: return load_json(f.read())
        
class URLFetch(Fetcher):
    def __init__(self, url): self.url = url
    def get_data(self): return load_json(requests.get(self.url).text)

class InputFetch(Fetcher):
    def __init__(self, template_data=None):
        if template_data is None:
            template_data = {
                "name": "Template Project",
                "description": "",
                "installation": "",
                "usage": "",
                "contribution": "",
                "testing": "",
                "questions": "",
                "license": ""
            }
        self.template_data = template_data

    def get_data(self):
        data = {}
        for i in self.template_data.keys():
            data[i] = input(f"{i.capitalize()}:> ")
        return data

class DataFetcher:
    def __init__(self, type=None, args=None):
        self.type = type
        if args is None:
            self.fetcher = self.type()
        else: 
            self.fetcher = self.type(*args)

    def get_data(self):
        return self.fetcher.get_data()


d = DataFetcher(JSONFetch)


class ArgHandler:
    def __init__(self, sys_args) -> None:
        if len(sys_args) <= 1:
            self.cls = DataFetcher(InputFetch)
            return
        self.type = None
        self.url = None
        for arg in sys_args:
            if arg == "-t":
                self.type = sys_args[sys_args.index(arg) + 1]
            if arg == "-u":
                self.url = sys_args[sys_args.index(arg) + 1]
        self.cls = None
        if self.type == "url":
            self.cls = DataFetcher(URLFetch, [self.url])
        if self.type == "json":
            self.cls = DataFetcher(JSONFetch)



class ReadMeGenerator:
    def __init__(self, data=None, filename="README.md", output=""):
        if data is None:
            data = {
                "name": "NewProject",
                "description": "Describe",
                "installation": "Run setup.bat then setup.py",
                "usage": "Use",
                "contribution": "Contribute",
                "testing": "",
                "questions": "How to install?\nCheck the install section for instructions",
                "license": "MIT"
            }
        self.data = data
        print(self.data)
        self.file_output = ""
        self.filename, self.output = filename, output
        self.generate_file()
        self.save_file()

    def save_file(self):
        with open(f'{self.output}{self.filename}', 'w') as f:
            f.write(self.file_output)

    def generate_file(self):
        for i in self.data.items():
            if i[1] == "":
                continue
            elif i[0] == "name":
                self.file_output += f"# Name\n{i[1]}\n"
            else:
                self.file_output += f"## {i[0].capitalize()}\n{i[1]}\n"
            if i[0] == "description":
                self.generate_table_of_contents()
                

    def generate_table_of_contents(self):
        self.file_output += "## Table of Contents\n"
        for i in self.data.items():
            if i[1] == "": continue
            if i[0] == "name": continue
            self.file_output += f" - {i[0].capitalize()}\n"
print(sys.argv)
rm = ReadMeGenerator(data=ArgHandler(sys.argv).cls.get_data())