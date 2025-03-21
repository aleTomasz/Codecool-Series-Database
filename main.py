from flask import Flask, render_template, url_for, jsonify
from data import queries
import math
from dotenv import load_dotenv

load_dotenv()
app = Flask('codecool_series')
SHOWS_PER_PAGE = 15
SHOWN_PAGE_NUMBERS = 5  # should be odd to have a symmetry in pagination


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/shows/')
@app.route('/shows/<int:page_number>')
@app.route('/shows/most-rated/')
@app.route('/shows/most-rated/<int:page_number>')
@app.route('/shows/order-by-<order_by>/')
@app.route('/shows/order-by-<order_by>-<order>/')
@app.route('/shows/order-by-<order_by>/<int:page_number>')
@app.route('/shows/order-by-<order_by>-<order>/<int:page_number>')
def shows(page_number=1, order_by="rating", order="DESC"):
    count = queries.get_show_count()
    pages_count = math.ceil(count[0]['count'] / SHOWS_PER_PAGE)
    shows = queries.get_shows_limited(order_by, order, SHOWS_PER_PAGE, (page_number - 1) * SHOWS_PER_PAGE)

    shown_pages_start = int(page_number - ((SHOWN_PAGE_NUMBERS - 1) / 2))
    shown_pages_end = int(page_number + ((SHOWN_PAGE_NUMBERS - 1) / 2))
    if shown_pages_start < 1:
        shown_pages_start = 1
        shown_pages_end = SHOWN_PAGE_NUMBERS
    elif shown_pages_end > pages_count:
        shown_pages_start = pages_count - SHOWN_PAGE_NUMBERS + 1
        shown_pages_end = pages_count

    return render_template(
        'shows.html',
        shows=shows,
        pages_count=pages_count,
        page_number=page_number,
        shown_pages_start=shown_pages_start,
        shown_pages_end=shown_pages_end,
        order_by=order_by,
        order=order
    )


@app.route('/show/<int:id>/')
def show(id):
    show = queries.get_show(id)
    characters = queries.get_show_characters(id, 3)
    seasons = queries.get_show_seasons(id)

    # format character names
    show['characters_str'] = \
        ', '.join([character['name'] for character in characters])

    # getting trailer id from URL to embed video
    show['trailer_id'] = \
        show['trailer'][show['trailer'].find('=') + 1:] if show['trailer'] else ''

    # format runtime
    hours, minutes = divmod(show['runtime'], 60)
    runtime_str = (str(hours) + 'h ' if hours else '') + (str(minutes) + 'min' if minutes else '')
    show['runtime_str'] = runtime_str

    return render_template('show.html', show=show, seasons=seasons)


@app.route('/actors/')
def get_actors():
    actors = queries.get_actors()
    return render_template("actors.html", actors=actors)


@app.route('/actors/<int:actor_id>')
def actor_details(actor_id):
    actor = queries.get_actor(actor_id)
    shows = queries.get_actor_shows(actor_id)
    return jsonify(actor=actor, shows=shows)





@app.route('/episodes/')
def get_episodes():
    episodes = queries.get_episodes()
    return render_template("episodes.html", episodes=episodes)


@app.route('/episodes/<int:episode_id>')
def episode_details(episode_id):
    episode = queries.get_episode(episode_id)
    return render_template('episode.html', episode=episode)


@app.route('/api/shows/<int:show_id>/actors')
def get_actors_by_show_api(show_id):
    actors = queries.get_actors_by_show(show_id)
    return jsonify(actors)


@app.route('/api/show/<int:show_id>/actors')
def get_actors_by_episode_api(episode_id):
    actors = queries.get_actors_by_episode(episode_id)
    return jsonify(actors)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
