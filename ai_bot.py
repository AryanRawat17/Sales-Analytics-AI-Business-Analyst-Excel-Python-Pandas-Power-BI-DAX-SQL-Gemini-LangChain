import getpass
import pandas as pd

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_experimental.tools import PythonAstREPLTool

from kpi_engine import calculate_kpis


# ===================================
# GEMINI API KEY
# ===================================

api_key = getpass.getpass(
    "Enter your Gemini API key: "
)

print("1. API key setup completed")


# ===================================
# LOAD EXCEL DATA
# ===================================

file_path = "Sales_Analytics_ML_Dataset.xlsx"

df = pd.read_excel(file_path)

print("\nDataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())


# ===================================
# BUSINESS KPI ENGINE
# ===================================

kpis = calculate_kpis(df)

print("\n2. Business KPI Engine loaded successfully!")


# ===================================
# CREATE GEMINI LLM
# ===================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key
)

print("3. Gemini LLM created")


# ===================================
# CREATE PYTHON TOOL
# ===================================

python_tool = PythonAstREPLTool(
    locals={
        "df": df
    }
)

print("4. Python tool created")


# ===================================
# CREATE AI BUSINESS ANALYST AGENT
# ===================================

agent = create_agent(
    model=llm,
    tools=[python_tool],
    system_prompt="""
You are an expert AI Business Analyst.

You are working with a Pandas DataFrame called `df`.

Your job is to understand the user's business question,
perform the required analysis using Python/Pandas,
and then provide a clear business answer.

===================================
CORE WORKFLOW
===================================

For every analytical question:

1. Understand the user's question.
2. Identify the relevant columns.
3. Decide what analysis is required.
4. Use the Python tool to perform the calculation.
5. Inspect the calculated result.
6. Compare relevant metrics when necessary.
7. Draw conclusions from the actual data.
8. Give a concise business-focused answer.

IMPORTANT:

- Never guess numerical values.
- Always use Python/Pandas for calculations.
- Do not perform important calculations mentally.
- Base conclusions only on the dataset.
- Do not invent information.
- Do not load the Excel file again.
- The DataFrame is already available as `df`.

===================================
PYTHON TOOL RULES
===================================

Use Python/Pandas for:

- totals
- averages
- counts
- percentages
- minimums
- maximums
- filtering
- sorting
- rankings
- group-by analysis
- comparisons
- trends
- correlations
- top/bottom performers
- unusual patterns
- business recommendations

Do NOT print the entire DataFrame.

Do NOT unnecessarily execute:

df.head()
df.tail()
df.info()
df.columns
df.describe()

For analytical questions, calculate only the information
needed to answer the question.

Do not return the entire dataframe.

Return summarized analysis results instead.

For example:

Question:
"Which region has the highest profit?"

Use Python similar to:

df.groupby("Region")["Profit"].sum().sort_values(ascending=False)

Question:
"What are the strongest and weakest performing regions?"

Calculate relevant regional metrics such as:

- Sales
- Profit
- Profit Margin
- Orders
- Returns

Then compare the regions and identify the strongest
and weakest performers.

Question:
"Which products are contributing most to overall profit?"

Calculate product-level:

- Sales
- Profit
- Profit Margin
- Quantity
- Orders

Then rank the products by Profit and explain the result.

Question:
"Which products have high sales but low profit?"

Calculate Sales and Profit Margin by Product,
then identify products satisfying the condition.

===================================
BUSINESS REASONING
===================================

Do not simply provide raw numbers.

When appropriate, explain:

- Why something is performing well.
- Why something is performing poorly.
- Which metrics support the conclusion.
- What business action could be considered.

Always distinguish between:

FACT:
A result calculated from the dataset.

RECOMMENDATION:
A business action based on those results.

===================================
FINAL RESPONSE FORMAT
===================================

Use clear, simple, professional business language.

You may use:

- headings
- numbered lists
- bullet points
- tables

IMPORTANT FORMATTING RULES:

DO NOT use Markdown bold formatting.

Never use:

**Laptop**
**Sales**
**Profit Margin**

Instead use:

Laptop
Sales
Profit Margin

Do not use double asterisks anywhere in the final answer.

Do not show Python code unless the user explicitly asks for it.

Do not show tool calls.

Do not show internal reasoning or chain-of-thought.

Do not show Gemini metadata or technical information.

If the requested information cannot be determined from
the dataset, clearly say so.

Always distinguish between facts calculated from the
dataset and business recommendations.
"""
)

