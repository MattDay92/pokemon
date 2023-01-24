from app import app
from flask import render_template, request, redirect, url_for, flash
from .forms import UserCreationForm, PokemonSearchForm, LoginForm, CatchPokemon
from .models import User, Pokemon, Catch
from flask_login import login_user, logout_user, current_user, login_required
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
@login_required
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

            caught = Pokemon.query.all()
            caught_set = set()
            my_pokemon = Pokemon.query.filter_by(user_id = current_user.id)
            my_pokemon_set = set()
            for name in caught:
                caught_set.add(name.id)
            for poke in my_pokemon:
                my_pokemon_set.add(poke.id)
            if id not in caught_set:
                if len(my_pokemon_set) < 5:
                    pokemon = Pokemon(id, current_user.id, pokename, img)

                    pokemon.saveToDB()
                else: 
                    flash(f"You can only hold five pokemon at a time.  To catch {pokename.title()}, please release one pokemon.", category='warning')

            else:
                flash(f"{pokename.title()} has already been caught.", category='warning')


        else:
            flash("The pokemon you're looking for does not exist.", category='warning')
            return redirect(url_for('catchPokemon'))

        return render_template('catch.html', pokemon_dict = pokemon_dict, pokename = pokename, id = id, catch=catch, img=img)
    
    return render_template('catch.html', catch=catch)

@app.route('/my_pokemon', methods=["GET"])
@login_required
def myPokemon():

    pokemon = Pokemon.query.all()
    my_pokemon = current_user.pokemon

    return render_template('my_pokemon.html', pokemon = pokemon, my_pokemon = my_pokemon)

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
            
        return redirect(url_for('myPokemon'))


    return render_template('login.html', form = form)

@app.route('/logout', methods=["GET"])
def logOutRoute():
    form = logout_user()

    return redirect(url_for('findpokemon'))


