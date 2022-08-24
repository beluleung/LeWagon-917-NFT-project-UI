mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

echo "\
[theme]
base=\"dark\"\n\
secondaryBackgroundColor=\"#2a3df9\"\n\
font=\"monospace\"\n\
" >> ~/.streamlit/config.toml
