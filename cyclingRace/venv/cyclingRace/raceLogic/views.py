from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Bike, Team, Person, Stage
# Create your views here.


# strona startowa
def printMsg(request):
    main_page = {'image': '/media/images/tdp.jpeg'}
    return render(request, 'raceLogic/printMsg.html', main_page)


def displayAllTeams(request):
    teams = Team.objects.all()
    return render(request, 'raceLogic/displayAllTeams.html', {'teams': teams})


#wyswietla wszystkie rowery teamow
def printBikes(request):
    bikes = Bike.objects.all()
    context = {'bikes': bikes }
    return render(request, 'raceLogic/printBikes.html', context)


def displayBike(request, bike_id):
    bike = get_object_or_404(Bike, pk=bike_id)
    return render(request,'raceLogic/displayBike.html', {'bike': bike})


#wyswietla wszytskich kolarzy
def displayAllCyclists(request):
    cyclists = Person.objects.all()
    return render(request, 'raceLogic/displayAllCyclists.html', {'cyclists': cyclists})


def cyclistDetail(request, cyclist_id):
    cyclist = get_object_or_404(Person, pk=cyclist_id)
    return render(request, 'raceLogic/cyclistDetail.html', {'cyclist': cyclist})


#szuka konkretnego kolarza
def searchCyclist(request):
    return render(request, 'raceLogic/searchCyclist.html')


# oblsuga formularza do wyszukiwania kolarza
def getCyclist(request):
    if request.method == 'GET':
        if 'name' in request.GET and 'surname' in request.GET and request.GET['name'] and request.GET['surname']:
            try:
                n = request.GET['name']
                sn = request.GET['surname']
                cyclist = Person.objects.get(surname__iexact=sn, name__iexact=n)
            except (KeyError, Person.DoesNotExist):
                return render(request, 'raceLogic/searchCyclist.html')
            else:
                return render(request,'raceLogic/cyclistDetail.html', {'cyclist': cyclist})

        elif 'name' in request.GET and 'surname' in request.GET and request.GET['surname'] and not request.GET['name']:
            try:
                sn = request.GET['surname']
                cyclist = Person.objects.get(surname__iexact=sn)
            except (KeyError, Person.DoesNotExist):
                return render(request, 'raceLogic/searchCyclist.html')
            else:
                return render(request, 'raceLogic/cyclistDetail.html', {'cyclist': cyclist})
        else: return render(request, 'raceLogic/searchCyclist.html')
    else: return HttpResponse('You have not used form')



#wyszukiwanie wszystkich kolarzy danego teamu z formularza
def searchTeamCyclists(request):
    if request.method == 'GET':
        if 'name' in request.GET and request.GET['name']:
            try:
                n = request.GET['name']
                team = Team.objects.get(name__iexact=n)
                if team:
                    cyclists = Person.objects.filter(team=team)
            except (KeyError, Team.DoesNotExist):
                return render(request, 'raceLogic/listTeams.html', {'teams': Team.objects.all()})
            except (KeyError, Person.DoesNotExist):
                return HttpResponse('There is no cyclists in this team')
            else: return render(request, 'raceLogic/displayTeam.html', {'cyclists': cyclists, 'team': team})

        else: return render(request, 'raceLogic/listTeams.html', {'teams': Team.objects.all()})
    else:
        return render(request, 'raceLogic/listTeams.html', {'teams': Team.objects.all()})


#wyszukiwanie wszystkich kolarzy danego teamu
def getTeamCyclists(request, team_id):
    try:
        team = Team.objects.get(pk=team_id)
        cyclists = Person.objects.filter(team=team)
    except (KeyError, Team.DoesNotExist):
        return HttpResponse('Such a team does not exist')
    except (KeyError, Person.DoesNotExist):
        return HttpResponse('There is no cyclists in this team')
    return render(request, 'raceLogic/displayTeam.html', {'cyclists': cyclists, 'team': team})



# lista teamow
def listTeams(request):
    teams = Team.objects.all()
    return render(request, 'raceLogic/listTeams.html', {'teams': teams})



#dodawanie roweru do bazy danych
def postBike(request):
    banners = {'banner': 'Add', 'mainBanner': 'Add a new bike!'}
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('est_year') and request.POST.get('image'):
            try:
                bike = Bike()
                bike.name = request.POST.get('name')
                bike.est_year = request.POST.get('est_year')
                bike.image = request.POST.get('image')
                for b in Bike.objects.all():
                    if b.name == bike.name:
                        return HttpResponse("Such bike already exists!")
                bike.save()

            except (KeyError, Bike.DoesNotExist):
                return render(request, 'raceLogic/postBike.html', {'banners': banners})
            else: return HttpResponseRedirect(reverse('raceLogic:register'))
        else:
            return render(request, 'raceLogic/postBike.html',  {'banners': banners })
    else: return render(request, 'raceLogic/postBike.html',  {'banners': banners })



def deleteBike(request):
    banners = {'banner': 'Delete', 'mainBanner': 'Delete a bike. Enter only name and establishment year!'}
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('est_year'):
            flag = 1
            bike = Bike()
            bike.name = request.POST.get('name')
            bike.est_year = request.POST.get('est_year')
            for b in Bike.objects.all():
                if b == bike:
                    b.delete()
                    flag = 0

            if flag == 0: return HttpResponseRedirect(reverse('raceLogic:register'))
            else: return HttpResponse("Such bike does not exist!")


        else:
            return render(request, 'raceLogic/postBike.html', {'banners': banners })
    else: return render(request, 'raceLogic/postBike.html', {'banners': banners })


