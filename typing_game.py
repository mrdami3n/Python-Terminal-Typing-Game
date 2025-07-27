import os
import random
import time

# --- Platform-specific non-blocking input ---
# This is necessary for the real-time timer. It allows the game to
# check for keystrokes without pausing the entire program.
IS_WINDOWS = False
try:
    # Posix (Linux, macOS)
    import sys
    import tty
    import termios
    import select

    def get_char_non_blocking():
        """Reads a single character from stdin without blocking."""
        # Check if there's input to be read
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.read(1)
        return None

    # We need to set the terminal to "cbreak" mode to read characters
    # instantly without waiting for the user to press Enter.
    # We'll save the old settings to restore them when the game exits.
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    def setup_terminal():
        """Puts the terminal into cbreak mode."""
        tty.setcbreak(sys.stdin.fileno())

    def restore_terminal():
        """Restores the terminal to its original settings."""
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

except ImportError:
    # Windows
    import msvcrt
    IS_WINDOWS = True

    def get_char_non_blocking():
        """Reads a single character from stdin without blocking on Windows."""
        if msvcrt.kbhit():
            # getch() returns a byte string, so we decode it
            return msvcrt.getch().decode('utf-8', errors='ignore')
        return None

    def setup_terminal():
        """No setup needed for Windows."""
        pass

    def restore_terminal():
        """No teardown needed for Windows."""
        pass

# --- Game Configuration ---
TOTAL_LEVELS = 25
STARTING_LIVES = 3
TIME_PER_LEVEL = 60  # in seconds
WORDS_PER_BOSS = 10
POINTS_PER_BOSS = 100

# --- ASCII Art for Bosses ---
# A list of tuples, where each tuple contains the boss name and its ASCII art.
BOSSES = [
    ("Slime Blob", """
       .--.
      / oo \\
     | |  | |
      \\ -- /
       `--'
    """),
    ("Googly Eye", """
      .-----.
     / O   O \\
    |   <   |
     \\  -  /
      `-----'
    """),
    ("Boss Bot", """
     .------.
     |[][][]|
     |[][][]|
     '------'
      |_|--|_|
    """),
    ("Spike", """
        /\\
       /  \\
      /----\\
     /      \\
    /________\\
    """),
    ("Ghostly", """
      .-.
     (o o)
     | O \\
      \\   \\
       `~~~'
    """),
    ("Angry Cloud", """
      .--.
     ( `-' )
    ( (   ) )
     `--'--'
    """),
    ("Skull", """
      .------.
     /  _  _  \\
    |  (o)(o)  |
    |   /\\   |
    |  `--'  |
     \\------/
    """),
    ("Spider", """
      /\\  /\\
     /  \\/  \\
    |  o  o  |
     \\  --  /
      `----'
    """),
    ("Snake", """
        .--.
       /o o \\
       \\  --<
        `---'
       /  /
      /  /
     /  /
    /  /
    `.'
    """),
    ("Bat", """
    \\    /\\    /
     \\  /  \\  /
      \\/o_o\\/
       `---'
    """),
    ("Tentacle Terror", """
        _
       / \\
      / _ \\
     / / \\ \\
    | | O | |
     \\ \\_/ /
      `---'
    """),
    ("Rock Golem", """
      .-----.
     / O   O \\
    |  `---'  |
    | | | | | |
     `-----'
    """),
    ("Evil Tree", """
       /\\
      /  \\
     / o o\\
    |  /\\  |
    | |  | |
     `----'
    """),
    ("UFO", """
       .---.
      /____\\
     ( o o o)
      `---'
    """),
    ("Dragon Head", """
       /\\_/\\
      / o o \\
     (  _  )
      `---'
    """),
    ("Cyber Eye", """
      .------.
     /  .--.  \\
    |  | o  |  |
     \\  `--'  /
      `------'
    """),
    ("Grumpy Cat", """
    /\\_/\\
   ( o.o )
    > ^ <
    """),
    ("Mech Jaw", """
     .------.
     |/\\/\\/\\|
     | o  o |
     |______|
    """),
    ("Cursed Mask", """
      .------.
     /  o  o  \\
    |    ^    |
    |  `---'  |
     \\------/
    """),
    ("Volcano", """
       /\\
      /  \\
     /____\\
    /`----'\\
   /________\\
    """),
    ("Deep Sea Horror", """
        .---.
       / o o \\
      |   J   |
       \\ --- /
      /  |  \\
     /   |   \\
    """),
    ("Crystal Fiend", """
       /\\
      /  \\
     <    >
      \\  /
       \\/
    """),
    ("Void Monster", """
       .....
      .o.o.o.
     .o.o.o.o.
      .o.o.o.
       .....
    """),
    ("Armored Knight", """
      .------.
     |  _ _  |
     | |o|o| |
     |  _|_  |
     `------'
    """),
    ("The Word Master", """
      .------.
     / A B C  \\
    |  D E F   |
     \\ G H I /
      `------'
    """)
]

