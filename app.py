import sqlite3
import pandas as pd
import streamlit as st

conn = sqlite3.connect("f1.db", check_same_thread=False)


st.title("visualizzatore e modificatore data f1!")
#st.write("c'è da divertirsi")
st.sidebar.title("menù di scelta per operazioni")
sidebar=st.sidebar.radio("scegli tra le ozpioni", ["search circuits", "insert new data", "tracks per year visualization"])

def form_nuovo_pilota(conn):
    st.write("inserisci i dati del pilota")
    with st.form("form_pilota"):
        name = st.text_input("name*")
        surname = st.text_input("surname*")
        number= st.number_input("number", min_value=1, max_value=100, step=1)
        code = st.text_input("pilot code (for ex LEC)")
        dob = st.date_input("date of birth")
        nationality = st.text_input("nationality")
        url = st.text_input("url to his wikipedia")
        
        inviato = st.form_submit_button("add driver")
        code = code.upper() if code != "" else None
        if inviato:
            if name and surname:
                query = "INSERT INTO drivers (name, surname, number, code, dob, nationality, url) VALUES (?, ? ,?, ? ,? , ?, ?)"
                with conn:
                    conn.execute(query, (name, surname,number, code, dob, nationality, url))
                    st.success(f"{name} {surname} has been added to the pilots!")
            else:
                st.warning("all * fields are mandatory !")

def pagina_calendario(conn):
    st.write("view every race for a said year!")

    anno_scelto = st.slider("Seleziona la stagione:", min_value=1950, max_value=2023, value=1950, step=1)

    
    query = """
            SELECT 
                round AS 'Tappa', 
                name AS 'Gran Premio', 
                date AS 'Data', 
                time_race AS 'Orario'
            FROM races 
            WHERE year = ? 
            ORDER BY round ASC
        """
        
    #qua andrebbe aggiunto un winner o qualcosa di simile
    df = pd.read_sql(query, conn, params=(anno_scelto,))
            
    if not df.empty:
        st.success(f"Trovate {len(df)} gare per la stagione {anno_scelto}!")
        st.dataframe(df, hide_index=True) 
    else:
        st.warning(f"Nessuna gara trovata per il {anno_scelto}.")


def pagina_inserimento(conn):
    st.subheader("aggiungamo nuovi dati")
    tipoinserimento=st.selectbox("che tabella vuoi inserire?",["piloti"])

    match tipoinserimento:
        case "piloti":
            form_nuovo_pilota(conn)

def circuitscountry():
    query = """
        select * from circuits 
        where country = ?
    """
    return query

def ricercacircuiti(conn):
    nazione = st.text_input("inserisci la nazione")
    df = pd.read_sql(circuitscountry(), conn, params=(nazione,))
    if nazione:
        st.dataframe(df)

match sidebar:
    case "search circuits":
        ricercacircuiti(conn)
    case "insert new data":
        pagina_inserimento(conn)
    case "tracks per year visualization":
        pagina_calendario(conn)