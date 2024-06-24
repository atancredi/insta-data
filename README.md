# insta-data
Python data scraper for instagram - working in 2023
Based on selenium (for cookies) + Instagram GraphQL API calls

## Usage
- A bit tricky: there has to be a `cookies` folder in the same directory, containing a `cookie.pkl` file with your instagram cookies (they must be valid, i.e. not expired).
- Install requests with `pip install requests`
- Run `python instascan` and wait for the result in the `results` and `results_comparisons` folders


## Roadmap
- automatic way to get cookies - like spawining a browser, logging in and getting cookies
- save results in a database and generate views on the data
- web ui