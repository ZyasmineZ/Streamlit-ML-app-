import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Définir la largeur de la page
st.set_page_config(layout="wide")

# Fonction pour initialiser la session
def init_session():
    if "page" not in st.session_state:
        st.session_state.page = 0  # Utiliser 0 comme numéro initial de page
        st.session_state.data = None  # Initialiser la variable "data" à None
        st.session_state.columns_to_drop = []  # Initialiser la liste des colonnes à supprimer

# Fonction pour afficher la landing page
def landing_page():

    with open('style.css') as f:
        css = f.read()

    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    st.markdown('<p class="font">Welcome !</p>', unsafe_allow_html=True)

    st.title("Bienvenue dans notre application de Machine Learning.")
    st.write("Cliquez sur le bouton ci-dessous pour commencer.")
    
    st.text("")  # Crée une séparation visuelle sans bordure
    with st.form(key="landing_form", border=False):
        st.form_submit_button("Get Started", on_click=lambda: st.session_state.update({"page": 1}))


# Fonction pour importer fichier csv
def import_csv(): 
    # Ajout de la fonctionnalité pour importer un fichier CSV
    uploaded_file = st.file_uploader("Importer un fichier CSV", type=["csv"])
    if uploaded_file is not None:
        st.session_state.data = pd.read_csv(uploaded_file)
        st.success("Vos données on été importées avec succès.")


# Fonction pour visualiser les données
def visualise_tab():
    # Vérifier si des données sont disponibles avant de procéder à la visualisation
        if st.session_state.data is not None:
            # Sélection des colonnes pour la visualisation
            st.subheader("Sélectionnez deux colonnes pour la visualisation:")
            st.session_state.selected_columns = st.multiselect("Sélectionnez deux colonnes", st.session_state.data.columns, key="select_columns")

            # Sélection du type de graphe
            chart_type = st.selectbox("Sélectionnez le type de graphe", ["Scatter Plot", "Line Plot", "Bar Plot"])

            # Affichage du graphe en fonction du type choisi
            if st.button("Afficher le graphe"):
                if len(st.session_state.selected_columns) == 2:
                    if chart_type == "Scatter Plot":
                        fig, ax = plt.subplots()
                        sns.scatterplot(x=st.session_state.selected_columns[0], y=st.session_state.selected_columns[1], data=st.session_state.data, ax=ax)
                        st.pyplot(fig)
                    elif chart_type == "Line Plot":
                        fig, ax = plt.subplots()
                        sns.lineplot(x=st.session_state.selected_columns[0], y=st.session_state.selected_columns[1], data=st.session_state.data, ax=ax)
                        st.pyplot(fig)
                    elif chart_type == "Bar Plot":
                        fig, ax = plt.subplots()
                        sns.barplot(x=st.session_state.selected_columns[0], y=st.session_state.selected_columns[1], data=st.session_state.data, ax=ax)
                        st.pyplot(fig)
                    else:
                        st.warning("Veuillez sélectionner un type de graphe valide.")
                else:
                    st.warning("Veuillez sélectionner exactement deux colonnes pour la visualisation.")
        else:
            st.warning("Veuillez importer des données d'abord.")


# Fonction pour afficher la tab "Split"
def split_tab():
    # Vérifier si des données sont disponibles avant de procéder à la division
    if st.session_state.data is not None:
        # Sélection de la cible pour la prédiction
        st.subheader("Sélectionnez la colonne cible:")
        target_column = st.selectbox("Sélectionnez la colonne cible", st.session_state.data.columns, key="select_target_column")

        # Pourcentage de données pour l'ensemble d'entraînement
        st.subheader("Pourcentage pour l'ensemble d'entraînement:")
        train_percentage = st.slider("Pourcentage d'entraînement", 0, 100, 80, key="train_percentage")

        # Bouton pour diviser les données
        if st.button("Diviser les données"):
            # Sélectionner uniquement les colonnes numériques
            numeric_columns = st.session_state.data.select_dtypes(include=['number']).columns

            # Vérifier s'il y a des colonnes numériques pour éviter l'erreur
            if not numeric_columns.empty:
                # Diviser les données
                from sklearn.model_selection import train_test_split

                X_train, X_test, y_train, y_test = train_test_split(
                    st.session_state.data.drop(columns=[target_column]),
                    st.session_state.data[target_column],
                    test_size=train_percentage / 100,
                    random_state=42  # Vous pouvez spécifier une graine aléatoire pour la reproductibilité
                )

                # Afficher des informations sur les ensembles
                st.write("Ensemble d'entraînement:")
                st.write(X_train.head())
                st.write("Ensemble de test:")
                st.write(X_test.head())

                st.success("Les données ont été divisées avec succès.")
            else:
                st.warning("Aucune colonne numérique pour diviser.")
        else:
            st.warning("Veuillez sélectionner une colonne cible.")

    else:
        st.warning("Veuillez importer des données d'abord.")

# Mock cleaning steps
@st.cache(allow_output_mutation=True)
def remove_nan(data):
    # Cleaning logic
    cleaned_data = data.fillna(0)  # Replace NaN with 0 for demonstration
    return cleaned_data

