from data import data_manager
from psycopg2 import sql


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_show_count():
    return data_manager.execute_select('SELECT count(*) FROM shows;')


def get_shows_limited(order_by="rating", order="DESC", limit=0, offset=0):
    return data_manager.execute_select(
        sql.SQL("""
            SELECT
                shows.id,
                shows.title,
                shows.year,
                shows.runtime,
                to_char(shows.rating::float, '999.9') AS rating_string,
                string_agg(genres.name, ', ' ORDER BY genres.name) AS genres_list,
                shows.trailer,
                shows.homepage
            FROM shows
                JOIN show_genres ON shows.id = show_genres.show_id
                JOIN genres ON show_genres.genre_id = genres.id
            GROUP BY shows.id
            ORDER BY
                CASE WHEN %(order)s = 'ASC' THEN {order_by} END ASC,
                CASE WHEN %(order)s = 'DESC' THEN {order_by} END DESC
            LIMIT %(limit)s
            OFFSET %(offset)s;
        """
        ).format(order_by=sql.Identifier(order_by)),
        {"order": order, "limit": limit, "offset": offset}
   )


def get_show(id):
    return data_manager.execute_select("""
        SELECT
            shows.id,
            shows.title,
            shows.year,
            shows.runtime,
            to_char(shows.rating::float, '999.9') AS rating_string,
            string_agg(genres.name, ', ' ORDER BY genres.name) AS genres_list,
            shows.trailer,
            shows.homepage,
            shows.overview
        FROM shows
            JOIN show_genres ON shows.id = show_genres.show_id
            JOIN genres ON show_genres.genre_id = genres.id
        WHERE shows.id = %(id)s
        GROUP BY shows.id;
    """, {"id": id}, False)


def get_show_characters(id, limit=3):
    return data_manager.execute_select("""
        SELECT sc.id, character_name, name, birthday, death, biography
        FROM actors a
        JOIN show_characters sc on a.id = sc.actor_id
        WHERE show_id = %(id)s
        ORDER BY id
        LIMIT %(limit)s
    """, {"id": id, "limit": limit})

def get_show_seasons(id):
    return data_manager.execute_select("""
        SELECT
            season_number,
            seasons.title,
            seasons.overview
        FROM shows
        JOIN seasons ON shows.id = seasons.show_id
        WHERE shows.id = %(id)s;
    """, {"id": id})

def get_actors():
    return data_manager.execute_select('SELECT * FROM actors LIMIT 20;')

# def get_show_details(id):
#     return data_manager.execute_select("""
#     SELECT * FROM show_characters
#     JOIN shows ON shows.id = show_characters.show_id
#     WHERE show_characters.actor_id = %(id)s;
#     """, {"id":id})
#
#
def get_actor(actor_id):
    return data_manager.execute_select("""
        SELECT * FROM actors WHERE id = %(actor_id)s
    """, {"actor_id": actor_id}, False)

def get_actor_shows(actor_id):
    return data_manager.execute_select("""
    SELECT shows.id, shows.title
    FROM shows
    JOIN show_characters ON shows.id = show_characters.show_id
    JOIN actors ON actors.id = show_characters.actor_id
    WHERE show_characters.actor_id = %(actor_id)s
    """, {"actor_id": actor_id})




def get_episodes():
    return data_manager.execute_select("""
        SELECT
            episodes.id,
            episodes.title,
            episodes.episode_number,
            episodes.overview,
            episodes.season_id,
            seasons.season_number,
            shows.title AS show_title
        FROM episodes
        JOIN seasons ON episodes.season_id = seasons.id
        JOIN shows ON seasons.show_id = shows.id
        ORDER BY shows.title, seasons.season_number, episodes.episode_number LIMIT 1;
    """)

def get_episode(episode_id):
    return data_manager.execute_select("""
        SELECT
            episodes.id,
            episodes.title,
            episodes.episode_number,
            episodes.overview,
            episodes.season_id,
            seasons.season_number,
            shows.title AS show_title
        FROM episodes
        JOIN seasons ON episodes.season_id = seasons.id
        JOIN shows ON seasons.show_id = shows.id
        WHERE episodes.id = %(episode_id)s
    """, {"episode_id": episode_id}, False)

def get_actors_by_show(show_id):
    return data_manager.execute_select("""
        SELECT
            actors.id,
            actors.name,
            actors.birthday,
            actors.death,
            actors.biography,
            show_characters.character_name
        FROM actors
        JOIN show_characters ON actors.id = show_characters.actor_id
        WHERE show_characters.show_id = %(show_id)s
        ORDER BY actors.name;
    """, {"show_id": show_id})

def get_actors_by_episode(episode_id):
    return data_manager.execute_select("""
        SELECT
            actors.id,
            actors.name,
            show_characters.character_name
        FROM actors
        JOIN show_characters ON actors.id = show_characters.actor_id
        WHERE show_id = %(episode_id)s
    """, {"episode_id": episode_id})