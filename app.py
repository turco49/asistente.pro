import streamlit as st
from groq import Groq

# 1. Configuración de seguridad
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ Configura la GROQ_API_KEY en los Secrets de Streamlit.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Configuración de la página (Cambié el ícono a un rayo para que sea general)
st.set_page_config(page_title="Asistente Pro", page_icon="⚡")
st.title("🤖 asistente.pro")

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # INSTRUCCIONES GENERALES (Ya no es solo de cocina)
            mensaje_sistema = {
                "role": "system", 
                "content": """
                Eres 'asistente.pro', un asistente virtual inteligente y experto en múltiples áreas.
                REGLAS:
                1. Puedes ayudar con programación, redacción, historia, ciencia, consejos y charlas generales.
                2. Responde siempre en español, de forma clara, educada y profesional.
                3. Si el usuario te pide ayuda creativa o técnica, sé detallado.
                4. Tu objetivo es ser el asistente más útil posible para el usuario.
                """
            }
            
            # Combinamos sistema + historial
            historial_completo = [mensaje_sistema] + st.session_state.messages

            # Llamada al modelo potente de Groq
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=historial_completo,
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            
            # Guardar respuesta del asistente
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Hubo un error con la IA: {e}")