@st.cache(allow_output_mutation=True)
def drop_columns(data, columns_to_drop):
    # Cleaning logic
    cleaned_data = data.drop(columns=columns_to_drop, errors='ignore')
    return cleaned_data

@st.cache(allow_output_mutation=True)
def replace_nan(data, replace_option):
    # Cleaning logic
    if replace_option == "0":
        cleaned_data = data.fillna(0)
    elif replace_option == "Moyenne":
        cleaned_data = data.fillna(data.mean())
    elif replace_option == "Médiane":
        cleaned_data = data.fillna(data.median())
    else:
        cleaned_data = data.copy()
    return cleaned_data

@st.cache(allow_output_mutation=True)
def encode_categorical(data, encoding_option):
    # Cleaning logic
    if encoding_option == "One-Hot":
        cleaned_data = pd.get_dummies(data, columns=data.select_dtypes(include=['object']).columns, drop_first=True)
    elif encoding_option == "Ordinal":
        cleaned_data = data.copy()  # Placeholder for ordinal encoding logic
    else:
        cleaned_data = data.copy()
    return cleaned_data

@st.cache(allow_output_mutation=True)
def normalize_data(data):
    # Cleaning logic
    numeric_columns = data.select_dtypes(include=['number']).columns
    if not numeric_columns.empty:
        data[numeric_columns] = (data[numeric_columns] - data[numeric_columns].min()) / (data[numeric_columns].max() - data[numeric_columns].min())
    return data

# Main cleaning function
def clean_data():
    # Affichage du nombre de valeurs manquantes
    if st.session_state.data is not None:
        # une copie des données
        original_data = st.session_state.data.copy()

        st.subheader("Analyse des données:")
        st.write("Nombre de valeurs manquantes par colonne:")
        missing_values = st.session_state.data.isnull().sum()
        st.write(missing_values)

        # Step 1: Remove NaN
        if st.button("Remove NaN"):
            original_data = remove_nan(original_data)
            st.session_state.data = original_data.copy()  # Mettez à jour la session_data avec les modifications
            st.success("Les NaN ont été remplacés par 0 avec succès.")
            st.write("Data after removing NaN:")
            st.write(st.session_state.data)

        # Step 2: Drop Columns
        st.subheader("Supprimer des colonnes:")
        selected_columns_to_drop = st.multiselect("Sélectionnez les colonnes à supprimer", st.session_state.data.columns)
        if st.button("Drop Columns"):
            original_data = drop_columns(original_data, selected_columns_to_drop)
            st.session_state.data = original_data.copy()  # Mettez à jour la session_data avec les modifications
            st.success("Les colonnes sélectionnées ont été supprimées avec succès.")
            st.write("Data after dropping columns:")
            st.write(st.session_state.data)

        # Step 3: Replace NaN
        st.subheader("Remplacer les valeurs manquantes:")
        replace_option = st.selectbox("Choisissez une option de remplacement :", ["0", "Moyenne", "Médiane"])
        if st.button("Replace NaN"):
            original_data = replace_nan(original_data, replace_option)
            st.session_state.data = original_data.copy()  # Mettez à jour la session_data avec les modifications
            st.success("Les valeurs manquantes ont été remplacées avec succès.")
            st.write("Data after replacing NaN:")
            st.write(st.session_state.data)

        # Step 4: Encode Categorical
        categorical_cols = original_data.select_dtypes(include=['object']).columns.tolist()
        if categorical_cols:
            st.subheader("Encodage des variables catégorielles:")
            encoding_option = st.selectbox("Choisissez une option d'encodage :", ["One-Hot", "Ordinal"])
            if st.button("Encode Categorical"):
                original_data = encode_categorical(original_data, encoding_option)
                st.session_state.data = original_data.copy()  # Mettez à jour la session_data avec les modifications
                st.success("Encodage appliqué avec succès.")
                st.write("Data after encoding categorical variables:")
                st.write(original_data)
        else:
            st.warning("Aucune variable catégorielle à encoder.")

        # Step 5: Normalize Data
        if st.button("Normalize Data"):
            original_data = normalize_data(original_data)
            st.session_state.data = original_data.copy()  # Mettez à jour la session_data avec les modifications
            st.success("Les données ont été normalisées avec succès.")
            st.write("Data after normalization:")
            st.write(original_data)

    else:
        st.warning("Veuillez importer des données d'abord.")



# Fonction pour afficher les onglets
def display_tabs():
    tab1, tab2, tab3, tab4 = st.tabs(["Data", "Visualise", "Clean", "Split"])

    # onglet importation des données
    with tab1:
        st.header("Data")

        import_csv()

        with st.form(key="Exit", border=False):
            st.form_submit_button("Exit", on_click=lambda: st.session_state.update({"page": 0}))  # Revenir à la landing page

    
    # onglet visualisation des données
    with tab2:
        st.header("Visualise")

        visualise_tab()


    # onglet netoyage des données  
    with tab3:
        st.header("Clean")
        
        clean_data()
        

    # onglet division des données  
    with tab4:
        st.header("Split")

        split_tab()

# Fonction principale
def main():
    init_session()

    if st.session_state.page == 0:
        landing_page()
    elif st.session_state.page == 1:
        display_tabs()

if __name__ == "__main__":
    main()