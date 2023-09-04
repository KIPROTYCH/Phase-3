from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import RestaurantModel, CustomerModel, ReviewModel

# Create a SQLAlchemy engine and session
engine = create_engine('sqlite:///restaurant_reviews.db')
Session = sessionmaker(bind=engine)
session = Session()

def seed_data():
    # Create and add sample data to the database
    # You can customize this data as needed
    restaurant1 = RestaurantModel(restaurant_name="Chicken Delight", restaurant_location="Kenya", restaurant_cuisine="Grilled Chicken", price_level="Ksh 10000")
    restaurant2 = RestaurantModel(restaurant_name="Juice Express", restaurant_location="Uganda", restaurant_cuisine="Apple Juice", price_level="Ksh 20000")
    customer1 = CustomerModel(first_name="Cheryl", last_name="Yegon")
    customer2 = CustomerModel(first_name="Taylor", last_name="Swift")
    review1 = ReviewModel(rating="27", comment="Great meal", restaurant=restaurant1, customer_model=customer1)
    review2 = ReviewModel(rating="30", comment="Enjoyed the Drink.", restaurant=restaurant1, customer_model=customer2)
    review3 = ReviewModel(rating="5", comment="Excellent!", restaurant=restaurant2, customer_model=customer1)
    session.add_all([restaurant1, restaurant2, customer1, customer2, review1, review2, review3])
    session.commit()

# Function to print the deliverables
def print_deliverables():
    # Retrieve all restaurants and distinct customers from the database
    restaurants = session.query(RestaurantModel).all()
    customers = session.query(CustomerModel).distinct(CustomerModel.customer_id).all()  # Use distinct() to retrieve distinct customers

    # Example 2: Print the favorite restaurant for each customer and its price
    print("\nFavorite Restaurants with Prices:")
    for customer in customers:
        favorite = customer.get_favorite_restaurant()
        if favorite:
            print(f"{customer.get_full_name()}'s favorite restaurant is {favorite.restaurant_name} with a price of {favorite.price_level}")
        else:
            print(f"{customer.get_full_name()} has no favorite restaurant.")

    # Example 3: Print the first few reviews for each restaurant
    print("\nFirst Few Reviews for Restaurants:")
    for restaurant in restaurants:
        print(f"Reviews for {restaurant.restaurant_name}:")
        reviews = restaurant.get_all_reviews()[:5]  # Limit the output to the first 5 reviews
        for review in reviews:
            print(review)

if __name__ == "__main__":
    # Seed the database with sample data
    seed_data()

    # Print the deliverables
    print_deliverables()
