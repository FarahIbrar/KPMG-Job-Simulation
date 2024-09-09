#!/usr/bin/env python
# coding: utf-8

# # KPMG - Data Analytics Task

# ### 1. **Exploratory Data Analysis (EDA)**
# 
# **Load and Inspect Data:**
# - **Import Libraries:** Using libraries like `pandas` for data manipulation and `matplotlib` or `seaborn` for visualization.
# - **Load Data:** Converting `.numbers` file to a `.csv` format if needed (in this case, it is already done), as Python handles `.csv` files directly. Alternatively, if you have other format file, you might need to use libraries like `pyexcel` or `openpyxl` for direct `.numbers` file handling (In this case, we don't).

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[4]:


# Load data
file_path = '/Users/farah/Desktop/Courses/KPMG - Job Simulation/Task_2/Dataset/Company Sales Dataset.csv'
data = pd.read_csv(file_path)


# In[5]:


# Inspect data
print(data.head())
print(data.info())
print(data.describe())


# In[ ]:





# ### 2. Data Cleaning
#    - **Check for Missing Values:** Ensure there are no missing values that could affect the analysis.
#    - **Data Types:** Verify that data types are correct (e.g., timestamps as datetime objects).
#    - **Duplicates:** Remove any duplicate entries if present.

# In[6]:


# Check for missing values
print(data.isnull().sum())


# In[7]:


# Convert timestamp to datetime
data['timestamp'] = pd.to_datetime(data['timestamp'])


# In[8]:


# Remove duplicates
data = data.drop_duplicates()


# In[13]:


#Check for data types
data_types = data.dtypes
print(data_types)


# In[ ]:





# ### 3. Basic Statistics
# 
# - Summary statistics for numerical columns.
# - Distribution of categorical variables (e.g., stores, regions).

# In[14]:


# Summary statistics
data.describe()


# In[15]:


# Distribution of categorical variables
data['store'].value_counts()
data['region'].value_counts()
data['product_item_category'].value_counts()


# ### 4. Initial Insights
#    - **Distribution Analysis:** Analyze distributions of key variables like `revenue`, `cost_of_goods_sold`, and `product_item_quantity`.
#    - **Visualizations:** Create charts to visualize sales trends, store performance, and product categories.

# In[17]:


# Visualize revenue distribution

# Create the plot
fig, ax = plt.subplots()
sns.histplot(data['revenue'], ax=ax)
ax.set_title('Revenue Distribution')

# Save the plot
fig.savefig('Revenue_Distribution.png')

# Show the plot
plt.show()


# In[18]:


# Revenue and cost distribution

plt.figure(figsize=(10, 6))
sns.histplot(data['revenue'], kde=True)
plt.title('Distribution of Revenue')

# Save the plot
plt.savefig('Distribution_of_Revenue.png')

# Show the plot
plt.show()


# In[22]:


# Visualize sales over time

# Ensure 'timestamp' is in datetime format
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Group by month and sum only numeric columns
monthly_revenue = data.groupby(data['timestamp'].dt.to_period('M')).sum(numeric_only=True)['revenue']

# Plot the results
plt.figure(figsize=(10, 6))
monthly_revenue.plot()
plt.title('Monthly Sales Trends')
plt.xlabel('Month')
plt.ylabel('Total Revenue')

# Save the plot
plt.savefig('Monthly_Sales_Trends.png')

# Show the plot
plt.show()


# In[24]:


# Store performance

store_performance = data.groupby('store').agg({
    'revenue': 'sum',
    'product_item_quantity': 'sum'
}).reset_index()

store_performance.sort_values(by='revenue', ascending=False, inplace=True)

# Store performance visualization
plt.figure(figsize=(12, 8))
store_performance.plot(kind='bar', x='store', y='revenue', legend=False, ax=plt.gca())
plt.title('Store Performance - Revenue')
plt.xlabel('Store')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45, ha='right')  # Rotate store names for better readability

