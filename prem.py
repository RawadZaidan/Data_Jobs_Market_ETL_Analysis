import scrapy
import pandas as pd

class PremierLeagueTableSpider(scrapy.Spider):
    name = 'premier_league_table'
    start_urls = ['https://www.premierleague.com/tables']

    def parse(self, response):
        # Create an empty DataFrame to store the data
        data = []

        # Extracting the team names and points from the Premier League table
        for row in response.css('table.standingTable tr[data-compseason]'):
            team_name = row.css('td.team span.long::text').get()
            points = row.css('td.points::text').get()

            if team_name and points:
                data.append({
                    'Team Name': team_name.strip(),
                    'Points': int(points)
                })

        # Create a pandas DataFrame from the collected data
        df = pd.DataFrame(data)

        # Print the DataFrame (you can save it or perform further operations)
        print(df)
