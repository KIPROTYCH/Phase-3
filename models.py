from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Create a SQLAlchemy engine and session
engine = create_engine('sqlite:///restaurant_reviews.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create a base class for declarative models
Base = declarative_base()

# Define the Restaurant model
class RestaurantModel(Base):
    __tablename__ = 'restaurants'

    restaurant_id = Column(Integer, primary_key=True)
    restaurant_name = Column(String)
    restaurant_location = Column(String)
    restaurant_cuisine = Column(String)
    price_level = Column(String)

    # Establish a one-to-many relationship with reviews
    reviews = relationship('ReviewModel', back_populates='restaurant')

    def get_all_reviews(self):
        # Return a list of strings with all the reviews for this restaurant
        review_strings = []
        for review in self.reviews:
            review_string = f"Review for {self.restaurant_name} by {review.customer_model.get_full_name()}: {review.rating} stars."
            review_strings.append(review_string)
        return review_strings

    @classmethod
    def get_fanciest(cls):
        # Return the restaurant instance with the highest price
        return session.query(cls).order_by(cls.price_level.desc()).first()

# Define the Customer model
class CustomerModel(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    # Establish a one-to-many relationship with reviews
    reviews = relationship('ReviewModel', back_populates='customer_model')

    def get_full_name(self):
        # Return the full name of the customer
        return f"{self.first_name} {self.last_name}"

    def get_favorite_restaurant(self):
        if not self.reviews:
            return None  # Return None if the customer has no reviews
        favorite_review = max(self.reviews, key=lambda review: int(review.rating))
        return favorite_review.restaurant  # Use the restaurant attribute directly

    def add_review(self, restaurant, rating):
        # Create a new review for the restaurant with the given rating
        new_review = ReviewModel(customer_model=self, restaurant=restaurant, rating=rating)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
        # Remove all reviews made by this customer for the specified restaurant
        reviews_to_delete = [review for review in self.reviews if review.restaurant == restaurant]
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()

    def get_restaurants(self):
        # Get the unique restaurants reviewed by this customer
        return list({review.restaurant for review in self.reviews})

# Define the Review model
class ReviewModel(Base):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True)
    rating = Column(String)
    comment = Column(Text)
    restaurant_id = Column(Integer, ForeignKey('restaurants.restaurant_id'))
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))

    # Establish many-to-one relationships with restaurant and customer
    restaurant = relationship('RestaurantModel', back_populates='reviews')
    customer_model = relationship('CustomerModel', back_populates='reviews')

    def get_full_review(self):
        # Return a string formatted as specified
        return f"Review for {self.restaurant.restaurant_name} by {self.customer_model.get_full_name()}: {self.rating} stars."

# Create the database tables
Base.metadata.create_all(engine)
