##############################################################################
## Imports and Libraries
##############################################################################
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
import io  
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import seaborn as sns
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist

##############################################################################
## web scripting and merging functions
##############################################################################
def normalize_country_names(data_dict):
    # Define name merges: key = old name, value = new unified name
    merge_map = {
        "Macedonia": "North Macedonia",
        "Czech Republic": "Czechia"
    }

    # Step 1: Merge old names into new keys
    for old_name, new_name in merge_map.items():
        if old_name in data_dict:
            if new_name not in data_dict:
                data_dict[new_name] = []
            data_dict[new_name].extend(data_dict[old_name])
            del data_dict[old_name]

    # Step 2: Normalize recipient names in values
    for giver in data_dict:
        data_dict[giver] = [merge_map.get(recipient, recipient) for recipient in data_dict[giver]]

    return data_dict

def get_all_12_point_given_history(start_year, end_year):
    """
    "This function loops through every Eurovision year (except 2020),
    grabs the Wikipedia table with final jury voting, cleans the data,
    saves it, and records who gave 12 points to whom.
    It returns a dictionary of all 12-point votes,
    and another with the full cleaned tables."
    :param start_year:
    :param end_year:
    :return: total_all_years_twelve_points, final_tables_per_year
    """
    final_tables_per_year = {}
    total_all_years_twelve_points = {}

    for year in [year for year in range(start_year, end_year +1 ) if year != 2020]:
        print(f"Processing {year}")
        """
         - Build the Wikipedia URL for that year
         - Send a request to get the page HTML
         - Parse the HTML using BeautifulSoup
         """
        url = f"https://en.wikipedia.org/wiki/Eurovision_Song_Contest_{year}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all("table", {"class": "wikitable"})
        """Loop through the tables to find the one that contains jury voting results for the final. Once found, stop the loop and remember the index."""
        for index, table in enumerate(tables):
            if (("Detailed jury voting results of the final") in table.get_text() or
                    ("Detailed voting results of the final") in table.get_text()):
                print(f"Found table index for {year}: {index}")
                break
        """Take the HTML code of the table, treat it like a file, and load it into a Pandas DataFrame"""
        html_str = str(tables[index])
        df = pd.read_html(io.StringIO(html_str))[0]

        # create original csv file for this year(before cleaning)
        df.to_csv(f"eurovision_{year}_votes.csv", index=False, encoding='utf-8-sig')

        """
        Different years have slightly different formats, so we clean the table based on the year
        - Remove extra columns (e.g., index or rank columns)
        - Focus on the first column (recipient names) and the score columns
        """
        if year in [2014,2015]: # in does years the table look different
            # create clean csv file for this year
            df = pd.read_csv(f"eurovision_{year}_votes.csv", skiprows=1)
            df.drop(df.columns[0], axis=1, inplace=True)
            df = df.iloc[1:]
            df = df.iloc[:, [0] + list(range(4, df.shape[1]))]

        elif year > 2015:
            # create clean csv file for this year
            df = pd.read_csv(f"eurovision_{year}_votes.csv", skiprows=2)
            df.drop(df.columns[0], axis=1, inplace=True)
            df = df.iloc[1:]
            df = df.iloc[:, [0] + list(range(4, df.shape[1]))]

        else:
            df.drop(df.columns[0], axis=1, inplace=True)
            df = df.iloc[:, [0] + list(range(2, df.shape[1]))]

        # create clean csv file for this year
        df.to_csv(f"eurovision_{year}_votes_clean.csv", index=False, encoding='utf-8-sig')

        # Save the cleaned full table for this year
        """Add this cleaned DataFrame to the dictionary so you can use it later"""
        final_tables_per_year[year] = df.copy()

        """
        Loop through each giver and recipient in the table:
        If the cell contains a 12, save the giver → recipient pair to a temporary dictionary.
        """
        twelve_points = {}
        for col_index in range(1, df.shape[1]):
            giver = df.columns[col_index]
            twelve_points[giver] = []

            for row_index in range(df.shape[0]):
                value = df.iat[row_index, col_index]
                if pd.notna(value) and value == 12:
                    recipient = df.iat[row_index, 0]
                    twelve_points[giver].append(recipient)
        """Add the current year’s 12-point votes to the overall history across all years"""
        # # איחוד לתוך מילון כולל
        for giver, recipients in twelve_points.items():
            if giver not in total_all_years_twelve_points:
                total_all_years_twelve_points[giver] = []
            total_all_years_twelve_points[giver].extend(recipients)

    """
    You get back:
    - A dictionary with all 12-point votes per country across all years
    - A dictionary with the cleaned voting tables per year
    """

    # pprint(total_all_years_twelve_points)
    return total_all_years_twelve_points, final_tables_per_year


