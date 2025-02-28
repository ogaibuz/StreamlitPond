import streamlit as st
import pandas as pd

def validarUsuario(usuario,clave): 
    """
    Args:
     usuario (str): El nombre del usuario
     clave (str): La contraseña del usuario

     Returns:
        bool: True usuario valido, False usuario invalido
    """
    dfusuarios = pd.read_csv('usuarios.csv')
    if len(dfusuarios[(dfusuarios['usuario']==usuario) & (dfusuarios['clave']==clave)])>0:
        return True
    else:
        return False

def generarMenu(usuario):

    with st.sidebar:
        # Cargamos la tabla de usuarios
        dfusuarios = pd.read_csv('usuarios.csv')
        # Filtramos la tabla de usuarios
        dfUsuario = dfusuarios[(dfusuarios['usuario']==usuario)]
        # Cargamos el nombre del usuario
        nombre= dfUsuario['nombre'].values[0]
        # Mostramos el nombre del usuario
        st.write(f"Hola **:blue-background[{nombre}]** ")

        # Mostramos los enlaces de páginas
        st.page_link("inicio.py", label="Inicio", icon="🔑")
        st.subheader("Tableros")
        st.page_link("pages/app.py", label="Cobranzas", icon="💁‍♀️")
        st.page_link("pages/app.py", label="Pagos", icon='👀')
        st.page_link("pages/pagina3.py", label="Personal", icon="💨")  
        # Boton para cerrar la sesion
        btnSalir=st.button('Salir')
        if btnSalir:
            st.session_state.clear()
            # Luego de borrar la Session State reiniciamos la app para mostrar la opcion de usuario y clave
            st.rerun()

def generarLogin():
    # Genera la ventana de login o muestra el menu si el login es valido 
    # Validamos si el usuario ya fue ingresado
    if 'usuario' in st.session_state:
        generarMenu(st.session_state['usuario'])
    else:
    # Si no hay usuario ingresado, mostramos la ventana de login
        with st.form('frmLogin'):
            parUsuario = st.text_input('Usuario')
            parPassword = st.text_input('Password', type="password")
            btnLogin = st.form_submit_button('Ingresar', type='primary')
            if btnLogin:
                # Validamos el usuario y password
                if validarUsuario(parUsuario, parPassword):
                    st.session_state['usuario'] = parUsuario
                    # Si el usuario es correcto reiniciamos la app para que se cargue el menu
                    st.rerun()
                else:
                    # Si el usuario es invalido, mostrmos el mensaje de error
                    st.error('Usuario o contraseña invalidos', icon="🚫")
                    

