import streamlit as st
import random
import matplotlib.pyplot as plt
import base64
import os

# --- Set Custom Background ---
def set_bg(img_file):
    try:
        with open(img_file, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Background image not found at path: {img_file}")

# --- Set a Logo ---
def set_logo(logo_path):
    try:
        st.logo(logo_path, size="large", link=None)
    except FileNotFoundError:
        st.warning(f"Logo not found at path: {logo_path}")

# --- Constants and Initialization ---
LOGO_PATH = r"C:/Users/Admin/Desktop/Family/DHARA/WORK/dc/IVAN_CHIBI.jpg"
BG_IMAGE_PATH = r"C:\Users\Admin\Desktop\Family\DHARA\DHANIDHARUCS\SIDE\GAMEHUB_BGDARK.png"

# Assume images are in the same directory as the script.
# Use relative paths for better portability.
script_dir = os.path.dirname(__file__)
set_logo(os.path.join(script_dir, LOGO_PATH))
set_bg(os.path.join(script_dir, BG_IMAGE_PATH))


defaults = {
    "is_logged_in": False,
    "username": "",
    "user_scores": {},
    "page": "login"
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- Game Logic Functions ---
def draw_hangman(attempts_left):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # gallows
    ax.plot([1, 1, 4, 4], [0, 5, 5, 4.2], color="saddlebrown", linewidth=4)
    
    parts_to_draw = 6 - attempts_left
    
    if parts_to_draw >= 1:  # head
        head = plt.Circle((4, 3.8), 0.3, fill=True, color="lightblue", ec="black", lw=2)
        ax.add_patch(head)
    if parts_to_draw >= 2:  # body
        ax.plot([4, 4], [3.5, 2.5], color="white", linewidth=3)
    if parts_to_draw >= 3:  # left arm
        ax.plot([4, 3.6], [3.3, 3.5], color="red", linewidth=3)
    if parts_to_draw >= 4:  # right arm
        ax.plot([4, 4.4], [3.3, 3.5], color="orange", linewidth=3)
    if parts_to_draw >= 5:  # left leg
        ax.plot([4, 3.7], [2.5, 2], color="green", linewidth=3)
    if parts_to_draw >= 6:  # right leg
        ax.plot([4, 4.3], [2.5, 2], color="blue", linewidth=3)

    st.pyplot(fig)
    plt.close(fig)

def handle_guess():
    letter_guess = st.session_state.hangman_input_value
    if letter_guess:
        letter = letter_guess.upper()
        word = st.session_state.hangman_word
        if letter in word:
            st.session_state.hangman_guessed = [letter if word[i] == letter else st.session_state.hangman_guessed[i] for i in range(len(word))]
        else:
            st.session_state.hangman_attempts -= 1
        st.session_state.hangman_input_value = "" # Clear input

def play_hangman():
    if 'hangman_word' not in st.session_state:
        word_list = {"PYTHON": "A popular programming language.", "SCHOOL": "A place for learning.", "COMPUTER": "A machine that processes data."}
        st.session_state.hangman_word = random.choice(list(word_list.keys()))
        st.session_state.hangman_guessed = ["_" for _ in st.session_state.hangman_word]
        st.session_state.hangman_attempts = 6
        st.session_state.hangman_hints = word_list
    
    st.header("Hangman")
    st.write(st.session_state.hangman_hints[st.session_state.hangman_word])
    st.markdown(f"**{' '.join(st.session_state.hangman_guessed)}**", unsafe_allow_html=True)
    st.write(f"Tries left: {st.session_state.hangman_attempts}")
    draw_hangman(st.session_state.hangman_attempts)

    st.text_input("Enter a letter:", max_chars=1, key="hangman_input_value", on_change=handle_guess)

    # Check for win/loss conditions
    if "_" not in st.session_state.hangman_guessed:
        st.success("You won!!")
        st.session_state.user_scores["Hangman"] = st.session_state.user_scores.get("Hangman", 0) + 10
        st.session_state.page = 'main_menu'
        st.session_state.pop('hangman_word', None)
        st.rerun()
    elif st.session_state.hangman_attempts == 0:
        st.error(f"💀 You lost! The word was: {st.session_state.hangman_word}")
        st.session_state.page = 'main_menu'
        st.session_state.pop('hangman_word', None)
        st.rerun()

    if st.button("Exit to Main Menu"):
        st.session_state.page = 'main_menu'
        st.session_state.pop('hangman_word', None)
        st.rerun()

def check_tictactoe_win():
    board = st.session_state.tictactoe_board
    wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    if " " not in board:
        return "Tie"
    return None

def handle_tictactoe_click(i):
    if st.session_state.tictactoe_board[i] == " ":
        st.session_state.tictactoe_board[i] = st.session_state.tictactoe_turn
        st.session_state.tictactoe_turn = "O" if st.session_state.tictactoe_turn == "X" else "X"
        winner = check_tictactoe_win()
        if winner:
            msg = "It's a Tie!" if winner == "Tie" else f"{winner} wins!"
            st.info(msg)
            score = 5 if winner == "Tie" else (10 if winner == "X" else 0)
            st.session_state.user_scores["Tic Tac Toe"] = st.session_state.user_scores.get("Tic Tac Toe", 0) + score
            st.session_state.page = 'main_menu'
            st.session_state.pop('tictactoe_board', None)
            st.session_state.pop('tictactoe_turn', None)
            st.rerun()

def play_tictactoe():
    if 'tictactoe_board' not in st.session_state:
        st.session_state.tictactoe_board = [" "] * 9
        st.session_state.tictactoe_turn = "X"

    st.header("Tic Tac Toe")
    st.write(f"Current Turn: {st.session_state.tictactoe_turn}")

    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            st.button(st.session_state.tictactoe_board[i], key=f"btn_{i}", on_click=handle_tictactoe_click, args=(i,), use_container_width=True)

    if st.button("Exit to Main Menu"):
        st.session_state.page = 'main_menu'
        st.session_state.pop('tictactoe_board', None)
        st.session_state.pop('tictactoe_turn', None)
        st.rerun()

def play_memory():
    if 'memory_cards' not in st.session_state:
        items = ["🍎","🍌","🍇","🍒","🍉","🥝"] * 2
        random.shuffle(items)
        st.session_state.memory_cards = items
        st.session_state.memory_flipped = []
        st.session_state.memory_matched = []
        st.session_state.memory_block_clicks = False

    st.header("Memory Match")

    cols = st.columns(4)
    
    if st.session_state.memory_block_clicks:
        st.info("Wait a moment...")
    
    for i, card in enumerate(st.session_state.memory_cards):
        with cols[i % 4]:
            is_flipped = i in st.session_state.memory_flipped
            is_matched = i in st.session_state.memory_matched
            display_char = card if is_flipped or is_matched else "❓"
            
            if st.button(display_char, key=f"mem{i}", disabled=is_flipped or is_matched or st.session_state.memory_block_clicks, use_container_width=True):
                if len(st.session_state.memory_flipped) < 2:
                    st.session_state.memory_flipped.append(i)
                    st.rerun()
                
    if len(st.session_state.memory_flipped) == 2:
        i1, i2 = st.session_state.memory_flipped
        if st.session_state.memory_cards[i1] == st.session_state.memory_cards[i2]:
            st.session_state.memory_matched.extend([i1, i2])
            st.session_state.user_scores["Memory Match"] = st.session_state.user_scores.get("Memory Match", 0) + 5
            st.session_state.memory_flipped = []
            st.rerun()
        else:
            st.session_state.memory_block_clicks = True
            import time
            time.sleep(1) # Pause to let user see
            st.session_state.memory_flipped = []
            st.session_state.memory_block_clicks = False
            st.rerun()


    if len(st.session_state.memory_matched) == len(st.session_state.memory_cards):
        st.balloons()
        st.success("You matched all pairs!")
        st.session_state.page = 'main_menu'
        st.session_state.pop('memory_cards', None)
        st.rerun()

    if st.button("Exit to Main Menu"):
        st.session_state.page = 'main_menu'
        st.session_state.pop('memory_cards', None)
        st.rerun()

# --- Page Display ---
def handle_login():
    st.session_state.is_logged_in = True
    st.session_state.username = st.session_state.username_input
    st.session_state.page = 'main_menu'
    st.rerun()
    
def show_login_page():
    st.header("Game Hub Login")
    st.text_input("Enter your name:", key="username_input", on_change=handle_login)
    st.button("Login", on_click=handle_login)

def show_main_menu():
    st.header(f"Welcome, {st.session_state.username}!")
    st.write("Choose a game to play:")

    if st.button("Hangman"):
        st.session_state.page = 'hangman'
        st.rerun()

    if st.button("❌⭕ Tic Tac Toe"):
        st.session_state.page = 'tictactoe'
        st.rerun()

    if st.button("Memory Match"):
        st.session_state.page = 'memory'
        st.rerun()

    if st.button("View My Scores"):
        st.session_state.page = 'scores'
        st.rerun()

    if st.button("Log Out"):
        st.session_state.clear()
        st.rerun()
        
def show_user_scores():
    st.header("📊 Your Scores")
    
    if not st.session_state.user_scores:
        st.write("You haven't played any games yet.")
    else:
        for game, score in st.session_state.user_scores.items():
            st.write(f"**{game}**: {score}")
            
    if st.button("⬅️ Back to Main Menu"):
        st.session_state.page = 'main_menu'
        st.rerun()

# --- Main App ---
def main():
    if not st.session_state.is_logged_in:
        show_login_page()
    else:
        page_functions = {
            'main_menu': show_main_menu,
            'hangman': play_hangman,
            'tictactoe': play_tictactoe,
            'memory': play_memory,
            'scores': show_user_scores
        }
        page_functions.get(st.session_state.page, show_main_menu)()

if __name__ == "__main__":
    main()


a='''import streamlit as st
import random
import matplotlib.pyplot as plt
import base64

st.logo(r'C:/Users/Admin/Desktop/Family/DHARA/WORK/dc/IVAN_CHIBI.jpg',size="large",link=None)

# === Set Custom Background ===
def set_bg(img_file):
    with open(img_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# === CHANGE THIS PATH TO YOUR IMAGE ===
set_bg(r"C:/Users/Admin/Desktop/Family/DHARA/DHANIDHARUCS/SIDE/GAMEHUB_BGDARK.png")

# Initialize session state safely
defaults = {
    "is_logged_in": False,
    "username": "",
    "role": "",
    "user_scores": {},
    "page": "login"
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# --- Game Logic Functions ---
def draw_hangman(attempts_left):
    try:
        fig, ax = plt.subplots()
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 6)
        ax.axis("off")

        # gallows
        ax.plot([1, 1, 4, 4], [0, 5, 5, 5], color="saddlebrown", linewidth=4)

        # rope
        ax.plot([4, 4], [5, 4.2], color="goldenrod", linewidth=3)

        # stickman parts (colorful)
        parts = 6 - attempts_left

        if parts >= 1:  # head
            head = plt.Circle((4, 3.8), 0.3, fill=True, color="lightblue", ec="black", lw=2)
            ax.add_patch(head)
        if parts >= 2:  # body
            ax.plot([4, 4], [3.5, 2.5], color="white", linewidth=3)
        if parts >= 3:  # left arm
            ax.plot([4, 3.6], [3.3, 3.5], color="red", linewidth=3)
        if parts >= 4:  # right arm
            ax.plot([4, 4.4], [3.3, 3.5], color="orange", linewidth=3)
        if parts >= 5:  # left leg
            ax.plot([4, 3.7], [2.5, 2], color="green", linewidth=3)
        if parts >= 6:  # right leg
            ax.plot([4, 4.3], [2.5, 2], color="blue", linewidth=3)

        st.pyplot(fig)
    except Exception as e:
        st.error(f"⚠️ Hangman drawing failed: {e}")


def play_hangman():
    try:
        if 'hangman_word' not in st.session_state:
            st.session_state.hangman_word = random.choice(["PYTHON", "SCHOOL", "COMPUTER"])
            st.session_state.hangman_guessed = ["_" for _ in st.session_state.hangman_word]
            st.session_state.hangman_attempts = 6
            st.session_state.hangman_hints = {
                "PYTHON": "Hint: A popular programming language.",
                "SCHOOL": "Hint: A place for learning.",
                "COMPUTER": "Hint: A machine that processes data."
            }
        
        st.header(" Hangman")
        st.write(st.session_state.hangman_hints[st.session_state.hangman_word])
        st.markdown(f"**{' '.join(st.session_state.hangman_guessed)}**", unsafe_allow_html=True)
        st.write(f" Tries left: {st.session_state.hangman_attempts}")
        draw_hangman(st.session_state.hangman_attempts)

        letter_guess = st.text_input("Enter a letter:", max_chars=1)
        
        if st.button("Guess"):
            if letter_guess:
                letter = letter_guess.upper()
                if letter in st.session_state.hangman_word:
                    for i in range(len(st.session_state.hangman_word)):
                        if st.session_state.hangman_word[i] == letter:
                            st.session_state.hangman_guessed[i] = letter
                else:
                    st.session_state.hangman_attempts -= 1

        if "_" not in st.session_state.hangman_guessed:
            st.success("You won!!")
            st.session_state.user_scores["Hangman"] = st.session_state.user_scores.get("Hangman", 0) + 10
            st.session_state.page = 'main_menu'
            st.rerun()
        elif st.session_state.hangman_attempts == 0:
            st.error(f"💀 You lost! The word was: {st.session_state.hangman_word}")
            st.session_state.user_scores["Hangman"] = st.session_state.user_scores.get("Hangman", 0)
            st.session_state.page = 'main_menu'
            st.rerun()

        if st.button("Exit to Main Menu"):
            st.session_state.page = 'main_menu'
            st.rerun()
    except Exception as e:
        st.error(f"⚠️ Hangman crashed: {e}")


def play_tictactoe():
    try:
        if 'tictactoe_board' not in st.session_state:
            st.session_state.tictactoe_board = [" "] * 9
            st.session_state.tictactoe_turn = "X"

        def check_win():
            wins = [(0,1,2), (3,4,5), (6,7,8),
                    (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
            for a, b, c in wins:
                if st.session_state.tictactoe_board[a] == st.session_state.tictactoe_board[b] == st.session_state.tictactoe_board[c] != " ":
                    return st.session_state.tictactoe_board[a]
            if " " not in st.session_state.tictactoe_board:
                return "Tie"
            return None

        st.header("Tic Tac Toe")
        
        cols = st.columns(3)
        for i in range(9):
            with cols[i % 3]:
                if st.button(st.session_state.tictactoe_board[i], key=f"btn_{i}", use_container_width=True):
                    if st.session_state.tictactoe_board[i] == " ":
                        st.session_state.tictactoe_board[i] = st.session_state.tictactoe_turn
                        winner = check_win()
                        if winner:
                            msg = "It's a Tie!" if winner == "Tie" else f"{winner} wins!"
                            st.info(msg)
                            score = 5 if winner == "Tie" else (10 if winner == "X" else 0)
                            st.session_state.user_scores["Tic Tac Toe"] = st.session_state.user_scores.get("Tic Tac Toe", 0) + score
                            st.session_state.page = 'main_menu'
                            st.rerun()
                        st.session_state.tictactoe_turn = "O" if st.session_state.tictactoe_turn == "X" else "X"
                        st.rerun()

        if st.button(" Exit to Main Menu"):
            st.session_state.page = 'main_menu'
            st.rerun()
    except Exception as e:
        st.error(f"⚠️ Tic Tac Toe crashed: {e}")


def play_memory():
    try:
        if 'memory_cards' not in st.session_state:
            items = ["🍎","🍌","🍇","🍒","🍉","🥝"] * 2
            random.shuffle(items)
            st.session_state.memory_cards = items
            st.session_state.memory_flipped = []
            st.session_state.memory_matched = []
        
        st.header("Memory Match")

        cols = st.columns(4)
        for i, card in enumerate(st.session_state.memory_cards):
            with cols[i % 4]:
                if i in st.session_state.memory_matched:
                    st.button(card, key=f"mem_done{i}", disabled=True, use_container_width=True)
                elif i in st.session_state.memory_flipped:
                    st.button(card, key=f"mem_flip{i}", disabled=True, use_container_width=True)
                else:
                    if st.button("❓", key=f"mem{i}", use_container_width=True):
                        st.session_state.memory_flipped.append(i)
        
        if len(st.session_state.memory_flipped) == 2:
            i1, i2 = st.session_state.memory_flipped
            if st.session_state.memory_cards[i1] == st.session_state.memory_cards[i2]:
                st.session_state.memory_matched += [i1, i2]
                st.session_state.user_scores["Memory Match"] = st.session_state.user_scores.get("Memory Match", 0) + 5
            st.session_state.memory_flipped = []
            st.rerun()

        if len(st.session_state.memory_matched) == len(st.session_state.memory_cards):
            st.balloons()
            st.success("You matched all pairs!")
            st.session_state.page = 'main_menu'
            st.rerun()

        if st.button("Exit to Main Menu"):
            st.session_state.page = 'main_menu'
            st.rerun()
    except Exception as e:
        st.error(f"⚠️ Memory Match crashed: {e}")


# --- Page Display ---
def show_login_page():
    st.header("Game Hub Login")
    username = st.text_input("Enter your name:")
    
    if st.button("Login"):
        try:
            if username:
                st.session_state.is_logged_in = True
                st.session_state.username = username
                st.session_state.role = "user"
                st.session_state.page = 'main_menu'
                st.rerun()
        except Exception as e:
            st.error(f"⚠️ Login failed: {e}")


def show_main_menu():
    st.header(f"Welcome, {st.session_state.username}!")
    st.write("Choose a game to play:")

    if st.button("Hangman"):
        st.session_state.page = 'hangman'
        st.rerun()

    if st.button("❌⭕ Tic Tac Toe"):
        st.session_state.page = 'tictactoe'
        st.rerun()

    if st.button("Memory Match"):
        st.session_state.page = 'memory'
        st.rerun()

    if st.button("View My Scores"):
        st.session_state.page = 'scores'
        st.rerun()

    if st.button("Log Out"):
        st.session_state.clear()
        st.rerun()
def show_user_scores():
    st.header("📊 Your Scores")
    
    if not st.session_state.user_scores:
        st.write("You haven't played any games yet.")
    else:
        for game, score in st.session_state.user_scores.items():
            st.write(f"**{game}**: {score}")
            
    if st.button("⬅️ Back to Main Menu"):
        st.session_state.page = 'main_menu'
        st.rerun()


# --- Main App ---
def main():
    try:
        if not st.session_state.is_logged_in:
            show_login_page()
        else:
            if st.session_state.page == 'main_menu':
                show_main_menu()
            elif st.session_state.page == 'hangman':
                play_hangman()
            elif st.session_state.page == 'tictactoe':
                play_tictactoe()
            elif st.session_state.page == 'memory':
                play_memory()
            elif st.session_state.page == 'Scores':
                show_user_scores()
    except Exception as e:
        st.error(f"⚠️ App crashed: {e}")


if __name__ == "__main__":
    main()
'''