##############################################################################
## getting all history of 12 point givers and receivers and export to Excel file
## Convert the total_all_years_dict to a DataFrame and save in a csv file
##############################################################################

# Get both values from your function
total_all_years_dict, separated_all_year_twelve_point = get_all_12_point_given_history(2010, 2025)

# Merge same country with different names
total_all_years_dict = normalize_country_names(total_all_years_dict)

#Export to Excel file with multiple sheets
with pd.ExcelWriter("eurovision_12_points_all_years.xlsx", engine='xlsxwriter') as writer:
    for year, df in separated_all_year_twelve_point.items():
        df.to_excel(writer, sheet_name=str(year), index=False)

# Convert the total_all_years_dict to a DataFrame
rows = []
for giver, recipients in total_all_years_dict.items():
    for recipient in recipients:
        rows.append([giver, recipient])
df_combined = pd.DataFrame(rows, columns=["Giver", "Recipient"])
# creates csv file for the data frame to not run every time the function and work easily with csv file to dataframe
df_combined.to_csv("eurovision_12_points_total_for_calculation.csv", index=False, encoding='utf-8-sig')


##############################################################################
## read from a csv file the total 12 point givers and receivers clean data to a DataFrame
##############################################################################

# read the data frame from the csv file
df = pd.read_csv("eurovision_12_points_total_for_calculation.csv", encoding='utf-8-sig')

##############################################################################
## Calculations
##############################################################################

def calculate_diversity(df, min_votes=0):
    """"
        - This function checks how "diverse" each country (Giver) is in giving 12 points.
        - It calculates, for each Giver, how many different countries they gave points to (unique),
        - how many times they gave points in total, and what the ratio is between them (DiversityRatio).
        - The function can also filter out countries that didn't give enough votes (using min_votes).
    """
    # Count how many total 12-point votes each Giver gave
    total_counts = df.groupby("Giver")["Recipient"].count()
    # Count how many different countries each Giver gave points to
    unique_counts = df.groupby("Giver")["Recipient"].nunique()
    # Calculate the diversity ratio: number of unique recipients divided by total votes
    diversity_ratio = unique_counts / total_counts ## Calculate ratio

    # # If we want to filter out Givers who gave very few votes
    if min_votes > 0:
        # Create a mask to keep only Givers who gave at least min_votes
        mask = total_counts >= min_votes # Boolean value means if the total country gives 12 points >= min_votes
        total_counts = total_counts[mask] # keeping only rows that mask with True value
        unique_counts = unique_counts[mask] # keeping only rows that mask with True value
        diversity_ratio = diversity_ratio[mask] # keeping only rows that mask with True value

    # Create a new DataFrame with the results for each Giver
    result_df = pd.DataFrame({
        'Total': total_counts, # Total votes given
        'Unique': unique_counts, # Number of different recipients
        'DiversityRatio': diversity_ratio # Unique / Total
    })
    return result_df


##############################################################################
## visual title 1
##############################################################################
"""
This code shows how "diverse" each country is 
when giving 12 points in Eurovision. 
It plots the number of different countries each country 
gave 12 points to, using colors (red = low diversity, 
green = high diversity) so it's easy to see which 
countries spread their votes more widely.
"""

#Calculate diversity first and get Total column
div_df = calculate_diversity(df)
## print(div_df)

# Get the 'Unique' column, which is the number of unique countries each giver gave 12 points to
unique_counts = div_df['Unique'].sort_values(ascending=False)

# Set the plot style to a clean white grid background
sns.set(style="whitegrid")

# Create a color gradient: from red (low diversity) to green (high diversity)
norm = plt.Normalize(vmin=0,vmax=unique_counts.max())
colors = plt.cm.RdYlGn(norm(unique_counts))

# Create a new figure for the plot, set figure size
plt.figure(figsize=(12, 8))

# Draw horizontal bar plot
bars = plt.barh(unique_counts.index, # y-axis: Giver countries
                unique_counts.values, # x-axis: Number of unique recipient countries
                color=colors, # Bar colors based on diversity
                edgecolor='black',  # Add border color here
                linewidth=1  # Border thickness
                )

plt.xlabel("Number of Unique Countries Received 12 Points", fontsize=12, weight='bold') # Set x-axis label
plt.ylabel("Giver Country", fontsize=12, weight='bold') # Set y-axis label
plt.title("Diversity of 12-Point Votes per Country (Low = Red, High = Green)", fontsize=15, weight='bold') # Set plot title
plt.grid(axis='x', linestyle='--', alpha=0.7) # Add vertical grid lines on x-axis for easier reading