# Save the plot
plt.savefig('Store_Performance_Revenue.png')

# Show the plot
plt.show()


# In[26]:


# Regional performance

# Create the regional performance DataFrame
region_performance = data.groupby('region').agg({
    'revenue': 'sum'
}).reset_index()

# Regional performance visualization
plt.figure(figsize=(12, 8))
region_performance.plot(kind='bar', x='region', y='revenue', legend=False, ax=plt.gca())
plt.title('Regional Performance - Revenue')
plt.xlabel('Region')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45, ha='right')  # Rotate region names for better readability

# Save the plot
plt.savefig('Regional_Performance_Revenue.png')

# Show the plot
plt.show()


# In[ ]:





# ### 4. Problem Solving:

# **1. Best and Worst Performing Stores:**
#    - **Aggregate Revenue and Profit by Store:**

# In[27]:


# Calculate total revenue and profit by store
store_performance = data.groupby('store').agg({
    'revenue': 'sum',
    'cost_of_goods_sold': 'sum'
   })
store_performance['profit'] = store_performance['revenue'] - store_performance['cost_of_goods_sold']
store_performance = store_performance.sort_values(by='profit', ascending=False)

print(store_performance)


# **2. Growth Potential Regions:**
#    - **Analyze Regional Sales Growth:**

# In[28]:


# Calculate total revenue by region
region_performance = data.groupby('region').agg({
    'revenue': 'sum'
})
region_performance = region_performance.sort_values(by='revenue', ascending=False)

print(region_performance)


# **3. Top 5 Products for New Stores:**
#    - **Determine Top Products by Profit:**

# In[29]:


# Calculate total revenue and profit by product
product_performance = data.groupby('product_item_id').agg({
    'revenue': 'sum',
    'cost_of_goods_sold': 'sum'
})
product_performance['profit'] = product_performance['revenue'] - product_performance['cost_of_goods_sold']
top_products = product_performance.sort_values(by='profit', ascending=False).head(5)

print(top_products)


# **4. Best and Worst Performing Stores:**
# - **Aggregate total revenue, quantity sold, and average revenue per transaction for each store.**

# In[33]:


# Best and worst performing stores

# Create the store performance DataFrame
store_performance = data.groupby('store').agg({
    'revenue': 'sum',
    'product_item_quantity': 'sum'
}).reset_index()

# Calculate average revenue per transaction
store_performance['avg_revenue_per_transaction'] = data.groupby('store')['revenue'].sum() / data.groupby('store')['revenue'].count()

# Sort by revenue
store_performance.sort_values(by='revenue', ascending=False, inplace=True)

# Identify best and worst performing stores
best_stores = store_performance.head(5)
worst_stores = store_performance.tail(5)

# Display results (for testing purposes)
print("Best Performing Stores:")
print(best_stores)

print("\nWorst Performing Stores:")
print(worst_stores)


# **5. Regions with Growth Potential:**
# - **Aggregate revenue by region and identify regions with high revenue growth.**

# In[34]:


# Revenue by region

# Verify the data
print(data.head())
print(data.columns)

# Group by region and sum revenue
region_performance = data.groupby('region').agg({
    'revenue': 'sum'
}).reset_index()

# Debug output
print(region_performance.head())

# Sort by revenue
region_performance.sort_values(by='revenue', ascending=False, inplace=True)

# Final output
print(region_performance.head())


# In[ ]:





# **6. Top 5 Products for New Stores:**
# - **Calculate the total profit and revenue for each product.**
# - **Identify the top 5 products with the highest revenue and profit.**

# In[35]:


# Total revenue and profit by product

# Verify the data
print(data.head())
print(data.columns)

# Group by product and aggregate revenue and cost
product_performance = data.groupby('product_item_id').agg({
    'revenue': 'sum',
    'cost_of_goods_sold': 'sum'
}).reset_index()

# Debug output
print(product_performance.head())

