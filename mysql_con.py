import mysql.connector, hashlib, binascii
from Crypto.Cipher import AES

class mysqlconnector():
    def __init__(self, _host : str, _port : int, _user : str, _password : str) -> None:

        self.connection = mysql.connector.connect(
            host = _host,
            port = _port,
            user = _user,
            password = _password
        )

        self.cursor = self.connection.cursor()
    
    # close: closes the mysql connection.
    def close(self):
        self.cursor.close()
        self.connection.close()

    # query: Shortens the coursor.execute() command for us.
    def query(self, sql):
        self.cursor.execute(sql)
    
    # fetchone: fetches one row.
    def fetchone(self):
        return self.cursor.fetchone()

    # fetchall: fetches all row.
    def fetchall(self):
        return self.cursor.fetchall()
    
    # create_database: creates the database.
    def create_database(self, database : str):
        self.query('create database if not exists {0}'.format(database))

        self.connection.commit()
    
    # create_user_table: creates the users table.
    def create_users(self, database : str, table : str):
        self.query('use {0}'.format(database))

        self.query('''
        create table if not exists {0} (
                id int not null auto_increment primary key,
                name varchar(30) default null unique,
                password varchar(260) default null
            )'''.format(table))
        
        self.connection.commit()

    
    # create_password_vault_table: creates the password vault table.
    def create_password_vault(self, database : str, vault_table : str, users_table : str):
        self.query('use {0}'.format(database))

        self.query('''
        create table if not exists {0} (
                id int not null auto_increment primary key,
                user_id int not null,
                username varchar(30) default null,
                description varchar(260) default null,
                password varchar(260) default null,
                FOREIGN KEY (id) REFERENCES {1}(id)
        )'''.format(vault_table, users_table))

        self.connection.commit()
    
    # insert_users: inserts into the users database.
    def insert_users(self, database : str, table : str, name : str, password : str):
        self.query('use {0}'.format(database))

        self.query('insert into {0} (name, password) values ("{1}", "{2}")'
        .format(table, name, self.SHA256Encryption(password)))

        self.connection.commit()
    
    # insert_password: insters into a password into passwords vault.
    def insert_password(self, database : str, vault_table : str, user_password : str, user_id : int, username : str, description : str, password : str):
        self.query('use {0}'.format(database))

        self.query('''insert into {0} (user_id, username, description, password) values ("{1}", "{2}", "{3}", "{4}")'''.
        format(vault_table, user_id, username, description, str(self.AESEncryption(user_password, password))))

        self.connection.commit()
    
    # print_passwords: prints the passwords inside the password vault for the specific user.
    def print_passwords(self, database : str, vault_table : str, user_id : int):
        self.query('use {0}'.format(database))
        
        self.query('select username, description, password from {0} where user_id = "{1}"'.format(vault_table, user_id))

        row = self.fetchall()

        return row
    
    # decrypt_password: decrypts the AES encryption.
    def decrypt_password(self, user_password : str, password : str):

        return str(self.AESDecryption(user_password, password))
    
    # remove_password: removes an password from the password vault table.
    def remove_password(self, database : str, vault_table : str, user_id : str, username : str, description : str, password : str):
        self.query('use {0}'.format(database))

        self.query('delete from {0} where user_id ={1} and username = "{2}" and description = "{3}" and password = "{4}"'
        .format(vault_table, user_id, username, description, password))

        self.connection.commit()
    
    # update_password: updates the password for an specific password in the table.
    def update_password(self, database : str, vault_table : str, user_password : str, user_id : int, username : str, description : str, password : str):
        self.query('use {0}'.format(database))

        self.query('update {0} set password = "{1}" where user_id = "{2}" and username = "{3}" and description = "{4}"'
        .format(vault_table, str(self.AESEncryption(user_password, password)), user_id, username, description))

        self.connection.commit()
    
    # auth: is the authentication it checks if the username and the hashes for the passwords matches.
    def auth(self, database : str, users_table : str , name : str, password : str):
        self.query('use {0}'.format(database))

        self.query('select id, name, password from {0} where name = "{1}"'.format(users_table, name))

        row = self.fetchone()

        try:
            if (row[1] == name):
                if (row[2] == self.SHA256Encryption(password)):
                    user_id = row[0]
                    username = row[1]
                    return ["True", user_id, username]
                else:
                    return [False]
            else:
                return [False]
        except:
            return [False]
    
    # SHA256Encryption: salts the password and then encrypts it using SHA256 method.
    def SHA256Encryption(self, password):
        saltedPassword = str(password + "s4lt")
        hashedPassword = hashlib.sha256(saltedPassword.encode()).hexdigest()
        return str(hashedPassword)
    
    # AESEncryption: is used to encrypt the password valut password.
    def AESEncryption(self, user_password, text):
        saltedPassword = str(user_password+ "s3lt")
        hashedPassword = hashlib.sha256(saltedPassword.encode()).hexdigest()
        
        cipher = AES.new(
            key = hashlib.sha256(str(hashedPassword).encode()).digest(),
            mode = AES.MODE_CBC,
            IV = hashlib.sha256(str("3LASMs1").encode()).digest()[0:16]
        )

        while len(text) % 16 != 0:
            text += " "
        
        encrypted_text = cipher.encrypt(text)
        hexing_text = binascii.hexlify(encrypted_text).decode('utf-8')

        return hexing_text
    
    # AESDecryption: is used to decrypt the password vault password.
    def AESDecryption(self, user_password, text : str):
        saltedPassword = str(user_password+ "s3lt")
        hashedPassword = hashlib.sha256(saltedPassword.encode()).hexdigest()

        unhex = binascii.unhexlify(text)

        chiper = AES.new(
            key = hashlib.sha256(str(hashedPassword).encode()).digest(),
            mode = AES.MODE_CBC,
            IV = hashlib.sha256(str("3LASMs1").encode()).digest()[0:16]
        )

        decrypted_text = chiper.decrypt(unhex)

        return str(decrypted_text)
