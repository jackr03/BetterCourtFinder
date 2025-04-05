import time

from datetime import timedelta, date
from court_finder import CourtFinder
from utils import get_day_of_week

def main():
    # Check the next 6 days for badminton courts
    court_finder = CourtFinder()
    current_date = date.today()
    for i in range(6):
        print(f'Checking date: {current_date} ({get_day_of_week(current_date)})')
        all_available_courts = court_finder.get_all_available_badminton_courts(current_date)
        if all_available_courts:
            print('\n'.join(map(str, all_available_courts)))
        else:
            print('No available courts')
        print()

        # Wait for 2 seconds so we don't get banned
        time.sleep(2)
        current_date += timedelta(days=1)

if __name__ == '__main__':
    main()
