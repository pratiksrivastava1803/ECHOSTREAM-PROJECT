import customtkinter as ctk
from PIL import Image, ImageTk
import os
import requests
import threading
import random
import time
import pygame
from io import BytesIO
from tkinter import font as tkfont


try:
    RESAMPLE_MODE = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE_MODE = getattr(Image, "LANCZOS", Image.ANTIALIAS)

all_movies = []
liked_movies = []
saved_movies = []

OMDB_API_KEY = "584f75b7"


JAMENDO_CLIENT_ID = "00a1bac1" 
JAMENDO_API_BASE = "https://api.jamendo.com/v3.0"

music_tracks = [] 
MOVIE_TITLES1 = [
    "The Shawshank Redemption",
    "The Godfather",
    "The Dark Knight",
    "Pulp Fiction",
    "Forrest Gump",
    "Inception",
    "Fight Club",
    "The Matrix",
    "Goodfellas",
    "The Lord of the Rings",
    "Star Wars",
    "Interstellar",
    "The Prestige",
    "The Lion King",
    "Gladiator",
    "The Departed",
    "The Pianist",
    "Parasite",
    "Whiplash",
    "The Green Mile",

    
    "Saving Private Ryan",
    "Schindler's List",
    "Se7en",
    "The Silence of the Lambs",
    "Titanic",
    "Avengers: Endgame",
    "The Avengers",
    "Iron Man",
    "Black Panther",
    "Doctor Strange",
    "The Wolf of Wall Street",
    "Django Unchained",
    "Once Upon a Time in Hollywood",
    "The Truman Show",
    "A Beautiful Mind",
    "The Social Network",
    "The Curious Case of Benjamin Button",
    "The Grand Budapest Hotel",
    "La La Land",
    "The Revenant",
    "Mad Max: Fury Road",
    "Joker",
    "Shutter Island",
    "Memento",
    "Blade Runner 2049",
    "Arrival",
    "Gravity",
    "The Hurt Locker",
    "Slumdog Millionaire",
    "Life of Pi",
    "Cast Away",
    "The Pursuit of Happyness",
    "12 Years a Slave",
    "Birdman",
    "Her",
    "Eternal Sunshine of the Spotless Mind",
    "The Big Short",
    "Moneyball",
    "The Imitation Game",
    "The Theory of Everything"
]

 

DOWNLOADED_MOVIES = [
    {
        "title": "HP 1 – The Philosopher's Stone",
        "file": r"C:/Users/sriva/OneDrive/Desktop/GUIPROJ/HP 1 The philosophers stone.mkv"
    },
    {
        "title": "HP 2 – The Chamber of Secrets",
        "file": r"C:/Users/sriva/OneDrive/Desktop/GUIPROJ/HP 2 The chamber of secret.mkv"
    },
    {
        "title": "HP 3 – The Prisoner of Azkaban",
        "file": r"C:/Users/sriva/OneDrive/Desktop/GUIPROJ/HP 3 and the Prisoner of Azkaban.mp4"
    },
    {
        "title": "HP 4 – The Goblet of Fire",
        "file": r"C:/Users/sriva/OneDrive/Desktop/GUIPROJ/HP 4 and the Goblet of Fire.mp4"
    },
    {
        "title": "HP 5 – The Order of the Phoenix",
        "file": r"C:/Users/sriva/OneDrive/Desktop/GUIPROJ/HP 5 The order of Phoenix.mkv"
    },
    {
        "title": "HP 6 – The Half-Blood Prince",
        "file": r"C:/Users/sriva/OneDrive/Desktop/GUIPROJ/HP 6 The half blood prince.mkv"
    },
    {
        "title": "HP 7.1 – The Deathly Hallows Part 1",
        "file": r"C:/Users/sriva/OneDrive/Desktop/GUIPROJ/HP 7.1 The deathly Hallows.mkv"
    },
]


SPLASH_MUSIC = r"C:/Users/sriva/OneDrive/Desktop/GUIPROJ/nightfall-future-bass-music-228100.mp3"


