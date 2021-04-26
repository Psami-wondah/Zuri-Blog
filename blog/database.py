def create(username, password, email):
    f = open('blog/user_record/'+str(username) + '.txt', 'w+')
    user_details = [username, password, email]
    f.write(str(user_details))

