from app import HotelDynamicPricingModel
from datetime import datetime, timedelta
import json

def test_pricing_scenarios():
    """Test the trained pricing model with various scenarios"""
    
    print("🏨 Hotel Dynamic Pricing Model - Testing Suite")
    print("=" * 60)
    
    pricing_model = HotelDynamicPricingModel()
    
    # Loading existing model
    try:
        pricing_model.load_model('hotel_pricing_model.pkl')
        print("✅ Model loaded successfully from saved file!")
    except:
        print("📚 Training new model...")
        pricing_model.train_model()
        pricing_model.save_model()
    
    print("\n🔍 Testing Price Predictions")
    print("=" * 60)
    
    # Test scenarios
    test_cases = [
        {
            'name': '🎄 Christmas Premium Suite',
            'checkin_date': '2025-12-25',
            'checkout_date': '2025-12-27',
            'room_type': 'Suite',
            'num_rooms': 1
        },
        {
            'name': '💝 Valentine\'s Day Executive',
            'checkin_date': '2025-02-14',
            'checkout_date': '2025-02-16',
            'room_type': 'Executive',
            'num_rooms': 1
        },
        {
            'name': '🎆 New Year Premium',
            'checkin_date': '2025-12-31',
            'checkout_date': '2026-01-02',
            'room_type': 'Premium',
            'num_rooms': 1
        },
        {
            'name': '☀️ Summer Family Vacation',
            'checkin_date': '2025-07-15',
            'checkout_date': '2025-07-22',
            'room_type': 'Deluxe',
            'num_rooms': 3
        },
        {
            'name': '💼 Business Trip Weekday',
            'checkin_date': '2025-03-11',
            'checkout_date': '2025-03-13',
            'room_type': 'Standard',
            'num_rooms': 1
        },
        {
            'name': '🎉 Weekend Getaway',
            'checkin_date': '2025-08-02',
            'checkout_date': '2025-08-04',
            'room_type': 'Deluxe',
            'num_rooms': 2
        },
        {
            'name': '🏖️ Last Minute Booking',
            'checkin_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'checkout_date': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
            'room_type': 'Premium',
            'num_rooms': 1
        },
        {
            'name': '📅 Early Bird Booking',
            'checkin_date': (datetime.now() + timedelta(days=120)).strftime('%Y-%m-%d'),
            'checkout_date': (datetime.now() + timedelta(days=125)).strftime('%Y-%m-%d'),
            'room_type': 'Suite',
            'num_rooms': 1
        }
    ]
    
    # Run tests
    results = []
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {case['name']} ---")
        
        try:
            prediction = pricing_model.predict_price(
                checkin_date=case['checkin_date'],
                checkout_date=case['checkout_date'],
                room_type=case['room_type'],
                num_rooms=case['num_rooms']
            )
            
            checkin = datetime.strptime(case['checkin_date'], '%Y-%m-%d')
            checkout = datetime.strptime(case['checkout_date'], '%Y-%m-%d')
            nights = (checkout - checkin).days
            
            # results
            print(f"📅 Check-in: {case['checkin_date']}")
            print(f"📅 Check-out: {case['checkout_date']}")
            print(f"🏠 Room Type: {case['room_type']}")
            print(f"🛏️  Number of Rooms: {case['num_rooms']}")
            print(f"🌙 Nights: {nights}")
            print(f"🎊 Occasions: {', '.join(prediction['occasions']) if prediction['occasions'] else 'None'}")
            print(f"💰 Base Price: ₹{prediction['base_price']:.2f}")
            print(f"📈 Occasion Multiplier: {prediction['occasion_multiplier']:.2f}x")
            print(f"🏷️  Price per Night: ₹{prediction['predicted_price_per_night']:.2f}")
            print(f"💳 Total Price: ₹{prediction['total_price']:.2f}")
            
            
            results.append({
                'test_name': case['name'],
                'details': case,
                'prediction': prediction,
                'nights': nights,
                'total_price': prediction['total_price']
            })
            
            print("✅ Success")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results.append({
                'test_name': case['name'],
                'error': str(e)
            })
        
        print("-" * 50)
    
    # Summary
    print(f"\n📊 TESTING SUMMARY")
    print("=" * 60)
    
    successful_tests = [r for r in results if 'error' not in r]
    failed_tests = [r for r in results if 'error' in r]
    
    print(f"✅ Successful Tests: {len(successful_tests)}")
    print(f"❌ Failed Tests: {len(failed_tests)}")
    
    if successful_tests:
        print(f"\n💰 Price Range Summary:")
        prices = [r['total_price'] for r in successful_tests]
        print(f"   • Minimum: ₹{min(prices):.2f}")
        print(f"   • Maximum: ₹{max(prices):.2f}")
        print(f"   • Average: ₹{sum(prices)/len(prices):.2f}")
        
        print(f"\n🏆 Most Expensive: {max(successful_tests, key=lambda x: x['total_price'])['test_name']}")
        print(f"💎 Most Affordable: {min(successful_tests, key=lambda x: x['total_price'])['test_name']}")
    
    if failed_tests:
        print(f"\n❌ Failed Tests:")
        for test in failed_tests:
            print(f"   • {test['test_name']}: {test['error']}")
    
    return results

