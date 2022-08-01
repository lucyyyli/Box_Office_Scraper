import requests
import csv
from bs4 import BeautifulSoup
import datetime

min_year = 1980
current_year = int(datetime.datetime.now().year)
year = input("Please enter year (%s-%s): "%(str(min_year), str(current_year)))
if int(year) < min_year or int(year) > current_year:
    print("The desired year is not available :(")
else:
    url = "https://www.boxofficemojo.com/year/world/%s/"%year
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    box_office_list = soup.find_all("tr")

    max_entries = 100
    num_entries = int(input("Please enter the number of entries (1-%s): "%(str(max_entries))))
    while num_entries < 1 or num_entries > max_entries:
        print("Please enter a valid number of entries!")
        num_entries = int(input("Please enter the number of entries (1-%s): "%(str(max_entries))))
    import_details = input("Would you like to write the details to a CSV file? (Y or N): ")
    while import_details.lower() != 'y' and import_details.lower() != 'n':
        print("Please enter a valid command!")
        import_details = input("Would you like to write the details to a CSV file? (Y or N): ")

    print("The %s Highest Grossing Movies of %s: "%(num_entries, year))

    for i in range (1, num_entries+1):
        movie = box_office_list[i].find("a")
        title = movie.text
        world_gross = box_office_list[i].find("td", {"class": "a-text-right mojo-field-type-money"}).text
        print(str(i) + ". " + title + ": " + world_gross)

        if import_details.lower() == 'y':
            grosses = box_office_list[i].find_all("td", {"class": "a-text-right mojo-field-type-money"})
            domestic_gross = grosses[1].text
            foreign_gross = grosses[2].text
            splits = box_office_list[i].find_all("td", {"class": "a-text-right mojo-field-type-percent"})
            domestic_split = splits[0].text
            foreign_split = splits[1].text
            link = "https://www.boxofficemojo.com/" + movie.get('href')

            file_name = "%s_highest_grossing_movies_of_%s.csv"%(num_entries, year)
            if i == 1:
                header = ['RANK', 'TITLE', 'WORLDWIDE', 'DOMESTIC', 'SPLIT', 'FOREIGN', 'SPLIT', 'LINK']
                with open(file_name, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
            entry_row = [i, title, world_gross, domestic_gross, domestic_split, foreign_gross, foreign_split, link]
            with open(file_name, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(entry_row)
