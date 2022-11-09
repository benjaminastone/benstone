def user_input():
    """Defines the user input values. Provides a hint as needed."""
    
    user = (input("""Please enter the STATEFP code for South Dakota.
If you do not know it, here is a hint: It is the special number from
The Hitchhiker's Guide to the Galaxy, + 4: """)).lower()

    if user == str(46):
        user = where_clause_state = '"STATEFP" = \'46\''    
    elif user != str(46):     
        print("""Look up that special number and refresh the program.""")
    else:
        print("""Look up that special number and refresh the program.""")

    return user  