print("5. AI Agent created")


# ===================================
# RESPONSE CLEANING FUNCTION
# ===================================

def clean_ai_response(response):

    # Remove Markdown bold
    response = response.replace("**", "")

    # Remove Markdown italic markers
    response = response.replace("__", "")

    # Remove Markdown code blocks
    response = response.replace("```text", "")
    response = response.replace("```markdown", "")
    response = response.replace("```", "")

    return response.strip()


# ===================================
# CHAT WITH EXCEL
# ===================================

print("\n===================================")
print("       AI BUSINESS ANALYST")
print("===================================")

print("Ask questions about your business data.")
print("Type 'exit' to stop.")


while True:

    question = input("\nYou: ")

    # ===================================
    # EXIT
    # ===================================

    if question.lower().strip() == "exit":
        print("\nGoodbye!")
        break


    # ===================================
    # EMPTY QUESTION
    # ===================================

    if not question.strip():
        print("\nPlease enter a question.")
        continue


    q = question.lower().strip()


    # ===================================
    # DIRECT KPI QUESTIONS
    # EXACT MATCH ONLY
    # NO GEMINI API CALL
    # ===================================

    if q in [
        "total gross sales",
        "what is total gross sales",
        "what are total gross sales",
        "what is the total gross sales"
    ]:

        print("\nAI:")
        print(
            f"Total Gross Sales: "
            f"₹{kpis['Total Gross Sales']:,.2f}"
        )
        continue


    if q in [
        "total sales",
        "what is total sales",
        "what are total sales",
        "what is the total sales"
    ]:

        print("\nAI:")
        print(
            f"Total Sales: "
            f"₹{kpis['Total Sales']:,.2f}"
        )
        continue


    if q in [
        "total cost",
        "what is total cost",
        "what are total costs",
        "what is the total cost"
    ]:

        print("\nAI:")
        print(
            f"Total Cost: "
            f"₹{kpis['Total Cost']:,.2f}"
        )
        continue


    if q in [
        "total profit",
        "what is total profit",
        "what are total profits",
        "what is the total profit"
    ]:

        print("\nAI:")
        print(
            f"Total Profit: "
            f"₹{kpis['Total Profit']:,.2f}"
        )
        continue


    if q in [
        "profit margin",
        "overall profit margin",
        "what is profit margin",
        "what is the profit margin",
        "what is the overall profit margin"
    ]:

        print("\nAI:")
        print(
            f"Profit Margin: "
            f"{kpis['Profit Margin']:.2f}%"
        )
        continue


    if q in [
        "total orders",
        "what are total orders",
        "how many orders",
        "how many total orders"
    ]:

        print("\nAI:")
        print(
            f"Total Orders: "
            f"{kpis['Total Orders']:,}"
        )
        continue


    if q in [
        "total customers",
        "what are total customers",
        "how many customers",
        "how many total customers"
    ]:

        print("\nAI:")
        print(
            f"Total Customers: "
            f"{kpis['Total Customers']:,}"
        )
        continue


    if q in [
        "average order value",
        "what is average order value",
        "what is the average order value"
    ]:

        print("\nAI:")
        print(
            f"Average Order Value: "
            f"₹{kpis['Average Order Value']:,.2f}"
        )
        continue


    if q in [
        "return rate",
        "overall return rate",
        "what is return rate",
        "what is the return rate",
        "what is the overall return rate"
    ]:

        print("\nAI:")
        print(
            f"Return Rate: "
            f"{kpis['Return Rate']:.2f}%"
        )
        continue


    if q in [
        "average customer age",
        "what is average customer age",
        "what is the average customer age"
    ]:

        print("\nAI:")
        print(
            f"Average Customer Age: "
            f"{kpis['Average Customer Age']:.2f} years"
        )
        continue


    if q in [
        "average delivery",
        "average delivery days",
        "what is average delivery",
        "what are average delivery days"
    ]:

        print("\nAI:")
        print(
            f"Average Delivery Days: "
            f"{kpis['Average Delivery Days']:.2f} days"
        )
        continue


    if q in [
        "average discount",
        "what is average discount",
        "what is the average discount"
    ]:

        print("\nAI:")
        print(
            f"Average Discount: "
            f"{kpis['Average Discount']:.2f}%"
        )
        continue


    if q in [
        "average rating",
        "average customer rating",
        "what is average rating",
        "what is the average customer rating"
    ]:

        print("\nAI:")
        print(
            f"Average Customer Rating: "
            f"{kpis['Average Customer Rating']:.2f}"
        )
        continue


    # ===================================
    # DATASET INFORMATION
    # NO GEMINI API CALL
    # ===================================

    if q in [
        "name every column",
        "name all columns",
        "show columns",
        "list columns",
        "what are the columns",
        "show me the columns",
        "what columns are there"
    ]:

        print("\nAI:")
        print("Columns in the dataset:\n")

        for i, column in enumerate(df.columns, start=1):
            print(f"{i}. {column}")

        continue


    if q in [
        "how many rows",
        "number of rows",
        "row count",
        "how many records",
        "number of records",
        "how many rows are there"
    ]:

        print("\nAI:")
        print(
            f"The dataset contains "
            f"{len(df):,} rows."
        )

        continue


    if q in [
        "how many columns",
        "number of columns",
        "column count"
    ]:

        print("\nAI:")
        print(
            f"The dataset contains "
            f"{len(df.columns)} columns."
        )

        continue


    if q in [
        "dataset shape",
        "what is the shape",
        "what is the shape of the dataset",
        "shape of dataset",
        "how big is the dataset"
    ]:

        print("\nAI:")
        print(
            f"The dataset has "
            f"{df.shape[0]:,} rows and "
            f"{df.shape[1]} columns."
        )

        continue


    if q in [
        "show first 5 rows",
        "first 5 rows",
        "show me first 5 rows",
        "display first 5 rows"
    ]:

        print("\nAI:")
        print(df.head())

        continue


    if q in [
        "show last 5 rows",
        "last 5 rows",
        "show me last 5 rows",
        "display last 5 rows"
    ]:

        print("\nAI:")
        print(df.tail())

        continue


    if q in [
        "show data types",
        "data types",
        "what are the data types",
        "column data types"
    ]:

        print("\nAI:")
        print(df.dtypes)

        continue


    if q in [
        "missing values",
        "show missing values",
        "check missing values",
        "how many missing values"
    ]:

        print("\nAI:")
        print(df.isnull().sum())

        continue


    # ===================================
    # COMPLEX QUESTIONS
    # GEMINI + PYTHON
    # ===================================

    try:

        print("\nProcessing your question...")

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            }
        )


        # ===================================
        # GET FINAL RESPONSE
        # ===================================

        print("\nAI:")

        response = result["messages"][-1].content


        # ===================================
        # HANDLE GEMINI RESPONSE FORMAT
        # ===================================

        if isinstance(response, list):

            text_parts = []

            for item in response:

                if isinstance(item, dict):

                    if item.get("type") == "text":
                        text_parts.append(
                            item.get("text", "")
                        )

                elif isinstance(item, str):
                    text_parts.append(item)

            response = "\n".join(text_parts)


        # ===================================
        # CLEAN MARKDOWN
        # ===================================

        response = clean_ai_response(response)

        print(response)


    # ===================================
    # ERROR HANDLING
    # ===================================

    except Exception as e:

        print("\nError:")
        print(type(e).__name__, ":", e)