def open_main_app(parent):
    
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass

   
    main_app = ctk.CTkToplevel(parent)
    main_app.geometry("1400x1000")
    main_app.title("EchoStream - Main")
    main_app.configure(fg_color="black")

    
    top_bar = ctk.CTkFrame(main_app, height=70, fg_color="#1a1a1a", corner_radius=0)
    top_bar.pack(fill="x", side="top")
    top_bar.pack_propagate(False)

    
    menu_panel = ctk.CTkFrame(main_app, width=220, fg_color="#111111", corner_radius=0)
    menu_open = {"value": False}

    def toggle_menu():
        if menu_open["value"]:
            menu_panel.place_forget()
            menu_open["value"] = False
        else:
            menu_panel.place(x=0, y=70, relheight=1.0)
            menu_panel.lift()
            menu_open["value"] = True

    menubtn = ctk.CTkButton(
        top_bar,
        text="☰",
        width=50,
        height=50,
        font=("Poppins", 24),
        fg_color="#2b2b2b",
        hover_color="#3d3d3d",
        command=toggle_menu
    )
    menubtn.pack(side="left", padx=15, pady=10)

    logo = ctk.CTkLabel(
        top_bar,
        text="EchoStream",
        font=("Poppins", 24, "bold"),
        text_color="#E50914"
    )
    logo.pack(side="left", padx=10)

    seentry = ctk.CTkEntry(
        top_bar,
        placeholder_text="Search Movies",
        width=400,
        height=40,
        font=("Poppins", 14),
        fg_color="#2b2b2b",
        border_color="#3d3d3d"
    )
    seentry.pack(side="left", padx=20, pady=15)

   
    maincont = ctk.CTkScrollableFrame(main_app, fg_color="#0a0a0a")
    maincont.pack(fill="both", expand=True, padx=0, pady=0)

    loadlabel = ctk.CTkLabel(
        maincont,
        text="Loading movies from OMDB please wait",
        font=("Poppins", 18),
        text_color="white"
    )
    loadlabel.pack(pady=100)

    prolabel = ctk.CTkLabel(
        maincont,
        text="0/20 Movies loaded",
        font=("Poppins", 14),
        text_color="#808080"
    )
    prolabel.pack(pady=10)

    
    def fetchapi():
        all_movies.clear()
        global MOVIE_TITLES
        MOVIE_TITLES = random.sample(MOVIE_TITLES1, 20)

        for idx, title in enumerate(MOVIE_TITLES, 1):
            try:
                url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    movie_data = response.json()
                    if movie_data.get("Response") == "True":
                        all_movies.append(movie_data)
                        main_app.after(0, lambda i=idx: update_progress(i))
            except Exception as e:
                print(f"Error fetching {title}: {e}")
                continue

        main_app.after(0, display_movies)

    def update_progress(count):
        if prolabel.winfo_exists():
            prolabel.configure(text=f"loading.{count}/{len(MOVIE_TITLES)}")

    

    def display_movies():
        for widget in maincont.winfo_children():
            widget.destroy()

        if not all_movies:
            errorlb = ctk.CTkLabel(
                maincont,
                text="No movies Loaded. check your internet connection and try again",
                font=('Poppins', 18),
                text_color="red"
            )
            errorlb.pack(pady=100)
            return

        successlb = ctk.CTkLabel(
            maincont,
            text=f"✓ Loaded {len(all_movies)} movies successfully!",
            font=("Poppins", 18, "bold"),
            text_color="#00ff00"
        )
        successlb.pack(pady=20)
        

        grid_frame = ctk.CTkFrame(
            maincont,
            fg_color="transparent"
        )
        grid_frame.pack(fill="both", expand=True, padx=30, pady=20)

        for idx, movie in enumerate(all_movies):
            row = idx // 5
            col = idx % 5
            create_movie_card(grid_frame, movie, row, col)

    
    def add_to_list_unique(lst, movie):
        imdb_id = movie.get("imdbID")
        for m in lst:
            if m.get("imdbID") == imdb_id:
                return
        lst.append(movie)

