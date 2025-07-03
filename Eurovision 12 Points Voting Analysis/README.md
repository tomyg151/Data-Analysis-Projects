# Eurovision "Douze Points" (12-Point) Voting Analysis
## About
<p>
Eurovision voting has long been suspected of being influenced by political or cultural biases. This project explores whether there are "common giver" countries that consistently award 12 points to the same countries over the years.
</P>
<p>
This project analyzes the voting patterns in the Eurovision Song Contest, focusing on the "Douze Points" (12 points) votes   awarded by each country.
</P>

### Research Question

Do the 12-point voting patterns in the Eurovision Song Contest indicate a persistent bias among countries, or do they demonstrate diversity and evolving trends over time?

** Data Collection

We scraped data from Wikipedia, extracting tables showing how many points each country gave to others (based on jury votes). Our main focus was on which country each country awarded its 12 points to.

### Data period
**Years analyzed:** 2010–2025 (excluding 2020 since there was no contest due to COVID-19).

### Data Sources
- **Wikipedia-2010:**<a href="https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2010#Detailed_voting_results">
Eurovision Song Contest 2010
</a><br>
- **Wikipedia-2011:** <a href="https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2011#Detailed_voting_results">
Eurovision Song Contest 2011
</a><br>
- **Wikipedia-2012:**<a href="https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2012#Detailed_voting_results">
Eurovision Song Contest 2012
</a><br>
- **Wikipedia-2013:**<a href="https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2013#Detailed_voting_results">
Eurovision Song Contest 2013
</a><br>
- **Wikipedia-2014:**<a href="https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2014#Detailed_voting_results">
Eurovision Song Contest 2014
</a><br>
- **Wikipedia-2015:**<a href="https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2015#Detailed_voting_results">
Eurovision Song Contest 2015
</a><br>
- **Wikipedia-2016:**<a href="https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2016#Detailed_voting_results">
Eurovision Song Contest 2016
</a><br>
- **Wikipedia-2017:**<a href="https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2017#Detailed_voting_results">
Eurovision Song Contest 2017
</a><br>
- **Wikipedia-2018:**<a href="https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2018#Detailed_voting_results">
Eurovision Song Contest 2018
</a><br>
- **Wikipedia-2019:**<a href="https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2019#Detailed_voting_results">
Eurovision Song Contest 2019
</a><br>
- **Wikipedia-2020:**<a href="https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2020#Detailed_voting_results">
Eurovision Song Contest 2020 — (cancelled) (Cancelled due to COVID-19)
</a><br>
- **Wikipedia-2021:**<a href="https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2021#Detailed_voting_results">
Eurovision Song Contest 2021
</a><br>
- **Wikipedia-2022:**<a href="https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2022#Detailed_voting_results">
Eurovision Song Contest 2022
</a><br>
- **Wikipedia-2023:**<a href="https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2023#Detailed_voting_results">
Eurovision Song Contest 2023
</a><br>
- **Wikipedia-2024:**<a href="https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2024#Detailed_voting_results">
Eurovision Song Contest 2024
</a><br>
- **Wikipedia-2025:**<a href="https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2025#Detailed_voting_results">
Eurovision Song Contest 2025
</a>
<br>

## 📋 Data Categories (Metadata)
- **year** — Year of the Eurovision contest
- **giver_country** — Country giving the 12 points
- **receiver_country** — Country receiving the 12 points
- **votes_12_count** — Number of times the giver gave 12 points to the receiver
- **total_votes** — Total number of voting years for the giver country
- **unique_recipients** — Number of unique countries that received 12 points from the giver
- **diversity_ratio** — Ratio of unique recipients to total votes (range 0 to 1)
- **loyalty_ratio** — Ratio of votes given to a specific receiver divided by total votes

### Special cases handled
- **2020:** No contest, skipped.
- Country name changes:<br>
                   * Macedonia vs North Macedonia<br>
                   * Czech Republic vs Czechia These were unified in the data.<br>
- 2014 and 2015 tables: Columns had different formats — handled with year-specific cleaning steps.

## ⚙️ Methodology and Analysis Steps

➡️ **Collect data** —  Using python scrape 12-point voting data from Wikipedia (2010–2025).

➡️ **Clean data** — Handle missing years, unify country names, adjust formats and structuring dataframes.

➡️ **Feature engineering** — Calculate unique votes, diversity ratio, loyalty ratio.

➡️ **Visualize** — Plot diversity per country and top loyalty pairs.

➡️ **Interpret** — Identify biases and summarize key patterns and statistical summaries.

### Data Processing

After scraping, we consolidated all data into one unified DataFrame containing only the countries that received 12 points from each giver country.

To assess diversity, we counted how many unique countries each giver awarded 12 points to over the years. Initially, we only counted unique recipient countries regardless of how many times each appeared.

However, we realized that not all countries participated every year. For example, Turkey only voted three times during this period, so comparing it directly to countries with 15 votes would be misleading.

![image](https://github.com/user-attachments/assets/88f56ece-0306-45a3-9045-523fcb781c76)

## 📈 KPI (Key Performance Indicators)
### 🎯 Diversity Ratio
Measures how diverse a country's 12-point votes are.
Calculation:

Number of unique countries that received 12 points
--------------------------------------------------
Total number of years the country gave votes

- Value close to 1 → High diversity.
- Value close to 0 → Strong bias.

### 🤝 Loyalty Ratio

Measures how often a country gave 12 points to the same specific country.
Calculation:

Times country A gave 12 points to country B
-------------------------------------------
Total votes given by country A

- High value → Strong "loyalty" to a specific country.

## 📊 Visualizations

**🟢 Diversity Ratio per Country:** 

Measures how diverse each country's 12-point votes are over the years (red = low diversity, green = high diversity)..
- Value close to 1 → highly diverse (votes for different countries each year).
- Value close to 0 → highly biased (votes for the same country repeatedly).

![image](https://github.com/user-attachments/assets/41ad6da1-4b3e-4f2a-b103-bfbae84a23d3)

**🔵 Top 5 Most Diverse vs Top 5 Most Biased Countries:**  
Highlights countries with the most diverse and most biased voting patterns.

![image](https://github.com/user-attachments/assets/483b525d-3c8b-45f1-9079-b89186ee8562)

**🟠 Top 10 Most Common 12-Point Pairs:**
- Displays the strongest "loyalty" relationships — who consistently gives 12 points to whom.


## Results
### Diversity Example
**We found a clear difference between countries:**

- **Hungary:** Most diverse (diversity ratio = 1), always gave 12 points to different countries.

- **Cyprus:** Least diverse (diversity ratio = 0.36), often gave points to the same count

## Conclusion
This analysis shows that some countries demonstrate consistent 12-point voting patterns, suggesting potential biases that may reflect political or cultural alliances rather than purely musical preferences.

While strong patterns were found, we did not establish direct causality.

## 📁 Project Structure
📂 eurovision-12points-analysis<br/>
│-- 📁 **data**                # Raw and processed data files<br/>
│-- 📁 **src**         # Python scripts (scraper, cleaning, analysis)<br/>
│-- 📁 **visualizations**      # Saved plots and images<br/>
│-- **README.md**             # Project documentation<br/>
