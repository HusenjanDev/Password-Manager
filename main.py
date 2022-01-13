import os
from mysql_con import mysqlconnector
from ui import UI
import pwinput


mysqlCon = mysqlconnector('127.0.0.1', 3306, 'root', '123')
mysqlCon.create_database('password_manager')
mysqlCon.create_users('password_manager', 'users')
mysqlCon.create_password_vault('password_manager', 'passwords', 'users')

mysqlCon.insert_users('password_manager', 'users', 'root', 'secret123')

ui_element = UI()

def main():
    os.system('cls||clear')

    username = str(input(ui_element.typewriter_number("Username: ", 0, 0)))
    password = str(pwinput.pwinput(ui_element.typewriter_number('Password: ', 0, 0)))

    auth = mysqlCon.auth('password_manager', 'users', username, password)

    if auth[0] == "True":
        os.system('cls||clear')

        while(True):
            encryptedPasswords = mysqlCon.print_passwords('password_manager', 'passwords', auth[1])

            ui_element.typewriter_number("Username\t\tDescription\t\tPasswords\n", 1, 0)

            for x in encryptedPasswords:
                count = 0
                for i in x:
                    if count == 0:
                        ui_element.typewriter_number(str(i + "\t\t"), 0, 0)
                    else: 
                        ui_element.typewriter_text(str(i + "\t\t\t"), 0, 0)
                    
                    count += 1
                
                print("")
            
            print("")

            ui_element.typewriter_number('Available Commands\n', 1, 0)

            ui_element.typewriter_number('!add [username] [description] [password]\n', 0, 0)
            ui_element.typewriter_number('!remove [username] [description] [password]\n', 0, 0)
            ui_element.typewriter_number('!update [username] [description] [new password]\n', 0, 0)
            ui_element.typewriter_number('!de [password]\n\n', 0, 0)

            user_choice = str(input(ui_element.typewriter_number("", 2, 0)))

            tmpSplit = user_choice.split(' ')

            if len(tmpSplit) >= 0:
                if tmpSplit[0] == '!add':
                    security_check = input(str(ui_element.typewriter_number("Password: ", 3, 0)))

                    if security_check == password:
                        mysqlCon.insert_password('password_manager', 'passwords', password, auth[1], tmpSplit[1], tmpSplit[2], tmpSplit[3])
                        ui_element.typewriter_number('Added password...\n', 0, 2)
                        os.system('cls||clear')
                    
                    os.system('cls||clear')

                elif tmpSplit[0] == '!update':
                    security_check = input(str(ui_element.typewriter_number("Password: ", 3, 0)))

                    if security_check == password:
                        mysqlCon.update_password('password_manager', 'passwords', password, auth[1], tmpSplit[1], tmpSplit[2], tmpSplit[3])
                        ui_element.typewriter_number('Updated the password...\n', 0, 2)
                    
                    os.system('cls||clear')

                elif tmpSplit[0] == '!remove':
                    security_check = input(str(ui_element.typewriter_number("Password: ", 3, 0)))

                    if security_check == password:
                        mysqlCon.remove_password('password_manager', 'passwords', auth[1], tmpSplit[1], tmpSplit[2], tmpSplit[3])
                        ui_element.typewriter_number('Removed the password...\n', 0, 1.5)
                    
                    os.system('cls||clear')
                
                elif tmpSplit[0] == '!de':
                    security_check = input(str(ui_element.typewriter_number("Password: ", 3, 0)))

                    if security_check == password:
                        unencrypted_password = mysqlCon.decrypt_password(password, tmpSplit[1])
                        ui_element.typewriter_number('Password: {0}'.format(unencrypted_password[2:len(unencrypted_password) - 1].rstrip()), 0, 7)
                    
                    os.system('cls||clear')
    else:
        ui_element.typewriter_number('Login was unsuccessfull...', 3, 2)

main()