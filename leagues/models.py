from django.db import models

class League(models.Model):
	name = models.CharField(max_length=50)
	sport = models.CharField(max_length=15)
	#teams = todos los equipos de la liga
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Team(models.Model):
	location = models.CharField(max_length=50)
	team_name = models.CharField(max_length=50)
	league = models.ForeignKey(League, related_name="teams", on_delete = models.CASCADE)
	#curr_players = jugadores actuales del equipo
	#all_players = jugadores que alguna vez han estado equipo

class Player(models.Model):
	first_name = models.CharField(max_length=15)
	last_name = models.CharField(max_length=15)
	curr_team = models.ForeignKey(Team, related_name="curr_players", on_delete = models.CASCADE)
	all_teams = models.ManyToManyField(Team, related_name="all_players")
