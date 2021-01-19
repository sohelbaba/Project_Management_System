# Project_Management_System
Repository contains RESTAPI's of this project

# Requirements 
pip install python

pip install flask_restful

pip install falsk_jwt_extended

pip install SQLAlchemy


# Steps to run Project
1. Enabled Virtual Env. if created or directly installed requiremnets.
2. go to Project_Management_System/code dir.
3. run command : python app.py


# Api's

1. Registration [POST] : http://127.0.0.1:5000/registration
   
   payload = {
      "name" : "xxxx",
      "username" : "xxxx",
      "password" : "xxxx"
    }
   
   return : json message

2. Login [GET]: http://127.0.0.1:5000/authentication
   
   payload = {
      "username" : "xxxx",
      "password" : "xxxx"
    }
   
   return : json with access_token
   
set header's for perfoming all operations : 
             
             { key : authorization , value : JWT-access-token }
             { key : Content-type , value : Application/json }

3. Logout [GET]: http://127.0.0.1:5000/logout
   
   return : json message
  
4. CreateProject [POST] : http://127.0.0.1:5000/project/<string:nameofproject>

   payload = {
      "name" : "xxxx",
      "description" : "xxxx",
      "project_color_identity" : "xxxx"
    }
      
    return : Json message
    
5.  GetProjectByName [GET] : http://127.0.0.1:5000/project/<string:nameofproject>

    return : Json message

6.  EditProject [PUT] : http://127.0.0.1:5000/project/<string:nameofproject>            
    
    payload = {
        "description" : "xxxx",
        [optional-param] "permission" : 'XXXX'  //if you are project owner then only allow
    }
    
    return : Json message
    
7.  DeleteProject [delete] : http://127.0.0.1:5000/project/<string:nameofproject>

    return : json message
    
8. GetAllProject [GET] :  http://127.0.0.1:5000/projects
                 
   return : json message

9. CreateTask [POST] : http://127.0.0.1:5000/project/task/<string:name>
    
   payload = {
      "uuid" : "xxxx",
      "task_name" : "xxxx",
      "task_desc" : "xxxx"
  }
  
   return : json message

10. EditTask [PUT] : http://127.0.0.1:5000/project/task/<string:name>
    
    payload = {
      "uuid" : "xxxx",
      "task_desc" : "xxxx"
    }
    
    return : json message

11. DeleteTask [DELETE] :  http://127.0.0.1:5000/project/task/<string:name>
    
    payload = {
       "uuid" : "xxxx"
    }
    
    return : json message

12. GetTaskByName [GET] : http://127.0.0.1:5000/project/task/<string:name>
    
    return : json message
    
13. GetAllTaskofProject : http://127.0.0.1:5000/project/task

    payload = {
       "uuid" : "xxxx"
    }
    
    return : json message
    
14.  ShareProject [POST] :  http://127.0.0.1:5000/project/share

     payload = {
      "uuid" : "xxxx",
      "share_with_id" : <int:id>,
      "permission" : "xxxx"
    }
    
   return : json message
   
# Admin Api's [just for Helping]

15.  GetAllUsers [GET] :  http://127.0.0.1:5000/users
     
     return :  json message
     
16.  GetAllPermission [GET] : http://127.0.0.1:5000/permissions

      return : json message
      
17. GetAllTasks [GET] : http://127.0.0.1:5000/tasks
    
    return : json message
    
18. GetAllSharedProjects [GET] : http://127.0.0.1:5000/shareprojects
    
    return : json message
    
19. GetAllProjects [GET]  : http://127.0.0.1:5000/Allprojects
    
    return : json message
    
20.  DeactivateUsers [PUT] :  http://127.0.0.1:5000/deactivate/<int:id>

     return : json message
    