# # Add labels
# for bar, value in zip(bars, unique_counts.values):
#     width = bar.get_width()
#     plt.text(width + 0.5,
#              bar.get_y() + bar.get_height() / 2,
#              str(value),
#              va='center',
#              fontsize=9,
#              color='black')

plt.yticks(fontsize=8) # Set smaller font size for y-axis ticks (country names)

plt.tight_layout() # Adjust layout to make sure nothing overlaps
plt.show()

##############################################################################
## visual title 2
##############################################################################
############################################################################################################
## Remove rows where total countries that voted is less than 5 and sort by DiversityRatio in ascending order
############################################################################################################

"""
 - Countries with low diversity (e.g., always giving 12s to the same few) are red
 - Countries with high diversity (spreading their votes widely) are green
 - Numbers on the bars make interpretation easier
"""
# Calculate diversity first and get Total column
df_diversity = calculate_diversity(df, min_votes=5)


# Sort by DiversityRatio ascending
filtered_ratio_sorted = df_diversity.sort_values(by="DiversityRatio", ascending=False)


# Set seaborn style for clean background
sns.set(style="whitegrid")

# גרדיאנט צבעים מאדום (מעט גיוון) לירוק (הרבה גיוון)
norm = plt.Normalize(vmin=filtered_ratio_sorted['DiversityRatio'].min(),
                     vmax=filtered_ratio_sorted['DiversityRatio'].max())
colors = plt.cm.RdYlGn(norm(filtered_ratio_sorted['DiversityRatio']))

# Create figure
plt.figure(figsize=(12, 8))

# Plot bars
bars = plt.barh(
    filtered_ratio_sorted.index,
    filtered_ratio_sorted['DiversityRatio'],
    color=colors,
    edgecolor='black'
)

# Title and labels
plt.title('Diversity of 12-Point Voting per Country (Unique / Total)', fontsize=15, weight='bold')
plt.xlabel('Diversity Ratio', fontsize=12, weight='bold')
plt.ylabel('Giver Country', fontsize=12, weight='bold')

# Annotate bars with ratio values
for bar, ratio in zip(bars, filtered_ratio_sorted['DiversityRatio']):
    plt.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
             f"{ratio:.2f}", va='center', fontsize=10)

# Tweak axes and grid
plt.xlim(0, 1.05)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis='x', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()



# ##############################################################################
# ## visual title 3
# ##############################################################################

"""
This code shows two side-by-side bar plots comparing Eurovision countries' 12-point voting diversity.

- Left plot (red): The 5 countries with the lowest diversity (they repeatedly give 12 points to the same countries).
- Right plot (green): The 5 countries with the highest diversity (they spread their 12 points more widely).

The code first calculates diversity, selects top and bottom countries, and then draws both plots with clear titles and labels.
"""
# Calculate diversity first and get Total column
filtered_ratio = calculate_diversity(df, min_votes=5)

# Identifying the top 5 and bottom 5
top_5 = filtered_ratio.sort_values(by="DiversityRatio", ascending=False).head(5)
bottom_5 = filtered_ratio.sort_values(by="DiversityRatio").head(5)

# Create a graph with two side-by-side axes
# One figure with two plots side by side
# Same y-axis to make them easy to compare
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Left graph – the least diverse
axes[0].bar(bottom_5.index, bottom_5["DiversityRatio"], color='red') # Draws red bars
axes[0].set_title("Bottom 5 Countries\n(Lowest Diversity Ratio)" ,fontsize=14, weight='bold' ) # Title: "Bottom 5 Countries"
axes[0].set_ylabel("Diversity Ratio",fontsize=12, weight='bold' ) # Adds rotation and boldness to the x-axis (country names)
axes[0].tick_params(axis='x', rotation=45) # Adds numeric labels on top of bars showing diversity values
for tick in axes[0].get_xticklabels():
    tick.set_fontweight('bold')

# Numeric labels on the bars (if it's a bar chart)
for i, val in enumerate(bottom_5["DiversityRatio"]):
    axes[0].text(i, val + 0.01, f"{val:.2f}", ha='center', va='bottom' , fontsize=8, weight='bold' )

# Right graph – most diverse
axes[1].bar(top_5.index, top_5["DiversityRatio"], color='green') # Draws green bars
axes[1].set_title("Top 5 Countries\n(Highest Diversity Ratio)", fontsize=14, weight='bold' ) # Title: "Top 5 Countries"
axes[1].tick_params(axis='x', rotation=45) # Adds numeric labels
for tick in axes[1].get_xticklabels():
    tick.set_fontweight('bold')

