from django.urls import path
from django.conf.urls import url
from django.conf import settings
from . import views

app_name = 'raceLogic'

urlpatterns = [
   path('', views.printMsg, name='printMsg'),
   path('displayAllTeams/', views.displayAllTeams, name='displayAllTeams'),
   path('listTeams/', views.listTeams, name='listTeams'),
   path('bikes/', views.printBikes, name='printBikes'),
   path('Bikeadd/', views.postBike, name='postBike'),
   path('Bikedel/', views.deleteBike,name='deleteBike'),
   path('<int:bike_id>/bike', views.displayBike, name='displayBike'),
   path('searchCyclist/', views.searchCyclist, name='searchCyclist'),
   path('getCyclist/', views.getCyclist, name='getCyclist'),
   path('<int:team_id>/getTeamCyclists/', views.getTeamCyclists, name='getTeamCyclists'),
   path('searchTeamCyclists/', views.searchTeamCyclists, name='searchTeamCyclists'),
   path('displayAllCyclists/', views.displayAllCyclists, name='displayAllCyclists'),
   path('<int:cyclist_id>/cyclistDetail/', views.cyclistDetail, name='cyclistDetail'),
   path('displayStages/', views.displayStages, name='displayStages'),
   path('<int:stage_id>/stageDetails/', views.stageDetails, name='stageDetails'),
   path('voteOnStage/', views.voteOnStage, name='voteOnStage'),
   path('voteResults/', views.voteResults, name='voteResults'),
   path('register/', views.register, name='register'),
   path('addPerson/', views.addPerson, name='addPerson'),
   path('deletePerson/', views.deletePerson, name='deletePerson'),
   path('addTeam/', views.addTeam, name='addTeam'),
   path('deleteTeam/', views.deleteTeam, name='deleteTeam')

]