#Moviesdetail popup
    def open_movie_detail(movie):
        """Opens a popup with detailed info about the movie."""
        detail = ctk.CTkToplevel(main_app)
        detail.title(movie.get("Title", "Movie Details"))
        detail.geometry("900x600")
        detail.configure(fg_color="#050505")

        detail.rowconfigure(0, weight=1)
        detail.columnconfigure(0, weight=1)
        detail.columnconfigure(1, weight=2)

        
        poster_frame = ctk.CTkFrame(detail, fg_color="#101010")
        poster_frame.grid(row=0, column=0, sticky="nsw", padx=20, pady=20)
        poster_frame.grid_rowconfigure(0, weight=1)
        poster_frame.grid_columnconfigure(0, weight=1)

        poster_label = ctk.CTkLabel(
            poster_frame,
            text="Loading poster...",
            width=260,
            height=380,
            fg_color="#202020"
        )
        poster_label.grid(row=0, column=0, padx=10, pady=10)

        # Right: info
        info_frame = ctk.CTkFrame(detail, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        info_frame.grid_columnconfigure(0, weight=1)

        title_text = f"{movie.get('Title', 'N/A')} ({movie.get('Year', 'N/A')})"
        title_label = ctk.CTkLabel(
            info_frame,
            text=title_text,
            font=("Poppins", 28, "bold"),
            text_color="white",
            anchor="w",
            justify="left"
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        rating = movie.get("imdbRating", "N/A")
        votes = movie.get("imdbVotes", "N/A")
        rating_label = ctk.CTkLabel(
            info_frame,
            text=f"⭐ IMDB: {rating}  |  Votes: {votes}",
            font=("Poppins", 16),
            text_color="#FFD700",
            anchor="w",
            justify="left"
        )
        rating_label.grid(row=1, column=0, sticky="w", pady=(0, 10))

        genre = movie.get("Genre", "N/A")
        runtime = movie.get("Runtime", "N/A")
        released = movie.get("Released", "N/A")
        meta_label = ctk.CTkLabel(
            info_frame,
            text=f"Genre: {genre}\nRuntime: {runtime}\nReleased: {released}",
            font=("Poppins", 14),
            text_color="#CCCCCC",
            anchor="w",
            justify="left"
        )
        meta_label.grid(row=2, column=0, sticky="w", pady=(0, 15))

        plot = movie.get("Plot", "No plot information available.")
        plot_label = ctk.CTkLabel(
            info_frame,
            text=plot,
            font=("Poppins", 14),
            text_color="white",
            anchor="nw",
            justify="left",
            wraplength=520
        )
        plot_label.grid(row=3, column=0, sticky="nw", pady=(0, 20))

        director = movie.get("Director", "N/A")
        actors = movie.get("Actors", "N/A")
        credits_label = ctk.CTkLabel(
            info_frame,
            text=f"Director: {director}\nCast: {actors}",
            font=("Poppins", 13),
            text_color="#AAAAAA",
            anchor="w",
            justify="left",
            wraplength=520
        )
        credits_label.grid(row=4, column=0, sticky="w")

        # Buttons (Like, Save for later, Trailer, Close)
        buttons_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        buttons_frame.grid(row=5, column=0, sticky="w", pady=20)

        status_label = ctk.CTkLabel(
            info_frame,
            text="",
            font=("Poppins", 13),
            text_color="#00ff88"
        )
        status_label.grid(row=6, column=0, sticky="w")

        def on_like():
            add_to_list_unique(liked_movies, movie)
            status_label.configure(text="✓ Added to Liked")

        def on_save_later():
            add_to_list_unique(saved_movies, movie)
            status_label.configure(text="✓ Saved for later")

        like_btn = ctk.CTkButton(
            buttons_frame,
            text="♥ Like",
            font=("Poppins", 14, "bold"),
            fg_color="#E50914",
            hover_color="#B20710",
            width=100,
            height=40,
            command=on_like
        )
        like_btn.grid(row=0, column=0, padx=(0, 10))

        save_btn = ctk.CTkButton(
            buttons_frame,
            text="⏰ Save for later",
            font=("Poppins", 14, "bold"),
            fg_color="#444444",
            hover_color="#666666",
            width=150,
            height=40,
            command=on_save_later
        )
        save_btn.grid(row=0, column=1, padx=(0, 10))

        trailer_btn = ctk.CTkButton(
            buttons_frame,
            text="Watch Trailer (coming soon)",
            font=("Poppins", 14),
            fg_color="#333333",
            hover_color="#555555",
            width=220,
            height=40
        )
        trailer_btn.grid(row=1, column=0, columnspan=2, pady=(10, 0))

        close_btn = ctk.CTkButton(
            buttons_frame,
            text="Close",
            font=("Poppins", 14),
            fg_color="#222222",
            hover_color="#444444",
            width=100,
            height=40,
            command=detail.destroy
        )
        close_btn.grid(row=0, column=2)

        # Load poster (reusing existing load_poster in a thread)
        threading.Thread(
            target=load_poster,
            args=(poster_label, movie, main_app),
            daemon=True
        ).start()

    # ---------- Movie card ----------
    def create_movie_card(parent, movie, row, col):
        card_frame = ctk.CTkFrame(
            parent,
            width=200,
            height=320,
            fg_color="#1a1a1a",
            corner_radius=10,
            cursor="hand2"
        )
        card_frame.grid(
            row=row,
            column=col,
            padx=10,
            pady=10,
            sticky="nsew"
        )
        card_frame.grid_propagate(False)

        title_label = ctk.CTkLabel(
            card_frame,
            text=movie.get('Title', 'N/A')[:30],
            font=("Poppins", 11, "bold"),
            text_color="white",
            wraplength=180
        )
        title_label.pack(side="bottom", pady=10)

        poster_label = ctk.CTkLabel(
            card_frame,
            text="Loading.",
            width=180,
            height=260,
            fg_color="#2b2b2b"
        )
        poster_label.pack(pady=(10, 0))

        # Load poster in background thread
        threading.Thread(
            target=load_poster,
            args=(poster_label, movie, main_app),
            daemon=True
        ).start()

        card_frame.bind("<Button-1>", lambda e: movie_clicked(movie))
        poster_label.bind("<Button-1>", lambda e: movie_clicked(movie))
        title_label.bind("<Button-1>", lambda e: movie_clicked(movie))

    # THREAD-SAFE POSTER LOADER
    def load_poster(label, movie, app):
        
        try:
            poster_url = movie.get('Poster', '')

            if poster_url and poster_url != 'N/A':
                import time
                time.sleep(0.2)   

                
                response = requests.get(poster_url, timeout=10)

                if response.status_code == 200:
                    img_data = response.content

                    # MAIN THREAD: all Tk work
                    def on_main_thread():
                        try:
                            if not label.winfo_exists():
                                return

                            img = Image.open(BytesIO(img_data))
                            img = img.resize((180, 260), RESAMPLE_MODE)

                            photo = ctk.CTkImage(
                                light_image=img,
                                dark_image=img,
                                size=(180, 260)
                            )

                            update_poster_label(label, photo)
                            print(f"✓ Loaded: {movie.get('Title')}")
                        except Exception as e_inner:
                            print(f"Error while creating CTkImage for {movie.get('Title')}: {e_inner}")
                            label.configure(
                                text=movie.get('Title', 'N/A')[:20],
                                wraplength=160
                            )

                    app.after(0, on_main_thread)
                    return

            # If no poster / invalid URL
            app.after(0, lambda: label.configure(
                text=movie.get('Title', 'N/A')[:20],
                wraplength=160
            ))

        except Exception as e:
            print(f"Error loading poster for {movie.get('Title')}: {e}")
            import traceback
            traceback.print_exc()
            app.after(0, lambda: label.configure(
                text=movie.get('Title', 'N/A')[:20],
                wraplength=160
            ))

    #  Update poster label 
    def update_poster_label(label, photo):
        
        try:
            if label.winfo_exists():
                label.configure(image=photo, text="")
                label.image = photo  # keep reference
                print("✓ Updated poster successfully")
        except Exception as e:
            print(f"Error in update: {e}")
            import traceback
            traceback.print_exc()

    # ---------- Movie clicked: OPEN DETAIL POPUP ----------
    def movie_clicked(movie):
        print(f"Clicked: {movie.get('Title')}")
        open_movie_detail(movie)

    # ========= SEARCH FEATURE (FULL OMDB SEARCH) =========

    def display_search_results(parent, movies, query):
        """Display search results in grid."""
        for widget in parent.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(
            parent,
            text=f"Search Results for '{query}' ({len(movies)} movies found)",
            font=("Poppins", 24, "bold"),
            text_color="white"
        )
        title_label.pack(pady=20, padx=30, anchor="w")

        grid_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        grid_frame.pack(fill="both", expand=True, padx=30, pady=20)

        for idx, movie in enumerate(movies):
            row = idx // 5
            col = idx % 5
            create_movie_card(grid_frame, movie, row, col)

    def display_no_results(parent, query, error_msg):
        """Show when no movies found."""
        for widget in parent.winfo_children():
            widget.destroy()

        error_label = ctk.CTkLabel(
            parent,
            text=f"No results found for '{query}'\n\n{error_msg}",
            font=("Poppins", 18),
            text_color="red"
        )
        error_label.pack(pady=100)

    def search_in_background(parent, query, app):
        """Search OMDB API in background thread."""
        try:
            url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={query}"
            print(f"Searching URL: {url}")

            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                print(f"API Response: {data.get('Response')}")

                if data.get('Response') == 'True':
                    search_results = data.get('Search', [])
                    print(f"Found {len(search_results)} movies")

                    detailed_movies = []

                    for movie in search_results[:15]:  # limit to 15
                        try:
                            imdb_id = movie.get('imdbID')
                            detail_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}"
                            detail_response = requests.get(detail_url, timeout=5)

                            if detail_response.status_code == 200:
                                movie_details = detail_response.json()
                                detailed_movies.append(movie_details)
                        except Exception as e:
                            print(f"Error fetching details: {e}")
                            continue

                    app.after(0, lambda: display_search_results(parent, detailed_movies, query))
                else:
                    error_message = data.get('Error', 'No results found')
                    app.after(0, lambda: display_no_results(parent, query, error_message))
            else:
                app.after(0, lambda: display_no_results(
                    parent, query, f"HTTP Error {response.status_code}"
                ))
        except Exception as e:
            print(f"Search error: {e}")
            app.after(0, lambda: display_no_results(parent, query, str(e)))

    def search_movies(parent, query):
        """Entry point for search button."""
        query = query.strip()
        if not query:
            print("Please enter a movie name!")
            return

        # Clear current content
        for widget in parent.winfo_children():
            widget.destroy()

        loading_label = ctk.CTkLabel(
            parent,
            text=f"Searching for '{query}'...",
            font=("Poppins", 18),
            text_color="white"
        )
        loading_label.pack(pady=100)

        threading.Thread(
            target=search_in_background,
            args=(parent, query, main_app),
            daemon=True
        ).start()

    # ========= REFRESH MOVIES =========

    def load_movies():
        threading.Thread(target=fetchapi, daemon=True).start()

    def refresh_movies():
        nonlocal loadlabel, prolabel

        for widget in maincont.winfo_children():
            widget.destroy()

        loadlabel = ctk.CTkLabel(
            maincont,
            text="Loading movies from OMDB please wait",
            font=("Poppins", 18),
            text_color="white"
        )
        loadlabel.pack(pady=100)

        prolabel = ctk.CTkLabel(
            maincont,
            text="0/20 Movies loaded",
            font=("Poppins", 14),
            text_color="#808080"
        )
        prolabel.pack(pady=10)

        load_movies()

    # ========= MUSIC MAIN WINDOW (USING JAMENDO) =========

    def open_music_main():
        """Opens a full main window for music (20 tracks grid)."""
        music_win = ctk.CTkToplevel(main_app)
        music_win.title("EchoStream Music")
        music_win.geometry("1200x800")
        music_win.configure(fg_color="black")

        top = ctk.CTkFrame(music_win, height=70, fg_color="#1a1a1a", corner_radius=0)
        top.pack(fill="x", side="top")
        top.pack_propagate(False)

        title = ctk.CTkLabel(
            top,
            text="EchoStream Music",
            font=("Poppins", 24, "bold"),
            text_color="#1DB954"
        )
        title.pack(side="left", padx=20)

        search_entry = ctk.CTkEntry(
            top,
            placeholder_text="Search tracks / artist",
            width=400,
            height=40,
            font=("Poppins", 14),
            fg_color="#2b2b2b",
            border_color="#3d3d3d"
        )
        search_entry.pack(side="left", padx=20, pady=15)

        music_maincont = ctk.CTkScrollableFrame(music_win, fg_color="#050505")
        music_maincont.pack(fill="both", expand=True, padx=0, pady=0)

        loading_label = ctk.CTkLabel(
            music_maincont,
            text="Loading tracks from Jamendo...",
            font=("Poppins", 18),
            text_color="white"
        )
        loading_label.pack(pady=80)

        status_label = ctk.CTkLabel(
            music_maincont,
            text="",
            font=("Poppins", 13),
            text_color="#00ff88"
        )
        status_label.pack()

        # LOCAL list for tracks in this window
        tracks_list = []

        # ---- Jamendo fetch ----
        def fetch_tracks(query=None):
            nonlocal tracks_list
            tracks_list.clear()

            params = {
                "client_id": JAMENDO_CLIENT_ID,
                "format": "json",
                "limit": 20,
                "audioformat": "mp31",
                "order": "popularity_total"
            }
            if query:
                params["search"] = query

            try:
                url = f"{JAMENDO_API_BASE}/tracks"
                print(f"Jamendo request: {url} params={params}")
                resp = requests.get(url, params=params, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    results = data.get("results", [])
                    tracks_list.extend(results)
                    music_win.after(0, lambda: display_tracks(query))
                else:
                    music_win.after(0, lambda: show_tracks_error(f"HTTP {resp.status_code}"))
            except Exception as e:
                print(f"Jamendo error: {e}")
                music_win.after(0, lambda: show_tracks_error(str(e)))

        def display_tracks(query=None):
            for w in music_maincont.winfo_children():
                w.destroy()

            header_text = "Popular Tracks" if not query else f"Results for '{query}'"
            header = ctk.CTkLabel(
                music_maincont,
                text=header_text,
                font=("Poppins", 22, "bold"),
                text_color="white"
            )
            header.pack(pady=20, padx=30, anchor="w")

            if not tracks_list:
                no_lbl = ctk.CTkLabel(
                    music_maincont,
                    text="No tracks found.",
                    font=("Poppins", 16),
                    text_color="red"
                )
                no_lbl.pack(pady=40)
                return

            grid_frame = ctk.CTkFrame(music_maincont, fg_color="transparent")
            grid_frame.pack(fill="both", expand=True, padx=30, pady=10)

            for idx, track in enumerate(tracks_list):
                row = idx // 5
                col = idx % 5
                create_music_card(grid_frame, track, row, col, music_win)

        def show_tracks_error(msg):
            for w in music_maincont.winfo_children():
                w.destroy()
            err = ctk.CTkLabel(
                music_maincont,
                text=f"Error loading tracks:\n{msg}",
                font=("Poppins", 16),
                text_color="red"
            )
            err.pack(pady=80)

        # ---- Music card & cover loader ----
        def create_music_card(parent, track, row, col, app):
            card = ctk.CTkFrame(
                parent,
                width=200,
                height=260,
                fg_color="#111111",
                corner_radius=10,
                cursor="hand2"
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            card.grid_propagate(False)

            cover_label = ctk.CTkLabel(
                card,
                text="Loading",
                width=180,
                height=180,
                fg_color="#333333"
            )
            cover_label.pack(pady=(10, 5))

            name = track.get("name", "Unknown")
            artist = track.get("artist_name", "Unknown Artist")

            title_lbl = ctk.CTkLabel(
                card,
                text=f"{name[:22]}",
                font=("Poppins", 11, "bold"),
                text_color="white",
                wraplength=180
            )
            title_lbl.pack(pady=(0, 2))

            artist_lbl = ctk.CTkLabel(
                card,
                text=artist[:22],
                font=("Poppins", 10),
                text_color="#AAAAAA",
                wraplength=180
            )
            artist_lbl.pack()

            # load cover
            image_url = track.get("image")
            threading.Thread(
                target=load_cover_image,
                args=(cover_label, image_url, app),
                daemon=True
            ).start()

            card.bind("<Button-1>", lambda e: open_track_player(track, app))
            cover_label.bind("<Button-1>", lambda e: open_track_player(track, app))
            title_lbl.bind("<Button-1>", lambda e: open_track_player(track, app))
            artist_lbl.bind("<Button-1>", lambda e: open_track_player(track, app))

        def load_cover_image(label, image_url, app):
            try:
                if not image_url:
                    app.after(0, lambda: label.configure(text="No Cover"))
                    return

                resp = requests.get(image_url, timeout=10)
                if resp.status_code == 200:
                    img_data = resp.content

                    def on_main():
                        try:
                            if not label.winfo_exists():
                                return
                            img = Image.open(BytesIO(img_data))
                            img = img.resize((180, 180), RESAMPLE_MODE)
                            photo = ctk.CTkImage(
                                light_image=img,
                                dark_image=img,
                                size=(180, 180)
                            )
                            label.configure(image=photo, text="")
                            label.image = photo
                        except Exception as e:
                            print(f"Cover error: {e}")
                            label.configure(text="Error")

                    app.after(0, on_main)
                else:
                    app.after(0, lambda: label.configure(text="No Cover"))
            except Exception as e:
                print(f"Cover load error: {e}")
                app.after(0, lambda: label.configure(text="Error"))

        # ---- Track player window ----
        def open_track_player(track, app):
            player = ctk.CTkToplevel(app)
            player.title(track.get("name", "Track"))
            player.geometry("700x400")
            player.configure(fg_color="#050505")

            left = ctk.CTkFrame(player, fg_color="#111111")
            left.pack(side="left", fill="both", expand=False, padx=20, pady=20)

            right = ctk.CTkFrame(player, fg_color="transparent")
            right.pack(side="right", fill="both", expand=True, padx=20, pady=20)

            cover_label = ctk.CTkLabel(
                left,
                text="Loading cover...",
                width=260,
                height=260,
                fg_color="#222222"
            )
            cover_label.pack(padx=10, pady=10)

            image_url = track.get("image")
            threading.Thread(
                target=load_cover_image,
                args=(cover_label, image_url, player),
                daemon=True
            ).start()

            name = track.get("name", "Unknown")
            artist = track.get("artist_name", "Unknown Artist")
            album = track.get("album_name", "Unknown Album")

            title_lbl = ctk.CTkLabel(
                right,
                text=name,
                font=("Poppins", 24, "bold"),
                text_color="white",
                anchor="w",
                justify="left"
            )
            title_lbl.pack(anchor="w", pady=(0, 10))

            artist_lbl = ctk.CTkLabel(
                right,
                text=f"Artist: {artist}\nAlbum: {album}",
                font=("Poppins", 14),
                text_color="#cccccc",
                anchor="w",
                justify="left"
            )
            artist_lbl.pack(anchor="w", pady=(0, 20))

            status_lbl = ctk.CTkLabel(
                right,
                text="Status: Stopped",
                font=("Poppins", 13),
                text_color="#00ff88",
                anchor="w",
                justify="left"
            )
            status_lbl.pack(anchor="w", pady=(0, 20))

            btn_frame = ctk.CTkFrame(right, fg_color="transparent")
            btn_frame.pack(anchor="w", pady=10)

            audio_url = track.get("audio")  # Jamendo streaming URL
            cache_dir = "music_cache"
            os.makedirs(cache_dir, exist_ok=True)
            local_file = os.path.join(cache_dir, f"{track.get('id', 'track')}.mp3")

            def ensure_mixer():
                if not pygame.mixer.get_init():
                    pygame.mixer.init()

            def download_and_play():
                try:
                    ensure_mixer()
                    if not os.path.exists(local_file):
                        status_lbl.configure(text="Status: Downloading...")
                        r = requests.get(audio_url, stream=True, timeout=20)
                        if r.status_code == 200:
                            with open(local_file, "wb") as f:
                                for chunk in r.iter_content(chunk_size=4096):
                                    if chunk:
                                        f.write(chunk)
                        else:
                            player.after(0, lambda: status_lbl.configure(
                                text=f"Error: HTTP {r.status_code}"
                            ))
                            return
                    pygame.mixer.music.load(local_file)
                    pygame.mixer.music.play()
                    player.after(0, lambda: status_lbl.configure(text="Status: Playing"))
                except Exception as e:
                    player.after(0, lambda: status_lbl.configure(text=f"Error: {e}"))

            def on_play():
                if not audio_url:
                    status_lbl.configure(text="No audio URL provided by API")
                    return
                threading.Thread(target=download_and_play, daemon=True).start()

            def on_pause():
                try:
                    pygame.mixer.music.pause()
                    status_lbl.configure(text="Status: Paused")
                except Exception as e:
                    status_lbl.configure(text=f"Error: {e}")

            def on_resume():
                try:
                    pygame.mixer.music.unpause()
                    status_lbl.configure(text="Status: Playing")
                except Exception as e:
                    status_lbl.configure(text=f"Error: {e}")

            def on_stop():
                try:
                    pygame.mixer.music.stop()
                    status_lbl.configure(text="Status: Stopped")
                except Exception as e:
                    status_lbl.configure(text=f"Error: {e}")

            play_btn = ctk.CTkButton(btn_frame, text="Play", width=80, command=on_play)
            play_btn.grid(row=0, column=0, padx=5, pady=5)

            pause_btn = ctk.CTkButton(btn_frame, text="Pause", width=80, command=on_pause)
            pause_btn.grid(row=0, column=1, padx=5, pady=5)

            resume_btn = ctk.CTkButton(btn_frame, text="Resume", width=80, command=on_resume)
            resume_btn.grid(row=0, column=2, padx=5, pady=5)

            stop_btn = ctk.CTkButton(btn_frame, text="Stop", width=80, command=on_stop)
            stop_btn.grid(row=0, column=3, padx=5, pady=5)

        # ---- search inside music window ----
        def on_music_search():
            q = search_entry.get().strip()
            if not q:
                # load popular tracks again
                for w in music_maincont.winfo_children():
                    w.destroy()
                lbl = ctk.CTkLabel(
                    music_maincont,
                    text="Loading tracks from Jamendo...",
                    font=("Poppins", 18),
                    text_color="white"
                )
                lbl.pack(pady=80)
                threading.Thread(target=fetch_tracks, daemon=True).start()
            else:
                for w in music_maincont.winfo_children():
                    w.destroy()
                lbl = ctk.CTkLabel(
                    music_maincont,
                    text=f"Searching '{q}'...",
                    font=("Poppins", 18),
                    text_color="white"
                )
                lbl.pack(pady=80)
                threading.Thread(target=fetch_tracks, args=(q,), daemon=True).start()

        music_search_btn = ctk.CTkButton(
            top,
            text="Search",
            width=80,
            height=40,
            font=("Poppins", 14),
            fg_color="#1DB954",
            hover_color="#169d40",
            command=on_music_search
        )
        music_search_btn.pack(side="left", padx=10, pady=15)

        # initial load
        threading.Thread(target=fetch_tracks, daemon=True).start()

    # ========= HAMBURGER MENU WINDOWS =========

    def open_downloaded_window():
        win = ctk.CTkToplevel(main_app)
        win.title("Downloaded Movies")
        win.geometry("600x400")
        win.configure(fg_color="#101010")

        info_label = ctk.CTkLabel(
            win,
            text="DOWNLOADED"
                 ,
            font=("Poppins", 14),
            text_color="white",
            justify="left"
        )
        info_label.pack(pady=10, padx=10, anchor="w")

        list_frame = ctk.CTkFrame(win, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=20, pady=20)

        status_label = ctk.CTkLabel(
            win,
            text="",
            font=("Poppins", 13),
            text_color="#00ff88"
        )
        status_label.pack(pady=(0, 10))

        def make_play_func(path, title):
            def _play():
                if os.path.exists(path):
                    try:
                        os.startfile(path)  # Opens with default OS video player (Windows)
                        status_label.configure(text=f"▶ Playing {title}")
                    except Exception as e:
                        status_label.configure(text=f"Error playing file: {e}")
                else:
                    status_label.configure(text=f"File not found: {path}")
            return _play

        for movie in DOWNLOADED_MOVIES:
            row_frame = ctk.CTkFrame(list_frame, fg_color="#1c1c1c")
            row_frame.pack(fill="x", pady=5)

            title_lbl = ctk.CTkLabel(
                row_frame,
                text=movie["title"],
                font=("Poppins", 14),
                text_color="white",
                anchor="w"
            )
            title_lbl.pack(side="left", padx=10, pady=8, fill="x", expand=True)

            play_btn = ctk.CTkButton(
                row_frame,
                text="Play",
                width=80,
                height=30,
                font=("Poppins", 13, "bold"),
                fg_color="#E50914",
                hover_color="#B20710",
                command=make_play_func(movie["file"], movie["title"])
            )
            play_btn.pack(side="right", padx=10, pady=5)

    def open_liked_window():
        win = ctk.CTkToplevel(main_app)
        win.title("Liked Movies")
        win.geometry("1000x700")
        win.configure(fg_color="#050505")

        if not liked_movies:
            lbl = ctk.CTkLabel(
                win,
                text="No liked movies yet.\nOpen a movie and press ♥ Like in the details.",
                font=("Poppins", 16),
                text_color="white",
                justify="center"
            )
            lbl.pack(expand=True)
            return

        scroll = ctk.CTkScrollableFrame(win, fg_color="#050505")
        scroll.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(
            scroll,
            text=f"Liked Movies ({len(liked_movies)})",
            font=("Poppins", 24, "bold"),
            text_color="white"
        )
        title_label.pack(pady=10, anchor="w")

        grid_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        for idx, movie in enumerate(liked_movies):
            row = idx // 5
            col = idx % 5
            create_movie_card(grid_frame, movie, row, col)

    def open_saved_window():
        win = ctk.CTkToplevel(main_app)
        win.title("Saved For Later")
        win.geometry("1000x700")
        win.configure(fg_color="#050505")

        if not saved_movies:
            lbl = ctk.CTkLabel(
                win,
                text="No movies saved for later yet.\nOpen a movie and press ⏰ Save for later.",
                font=("Poppins", 16),
                text_color="white",
                justify="center"
            )
            lbl.pack(expand=True)
            return

        scroll = ctk.CTkScrollableFrame(win, fg_color="#050505")
        scroll.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(
            scroll,
            text=f"Saved For Later ({len(saved_movies)})",
            font=("Poppins", 24, "bold"),
            text_color="white"
        )
        title_label.pack(pady=10, anchor="w")

        grid_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        for idx, movie in enumerate(saved_movies):
            row = idx // 5
            col = idx % 5
            create_movie_card(grid_frame, movie, row, col)

    def open_info_window():
        win = ctk.CTkToplevel(main_app)
        win.title("Project Info")
        win.geometry("600x400")
        win.configure(fg_color="#050505")

        title_label = ctk.CTkLabel(
            win,
            text="EchoStream Project",
            font=("Poppins", 24, "bold"),
            text_color="white"
        )
        title_label.pack(pady=(20, 10))

        info_text = (
            "This application was built as a GUI movie & music browser demo.\n\n"
            "Technologies used:\n"
            "- Python\n"
            "- customtkinter\n"
            "- OMDB API for movie data\n"
            "- Jamendo API for music\n"
            "- Pygame for audio playback\n\n"
            "Developers:\n"
            "- Pratik Srivastava(logic, design, concept)\n"
            "- Vatsal Soni"
            "- Rishi Tambi"
            "- \n\n"
            "This is a learning project to practice Python, GUI, APIs, and app structure."
        )

        info_label = ctk.CTkLabel(
            win,
            text=info_text,
            font=("Poppins", 14),
            text_color="#dddddd",
            justify="left",
            wraplength=540
        )
        info_label.pack(padx=20, pady=10, anchor="w")

    # Build the content of menu_panel
    menu_title = ctk.CTkLabel(
        menu_panel,
        text="  ☰  Menu",
        font=("Poppins", 20, "bold"),
        text_color="white",
        anchor="w"
    )
    menu_title.pack(pady=(15, 10), padx=15, anchor="w")

    btn_downloaded = ctk.CTkButton(
        menu_panel,
        text="Downloaded",
        font=("Poppins", 16),
        fg_color="#222222",
        hover_color="#333333",
        anchor="w",
        command=open_downloaded_window
    )
    btn_downloaded.pack(fill="x", padx=15, pady=5)

    # MUSIC PLAYER -> now opens the MUSIC MAIN PAGE
    btn_music = ctk.CTkButton(
        menu_panel,
        text="Music Player",
        font=("Poppins", 16),
        fg_color="#222222",
        hover_color="#333333",
        anchor="w",
        command=open_music_main
    )
    btn_music.pack(fill="x", padx=15, pady=5)

    btn_liked = ctk.CTkButton(
        menu_panel,
        text="Liked",
        font=("Poppins", 16),
        fg_color="#222222",
        hover_color="#333333",
        anchor="w",
        command=open_liked_window
    )
    btn_liked.pack(fill="x", padx=15, pady=5)

    btn_saved = ctk.CTkButton(
        menu_panel,
        text="Saved For Later",
        font=("Poppins", 16),
        fg_color="#222222",
        hover_color="#333333",
        anchor="w",
        command=open_saved_window
    )
    btn_saved.pack(fill="x", padx=15, pady=5)

    btn_info = ctk.CTkButton(
        menu_panel,
        text="Info",
        font=("Poppins", 16),
        fg_color="#222222",
        hover_color="#333333",
        anchor="w",
        command=open_info_window
    )
    btn_info.pack(fill="x", padx=15, pady=5)

    # ---------- Buttons on top bar ----------
    search_btn = ctk.CTkButton(
        top_bar,
        text="🔍",
        width=50,
        height=40,
        font=("Poppins", 18),
        fg_color="#2b2b2b",
        hover_color="#3d3d3d",
        command=lambda: search_movies(maincont, seentry.get())
    )
    search_btn.pack(side="left", padx=(0, 20), pady=15)

    refresh_btn = ctk.CTkButton(
        top_bar,
        text="⟳ Refresh",
        width=120,
        height=40,
        font=("Poppins", 14, "bold"),
        fg_color="#E50914",
        hover_color="#B20710",
        command=refresh_movies
    )
    refresh_btn.pack(side="right", padx=15, pady=15)

    # auto load on open
    main_app.after(500, load_movies)



def front():
    app = ctk.CTk()
    app.geometry("1400x1000")
    app.title("EchoStream")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    try:
        custom_font_path = "Poppins-Bold.ttf"
        custom_font_regular = "Poppins-Regular.ttf"
        custom_font_italic = "Poppins-Italic.ttf"
    except Exception:
        pass

    
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(SPLASH_MUSIC)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Could not start splash music: {e}")

    
    app.rowconfigure(0, weight=1)
    app.columnconfigure(0, weight=2)
    app.columnconfigure(1, weight=1)

    frame2 = ctk.CTkFrame(app, fg_color="#1a1a1a")
    frame2.grid(row=0, column=1, sticky="nsew")

    content_frame = ctk.CTkFrame(frame2, fg_color="transparent")
    content_frame.place(relx=0.5, rely=0.5, anchor="center")

    welcome_label = ctk.CTkLabel(
        content_frame,
        text="Welcome to",
        font=("Poppins", 36),
        text_color="white"
    )
    welcome_label.pack(pady=(0, 5))

    title_label = ctk.CTkLabel(
        content_frame,
        text="EchoStream",
        font=("Poppins", 62, "bold"),
        text_color="Red"
    )
    title_label.pack(pady=(0, 10))

    tagline_label = ctk.CTkLabel(
        content_frame,
        text="Where movies and music meet",
        font=("Poppins", 18, "italic"),
        text_color="white"
    )
    tagline_label.pack(pady=(0, 50))

    get_started_btn = ctk.CTkButton(
        content_frame,
        text="Get Started",
        font=("Poppins", 20, "bold"),
        fg_color="red",
        hover_color="#cc0000",
        width=220,
        height=55,
        corner_radius=10,
        command=lambda: open_main_app(app)
    )
    get_started_btn.pack()
    

    
    list1 = [
         "down3.png", "down4.jpg",
        "down5.png", "down6.jpg", "down7.jpg", "down8.jpg",
         "download10.jpg", "download11.jpg","down31.jpg","down32.jpg","down33.jpg","down34.jpg","down36.jpg","down37.jpg"
    ]

    canvas1 = ctk.CTkCanvas(app, bg="#000000", highlightthickness=0)
    canvas1.grid(row=0, column=0, sticky="nsew")

    current_index = [0]
    photo_reference = [None]

    def display_image():
        canvas_width = canvas1.winfo_width()
        canvas_height = canvas1.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return

        img_path = list1[current_index[0]]

        try:
            img = Image.open(img_path)
            img_resized = img.resize((canvas_width, canvas_height), RESAMPLE_MODE)

            photo_reference[0] = ImageTk.PhotoImage(img_resized)

            canvas1.delete("all")
            canvas1.create_image(0, 0, image=photo_reference[0], anchor="nw")

        except FileNotFoundError:
            canvas1.delete("all")
            canvas1.create_text(
                canvas_width // 2,
                canvas_height // 2,
                text=f"Image not found: {img_path}",
                fill="white",
                font=("Arial", 20)
            )

    def update_slideshow():
        display_image()
        current_index[0] = (current_index[0] + 1) % len(list1)
        app.after(3000, update_slideshow)

    def on_canvas_resize(event):
        display_image()

    canvas1.bind("<Configure>", on_canvas_resize)
    app.after(200, update_slideshow)

    app.mainloop()

    try:
        pygame.mixer.music.stop()
    except Exception:
        pass



if __name__ == "__main__":
    front()
