[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# FB_Group_Posts_Scraper

This Python script efficiently scrapes posts from the "ConsumerWatchdogBW" Facebook group, providing valuable insights into public discussions and opinions. It extracts relevant information such as post content, author, reactions, and comments, offering a structured dataset for analysis.

## Key Features:

1. Efficient Data Extraction: Leverages Selenium and BeautifulSoup to efficiently scrape posts, handling dynamic content and pagination.
2. Comprehensive Data Capture: Extracts essential information like post content, author, number of reactions, comments, and even individual comment text.
Flexible Output: Saves scraped data in a CSV format for easy analysis and visualization.
3. Customizable: Easily adaptable to scrape other Facebook groups by modifying the group URL and login credentials.

## Use Cases:
1. Market Research: Analyze public sentiment and trends within the consumer protection community.
2. Competitive Analysis: Gain insights into competitor activities and customer feedback.
3. Content Analysis: Identify frequently discussed topics and emerging trends.
4. Data-Driven Decision Making: Inform business strategies and product development based on consumer insights.

## How to Use

1. **Get Python**
   Get [Python](https://www.python.org/downloads/) (recommended Python 3.7+)


2. **Clone the Repository**:
   ```sh
   git clone https://github.com/SandileDesmondMfazi/FB_Group_Posts_Scraper.git
   ```

3. **Create Config JSON file for you log in details**

   ```sh
   echo '{"facebook":{"username": [Input Username],"password": [Input Password]}}' > Config_file.json

   For example:
   echo '{"facebook":{"username": 71234567,"password": "My_Password"}}' > Config_file.json 
   ```

4. **Create Virtual Environment**
   ```sh
   python3 -m venv FB_GROUPS_ENV
   ```

5. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

6. **Run the .ipynb file**

   Run each cell individually at first, note that some cells my take longer to run, but after the first run, they are good.

