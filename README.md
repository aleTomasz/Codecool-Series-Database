# 🎬 Codecool Series Database

A Flask web application that allows users to browse and explore a collection of TV shows, actors, episodes, and detailed information.

## 📚 Description

**Codecool Series Database** is a mini-series browser platform built using Python's Flask framework. It allows users to:

- View all available TV shows
- Sort shows by rating or other parameters
- Paginate through shows (15 per page)
- View individual show details (seasons, runtime, trailer, characters)
- Browse all actors and episodes
- View actor-related shows
- Access selected API endpoints for integration

## 🧰 Technologies Used

- Python 3
- Flask
- Jinja2 templating
- HTML/CSS (Bootstrap-ready)
- dotenv (for environment variables)
- SQLite or other backend database (via `queries.py` layer)

## 🔍 Features

- Dynamic pagination with symmetric page display
- Sorting by rating or other fields
- TV show detail pages with:
  - Characters
  - Seasons
  - Trailer video embedding
  - Runtime formatting
- Actors listing and detailed JSON API
- Episodes listing with single view
- Custom routes for UI and backend data access

## 🚀 Routes Overview

| Route | Description |
|-------|-------------|
| `/` | Home page showing shows |
| `/shows/`, `/shows/<page_number>` | Paginated list of shows |
| `/shows/order-by-<order_by>/<page_number>` | Sorted and paginated shows |
| `/show/<id>/` | Detailed page for a single show |
| `/actors/` | All actors |
| `/actors/<actor_id>` | JSON API of a single actor and their shows |
| `/episodes/` | List of all episodes |
| `/episodes/<episode_id>` | Episode details |
| `/api/shows/<show_id>/actors` | API: Get actors by show (JSON) |
| `/api/show/<show_id>/actors` | API: Get actors by episode (JSON - note: possible typo in function) |

## ⚠️ Note

There are placeholder views such as `/design` and a "Welcome" section, but these do not contain functional logic (e.g., login/registration).

## 💾 Setup & Run Locally

## 📦 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/aleTomasz/Codecool-Series-Database.git
