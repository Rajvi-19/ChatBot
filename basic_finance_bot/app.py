import pandas as pd
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
panda_obj = pd.read_excel("Finance_document.xlsx")
print(panda_obj)

# -----------------------
#   ROUTES
# -----------------------

@app.route("/")
def index():
    return render_template("bot.html")


@app.route("/bot", methods=["GET"])
def chatbot_reply():
    query = request.args.get("query", "").strip().lower()

    answers = get_answer_dict()  # get all possible Q&A

    if query in answers:
        response = answers[query]
    else:
        response = "I'm sorry, I don't understand your question."

    return jsonify({"reply": response})


# -----------------------
#   ANSWER DICTIONARY
# -----------------------

def get_answer_dict():
    return {
        "what is the total revenue across all years?": get_total_revenue(),
        "what is the revenue for each year?": get_revenue_per_year(),
        "which year had the highest revenue?": get_highest_revenue_year(),
        "what is the net income for each year?": get_net_income_per_year(),
        "how did net income change from 2023 to 2024?": get_net_income_change(),
        "which year had the highest net income?": get_highest_net_income_year(),
        "what are the total assets and total liabilities for each year?": get_assets_liabilities_per_year()
    }


# -----------------------
#   ANSWER FUNCTIONS
# -----------------------

def get_total_revenue():
    total_revenue = panda_obj["Revenue"].sum()
    return f"The total revenue across all years is {total_revenue}."


def get_revenue_per_year():
    result = ""
    for year in panda_obj["Year"].unique():
        year_revenue = panda_obj[panda_obj["Year"] == year]["Revenue"].sum()
        result += f"{year}: ${year_revenue}, "

    return f"The revenue for each year is: {result}"


def get_highest_revenue_year():
    year = panda_obj.loc[panda_obj["Revenue"].idxmax(), "Year"]
    highest_revenue = panda_obj["Revenue"].max()

    return f"The year with the highest revenue is {year} with ${highest_revenue}."


def get_net_income_per_year():
    result = ""
    for year in panda_obj["Year"].unique():
        income = panda_obj[panda_obj["Year"] == year]["Net Income"].sum()
        result += f"{year}: ${income}, "

    return f"The net income for each year is: {result}"


def get_net_income_change():
    income_2023 = panda_obj.loc[panda_obj["Year"] == 2023, "Net Income"].values[0]
    income_2024 = panda_obj.loc[panda_obj["Year"] == 2024, "Net Income"].values[0]
    change = income_2024 - income_2023

    return f"The net income changed by ${change} from 2023 to 2024."


def get_highest_net_income_year():
    row = panda_obj.loc[panda_obj["Net Income"].idxmax()]
    year = row["Year"]
    income = row["Net Income"]

    return f"The year with the highest net income is {year} with ${income}."


def get_assets_liabilities_per_year():
    result = ""
    for year in panda_obj["Year"].unique():
        data = panda_obj[panda_obj["Year"] == year]
        # Check if columns exist before accessing them
        if "Total Assets" in panda_obj.columns and "Total Liabilities" in panda_obj.columns:
            assets = data["Total Assets"].values[0]
            liabilities = data["Total Liabilities"].values[0]
            result += f"{year} - Assets: ${assets}, Liabilities: ${liabilities}; "
        else:
            result = "Assets and Liabilities columns not found in the dataset."

    return f"The total assets and liabilities for each year are: {result}"


# -----------------------
#   RUN APP
# -----------------------

if __name__ == "__main__":
    app.run(debug=True)
