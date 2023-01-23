from app import app
from flask import render_template, request, redirect, url_for
from .forms import UserCreationForm, PokemonSearchForm, LoginForm, CatchPokemon
from .models import User, Pokemon, Catch
from flask_login import login_user, logout_user, current_user
import requests as r

@app.route('/', methods=['GET', 'POST'])
def findpokemon():
    poke = PokemonSearchForm()
    if request.method == "POST":
        url = f'https://pokeapi.co/api/v2/pokemon/{poke.choose.data}'
        response = r.get(url)
        if response.ok:
            my_dict = response.json()
            pokemon_dict = {}
            pokemon_dict["Name"] = my_dict["name"]
            pokemon_dict["Ability"] = my_dict["abilities"][0]["ability"]["name"]
            pokemon_dict["Base XP"] = my_dict["base_experience"]
            pokemon_dict["Front Shiny"] = my_dict["sprites"]["front_shiny"]
            pokemon_dict["Base ATK"] = my_dict["stats"][1]["base_stat"]
            pokemon_dict["Base HP"] = my_dict["stats"][0]["base_stat"]
            pokemon_dict["Base DEF"] = my_dict["stats"][2]["base_stat"]

        else:
            return "The pokemon you're looking for does not exist."

        return render_template('index.html', poke = poke, pokemon_dict = pokemon_dict)
    
    return render_template('index.html', poke = poke)


@app.route('/catch', methods=['GET', 'POST'])
def catchPokemon():
    catch = CatchPokemon()
    if request.method == "POST":
        url = f'https://pokeapi.co/api/v2/pokemon/{catch.choose.data}'
        response = r.get(url)
        if response.ok:
            my_dict = response.json()
            pokemon_dict = {}
            pokemon_dict["Name"] = my_dict["name"]
            pokemon_dict["Front Shiny"] = my_dict["sprites"]["front_shiny"]

            id = my_dict["id"]
            pokename = pokemon_dict["Name"]
            img = pokemon_dict["Front Shiny"]

            pokemon = Pokemon(id, pokename, img)

            pokemon.saveToDB()


        else:
            return "The pokemon you're looking for does not exist."

        return render_template('catch.html', pokemon_dict = pokemon_dict, pokename = pokename, id = id, catch=catch, img=img)
    
    return render_template('catch.html', catch=catch)

@app.route('/my_pokemon', methods=["GET"])
def myPokemon():


    return render_template('my_pokemon.html')

@app.route('/signup', methods=["GET", "POST"])
def signUpPage():
    form = UserCreationForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            user = User(username, email, password)

            user.saveToDB()

            return redirect(url_for('findpokemon'))

    return render_template('signup.html', form = form)


@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    form = LoginForm()

    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user: 
                if user.password == password:
                    login_user(user)
                else:
                    print('WRONG PASSWORD')
            else:
                print('User doesn\'t exist')
            
        return redirect(url_for('findpokemon'))


    return render_template('login.html', form = form)

@app.route('/logout', methods=["GET"])
def logOutRoute():
    form = logout_user()

    return redirect(url_for('findpokemon'))