# --- Word Lists by Difficulty ---
WORDS = {
    "easy": [
        "act", "air", "art", "ask", "awe", "bad", "bag", "ban", "bat", "bed", "bee", "big", "bit", "box", "boy",
        "bug", "bus", "but", "buy", "can", "cap", "car", "cat", "cow", "cry", "cub", "cup", "cut", "dad", "day",
        "den", "did", "dig", "dim", "dog", "dot", "dry", "due", "eat", "egg", "elf", "elk", "end", "era", "fan",
        "far", "fat", "few", "fig", "fin", "fit", "fix", "fly", "fog", "for", "fox", "fun", "fur", "gap", "gas",
        "gem", "get", "gig", "god", "got", "gum", "gun", "gut", "guy", "had", "has", "hat", "hen", "her", "hey",
        "hid", "him", "hip", "his", "hit", "hog", "hop", "hot", "how", "hug", "hum", "hut", "ice", "icy", "ill",
        "ink", "inn", "ion", "its", "ivy", "jam", "jar", "jaw", "jet", "job", "jog", "joy", "jug", "jun", "key"
    ],
    "medium": [
        "able", "acid", "also", "area", "army", "away", "baby", "back", "ball", "band", "bank", "base", "bean",
        "bear", "beat", "bell", "belt", "bend", "best", "bird", "bite", "blow", "blue", "boat", "body", "boil",
        "bold", "bone", "book", "boom", "born", "boss", "both", "bowl", "burn", "bury", "busy", "cake", "call",
        "calm", "came", "camp", "card", "care", "case", "cash", "cast", "cell", "chat", "chip", "city", "club",
        "coal", "coat", "code", "cold", "come", "cook", "cool", "copy", "core", "cost", "crew", "crop", "dark",
        "data", "date", "dawn", "dead", "deal", "dean", "dear", "debt", "deck", "deep", "deer", "desk", "dirt",
        "dish", "dive", "dock", "does", "done", "door", "dose", "down", "draw", "dream", "dress", "drink", "drive",
        "drop", "drug", "drum", "duck", "dull", "dust", "duty", "each", "earn", "east", "easy", "edge", "else"
    ],
    "hard": [
        "ability", "absence", "academy", "account", "accused", "achieve", "acquire", "address", "advance", "advice",
        "against", "airline", "airport", "alcohol", "already", "amazing", "another", "anxiety", "anybody", "anything",
        "anywhere", "appoint", "approve", "arrival", "article", "assault", "athlete", "attempt", "attitude", "average",
        "balance", "balloon", "bargain", "barrier", "battery", "battle", "bearing", "beating", "because", "bedroom",
        "believe", "beneath", "benefit", "besides", "between", "bicycle", "billion", "binding", "breathe", "briefly",
        "brother", "brought", "building", "burning", "business", "cabinet", "calling", "capable", "capital", "captain",
        "capture", "careful", "carrier", "caution", "ceiling", "central", "century", "certain", "chamber", "champion",
        "channel", "chapter", "charity", "chasing", "cheaper", "checking", "chicken", "citizen", "classic", "climate",
        "closing", "clothing", "collect", "college", "combine", "comment", "company", "compare", "compete", "complain"
    ],
    "expert": [
        "abbreviation", "abolishment", "accelerator", "accessible", "accommodation", "accomplishment", "accountability",
        "accreditation", "accumulation", "achievement", "acquaintance", "acquisition", "acrimonious", "adaptability",
        "administrative", "admiration", "admonishment", "advantageous", "advertisement", "affectionately", "affirmation",
        "afterthought", "agglomeration", "aggravating", "agricultural", "altercation", "ambidextrous", "amortization",
        "amplification", "anachronism", "antagonistic", "anthropology", "anticipation", "antidisestablishmentarianism",
        "apologetic", "apothecary", "appreciation", "apprehensive", "appropriation", "archaeologist", "architectural",
        "articulation", "artificial", "asphyxiation", "assassination", "assertiveness", "astonishingly", "astronomical",
        "atrocious", "authoritarian", "autobiography", "availability", "belligerent", "benevolence", "biodegradable",
        "biotechnology", "bureaucracy", "catastrophic", "characteristically", "chronological", "circumference",
        "circumlocution", "circumnavigate", "circumstantial", "classification", "claustrophobia", "collaboration",
        "commemoration", "commercialism", "communication", "comparatively", "compassionate", "compatibility",
        "compensatory", "competitiveness", "comprehensive", "compulsively", "computerization", "conglomerate",
        "congratulatory", "conscientious", "consciousness", "consequential", "conservatory", "consideration",
        "conspicuous", "conspirator", "constitutional", "contemporary", "contradiction", "controversial", "conventional"
    ]
}

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if IS_WINDOWS else 'clear')

