# Password Manager <MySQL>
This was an College Project which ended up landing me an A *"Had to brang 😄"*. This was an amazing project to work on! The requirements for the project were the following.

- The user would need to enter an master password to add, update, remove and decrypt an password.
- All the passwords had to be encrypted.
- All the passwords had to be stored inside an MySQL Database.

The encryption method that was choosen for the master password was SHA-256 because it's an one-way encryption method and for the passwords the user stored on the database they were encrypted using the AES encryption method because this allows us to encrypt and decrypt the passwords. **What we are doing basically is** storing the encrypted AES text inside the MySQL Server so only the user will be able to decrypt the password. And if in the future our database ends up getting leaked it's not an big deal because all the passwords the users stored are secured and only they will be able to unlock it. **Implementing** all the other features were pretty easy because its about adding, updating and removing mysql data.

**Important:** This project was done within 7 days.

## Todo List
- Clean up the code.
