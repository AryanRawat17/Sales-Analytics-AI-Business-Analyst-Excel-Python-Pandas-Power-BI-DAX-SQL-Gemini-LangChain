import pandas as pd

# ===================================
# PHASE 3 — BUSINESS INSIGHTS ENGINE
# ===================================


def generate_overall_insights(kpis):
    """
    Generate business insights from overall KPIs.
    """

    insights = []

    # Profit margin
    profit_margin = kpis["Profit Margin"]

    if profit_margin < 10:
        insights.append(
            f"Profit margin is {profit_margin:.2f}%, "
            "which indicates relatively low profitability. "
            "The business should review costs, discounts, "
            "and low-margin products."
        )

    elif profit_margin < 20:
        insights.append(
            f"Profit margin is {profit_margin:.2f}%, "
            "indicating moderate profitability."
        )

    else:
        insights.append(
            f"Profit margin is {profit_margin:.2f}%, "
            "indicating strong profitability."
        )


    # Return rate
    return_rate = kpis["Return Rate"]

    if return_rate > 10:
        insights.append(
            f"Return rate is {return_rate:.2f}%, "
            "which is relatively high. "
            "The business should investigate product quality, "
            "delivery issues, and customer expectations."
        )

    else:
        insights.append(
            f"Return rate is {return_rate:.2f}%, "
            "which is relatively controlled."
        )


    # Average discount
    discount = kpis["Average Discount"]

    if discount > 15:
        insights.append(
            f"Average discount is {discount:.2f}%. "
            "High discounting may be reducing profitability."
        )

    else:
        insights.append(
            f"Average discount is {discount:.2f}%, "
            "indicating controlled discounting."
        )


    # Delivery
    delivery_days = kpis["Average Delivery Days"]

    if delivery_days > 7:
        insights.append(
            f"Average delivery time is {delivery_days:.2f} days. "
            "Delivery performance should be reviewed."
        )

    else:
        insights.append(
            f"Average delivery time is {delivery_days:.2f} days, "
            "which indicates relatively efficient delivery."
        )


    return insights


# ===================================
# PRODUCT INSIGHTS
# ===================================

def generate_product_insights(product_data):

    insights = []

    # Highest sales product
    top_sales_product = product_data["Sales"].idxmax()
    top_sales_value = product_data["Sales"].max()

    insights.append(
        f"{top_sales_product} is the top-selling product "
        f"with sales of {top_sales_value:,.2f}."
    )


    # Highest profit product
    top_profit_product = product_data["Profit"].idxmax()
    top_profit_value = product_data["Profit"].max()

    insights.append(
        f"{top_profit_product} generates the highest profit "
        f"of {top_profit_value:,.2f}."
    )


    # Lowest sales product
    lowest_sales_product = product_data["Sales"].idxmin()
    lowest_sales_value = product_data["Sales"].min()

    insights.append(
        f"{lowest_sales_product} has the lowest sales "
        f"at {lowest_sales_value:,.2f}."
    )


    return insights

# ===================================
# REGIONAL INSIGHTS
# ===================================

def generate_regional_insights(regional_data):

    insights = []

    top_region = regional_data["Sales"].idxmax()
    top_region_sales = regional_data["Sales"].max()

    insights.append(
        f"{top_region} is the strongest region by sales, "
        f"generating {top_region_sales:,.2f}."
    )


    lowest_region = regional_data["Sales"].idxmin()
    lowest_region_sales = regional_data["Sales"].min()

    insights.append(
        f"{lowest_region} has the lowest sales "
        f"at {lowest_region_sales:,.2f}."
    )


    return insights