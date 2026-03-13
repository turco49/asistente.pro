import streamlit as st
from groq import Groq

# 1. Configuración de seguridad
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ Falta la configuración de GROQ_API_KEY en los Secrets.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Configuración del producto
PRODUCTO = {
    "nombre": "Cocinero Pro en 30 Días",
    "precio": "47 USD",
    "beneficios": "Certificado oficial, acceso de por vida, garantía de 7 días.",
    "link": "https://hotmart.com/tu-link-aqui"
}

st.set_page_config(page_title="Asistente Pro", page_icon="👨‍🍳")
st.title("🤖 asistente.pro")

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt := st.chat_input("Pregúntame sobre el curso..."):
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Construimos la lista de mensajes correctamente
            mensaje_sistema = {
                "role": "system", 
                "content": f"Eres un experto vendedor. Producto: {PRODUCTO['nombre']}. Precio: {PRODUCTO['precio']}. Link: {PRODUCTO['link']}. Responde breve y profesional."
            }
            
            # Combinamos sistema + historial
            historial_completo = [mensaje_sistema] + st.session_state.messages

            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=historial_completo,
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            
            # Guardar respuesta del asistente
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Hubo un error con la IA: {e}")
