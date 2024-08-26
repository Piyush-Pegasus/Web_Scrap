from datetime import datetime
def get_day(date):
    words=date.split()
    day=int(words[1].split(',')[0])
    print(day)
    month=words[0]
    m=0
    if month=='Jan':
        m= 1
    elif month=='Feb':
        m= 2
    elif month=='Mar':
        m= 3
    elif month=='Apr':
        m= 4
    elif month=='May':
        m= 5
    elif month=='Jun':
        m= 6
    elif month=='Jul':
        m= 7
    elif month=='Aug':
        m= 8
    elif month=='Sep':
        m= 9
    elif month=='Oct':
        m= 10
    elif month=='Nov':
        m= 11
    elif month=='Dec':
        m= 12
    print(m)
    year=int(words[2])
    print(year)
    print(words)
    # Create a datetime object
    date_obj = datetime(year, m, day)
    
    # Get the day of the week
    day_of_week = date_obj.strftime('%A')
    
    print(day_of_week)

date="Aug 30, 2024"
get_day(date)