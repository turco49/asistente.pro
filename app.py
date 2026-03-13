import streamlit as st
from groq import Groq

# 1. Configuración de seguridad con Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Configura la GROQ_API_KEY en los Secrets de Streamlit.")
    st.stop()

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
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # LLAMADA CORRECTA A GROQ (Reemplaza a Ollama)
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system", 
                    "content": f"Eres un vendedor de Hotmart experto. Producto: {PRODUCTO['nombre']}. Precio: {PRODUCTO['precio']}. Beneficios: {PRODUCTO['beneficios']}. Link: {PRODUCTO['link']}. Responde siempre en español de forma breve. Usa el método SPIN Selling y manejo de objeciones Boomerang. No uses palabras de spam. Tono de autoridad y consultivo."
                }
            ] + st.session_state.messages
        )
        
        full_response = completion.choices[0].message.content
        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
