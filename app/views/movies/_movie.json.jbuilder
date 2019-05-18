json.extract! movie, :id, :title, :release_date, :poster_path, :overview, :created_at, :updated_at
json.url movie_url(movie, format: :json)