# Calculate profit
product_performance['profit'] = product_performance['revenue'] - product_performance['cost_of_goods_sold']
print(product_performance.head())

# Sort by profit
product_performance.sort_values(by='profit', ascending=False, inplace=True)

# Final output
top_5_products = product_performance.head(5)
print(top_5_products)


# In[42]:


# Top 5 and Bottom 5 stores:

# Aggregate revenue and quantity sold by store
store_performance = data.groupby('store').agg(
    revenue=('revenue', 'sum'),
    quantity_sold=('product_item_quantity', 'sum')
).reset_index()

# Sort stores by revenue
store_performance = store_performance.sort_values(by='revenue', ascending=False)

# Select top 5 and bottom 5 stores
top_5_stores = store_performance.head(5)
bottom_5_stores = store_performance.tail(5)

# Combine top 5 and bottom 5 stores for plotting
combined_stores = pd.concat([top_5_stores, bottom_5_stores])

# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Bar chart for Revenue
bar_width = 0.35
index = range(len(combined_stores))

bars1 = ax1.bar(index, combined_stores['revenue'], bar_width, label='Revenue', color='b')
ax2 = ax1.twinx()
bars2 = ax2.bar([i + bar_width for i in index], combined_stores['quantity_sold'], bar_width, label='Quantity Sold', color='g')

# Adding labels and title
ax1.set_xlabel('Store')
ax1.set_ylabel('Revenue', color='b')
ax2.set_ylabel('Quantity Sold', color='g')
ax1.set_title('Top 5 and Bottom 5 Stores: Revenue and Quantity Sold')
ax1.set_xticks([i + bar_width / 2 for i in index])
ax1.set_xticklabels(combined_stores['store'], rotation=45, ha='right')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.tight_layout()

# Save the chart as an image file
plt.savefig('Store_Performance_Comparison.png')

plt.show()


# In[52]:


# Top 5 products

# Calculate total revenue and cost of goods sold for each product category
category_performance = data.groupby('product_item_category').agg({
    'revenue': 'sum',
    'cost_of_goods_sold': 'sum'
}).reset_index()

# Calculate profit
category_performance['profit'] = category_performance['revenue'] - category_performance['cost_of_goods_sold']

# Sort by profit and get top 5 categories
top_5_categories = category_performance.sort_values(by='profit', ascending=False).head(5)

# Plotting
plt.figure(figsize=(12, 8))
plt.bar(top_5_categories['product_item_category'], top_5_categories['profit'], color='skyblue')
plt.xlabel('Product Category')
plt.ylabel('Profit')
plt.title('Top 5 Product Categories by Profit')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save plot to file
plt.savefig('Top_5_Products_by_Profit_Chart.png')
plt.show()


# In[45]:


# For Top 5 Stores
top_5_products = data[data['store'].isin(top_5_stores['store'])]
top_5_product_summary = top_5_products.groupby(['store', 'product_item_id']).agg(
    total_revenue=('revenue', 'sum'),
    total_quantity=('product_item_quantity', 'sum')
).reset_index()

plt.figure(figsize=(14, 7))
sns.barplot(x='product_item_id', y='total_revenue', hue='store', data=top_5_product_summary)
plt.title('Top 5 Stores: Product Performance')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_5_stores_products.png')
plt.show()

# For Bottom 5 Stores
bottom_5_products = data[data['store'].isin(bottom_5_stores['store'])]
bottom_5_product_summary = bottom_5_products.groupby(['store', 'product_item_id']).agg(
    total_revenue=('revenue', 'sum'),
    total_quantity=('product_item_quantity', 'sum')
).reset_index()

plt.figure(figsize=(14, 7))
sns.barplot(x='product_item_id', y='total_revenue', hue='store', data=bottom_5_product_summary)
plt.title('Bottom 5 Stores: Product Performance')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('bottom_5_stores_products.png')
plt.show()


# In[ ]:




