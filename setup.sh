
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
token='pk.eyJ1IjoibWFzc2RvIiwiYSI6ImNraDR5MnBnNDBkZTIyeW85cmh3b3N3cXUifQ.AKd071Qk75Iw2UaNtNN_2Q'\n\
\n\
" > ~/.streamlit/config.toml