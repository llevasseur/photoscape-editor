
import argparse

def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Creates a PSX project of your choice for the Vancouver Canucks game today or a specified date.')

    # Add argument for the date
    parser.add_argument('--date', type=valid_date, help='Date in the format jan09-24.')

    # Parse the command line arguments
    args = parser.parse_args()

    # Determine date for game
    if (args.date):
        date_file = args.date.strftime('%b%d-%y').lower()
    else:
        date_file = datetime.now().strftime('%b%d-%y').lower()
        
    print(f'''
    Preview data has been fetched from {website} and saved to games/{date_file}/game-day.json
    ''')
    return


if __name__ == '__main__':
    main()