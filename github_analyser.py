import requests
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to fetch GitHub repo data
def fetch_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code != 200:
        messagebox.showerror("Error", f"Failed to fetch data for {username}.")
        return None
    return response.json()

# Function to analyze repositories
def analyze_repos(repos):
    language_count = defaultdict(int)
    total_stars = 0
    total_forks = 0
    
    for repo in repos:
        language = repo['language'] or "Unknown"
        language_count[language] += 1
        total_stars += repo.get('stargazers_count', 0)
        total_forks += repo.get('forks_count', 0)
        
    return language_count, total_stars, total_forks

# Function to update UI and display data
def show_data():
    username = entry.get().strip()
    if not username:
        messagebox.showwarning("Warning", "Please enter a GitHub username!")
        return
    
    repos = fetch_repos(username)
    if not repos:
        return
    
    language_count, total_stars, total_forks = analyze_repos(repos)
    
    # Update labels
    total_repos_label.config(text=f"Total Repositories: {len(repos)}")
    total_stars_label.config(text=f"Total Stars: {total_stars}")
    total_forks_label.config(text=f"Total Forks: {total_forks}")
    
    # Display languages
    language_text.set("\n".join([f"{lang}: {count}" for lang, count in language_count.items()]))
    
    # Show pie chart
    plot_language_distribution(language_count, username)

# Function to plot language distribution
def plot_language_distribution(language_count, username):
    labels = list(language_count.keys())
    sizes = list(language_count.values())
    
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title(f"Language Distribution for {username}")
    
    # Embed Matplotlib chart in Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=7, column=0, columnspan=2)

# Create Tkinter window
window = tk.Tk()
window.title("GitHub Profile Analyzer")
window.geometry("500x600")

# Username Input
tk.Label(window, text="Enter GitHub Username:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
entry = tk.Entry(window, width=30)
entry.grid(row=0, column=1, padx=10, pady=10)

# Fetch Data Button
fetch_button = tk.Button(window, text="Analyze", command=show_data, font=("Arial", 12), bg="blue", fg="white")
fetch_button.grid(row=1, column=0, columnspan=2, pady=10)

# Result Labels
total_repos_label = tk.Label(window, text="Total Repositories: ", font=("Arial", 10))
total_repos_label.grid(row=2, column=0, columnspan=2)

total_stars_label = tk.Label(window, text="Total Stars: ", font=("Arial", 10))
total_stars_label.grid(row=3, column=0, columnspan=2)

total_forks_label = tk.Label(window, text="Total Forks: ", font=("Arial", 10))
total_forks_label.grid(row=4, column=0, columnspan=2)

# Language List
tk.Label(window, text="Languages Used:", font=("Arial", 12)).grid(row=5, column=0, columnspan=2)
language_text = tk.StringVar()
language_label = tk.Label(window, textvariable=language_text, font=("Arial", 10), justify="left")
language_label.grid(row=6, column=0, columnspan=2)

# Run the app
window.mainloop()
