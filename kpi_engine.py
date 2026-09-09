import pandas as pd

# Load your Excel file into 'df'
df = pd.read_excel("Sales_Analytics_ML_Dataset.xlsx")



# ===================================
# BUSINESS KPI ENGINE
# ===================================

def calculate_kpis(df):

    total_sales = df["Sales"].sum()
    total_gross_sales = df["Gross_Sales"].sum()
    total_cost = df["Cost"].sum()
    total_profit = df["Profit"].sum()

    total_orders = df["Order_ID"].nunique()
    total_customers = df["Customer_ID"].nunique()

    total_quantity = df["Quantity"].sum()

    average_order_value = (
        total_sales / total_orders
        if total_orders > 0
        else 0
    )

    profit_margin = (
        (total_profit / total_sales) * 100
        if total_sales > 0
        else 0
    )

    return_rate = (
        (df["Returned"] == "Yes").mean() * 100
        if len(df) > 0
        else 0
    )

    average_customer_age = df["Customer_Age"].mean()

    average_delivery_days = df["Delivery_Days"].mean()

    average_discount = df["Discount_Pct"].mean()

    average_customer_rating = df["Customer_Rating"].mean()

    kpis = {
        "Total Sales": total_sales,
        "Total Gross Sales": total_gross_sales,
        "Total Cost": total_cost,
        "Total Profit": total_profit,
        "Profit Margin": profit_margin,
        "Total Orders": total_orders,
        "Total Customers": total_customers,
        "Total Quantity": total_quantity,
        "Average Order Value": average_order_value,
        "Return Rate": return_rate,
        "Average Customer Age": average_customer_age,
        "Average Delivery Days": average_delivery_days,
        "Average Discount": average_discount,
        "Average Customer Rating": average_customer_rating
    }

    return kpis

# ===================================
# CALCULATE BUSINESS KPIs
# ===================================

kpis = calculate_kpis(df)

print("\n===================================")
print("       BUSINESS KPI ENGINE")
print("===================================")

for name, value in kpis.items():

    if "Margin" in name or "Rate" in name or "Discount" in name:
        print(f"{name}: {value:.2f}%")

    elif "Average" in name:
        print(f"{name}: {value:.2f}")

    else:
        print(f"{name}: {value:,.2f}")

# ===================================
# PRODUCT PERFORMANCE
# ===================================

def product_performance(df):

    product_data = (
        df.groupby("Product")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum"),
            Orders=("Order_ID", "nunique"),
            Returns=("Returned", lambda x: (x == "Yes").sum())
        )
        .sort_values("Sales", ascending=False)
    )

    return product_data

product_kpis = product_performance(df)

print("\n===================================")
print("       PRODUCT PERFORMANCE")
print("===================================")

print(product_kpis)

# ===================================
# REGIONAL PERFORMANCE
# ===================================

def regional_performance(df):

    regional_data = (
        df.groupby("Region")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
            Quantity=("Quantity", "sum"),
            Returns=("Returned", lambda x: (x == "Yes").sum())
        )
        .sort_values("Sales", ascending=False)
    )

    return regional_data

regional_kpis = regional_performance(df)

print("\n===================================")
print("       REGIONAL PERFORMANCE")
print("===================================")

print(regional_kpis)

# ===================================
# CHANNEL PERFORMANCE
# ===================================

def channel_performance(df):

    channel_data = (
        df.groupby("Channel")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
            Quantity=("Quantity", "sum"),
            Returns=("Returned", lambda x: (x == "Yes").sum())
        )
        .sort_values("Sales", ascending=False)
    )

    return channel_data

channel_kpis = channel_performance(df)

print("\n===================================")
print("       CHANNEL PERFORMANCE")
print("===================================")

print(channel_kpis)

# ===================================
# CUSTOMER SEGMENT PERFORMANCE
# ===================================

def customer_segment_performance(df):

    segment_data = (
        df.groupby("Customer_Segment")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
            Quantity=("Quantity", "sum"),
            Average_Age=("Customer_Age", "mean"),
            Returns=("Returned", lambda x: (x == "Yes").sum())
        )
        .sort_values("Sales", ascending=False)
    )

    return segment_data

segment_kpis = customer_segment_performance(df)

print("\n===================================")
print("     CUSTOMER SEGMENT PERFORMANCE")
print("===================================")

print(segment_kpis)