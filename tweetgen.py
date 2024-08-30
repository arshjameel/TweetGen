from ntscraper import Nitter
import random
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import threading

class TweetGenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TweetGen")
        self.root.minsize(500, 500)
        
        # Initialize tweet list and index
        self.tweet_list = []
        self.current_tweet_index = -1
        
        self.default_font = tkfont.Font(family="Consolas", size=12)  # specify font
        self.bg_color = "#ebdbb2"  # dark background
        self.bg_color_alt = "#fbf1c7"  # light background
        self.fg_color = "#282828"  # text color
        self.root.option_add("*Font", self.default_font)  # apply font to widgets
        self.root.option_add("*Background", self.bg_color)  # apply background color to widgets
        self.root.option_add("*Foreground", self.fg_color)  # apply foreground color to widgets
        self.root.configure(bg=self.bg_color)  # apply background color to the entire program
        
        # Configure grid columns and rows
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)  # column for username entry and scrape button
        self.root.grid_columnconfigure(2, weight=0)  # column for the progress bar
        
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=0)  # row for the progress bar
        self.root.grid_rowconfigure(3, weight=1)  # row for the result label

        self.create_widgets() # load GUI Components

    def create_widgets(self):
        # welcome label
        welcome_label = tk.Label(self.root, text="Welcome to TweetGen!\nPlease enter a username and click 'Fetch'.", font=self.default_font, fg=self.fg_color)
        welcome_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="n")
        # username label
        username_label = tk.Label(self.root, text="username: @", font=self.default_font, bg=self.bg_color, fg=self.fg_color)
        username_label.grid(row=1, column=0, padx=(10,0), pady=10, sticky="e")
        # textbox
        self.username_entry = tk.Entry(self.root, width=30, font=self.default_font, bg=self.bg_color_alt, fg=self.fg_color)
        self.username_entry.grid(row=1, column=1, padx=0, pady=10, sticky="ew")
        # scrape/fetch button
        self.scrape_button = tk.Button(self.root, text="Fetch", command=self.start_scraping, font=self.default_font, bg=self.fg_color, fg=self.bg_color)
        self.scrape_button.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        # progress bar
        self.progress_bar = ttk.Progressbar(self.root, mode='determinate')
        self.progress_bar.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.progress_bar.grid_remove()
        # next button (hidden initially)
        self.next_button = tk.Button(self.root, text="Next", command=self.show_next_tweet, font=self.default_font, bg=self.fg_color, fg=self.bg_color)
        self.next_button.grid(row=2, column=1, padx=10, pady=10, sticky="n")
        self.next_button.grid_remove()
        # result label = tweet
        self.result_label = tk.Label(self.root, text="", justify="left", wraplength=480, font=self.default_font, bg=self.bg_color_alt, fg=self.fg_color)
        self.result_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="n")

    def start_scraping(self):
        self.next_button.grid_remove()  # hide the "Next" button
        self.progress_bar.grid()  # show the loading bar
        self.progress_bar.start()  # start the loading bar
        
        username = self.username_entry.get() # get username from user and start scraping
        if username:
            threading.Thread(target=self.scrape_random_tweet, args=(username,)).start()  # scraping done in a new thread to keep the GUI responsive

    def scrape_random_tweet(self, username):
        scraper = Nitter(log_level=0, skip_instance_check=False)  # initialize the scraper with a nitter instance
        try:
            tweets = scraper.get_tweets(username, mode='user', number=50) # set number of tweets to fetch per user
            if isinstance(tweets, dict) and 'tweets' in tweets: # check if 'tweets' is a dictionary and access the correct key
                self.tweet_list = tweets['tweets']
            else:
                self.tweet_list = tweets
            if not self.tweet_list:
                self.result_label.config(text="No tweets found for this user.")
                return
            
            self.current_tweet_index = random.randint(0, len(self.tweet_list) - 1) # choose a random index for the first tweet
            self.show_tweet(self.current_tweet_index)  # show the tweet at the chosen index
            
        # error handling
        except KeyError as e:
            self.result_label.config(text=f"An error occurred while accessing tweets: {e}")
        except Exception as e:
            self.result_label.config(text=f"An unexpected error occurred: {e}")
        finally: # stop and hide the loading bar once fetching is done, then show the "Next" button
            self.progress_bar.stop()
            self.progress_bar.grid_remove()
            self.next_button.grid()
            
    def show_tweet(self, index): # set the tweet format that is to be displayed
        if self.tweet_list:
            tweet = self.tweet_list[index]
            tweet_text = (
                f"\nFrom: @{self.username_entry.get()}"
                f"\nDate: {tweet.get('date', 'Unknown date')}"
                f"\nContent: \n\t{tweet.get('text', 'No content available')}\n"
            )
            self.result_label.config(text=tweet_text)

    def show_next_tweet(self): # goes to the next tweet in the list in a random order
        if self.tweet_list:
            self.current_tweet_index = random.randint(0, len(self.tweet_list) - 1)
            self.show_tweet(self.current_tweet_index)

def main():
    root = tk.Tk()  # create the main window
    app = TweetGenApp(root)
    root.mainloop()  # main loop

if __name__ == "__main__":
    main()