def get_word_list(level):
    """Selects a list of random words based on the current level."""
    if 1 <= level <= 5:   difficulty = "easy"
    elif 6 <= level <= 12:  difficulty = "medium"
    elif 13 <= level <= 20: difficulty = "hard"
    else:                   difficulty = "expert"
    available_words = WORDS[difficulty]
    num_to_pick = min(WORDS_PER_BOSS, len(available_words))
    return random.sample(available_words, num_to_pick)

def display_hud(level, score, lives, time_left, words_left):
    """Displays the Heads-Up Display (HUD) with game stats."""
    print("=" * 50)
    print(f" Level: {level}/{TOTAL_LEVELS} | Score: {score} | Lives: {'❤' * lives}")
    print(f" Time Left: {int(time_left):02d}s | Words to Defeat Boss: {words_left}")
    print("=" * 50)

def display_boss(level):
    """Displays the name and ASCII art for the current boss."""
    boss_name, boss_art = BOSSES[level - 1]
    print(f"\n--- BOSS: {boss_name} ---")
    print(boss_art)

# --- Main Game Logic ---

def play_level(level, current_score, current_lives):
    """
    Manages gameplay for a single level with a real-time timer.
    This function now loops continuously, redrawing the screen and
    checking for non-blocking input on each frame.
    """
    start_time = time.time()
    words_to_type = get_word_list(level)
    words_typed_count = 0
    boss_name, _ = BOSSES[level - 1]
    user_input = ""
    
    while True:
        # --- Calculate Timings and Progress ---
        elapsed_time = time.time() - start_time
        time_left = TIME_PER_LEVEL - elapsed_time
        words_left_to_type = len(words_to_type) - words_typed_count

        # --- Check for Win/Loss Conditions ---
        if words_left_to_type <= 0:
            clear_screen()
            display_boss(level)
            print(f"\n*** {boss_name.upper()} DEFEATED! ***")
            time.sleep(2)
            return (True, current_score + POINTS_PER_BOSS, current_lives)

        if time_left <= 0:
            clear_screen()
            print("\n*** TIME'S UP! ***")
            print("You lost a life.")
            time.sleep(2)
            return (False, current_score, current_lives - 1)

        # --- Handle Non-Blocking Input ---
        char = get_char_non_blocking()
        if char:
            if char in ('\r', '\n'):  # Enter key
                if user_input.strip().lower() == words_to_type[words_typed_count]:
                    words_typed_count += 1
                    user_input = ""
                    # BUG FIX: Use 'continue' to restart the loop immediately.
                    # This ensures the win condition is checked before we try
                    # to access the next word, which might not exist.
                    continue
                else:
                    # Incorrect word - just clear the input for now
                    user_input = ""
            # Handle backspace for different OSs
            elif char in ('\x08', '\x7f', '\b'):
                user_input = user_input[:-1]
            elif char == '\x03':  # Ctrl+C
                raise KeyboardInterrupt
            # Ignore other special characters and add valid ones
            elif char.isprintable():
                user_input += char

        # --- Render the Game Screen on Every Frame ---
        clear_screen()
        display_hud(level, current_score, current_lives, time_left, words_left_to_type)
        display_boss(level)
        
        current_word = words_to_type[words_typed_count]
        print(f"\nType this word: -> {current_word} <-")
        # Display the user's current input as they type
        print(f" > {user_input}", end='', flush=True)

        # Control the loop speed to prevent high CPU usage
        time.sleep(0.05)

def game():
    """The main function to run the game."""
    score = 0
    lives = STARTING_LIVES
    level = 1

    # --- Welcome Screen ---
    clear_screen()
    print("=" * 40)
    print("      WELCOME TO TYPING BOSS RUSH!")
    print("=" * 40)
    print("\nDefeat the bosses by typing the words shown.")
    print(f"You have {STARTING_LIVES} lives and {TIME_PER_LEVEL} seconds per level.")
    print("\nPress Enter to start...")
    input()

    # --- Setup and Main Game Loop ---
    setup_terminal()
    try:
        while lives > 0 and level <= TOTAL_LEVELS:
            level_passed, score, lives = play_level(level, score, lives)
            if level_passed:
                level += 1
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nGame exited by user.")
    finally:
        # CRITICAL: Always restore the terminal to its normal state
        restore_terminal()

    # --- Game Over Screen ---
    clear_screen()
    print("=" * 40)
    print("              GAME OVER")
    print("=" * 40)
    if level > TOTAL_LEVELS:
        print("\nCONGRATULATIONS! You defeated all the bosses!")
    else:
        print("\nYou ran out of lives or quit the game.")
        
    print(f"\nFinal Score: {score}")
    print(f"You reached Level: {level -1}")
    print("\nThanks for playing!")


# --- Start the Game ---
if __name__ == "__main__":
    game()
