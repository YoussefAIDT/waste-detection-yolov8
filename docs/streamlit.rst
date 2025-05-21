Lancer l'application Streamlit
==============================

1. Installez Streamlit et LocalTunnel :
   .. code-block:: bash

      pip install streamlit
      npm install -g localtunnel

2. Lancez l’application dans Colab :
   .. code-block:: bash

      !streamlit run app.py & npx localtunnel --port 8501

3. Récupérez l’adresse IP :
   .. code-block:: bash

      !wget -q -O - ipv4.icanhazip.com

4. Copiez-la dans "Tunnel Password", puis cliquez sur "Click to Submit"
5. L’interface Web est accessible depuis le lien généré
