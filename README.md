# Football_bot

Хост на HEROKU:

heroku login #Вводим email и пароль

heroku create --region eu <habrparserbot>
  
OR
  
heroku git:remote -a <example-app>
heroku buildpacks:set heroku/python
  
git push heroku master
  
heroku ps:scale bot=1 # запускаем бота

Чтобы выключить бота
  
heroku ps:scale bot=0
  
heroku ps:stop bot
