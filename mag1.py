import streamlit as st
import json
import os

# Nazwa pliku do przechowywania danych (symulacja "bazy danych")
DATA_FILE = 'inventory.json'

def load_inventory():
    """Wczytuje listę produktów z pliku JSON."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_inventory(inventory_list):
    """Zapisuje listę produktów do pliku JSON."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(inventory_list, f, indent=4)

def add_item(item_name, quantity, inventory_list):
    """Dodaje nowy produkt lub aktualizuje jego ilość."""
    if item_name and quantity > 0:
        found = False
        for item in inventory_list:
            if item['name'] == item_name:
                item['quantity'] += quantity
                found = True
                break
        if not found:
            inventory_list.append({'name': item_name, 'quantity': quantity})
        save_inventory(inventory_list)

def remove_item(item_name, inventory_list):
    """Usuwa produkt z listy."""
    # Używamy list comprehension do stworzenia nowej listy bez wybranego produktu
    updated_inventory = [item for item in inventory_list if item['name'] != item_name]
    if len(updated_inventory) < len(inventory_list):
        save_inventory(updated_inventory)
        return updated_inventory
    return inventory_list


st.title("Prosty Magazyn (bez Session State)")

# --- Sekcja dodawania towaru ---
st.subheader("Dodaj towar")
with st.form(key='add_form', clear_on_submit=True):
    new_item_name = st.text_input("Nazwa towaru")
    new_item_quantity = st.number_input("Ilość", min_value=1, step=1, value=1)
    submit_button = st.form_submit_button("Dodaj")
    if submit_button:
        # Wczytujemy aktualny stan, dodajemy, i zapisujemy
        current_inventory = load_inventory()
        add_item(new_item_name.strip(), new_item_quantity, current_inventory)
        st.success(f"Dodano {new_item_quantity} szt. {new_item_name}")

# Wczytanie aktualnego stanu magazynu do wyświetlenia
inventory_display = load_inventory()

# --- Sekcja wyświetlania i usuwania towaru ---
st.subheader("Stan magazynu")

if not inventory_display:
    st.info("Magazyn jest pusty.")
else:
    # Wyświetlanie w formie tabeli
    st.table(inventory_display)

    # Sekcja usuwania (przyciski do usuwania są generowane dynamicznie)
    st.subheader("Usuń towar")
    for item in inventory_display:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{item['name']} ({item['quantity']} szt.)")
        with col2:
            # Użycie unikalnego klucza dla każdego przycisku
            if st.button(f"Usuń {item['name']}", key=f"del_{item['name']}"):
                # Wczytujemy stan, usuwamy, zapisujemy i wymuszamy przeładowanie, aby odświeżyć widok
                current_inventory = load_inventory()
                updated_list = remove_item(item['name'], current_inventory)
                st.success(f"Usunięto {item['name']}")
                # Aby natychmiast odświeżyć widok tabeli po usunięciu
                st.rerun() 
