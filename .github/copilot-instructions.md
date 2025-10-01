# Copilot instructions for this repo

Goal: help AI agents quickly make accurate changes in this Django 5 project.

## Project map (big picture)
- Framework: Django 5, SQLite (`db.sqlite3`), Python 3.13 artifacts present (`__pycache__` cpython-313).
- Root app: `moviesstore/` with global `settings.py`, `urls.py`, and base templates/static.
- Apps and responsibilities:
  - `home/`: marketing pages (`index`, `about`).
  - `movies/`: catalog (list/detail) + reviews (CRUD + report flag).
  - `accounts/`: auth flows (login/signup/logout) + user order history.
  - `cart/`: session-based cart + checkout creates `Order` and `Item` rows.
- Media: `MEDIA_ROOT` = `media/`, `MEDIA_URL` served via `urlpatterns += static(...)`.

## Data model and flows
- `movies.models.Movie(id,name,price:int,description,image:ImageField)`
- `movies.models.Review(comment,date auto, movie FK, user FK, reported:bool)`
- `cart.models.Order(total:int, date auto, user FK)`; `Item(price:int, quantity:int, order FK, movie FK)`
- Core flows:
  - Catalog: `movies/views.index` supports `?search=`; `movies/views.show` renders details and unreported reviews.
  - Reviews: create/edit/delete/report (all `@login_required`; edit/delete require ownership).
  - Cart: stored in session; checkout (`cart.views.purchase`) computes total, persists `Order` and `Item`s, clears session.

## Conventions to follow
- Context pattern: views build a `template_data` dict and render with `{'template_data': template_data}`. Keep this shape for new views.
- URL names: use "app.view" style (e.g., `name='movies.show'`, `name='cart.index'`). Reverse by these names in templates/views.
- Templates: extend `moviesstore/templates/base.html`. Base loads Bootstrap 5.3, Font Awesome, and `static/css/style.css`; navigation expects the URL names above.
- Static/Media: project static under `moviesstore/static/`; images uploaded to `movie_images/` under `MEDIA_ROOT`.

## Session cart contract (important)
- `request.session['cart']` is a dict of string keys and string quantities: `{ '<movie_id>': '<qty>' }`.
- Access keys as strings. Examples:
  - Utils: `calculate_cart_total(cart, movies)` uses `cart[str(movie.id)]` and `int(quantity)`.
  - Template filter `cart_filters.get_quantity(cart, movie_id)` returns `cart[str(movie_id)]`.
- When adding to cart: `cart[id] = request.POST['quantity']` (id is an int from URL; stored under its string representation). Do not change this contract without updating utils/filters and templates.

## Routing
- Project urls (`moviesstore/urls.py`) include app urlconfs at roots: `/`, `/movies/`, `/accounts/`, `/cart/`.
- App url examples (see `movies/urls.py` and `cart/urls.py`):
  - `path('<int:id>/', views.show, name='movies.show')`
  - `path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review')`
  - `path('<int:id>/add/', views.add, name='cart.add')`

## Auth patterns
- Use `@login_required` for actions that mutate data: review create/edit/delete/report; cart purchase; accounts orders/logout.
- Ownership checks: for review edits/deletes, compare `request.user` to `review.user`.

## Common tasks (commands)
- Create venv and install Django 5 (if missing):
  - python -m venv .venv; source .venv/bin/activate
  - pip install "Django>=5,<6"
- Run DB migrations and dev server:
  - python manage.py migrate
  - python manage.py createsuperuser  # optional for admin
  - python manage.py runserver
- Run tests (apps have `tests.py` stubs):
  - python manage.py test

## Implementation tips (repo-specific)
- Prefer `get_object_or_404` when resolving ids from URLs (see `cart.views.add`, `movies.views.edit_review`).
- When adding new context fields to templates, extend `template_data` and keep base layout expectations (e.g., `title`).
- File uploads: for any new `ImageField`/upload form, ensure view handles `request.FILES` and template `enctype="multipart/form-data"`; media is served in dev via `static(settings.MEDIA_URL, ...)`.

## Where to look for examples
- Views: `movies/views.py`, `cart/views.py`, `accounts/views.py`, `home/views.py`.
- URL naming/patterns: `movies/urls.py`, `cart/urls.py`, `accounts/urls.py`.
- Template structure & nav: `moviesstore/templates/base.html`.
- Cart utilities & filters (session contract): `cart/utils.py`, `cart/templatetags/cart_filters.py`.
- Models/relations: `movies/models.py`, `cart/models.py`.

If anything here is unclear or you notice a convention that differs from these notes (e.g., cart key types, context shape, or URL naming), call it out so we can update this guide.