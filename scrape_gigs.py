from fake_data import fake_gig_data  # Importing the fake data

def fetch_gig_data():
    """Fetches Fiverr gigs data (returns fake data for now)."""
    return fake_gig_data  # Returns the predefined dataset

# Run when executed directly
if __name__ == "__main__":
    gigs = fetch_gig_data()  # Get the fake data
    print("\nFetched Fiverr Gigs Data:\n")
    for gig in gigs:
        print(f"{gig['title']} by {gig['seller']} - ${gig['price']} ({gig['rating']}⭐ from {gig['reviews']} reviews)")
