import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytask.settings')


import django
django.setup()
from task.models import UserProfile, Task
from django.contrib.auth.models import User

def populate():

    #list of users to generate
    userlist = [
        ["John", "Smith", "+441632960338"],
        ["Mary", "Jones", "+441632960517"],
        ["James", "Fraser", "+441632960774"],
        ["Derek", "Oswald", "+441632960081"],
        ["Micheal", "Johnson", "+441632960194"]
        ]

    #list of potential task titles to generate
    tasklist = [
        ["gardening" , 50, "doing some gardening"],
        ["homework", 20, "compute these problems"], 
        ["maths", 10, "solve these sums"], 
        ["tutoring", 5, "help these students"], 
        ["cleaning", 35, "clean the tables"]
        ]


    users = []

    for user in userlist:
        #create a new user
        new_user = User.objects.create( username = user[0] + "_" + user[1], first_name = user[0], last_name = user[1], email = user[0] + "_" + user[1] + "@gmail.com")
        new_user.save()

        #create a userprofile for the new user
        up = UserProfile.objects.create(user = new_user)
        up.phone_number = user[2]
        up.save()

        users.append(up)
    
    #generate tasks and assign them to users
    for user in users:
        if users.index(user) == 0:
            new_task = Task.objects.create(publisher = user, receiver = users[users.index(user) + 3], task_title = tasklist[users.index(user)][0], task_reward = tasklist[users.index(user)][1], task_description = tasklist[users.index(user)][2])
            user.tasks_posted = user.tasks_posted + 1
            user.save()
            users[users.index(user) + 3].tasks_received = users[users.index(user) + 3].tasks_received + 1
            users[users.index(user) + 3].save()

        elif users.index(user) == users.index(users[-1]):
            new_task = Task.objects.create(publisher = user, receiver = users[users.index(user) - 1], task_title = tasklist[users.index(user)][0], task_reward = tasklist[users.index(user)][1], task_description = tasklist[users.index(user)][2])
            user.tasks_posted = user.tasks_posted + 1
            user.save()
            users[users.index(user) - 1].tasks_received = users[users.index(user) - 1].tasks_received + 1
            users[users.index(user) - 1].save()

        else:
            new_task = Task.objects.create(publisher = user, receiver = users[users.index(user) + 1], task_title = tasklist[users.index(user)][0], task_reward = tasklist[users.index(user)][1], task_description = tasklist[users.index(user)][2])
            user.tasks_posted = user.tasks_posted + 1
            user.save()
            users[users.index(user) + 1].tasks_received = users[users.index(user) + 1].tasks_received + 1
            users[users.index(user) + 1].save()

        new_task.save()
            



if __name__ == '__main__':
    print("starting mytask population script")
    populate()
