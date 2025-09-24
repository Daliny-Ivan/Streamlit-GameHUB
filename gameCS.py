import streamlit as st
import random
import matplotlib.pyplot as plt
import base64
import os

#-----------------------------------------------------------------Take Folder from File
script_dir = os.path.dirname(os.path.abspath(__file__))
BG_LIGHT = os.path.join(script_dir, "assets", "GAMEHUB_BG_LIGHT.png")
BG_DARK = os.path.join(script_dir, "assets", "GAMEHUB_BG_DARK.png")


#----------------------------------------------------------------Theme (DARK/LIGHT)
def set_theme(theme):
    bg_img = BG_LIGHT if theme == "Light" else BG_DARK
    text_color = "#26c0fc" if theme == "Light" else "skyblue"
    try:
        with open(bg_img, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            color: {text_color};
        }}
        /* Force all text and headers to match theme */
        h1, h2, h3, h4, h5, h6, p, span, div, label {{
            color: {text_color} !important;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Background/theme error: {e}")
theme = st.sidebar.selectbox("Choose Theme", ["Light", "Dark"])
set_theme(theme)



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
        ax.plot([4, 4], [3.5, 2.5], color="red", linewidth=3)
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
    
def show_login_page():
    st.header(" ")
    st.header(" ")
    st.header("Game Hub Login")
    st.text_input("Enter your name:", key="username_input", on_change=handle_login)
    st.button("Login", on_click=handle_login)

def show_main_menu():
    st.header(" ")   #To add space between text start and the header in bg
    st.header(" ")      # cz it was overlapping
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







