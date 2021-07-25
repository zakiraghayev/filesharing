# filesharing

* File share with username and email
* Comment on file, (CRUD)
* Real time commenting as well


> docker-compose build
> docker-compose up

It is file sharing app. Only users who registered can upload file to the system. The file uploaded will be deleted after 7 days from time uploaded (Celery).
File can be shared with any users in the systems with just typing username or email to share. Sharing has two options: View and View&Comment access. in view access case, users whom the file shared with can see the comments but cannot comment to. If a user has an access View&Comment can comment, can edit comment and can delete comment that the user has made. Comment system is built on real-time socket (Django-CHannels) 