# Numeric labels on the columns
# Adds numeric labels
for i, val in enumerate(top_5["DiversityRatio"]):
    axes[1].text(i, val + 0.01, f"{val:.2f}", ha='center', va='bottom')

# Automatically arrange the graph layout
plt.suptitle("Countries Voting Diversity in Eurovision", fontsize=16, weight='bold' )
plt.tight_layout(rect=[0, 0, 1, 0.95]) # Adjusts spacing so titles and labels do not overlap
plt.show()



# ##############################################################################
# ## visual title 4
# ##############################################################################

"""
Bias Ratio (towards most-favored country)

For each giver country, calculate how often it gives 12 points to the same recipient over the years. Specifically:
Bias Ratio  = Max(count of 12-point votes to a single recipient) / Total 12-point votes given

This KPI ranges from:
 - 1.0 → the giver always gave 12 points to the same country.

 - 0.1 - 0.3 → some repeated preference.

 - ~0 → very diverse giving pattern.

This helps answer your academic question:
Are there countries that systematically give their 12 points to the same country, possibly due to cultural or political ties?
"""
# Calculate diversity first and get Total column (number of 12-point votes each country gave)
div_df = calculate_diversity(df, min_votes=5)

# Count how many times each "Giver" gave 12 points to each "Recipient"
giver_recipient_counts = df.groupby(["Giver", "Recipient"]).size().reset_index(name="Count")

# Keep only the givers that passed the minimum votes threshold (filtered in div_df)
giver_recipient_counts = giver_recipient_counts[giver_recipient_counts["Giver"].isin(div_df.index)]

# Find the recipient that each giver gave 12 points to the most (the "favorite" recipient)
idx = giver_recipient_counts.groupby("Giver")["Count"].idxmax()
max_recipient_df = giver_recipient_counts.loc[idx].copy()

# Add TotalGiven column from div_df# Add total 12-point votes given by each giver, from div_df
max_recipient_df = max_recipient_df.merge(div_df["Total"], left_on="Giver", right_index=True)

# Calculate bias ratio# Calculate the "bias ratio" = (most frequent recipient votes) / (total votes given)
max_recipient_df["bias_ratio"] = max_recipient_df["Count"] / max_recipient_df["Total"]

# Sort givers by their bias ratio in descending order
bias_df = max_recipient_df.sort_values(by="bias_ratio", ascending=False)

# Select the top 10 givers with the highest bias ratio
top_basis_df = bias_df.head(10)

# Set Seaborn plot style
sns.set(style="whitegrid")


# Normalize bias ratios for color scaling (min to max)
norm = mcolors.Normalize(vmin=top_basis_df["bias_ratio"].min(), vmax=top_basis_df["bias_ratio"].max())
cmap = plt.cm.RdYlGn  # Choose a color map (red-yellow-green)

# Create list of colors for bars based on bias ratios
bar_colors = [cmap(norm(val)) for val in top_basis_df["bias_ratio"]]

# Create a new figure with specific size
plt.figure(figsize=(10, 7))
# Draw horizontal bar plot
bars = plt.barh(
    top_basis_df["Giver"], # y-axis: Givers
    top_basis_df["bias_ratio"], # x-axis: Bias ratios
    color=bar_colors, # Bar colors
    edgecolor='black' # Bar edge color
)
# Invert y-axis so the highest ratio appears at the top
plt.gca().invert_yaxis()

plt.title("Top 10 Most Bias Ratio Eurovision 12-Point Givers", fontsize=15, weight='bold') # Add plot title
plt.xlabel("Bias Ratio (Most Common Recipient / Total 12s Given)", fontsize=12, weight='bold') # Add x-axis label

# Set font size and bold style for ticks
plt.xticks(fontsize=10, weight='bold')
plt.yticks(fontsize=10, weight='bold')

# Add text labels on each bar showing recipient name and ratio
for bar, recipient, score in zip(bars, top_basis_df["Recipient"], top_basis_df["bias_ratio"]):
    width = bar.get_width()
    label = f"{recipient} ({score:.2f})"
    plt.text(width + 0.01, bar.get_y() + bar.get_height() / 2,
             label, va='center', ha='left', fontsize=10, weight='bold', color='black') # countries names

plt.xlim(0, 1.05) # Set x-axis limits to make sure all text fits
plt.tight_layout() # Adjusts spacing so titles and labels do not overlap
plt.show() # Display the plot















