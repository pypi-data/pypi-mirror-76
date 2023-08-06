''' A smiple python mini-database . Created by Himanshu singh cahuhan
For more visit https://github.com/chauhanprogrammer/mini-database'''


#--------------Importing required modules------------------#
import sqlite3 as dbf, pandas as pd, os
from termcolor import colored as xol


#---------------- Database -------------------#

class Database:
    ''' Creates a database '''
    def __init__(self,name):
        self.name = name
        self.filex = self.name+'.sqlite'
        self.__create()
    
    def __create(self):
        with open(self.filex,'w') as f:
        	f.close()
        
        connection = dbf.connect(self.filex)
        edit = connection.cursor() 
        self.edit = edit
        self.connection = connection
        
        

    def delete(self):
        with open(self.filex,'w') as db:
            x = db.write('')

class Table:
    def __init__(self,title,*args):
        if len(args)==0:
            raise Exception('provide at least one column')
        self.title = title
        self.desc = list(args)
        db = Database(title)
        self.db = db
        self.__create()

    @classmethod
    def __doc__(self):
        print("Creates table object or you can say a table, use it like this \n object_name = mdb.Table('Table-name','Column-name','Column2-name'...) and then use methods \n like this object_name.insert('column1value','column2value') for more see https://github.com/chauhanprogrammer/mdb")
    
    def __create(self):
        
        def create_columns(lx):
            data = lx[0] + " varchar"
            for item in lx[1:]:
                data += ' ,'+str(item)+' varchar'
            return data 

        try:
            data = create_columns(self.desc)
            command = f"CREATE TABLE {self.title}({data})"
            self.db.edit.execute(command)
        
        except dbf.Error as e:
            pass
        
    def insert(self,*args):
        error = f'There are {len(self.desc)} columns but provided {len(args)} values'

        if len(args) != len(self.desc):
            raise Exception(error)

        def create_values(lx):
            data = f"'{lx[0]}'"
            for item in lx[1:]:
                data += ' ,'+"'"+str(item)+"'"
            return data
        
        data = create_values(args)
        command = f"INSERT INTO {self.title} VALUES({data})"
        self.db.edit.execute(command)
    

    
    def update(self,condition):
        command = f"UPDATE {self.title} {condition}"
        self.db.edit.execute(command)
        

    def addcolumn(self,nameofcolumn):
        self.db.edit.execute(f"ALTER TABLE {self.title} ADD COLUMN {nameofcolumn} varchar")   
        self.desc.append(nameofcolumn)

    def select(self,condition):
        command = f"SELECT {condition}"
        self.db.edit.execute(command)
        data = self.db.edit.fetchall()
        return data
    
    def show(self):
        command = f"SELECT * FROM {self.title}"
        self.db.edit.execute(command)
        print(xol(f"Table Name: {self.title}\n",'green',None,['bold']))
        
        def prepare():
            '''Prepares the output of the table'''
            keys = self.desc
            vaxel = self.db.edit.fetchall()
            value = ""

            for item in keys:
                value += f"'"+str(item)+"':[],"
            value = eval('{'+value+'}')

            lisx = [x for x in value.keys()]     
            dashes = ['->' for x in range(len(vaxel))]
            
            for item in lisx:
                for ix in vaxel:
                    a = ix[lisx.index(item)]
                    value[item].append(a)
            
            data = pd.DataFrame(value,index=dashes)
            return data
		
        print(xol(prepare(),'green',None,['bold']))
    
    def __call__(self):
        self.show()
    
    def delete(self):
        os.remove(self.db.filex)
        
