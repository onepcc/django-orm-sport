from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Q, Count

from . import team_maker

def index(request):
	todas_ligas = League.objects.all()
	todos_jugadores = Player.objects.all()
	ligas_baseball = League.objects.all().filter(name__icontains='baseball')
	ligas_mujeres = League.objects.all().filter(name__icontains='women')
	ligas_hockey = League.objects.all().filter(name__icontains='hockey')
	ligas_no_football = League.objects.all().exclude(name__icontains='football')
	ligas_conference = League.objects.all().filter(name__icontains='conference')
	ligas_atlantic = League.objects.all().filter(name__icontains='atlantic')
	equipos_dallas = Team.objects.all().filter(location__icontains='dallas')
	equipos_raptors = Team.objects.all().filter(team_name__icontains='raptors')
	equipos_city = Team.objects.all().filter(location__icontains='city')
	equipos_t = Team.objects.all().filter(team_name__istartswith='t')
	equipos_orderby_loc = Team.objects.all().order_by('location')
	equipos_orderby_teaminv = Team.objects.all().order_by('-team_name')
	players_coopers=Player.objects.all().filter(last_name__icontains='cooper')
	players_joshua=Player.objects.all().filter(first_name__icontains='joshua')
	players_coopers_nojoshua=Player.objects.all().filter(last_name__icontains='cooper').exclude(first_name__icontains='joshua')
	players_alexander_o_wyatt=Player.objects.all().filter(first_name__icontains='alexander') | Player.objects.all().filter(first_name__icontains='wyatt')
	players_alexander_o_wyattq=todos_jugadores.filter(Q(first_name__icontains='alexander') | Q(first_name__icontains='wyatt'))
	
	
	
	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
		"ligas_baseball": ligas_baseball,
		"ligas_mujeres": ligas_mujeres,
		"ligas_hockey": ligas_hockey,
		"ligas_no_football": ligas_no_football,
		"ligas_conference": ligas_conference,
		"ligas_atlantic": ligas_atlantic,
		"equipos_dallas": equipos_dallas,
		"equipos_raptors": equipos_raptors,
		"equipos_city": equipos_city,
		"equipos_t": equipos_t,
		"equipos_orderby_loc": equipos_orderby_loc,
		"equipos_orderby_teaminv": equipos_orderby_teaminv,
		"players_coopers":players_coopers,
		"players_joshua":players_joshua,
		"players_coopers_nojoshua": players_coopers_nojoshua,
		"players_alexander_o_wyatt": players_alexander_o_wyatt,
		"players_alexander_o_wyattq": players_alexander_o_wyattq

		
	}
	return render(request, "leagues/index.html", context)

def index2(request):
	todas_ligas = League.objects.all()
	todos_equipos = Team.objects.all()
	todos_jugadores = Player.objects.all()
	# 1.- todos los equipos en la Atlantic Soccer Conference
	atlantic_soccer_teams= todos_equipos.filter(league__name='Atlantic Soccer Conference')
	
	#2.- todos los jugadores (actuales) en los Boston Penguins
	current_players_boston_penguins = todos_jugadores.filter(curr_team__team_name ='Penguins')
	
	#3.- todos los jugadores (actuales) en la International Collegiate Baseball Conference
	current_players_icbc = todos_jugadores.filter(curr_team__league__name ='International Collegiate Baseball Conference')
	#current_players_icbc = todos_jugadores.filter(curr_team__league__name__icontains =('International Collegiate baseball conference'))
	
	#4.- todos los jugadores (actuales) en la Conferencia Americana de Fútbol Amateur con el apellido "López"
	current_players_cafa_lopez = todos_jugadores.filter(Q(curr_team__league__name ='American Conference of Amateur Football')&Q(last_name__icontains='lopez'))
	
	#5.- todos los jugadores de fútbol
	todos_jugadores_football = todos_jugadores.filter(curr_team__league__sport ='Football')
	
	#6.- todos los equipos con un jugador (actual) llamado "Sophia" / varias sofias
	todos_jugadores_sophia = todos_jugadores.filter(first_name ='Sophia')

	#7.- todos las ligas con un jugador (actual) llamado "Sophia"
	todos_jugadores_sophia = todos_jugadores.filter(first_name ='Sophia')

	#8.- todos con el apellido "Flores" que NO (actualmente) juegan para los Washington Roughriders
	current_noplayers_wr_flores = todos_jugadores.filter(~Q(curr_team__team_name ='Roughriders')&Q(last_name__icontains='flores'))

	#9.- todos los equipos, pasados y presentes, con los que Samuel Evans ha jugado
	current_samuel_evans = todos_jugadores.get(Q(first_name ='Samuel')&Q(last_name='Evans'))

	#10.- todos los jugadores, pasados y presentes, con los gatos tigre de Manitoba
	all_players_manitoba_tigers= todos_equipos.get(team_name ='Tiger-Cats',location='Manitoba').all_players.all()

	#11.- todos los jugadores que anteriormente estaban (pero que no lo están) con los Wichita Vikings
	all_players_antes_wv= todos_equipos.get(Q(team_name ='Vikings')&Q(location='Wichita')).all_players.all()

	#12.- cada equipo para el que Jacob Gray jugó antes de unirse a los Oregon Colts
	teams_jacob_gray = todos_jugadores.get(Q(first_name ='Jacob')&Q(last_name='Gray'))
	teams_jacob_gray1 = todos_equipos.filter(all_players__first_name='Jacob',all_players__last_name='Jacob').exclude(team_name='Colts')

	#13.- todos llamados "Joshua" que alguna vez han jugado en la Atlantic Federation of Amateur Baseball Players
	all_joshuas_afabp= todos_jugadores.filter(Q(first_name ='Joshua')&Q(all_teams__league__name__icontains='Atlantic Federation of Amateur Baseball Players'))

	#14.- todos los equipos que han tenido 12 o más jugadores, pasados y presentes. (SUGERENCIA: busque la función de anotación de Django).
	all_teams_mas12p= todos_equipos.annotate(Count('all_players'))
	all_teams_mayor12p= todos_equipos.annotate(njugadores=Count('all_players')).filter(njugadores__gte=12)
	t12 = todos_equipos.alias(njugadores=Count('all_players')).filter(njugadores__gte=12)

	#15.- todos los jugadores y el número de equipos para los que jugó, ordenados por la cantidad de equipos para los que han jugado
	all_players_nequipos_ordernados= todos_jugadores.annotate(nequipos=Count('all_teams')).order_by('-nequipos')

	
	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
		"atlantic_soccer_teams": atlantic_soccer_teams,
		"current_players_boston_penguins":current_players_boston_penguins,
		"current_players_icbc":current_players_icbc,
		"current_players_cafa_lopez":current_players_cafa_lopez,
		"todos_jugadores_football":todos_jugadores_football,
		"todos_jugadores_sophia":todos_jugadores_sophia,
		"current_noplayers_wr_flores":current_noplayers_wr_flores,
		"current_samuel_evans":current_samuel_evans,
		"all_players_manitoba_tigers":all_players_manitoba_tigers,
		"all_players_antes_wv":all_players_antes_wv,
		"teams_jacob_gray":teams_jacob_gray,
		"all_joshuas_afabp":all_joshuas_afabp,
		"all_teams_mas12p":all_teams_mas12p,
		"team12":t12,
		"all_players_nequipos_ordernados":all_players_nequipos_ordernados

	}
	return render(request, "leagues/index2.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")