#dodawanie kolarza do bazy danych
def addPerson(request):
    banners = {'banner': 'Add', 'mainBanner': 'Add a new Person!'}
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('surname') and request.POST.get('birthDate') and request.POST.get('team') and request.POST.get('image'):

            person = Person()
            person.name = request.POST.get('name')
            person.surname = request.POST.get('surname')
            person.birthDate = request.POST.get('birthDate')
            person.image = request.POST.get('image')
            try:
                team = request.POST.get('team')
                person.team = Team.objects.get(name__iexact=team)
            except (KeyError, Team.DoesNotExist):
                return HttpResponse('Such team does not exist')
            else:

                for p in Person.objects.all():
                    if p.name == person.name and p.surname == person.surname and p.birthDate == person.birthDate:
                        return HttpResponse("Such Person already exists!")
                person.save()
                return HttpResponseRedirect(reverse('raceLogic:register'))
        else:
            return render(request, 'raceLogic/postPerson.html', {'banners': banners})
    else:
        return render(request, 'raceLogic/postPerson.html', {'banners': banners})



def deletePerson(request):
    banners = {'banner': 'Delete', 'mainBanner': 'Delete a Person! Enter only name and surname '}
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('surname'):
            flag = 1
            person = Person()
            person.name = request.POST.get('name')
            person.surname = request.POST.get('surname')
            for p in Person.objects.all():
                if p.name == person.name and p.surname == person.surname:
                    p.delete()
                    flag = 0

            if flag == 0:
                return HttpResponseRedirect(reverse('raceLogic:register'))
            else:
                return HttpResponse("Such Person does not exist!")


        else:
            return render(request, 'raceLogic/postPerson.html', {'banners': banners})
    else:
        return render(request, 'raceLogic/postPerson.html', {'banners': banners})


#dodawanie teamu do bazy danych
def addTeam(request):
    banners = {'banner': 'Add', 'mainBanner': 'Add a new Team!'}
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('est_year') and \
                request.POST.get('cyclist_amount') and request.POST.get('bike_brand') and request.POST.get('image'):
            team = Team()
            team.name = request.POST.get('name')
            team.est_year = request.POST.get('est_year')
            team.cyclist_amount = request.POST.get('cyclist_amount')
            bike = request.POST.get('bike_brand')
            try:
                team.bike_brand = Bike.objects.get(name__iexact=bike)
            except (KeyError, Bike.DoesNotExist):
                return HttpResponse("Such a bike does not exist")
            else:
                team.image = request.POST.get('image')
                for t in Team.objects.all():
                    if t.name == team.name and t.est_year == team.est_year and t.cyclist_amount == team.cyclist_amount:
                        return HttpResponse("Such Team already exists!")
                team.save()
                return HttpResponseRedirect(reverse('raceLogic:register'))
        else:
            return render(request, 'raceLogic/postTeam.html', {'banners': banners})
    else:
        return render(request, 'raceLogic/postTeam.html', {'banners': banners})
    


def deleteTeam(request):
    banners = {'banner': 'Delete', 'mainBanner': 'Delete a Team! Enter only team name!'}
    if request.method == 'POST':
        if request.POST.get('name'):
            flag = 1
            team = Team()
            team.name = request.POST.get('name')
            
            for t in Team.objects.all():
                if t.name == team.name:
                    t.delete()
                    flag = 0

            if flag == 0:
                return HttpResponseRedirect(reverse('raceLogic:register'))
            else:
                return HttpResponse("Such Team does not exist!")


        else:
            return render(request, 'raceLogic/postTeam.html', {'banners': banners})
    else:
        return render(request, 'raceLogic/postTeam.html', {'banners': banners})



# szczegoly danego teamu
def displayTeam(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    context = {'team': team}
    return render(request, 'raceLogic/displayTeam.html', context)


#widok wszystkich etapow wyscigu
def displayStages(request):
    stages = Stage.objects.all()
    return render(request, 'raceLogic/displayStages.html', {'stages': stages})


def stageDetails(request, stage_id):
    stage = get_object_or_404(Stage, pk=stage_id)
    return render(request, 'raceLogic/stageDetails.html', {'stage': stage})


# formularz do glosowania na najtrudniejszy etap wyscigu
def voteOnStage(request):
    try:
        selected = request.POST['stage']
        stage =Stage.objects.get(pk=selected)
    except (KeyError, Stage.DoesNotExist):
        return render(request, 'raceLogic/displayStages.html', {'stages': Stage.objects.all(), 'error': 'Error while voting on the hardest stage'})
    else:
        stage.difficulty = stage.difficulty+1
        stage.save()

        return HttpResponseRedirect(reverse('raceLogic:voteResults'))


#wyniki glosowania na najtrudniejszy etap
def voteResults(request):
    hardest = 1
    for st in Stage.objects.all():
        if st.difficulty > hardest:
            hardest = st.difficulty
    return render(request, 'raceLogic/voteResults.html', {'stages': Stage.objects.all(), 'hardest': hardest})


#widok do wyswietlania listy mozliwych modyfikacji na bazie danych
def register(request):
    return render(request, 'raceLogic/register.html')