def interactive_price_test():
    """Interactive function to test custom pricing scenarios"""
    
    print(f"\n🎯 Interactive Price Testing")
    print("=" * 60)
    
    
    pricing_model = HotelDynamicPricingModel()
    try:
        pricing_model.load_model('hotel_pricing_model.pkl')
    except:
        print("Training model first...")
        pricing_model.train_model()
        pricing_model.save_model()
    
    while True:
        try:
            print(f"\n📝 Enter booking details (or 'quit' to exit):")
            
            checkin_date = input("Check-in date (YYYY-MM-DD): ").strip()
            if checkin_date.lower() == 'quit':
                break
                
            checkout_date = input("Check-out date (YYYY-MM-DD): ").strip()
            if checkout_date.lower() == 'quit':
                break
            
            print("Room types: Standard, Deluxe, Suite, Premium, Executive")
            room_type = input("Room type: ").strip()
            if room_type.lower() == 'quit':
                break
                
            num_rooms = int(input("Number of rooms: ").strip())
            
            
            prediction = pricing_model.predict_price(
                checkin_date=checkin_date,
                checkout_date=checkout_date,
                room_type=room_type,
                num_rooms=num_rooms
            )
            
            print(f"\n🎯 PRICE PREDICTION RESULT:")
            print(f"💰 Total Price: ₹{prediction['total_price']:.2f}")
            print(f"🏷️  Price per Night: ₹{prediction['predicted_price_per_night']:.2f}")
            print(f"🎊 Special Occasions: {', '.join(prediction['occasions']) if prediction['occasions'] else 'None'}")
            print(f"📈 Occasion Multiplier: {prediction['occasion_multiplier']:.2f}x")
            
        except KeyboardInterrupt:
            print(f"\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("Please try again with valid inputs.")

def quick_price_check():
    """Quick function to check a single price"""
    
    
    pricing_model = HotelDynamicPricingModel()
    
    try:
        pricing_model.load_model('hotel_pricing_model.pkl')
        print("✅ Model loaded successfully!")
    except:
        print("📚 Training model...")
        pricing_model.train_model()
        pricing_model.save_model()
    
    
    prediction = pricing_model.predict_price(
        checkin_date='2025-12-25',  # Christmas
        checkout_date='2025-12-27', 
        room_type='Deluxe',
        num_rooms=1
    )
    
    print(f"\n🎄 Christmas Weekend - Deluxe Room")
    print(f"💳 Total Price: ₹{prediction['total_price']:.2f}")
    print(f"🏷️  Price per Night: ₹{prediction['predicted_price_per_night']:.2f}")
    print(f"🎊 Occasions: {', '.join(prediction['occasions'])}")
    print(f"📈 Multiplier: {prediction['occasion_multiplier']:.2f}x")
    
    return prediction

if __name__ == "__main__":
    # Run different test modes based on user choice
    print("🏨 Hotel Dynamic Pricing Model - Test Suite")
    print("=" * 60)
    print("Choose testing mode:")
    print("1. Quick Price Check (Christmas example)")
    print("2. Full Test Suite (8 scenarios)")
    print("3. Interactive Testing")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            quick_price_check()
        elif choice == "2":
            test_pricing_scenarios()
        elif choice == "3":
            interactive_price_test()
        else:
            print("Running quick price check...")
            quick_price_check()
            
    except KeyboardInterrupt:
        print(f"\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Running default quick price check...")
        quick_price_check()