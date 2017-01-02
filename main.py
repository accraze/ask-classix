import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

game_data = [
    {'band': 'The Beatles', 
        'members': ['John Lennon', 'Paul McCartney', 'George Harrison', 'Ringo Starr']},
    {'band': 'Pink Floyd', 
        'members': ['David Gilmour', 'Roger Waters', 'Richard Wright', 'Nick Mason']},
    {'band': 'Led Zeppelin', 
        'members': ['Robert Plant', 'Jimmy Page', 'John Paul Jones', 'John Bonham']},
    {'band': 'Kiss', 
        'members': ['Paul Stanley', 'Gene Simmons', 'Peter Criss', 'Ace Frehley']},
    {'band': 'Cream', 
        'members': ['Eric Clapton', 'Jack Bruce', 'Ginger Baker']},
    {'band': 'Black Sabbath', 
        'members': ['Ozzy Osbourne', 'Tommy Iommi', 'Bill Ward', 'Geezer Butler']},
    {'band': 'Rush', 
        'members': ['Neil Peart', 'Geddy Lee', 'Alex Lifeson']},
]


@ask.launch

def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("YesIntent")

def next_round():

    number = randint(0, len(game_data) - 1)
    record = game_data[number] 

    round_msg = render_template('round', members=record['members'])

    session.attributes['band'] = record['band']

    return question(round_msg)


@ask.intent("AnswerIntent", convert={'band': str})

def answer(band):

    answer = session.attributes['band']

    if band == answer:

        msg = render_template('win')

    else:

        msg = render_template('lose', answer=answer)

    return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)
