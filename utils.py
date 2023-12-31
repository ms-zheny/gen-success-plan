import streamlit as st
import security


def setup_page(page_title):
    st.set_page_config(
        page_title=page_title,
        page_icon="👋",
    )

    if st.experimental_get_query_params().get('code'):
        security.handle_redirect()

    access_token = st.session_state.get('access_token')

    if access_token:
        #user_info = security.get_user_info(access_token)
        #st.session_state['user_info'] = user_info
        st.write('Welcom back! ' + st.session_state['user_info'])
        
        return True
    else:
        col1, col2 = st.columns([1,3])

        with col1:
           st.image('assets/home.jpg', width=185)

        with col2:
            container = st.container(border=True)
            container.title("Welcome")
            container.write("Please sign-in to continue")
            auth_url = security.get_auth_url()
            container.markdown(f"<a href='{auth_url}' target='_self'>Log in</a>", unsafe_allow_html=True)

        st.stop()

