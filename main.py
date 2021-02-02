import sqlite3
from tkinter import ttk, messagebox, Tk, Frame, LabelFrame, Label, StringVar, Entry, CENTER, Toplevel, END
from tkinter.ttk import Treeview

class App():
    def __init__(self, root):
        #Ventana principal
        self.root = root
        self.root.title('DataBase')

        #Creando un administrador de pestañas
        tabs = ttk.Notebook(self.root)
        tabs.grid() 

        #insertando un frame a la pestaña
        tabsFrame = Frame(tabs)
        tabsFrame.grid()

        #agregando una pestaña
        tabs.add(tabsFrame, text='Main')

        #Frame contenedor del formulario de registro
        myFrame = LabelFrame(tabsFrame)
        myFrame.grid(row = 0, column = 0, columnspan = 3, pady = 10, padx = 10)

        #1ra fila
        Label(myFrame, text = "User : ").grid(row = 1, column = 0, padx = 10, pady = 10)
        self.userFieldValue = StringVar()
        self.userEntry = Entry(myFrame, textvariable = self.userFieldValue, width = 30)
        self.userEntry.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.userEntry.focus()

        #2da fila
        Label(myFrame, text = "Password : ").grid(row = 2, column = 0, padx = 10, pady = 10)
        self.passwordFieldValue = StringVar()
        self.passwordEntry = Entry(myFrame, textvariable = self.passwordFieldValue, width = 30)
        self.passwordEntry.grid(row = 2, column = 1, padx = 10, pady = 10)

        #3ra fila
        Label(myFrame, text = "Email : ").grid(row = 3, column = 0, padx = 10, pady = 10)
        self.emailFieldValue = StringVar()
        self.emailEntry = Entry(myFrame, textvariable = self.emailFieldValue, width = 30)
        self.emailEntry.grid(row = 3, column = 1, padx = 10, pady = 10)

        #4ta fila
        Label(myFrame, text = "Page : ").grid(row = 4, column = 0, padx = 10, pady = 10)
        self.pageFieldValue = StringVar()
        self.pageEntry = Entry(myFrame, textvariable = self.pageFieldValue, width = 30)
        self.pageEntry.grid(row = 4, column = 1, padx = 10, pady = 10)

        #5ta fila
        ttk.Button(myFrame, text = "Add", command = self.add_Account).grid(row = 5, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = "WE")

        #3 Botones y posicionamiento de Search/Update/Delete
        myFrame1 = Frame(tabsFrame)
        myFrame1.grid()

        ttk.Button(myFrame1, text = "Search", command = self.search_Account).grid(row = 1, column = 0, padx = 5, pady = 10)
        ttk.Button(myFrame1, text = "Update", command = self.update_Account).grid(row = 1, column = 1, columnspan = 2, padx = 5, pady = 10)
        ttk.Button(myFrame1, text = "Delete", command = self.delete_Account).grid(row = 1, column = 3, padx = 5, pady = 10)

        #Tabla arbol, donde la informacion de las cuentas sera mostrada
        self.tree = ttk.Treeview(myFrame1, height = 10, columns = ("#0", "#1","#2", "#3"), show = "headings")
        self.tree.grid(row = 2, column = 0, columnspan = 4)
        self.tree.heading('#1', text = 'User', anchor      = CENTER)
        self.tree.heading('#2', text = 'Password', anchor = CENTER)
        self.tree.heading('#3', text = 'Email', anchor       = CENTER)
        self.tree.heading('#4', text = 'Page', anchor     = CENTER)

        #Configuracion de la barra de desplazamiento para la tabla arbol
        self.ScrollVert = ttk.Scrollbar(myFrame1, command = self.tree.yview, orient = 'vertical')
        self.ScrollVert.grid(row = 2, column = 4, sticky = 'nsew')
        self.tree.config(yscrollcommand = self.ScrollVert.set)

    def run_Query(self, query, parameters=()):
        """
        Envia la consulta a la bbdd sin parametros por defecto
        :query: Consulta sql
        :parameters: parametros que requiere dicha consulta
        :return: resultado de la consulta o Error
        """

        with sqlite3.connect('sqliteDB.db') as myConection:
            cursor = myConection.cursor()

            try:
                result = cursor.execute(query, parameters)
            except Exception as e:
                print(e)
            else:
                return result
                
    def get_Accounts(self):
        """
        actualiza la informacion de la tabla arbol
        :return: None
        """
        #cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        #quering data
        query = 'SELECT * FROM accounts'
        db_rows = self.run_Query(query)

        #filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[0], values = (row[1], row[2], row[3], row[4]))   

    def createDB(self):
        """
        Consulta SQL para crear la tabla necesaria para el funcionamiento del programa
        :return: None
        """
        query = '''
                    CREATE TABLE accounts (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    user TEXT,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL,
                    page TEXT NOT NULL)
                '''
        self.run_Query(query)

    def clearFields(self):
        """
        limpia los campos de texto de la ventana principal
        :return: None
        """
        self.userEntry.delete(0, END)
        self.passwordEntry.delete(0, END)
        self.emailEntry.delete(0, END)
        self.pageEntry.delete(0, END)

    def add_Account(self):
        """
        Agrega un registro a la base de datos
        :return: None
        """
        query = 'INSERT INTO accounts VALUES (NULL,?,?,?,?)'
        parameters = (self.userEntry.get(), self.passwordEntry.get(), self.emailEntry.get(), self.pageEntry.get())
        self.run_Query(query, parameters)
        self.get_Accounts()
        self.clearFields()
        messagebox.showinfo('DB', 'An email has been sucessfully added')

    def delete_Account(self):
        """
        borra un registro seleccionado en la tabla arbol, luego de una confirmacion
        :return: None
        """
        if self.tree.item(self.tree.selection())['values']:

            user, password, email, page = self.tree.item(self.tree.selection())['values']
            query = 'DELETE FROM accounts WHERE user = ? AND password = ? AND email = ? AND page = ?'
            parameters = (user, password, email, page)
            
            #validando la decision de borrar un registro
            question = messagebox.askyesno('Warning', 'Are you sure you want to delete the selected record?')
            if question:
                self.run_Query(query, parameters)
                self.get_Accounts()
                messagebox.showinfo('DB', 'A record has been deleted')
        else:
            messagebox.showwarning('DB', 'Please, select a record')
            return
        
    def search_Account(self):
        """
        Abre una nueva ventana para filtrar la informacion a partir de emails/paginas
        :return: None
        """
        #Positioning by rows
        window1 = Toplevel(self.root)
        #window1.geometry('+890+280')
        window1.title('Searching info')

        Label(window1, text = 'Filter by Email:').grid(row = 0, column = 0, padx = 10, pady = 10)
        self.variableEmail = StringVar()
        search_Entry1 = Entry(window1, textvariable = self.variableEmail)
        search_Entry1.bind('<Return>', lambda x: self.confirm_Search('email', self.variableEmail))
        search_Entry1.grid(row = 1, column = 0, padx = 10, pady = 10)
        search_Entry1.focus()

        Label(window1, text = 'Filter by Page:').grid(row = 2, column = 0, padx = 10, pady = 10)
        self.variablePage = StringVar()
        search_Entry2 = Entry(window1, textvariable = self.variablePage)
        search_Entry2.bind('<Return>', lambda x: self.confirm_Search('page', self.variablePage))
        search_Entry2.grid(row = 3, column = 0, padx = 10, pady = 10)

        ttk.Button(window1, text = 'Check', width = 10, command = lambda: self.confirm_Search('email', self.variableEmail)).grid(row = 1, column = 1, padx = 10, pady = 10)
        ttk.Button(window1, text = 'Check', width = 10, command = lambda: self.confirm_Search('page', self.variablePage)).grid(row = 3, column = 1, padx = 10, pady = 10)

        Label(window1, text = 'note: to view all emails, leave the field empty \n and press check', fg = 'red').grid(row = 4, column = 0, columnspan = 2)

    def confirm_Search(self, columnTable, field):
        """
        Confirma los cambios y envia la consulta sql
        :columnTable: str, indicando la columna de la tabla de la bbdd
        :field: str, valor del campo de texto de la variable pasada
        :return: None
        """
        #sends a query and return filtered info
        if columnTable == 'email':
            email = field.get()
            query = 'SELECT * FROM accounts WHERE {} LIKE "%{}%"'. format(columnTable, email)
        elif columnTable == 'page':
            page = field.get()
            query = 'SELECT * FROM accounts WHERE {} LIKE "%{}%"'. format(columnTable, page)

        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        db_rows = self.run_Query(query)

        for row in db_rows:
            self.tree.insert('', 0, text = row[0], values = (row[1], row[2], row[3], row[4]))

    def update_Account(self):
        """
        Abre una nueva ventana a partir del registro seleccionado, con campos de texto para actualizar informacion 
        :return: None
        """
        if not self.tree.item(self.tree.selection())['values']:
            messagebox.showwarning('DB', 'Please, select a record')
            return
        
        user, password, email, page = self.tree.item(self.tree.selection())['values']
        #Configuring new opened window
        window1 = Toplevel(self.root)
        #window1.geometry('+880+280')

        myFrame2 = LabelFrame(window1)
        myFrame2.grid(row = 0, column = 0, padx = 10, pady = 5)

        Label(myFrame2, text = 'New user :').grid(row = 1, column = 0)
        userEntry = Entry(myFrame2, textvariable = StringVar(window1, value = user), width = 25)
        userEntry.grid( row = 1, column = 1)

        Label(myFrame2, text = 'New password :').grid(row = 2, column = 0)
        passwordEntry = Entry(myFrame2, textvariable = StringVar(window1, value = password), width = 25)
        passwordEntry.grid(row = 2, column = 1)

        Label(myFrame2, text = 'New email :').grid(row = 3, column = 0)
        emailEntry = Entry(myFrame2, textvariable = StringVar(window1, value = email), width = 25)
        emailEntry.grid(row = 3, column = 1)
        
        Label(myFrame2, text = 'New page :').grid(row = 4, column = 0)
        pageEntry = Entry(myFrame2, textvariable = StringVar(window1, value = page), width = 25)
        pageEntry.grid(row = 4, column = 1)
        
        inputFields = [userEntry, passwordEntry, emailEntry, pageEntry]
        #Confirm update button
        ttk.Button(window1, text = 'Confirm', command = lambda: self.confirm_Update(inputFields, window1)).grid(row = 5, column = 0, columnspan = 2)

    def confirm_Update(self, fields, window):
        """
        Recolecciona los datos escritos en los campos, realiza la consulta sql y actualiza los datos
        :fields: lista de variables de los campos de texto a actualizar
        :window: variable ventana
        :return: None
        """
        user, password, email, page = list(map(lambda x: x.get(), fields))
        query = 'UPDATE accounts SET user = ? , password = ? , email = ? , page = ? WHERE id = ?'
        id = self.tree.item(self.tree.selection())['text']
        parameters = (user, password, email, page, id)
        
        self.run_Query(query, parameters)
        self.get_Accounts()
        window.destroy()

if __name__ == '__main__':
    root = Tk()

    application = App(root)
    application.createDB()
    application.get_Accounts()

    root.mainloop() 