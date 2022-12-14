import streamlit as st
from PIL import Image
import requests


# Set page tab display
st.set_page_config(
   page_title="Pawlaroid NFT",
   page_icon= '🐾',
   layout="wide",
   initial_sidebar_state="expanded",
)

# Session State also supports attribute based syntax
if 'check' not in st.session_state:
    st.session_state.check = False

if 'gan_res' not in st.session_state:
    st.session_state.gan_res = False

if 'pet_picked' not in st.session_state:
    st.session_state.pet_picked = False

if 'transforming' not in st.session_state:
    st.session_state.transforming = False

if 'tracker' not in st.session_state:
    st.session_state.tracker = False

if 'style' not in st.session_state:
    st.session_state.style = False




# api url
bg_url = 'https://rembg-with-model-xu4pc2grda-ew.a.run.app'
cat_url = 'https://gan-api-l6f5cicmxa-as.a.run.app/guttercatgang'
dog_url = 'https://gan-api-l6f5cicmxa-as.a.run.app/gutterdogsE400'
trans_url = 'http://34.133.155.163:9000'

# Cover and title of app
st.image('NFT_cover.png', width=1300)
st.markdown("---")


#### automatically generate nft in middle block

def picked_pet():
    st.session_state.pet_picked = True

def unset_nft():
    st.session_state.pet_picked = True
    st.session_state.transforming = False

def persist_nft():
    st.session_state.transforming = True

col1, col2 = st.columns(2)
with col1:
    st.markdown("## 🔥 NFT OF THE DAY 🔥")
    st.markdown("#### ---- Pet NFT made by AI ----")
    st.session_state.check = st.radio('Choose a pet!', options=('Dog 🐶', 'Cat 😺'), on_change=picked_pet)
    nft_image_box = st.empty()
    if st.session_state.pet_picked:
        if not st.session_state.transforming:
            if st.session_state.check  == 'Cat 😺':
                with st.spinner("Wait for it..."):
                    nft_content = requests.get(cat_url).content
                    st.session_state.gan_res = requests.post(bg_url+'/colour_nft', files={'img':nft_content}).content
            else:
                nft_content = requests.get(dog_url).content
                st.session_state.gan_res = requests.post(bg_url+'/colour_nft', files={'img':nft_content}).content

        st.image(st.session_state.gan_res, caption="Your AI generated NFT ⭐️", width=400)


### third layers for buttons

col4, col5, col6, col7, col8, col9 = st.columns(6)
with col4:
    if st.button('Generate a new one', on_click=unset_nft):
        st.write("'til you're satisfied")


with col5:
    st.button('Try with your pet', on_click=persist_nft)

with col2:
    if st.session_state.transforming:
        # upload the pet image
        st.markdown(f"#### Upload your {st.session_state.check} photo👇")
        st.session_state.img_file_buffer = st.file_uploader('')
        # creating the imagelocation to replace images
        if st.session_state.img_file_buffer:
            imageLocation = st.empty()
            img_bytes = st.session_state.img_file_buffer.getvalue()
            old_image = Image.open(st.session_state.img_file_buffer)
            imageLocation.image(old_image, caption="Here's the image you uploaded ☝️", output_format='JPEG', width=190)

        # preprocessing the image
            with st.spinner("Wait for it..."):
            # remove the pet image bg via api
                res = requests.post(bg_url + "/rmimg", files={'img':img_bytes})
                if res.status_code == 200:
                    st.session_state.preproecessing = res.content
                    imageLocation.image(st.session_state.preproecessing, caption="Preprocessed successfully ☝️", width=190)
                    st.session_state.tracker = st.success('Starting transforming ', icon="✅")

# transforming the pet with genereted nft
st.markdown("---")
c1, c2, c3 = st.columns(3)
params = {'epochs' : 2,
        'steps_per_epoch' : 10,
        'style_weight' : 0.009,
        'content_weight' : 0.1,
        'total_variation_weight' : 2}

with c2:
    if st.session_state.tracker:
        st.write("### 😺 YOUR PAWLAROID NFT 🐶")
        with st.spinner("Wait for it..."):
            s = requests.Session()
            imageLocation1 = st.empty()
            with s.post(trans_url + '/generate',files={'style_image':st.session_state.preproecessing,
                                                       'content_image':st.session_state.gan_res},
                                                       params=params, stream=True
                                                       ) as trans_res:
                print('----- trans_res.headers ------', trans_res.headers)
                for line in trans_res.iter_content(chunk_size=786432):
                    print('----- line length ------', len(line))
                    img = Image.frombytes('RGB', (512,512), line, 'raw')
                    imageLocation1.image(img)

# st.session_state.style = st.select_slider(
#      'Customizing your NFT',
#      options=['more pet', ' pet', 'original', 'NFT', 'more NFT'])
# st.write('My favorite style is', st.session_state.style)
