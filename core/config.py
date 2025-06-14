import google.generativeai as genai
from jinja2 import Environment, FileSystemLoader

# === Gemini API Key and Setup ===
API_KEY = "AIzaSyB9jeDjHFp319jUiiBNaibr4KPrn9ylpDY"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

#===============Cognito user Pool ===========================
COGNITO_REGION = "ap-southeast-1"
USER_POOL_ID = "ap-southeast-1_RTjDQmHAJ"
APP_CLIENT_ID = "2mpbj34oofs7nlu062l776dogd"
COGNITO_ISSUER = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}"


# === Choose the Gemini Model ===
model = genai.GenerativeModel("gemini-2.0-flash")

# === LaTeX setup ===
env = Environment(
    loader=FileSystemLoader("templates"),
    block_start_string="((*",
    block_end_string="*))",
    variable_start_string="(((",
    variable_end_string=")))",
    comment_start_string="((#",
    comment_end_string="#))",
)
latex_template = env.get_template("basic.tex")
