# FAST API Learning

## Feature

1. Create user : This will be contolled using the command line interface
2. Create token : For a given user generate a token, encypt with randome seed and provide token
3. Hash password :  Password to be hashed and stored, for verification, hash the given password during loging and compare the hash value, use murmur hashing for a quick hashing logic
4. Create note : User has the ability to create note
5. Update note : User has the ability to update a note along with title and descirption
6. Note history : Application keeps track of the changes in the notes 
7. Note delete :  User has the ability to delete notes


## Folder structure
1. alembic : contain code related to db managment 
2. api : contain code related to apis
3. app : contains code related to main application
4. tests : contain test code 

## Some helpful command

### DB update
```
# provide config file path because the command will executed on the parent folder
alembic -c alembic/alembic.ini revision --autogenerate -m "Test revision"
alembic -c alembic/alembic.ini upgrade head

```
### Testing with coverage
```
pytest --cov=api
```
