import streamlit as st
import datetime
import pytz
import random
import os

# --- Configuration ---
EID_DATE = datetime.date(2025, 3, 31)  # Approximate Eid date for 2025
SAVE_FILE = "save.txt"  # File to store user wishes

COLORS = {
    "primary": "#8B008B", 
    "background": "#FFF8DC", 
    "wish_box": "#E6E6FA", 
    "eid_green": "#4CAF50"
}

WISHES = {
    "Family": [
        "Eid Mubarak to my wonderful family! May our bond strengthen and our joy multiply.",
        "To my amazing family, Eid greetings! May Allah's blessings shower upon us all.",
        "May this Eid bring you and your family immense happiness and prosperity.",
        "To my family, may the spirit of Eid fill our hearts with love and unity.",
    ],
    "Friend": [
        "Wishing my dearest friend a blessed Eid filled with laughter and cherished moments.",
        "Eid Mubarak Friend! Let's celebrate this joyous occasion together.",
        "Sending warm Eid wishes to my beloved friend. May your day be filled with peace.",
        "Eid Mubarak Beautiful! Wishing you a day as bright as your smiles.",
    ],
    "Cousin": [
        "Eid Mubarak to my awesome cousin! May this Eid be filled with fun and laughter.",
        "Wishing my cousin a joyous Eid filled with sweet memories.",
        "To my dear cousin, may this Eid bring us closer together.",
        "Eid Mubarak, cousin! Let's make this Eid unforgettable.",
    ],
    "Siblings": [
        "Eid Mubarak to my amazing siblings! May our bond continue to grow stronger.",
        "Wishing my siblings a blessed Eid filled with joy and happiness.",
        "To my wonderful siblings, may this Eid bring us closer than ever.",
        "Eid Mubarak, siblings! Let's cherish the moments we share.",
    ],
}

# --- Functions ---
def save_wish(sender, wish):
    """Save user wish to a text file."""
    with open(SAVE_FILE, "a") as file:
        file.write(f"{sender}|{wish}\n")

def load_wishes():
    """Load saved wishes from file."""
    wishes = []
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            wishes = [line.strip().split("|") for line in file.readlines()]
    return wishes

def delete_wish(sender, wish):
    """Delete a specific wish from the file."""
    wishes = load_wishes()
    with open(SAVE_FILE, "w") as file:
        for s, w in wishes:
            if s != sender or w != wish:  # Keep other wishes
                file.write(f"{s}|{w}\n")

def display_eid_wishes(name, category):
    """Displays a random Eid wish for the given name and category."""
    st.markdown(
        f"<h3 style='text-align: center; color: {COLORS['primary']}'>Eid Wishes for {name} 🎉</h3>", 
        unsafe_allow_html=True
    )
    wish = random.choice(WISHES[category])
    st.markdown(
        f"""
        <div style='background-color: {COLORS['wish_box']}; padding: 20px; border-radius: 10px; text-align: center; margin: 10px 0;'>
            <p style='font-size: 18px;'>{wish}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
def display_countdown():
    """Displays a countdown to Eid or an 'Eid Mubarak' message."""
    # Ensure the correct timezone (Set to your local timezone if needed)
    tz = pytz.timezone("Asia/Karachi")  # Change according to your region
    today = datetime.datetime.now(tz).date()  # Use timezone-aware date
    days_until_eid = (EID_DATE - today).days

    # Ensure it does not display an extra day
    if days_until_eid < 0:
        days_until_eid = 0

    if days_until_eid > 0:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 20px; border-radius: 10px; background-color: {COLORS['background']}; margin-bottom: 20px;'>
                <p style='font-size: 28px; color: {COLORS['primary']}; font-weight: bold;'>{days_until_eid} days until Eid! 🎊</p>
                <p style='font-size: 18px;'>Get ready for a joyous celebration!</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    elif days_until_eid == 0:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 30px; border-radius: 15px; background-color: {COLORS['eid_green']}; margin-bottom: 20px;'>
                <p style='font-size: 36px; color: white; font-weight: bold;'>🎉 Eid Mubarak! 🎉</p>
                <p style='font-size: 22px; color: white;'>May your Eid be filled with joy and blessings.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style='text-align: center; padding: 20px; border-radius: 10px; background-color: #f0f0f0; margin-bottom: 20px;'>
                <p style='font-size: 24px; color: #888;'>Eid has passed. Wishing you continued blessings. 🌙</p>
            </div>
            """,
            unsafe_allow_html=True
        )

def user_input_wish():
    """Allows the user to input and manage their personalized Eid wishes."""
    st.markdown(
        f"<h4 style='text-align: center; color: {COLORS['primary']}'> Send Best Wishes to Rida Fatima!💌</h4>", 
        unsafe_allow_html=True
    )
    sender_name = st.text_input("Enter Your Name:")
    user_wish = st.text_area("Write your personalized Eid wish:")

    if st.button("Send Wishes 💖"):
        if not sender_name or not user_wish:
            st.warning("⚠️ Please enter your name and a wish.")
        else:
            save_wish(sender_name, user_wish)
            st.success("✅ Your wish has been saved!")

    # --- Display saved wishes ---
    st.markdown(f"<h3 style='text-align: center; color: {COLORS['primary']}'>📜 Wishes Received by Rida:</h3>", unsafe_allow_html=True)
    wishes = load_wishes()
    
    if not wishes:
        st.info("No wishes sent yet.")
    else:
        for sender, wish in wishes:
            with st.expander(f"💌 {sender}'s Wish"):
                st.write(wish)
                if st.button(f"🗑 Delete Wish", key=f"delete_{sender}_{wish}"):
                    delete_wish(sender, wish)
                    st.rerun()

# --- Main App ---
st.set_page_config(page_title="Eid Wishes App", page_icon="🌙", layout="centered")
st.markdown(
    f"<h1 style='text-align: center; color: {COLORS['primary']}'>Eid Ul Fitr Greetings!🌙</h1>", 
    unsafe_allow_html=True
)

# Eid Wishes Section
st.markdown("<br>", unsafe_allow_html=True)
name_input = st.text_input("Enter a name to generate a wish:")
category_select = st.selectbox("Select Category:", list(WISHES.keys()))

if name_input:
    display_eid_wishes(name_input, category_select)

display_countdown()
user_input_wish()

# Footer
st.markdown("----------------------------------------------------------------------------------------------------")
st.markdown(
    "<p style='text-align: center; font-size: small;'>💖 Created with love by <strong>Rida Fatima</strong></p>", 
    unsafe_allow_html=True
)
