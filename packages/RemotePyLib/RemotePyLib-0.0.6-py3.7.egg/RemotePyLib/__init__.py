"""
A python Library from Nalin Studios to import and export libraries remotely without downloading them
Author: Nalin Angrish (from Nalin Studios)
"""
import requests
import os
import importlib
from bs4 import BeautifulSoup
from RemotePyLib import Exceptions


API_GET = "http://localhost/remotepylib/get"
API_UPLOAD = "http://localhost/remotepylib/upload"

class Importer(object):
    """A class made to import libraries using nalinstudios RemotePyLib API
    """
    def execModule(self, modulename, key):
        """This method is used to execute the remote module on the local machine.

        Args:
            modulename (str): name of the module you have uploaded (The name is not surely the name of the python file you have uploaded. You would have entered a specific name in the 'name of module field' of the website)
            key (str): The access key given to you after you have uploaded the python module.
        Usage:
            importer = Importer()
            importer.execModule('module', 'key')
        """
        data = {"module":modulename, "key":key}
        x = requests.post(API_GET, data)
        if x.text == "Invalid Access":
            raise Exceptions.InvalidAccessError()
        elif x.text == f'No module named {modulename} found':
            raise Exceptions.RemoteModuleNotFoundError()
        else:
            response = x.text
            exec(response)
    
    def importModule(self, modulename, key):
        """This method is used to import the remote module as a standard module.
        The classes and methods inside the remote module will work as if there was another python file along
        Note that there should not be any python file with the same name as 'modulename' otherwise all the data in that file will be cleared
        It returns the module object for the imported module.
        Args:
            modulename (str): name of the module you have uploaded (The name is not surely the name of the python file you have uploaded. You would have entered a specific name in the 'name of module field' of the website)
            key (str): The access key given to you after you have uploaded the python module.
        Usage:
            importer = Importer()
            module = importer.importModule('module', 'key')
            module.func()
            var = module.variable
            myClass = module.myClass()
        """

        data = {"module":modulename, "key":key}
        x = requests.post(API_GET, data)
        if x.text == "Invalid Access":
            raise Exceptions.InvalidAccessError()
        elif x.text == f'No module named {modulename} found':
            raise Exceptions.RemoteModuleNotFoundError(modulename)
        else:
            code = x.text
            with open(modulename+'.py', 'w+') as codefile:
                codefile.write(code)
            mModule = importlib.import_module(modulename)
            os.remove(modulename+".py")
            return mModule



class Exporter(object):
    """A class to export custom libraries to nalinstudios - RemotePyLib API.
    """
    def exportFile(self, filepath, modulename):
        """Export a python file to the NalinStudios API
            Returns the access key.
            Please keep the access key with you because it is required for importing the library. in case lost, contact the owner (go the the website and contact using email).
        
        Args:
            filepath (str): path of the python file to be uploaded
            modulename (str): name of the module with which it can be imported later.
        Usage:
            exporter = Exporter()
            key = exporter.exportFile('/mymodule.py', 'modulename')
            print(key)
        """
        file = {'pyfile': open(os.path.join(os.getcwd() + filepath), 'rb')}
        data = {'pyname': modulename}
        headers = {'Accept-Encoding': 'identity'}
        x = requests.post(API_UPLOAD, files=file, data=data, headers=headers)
        html = x.content
        try:
            soup = BeautifulSoup(html, features="html.parser")
            mKey = soup.find('code', id='auth-key')
            nKey = ''.join(map(str, mKey.contents))
            return nKey.replace(" ","").replace("\n", "")
        except:
            raise Exceptions.ExportError(modulename)
        return None