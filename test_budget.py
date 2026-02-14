from utils.budget import calculate_smart_budget

# Test Pakistan Luxury calculation
result = calculate_smart_budget('Pakistan', 'Luxury', 2, 7, 'PKR')

print(f"\n=== Budget Test: Pakistan - Luxury - 7 Days - 2 People ===")
print(f"Total Cost: {result['total_cost']:,.2f} PKR")
print(f"Exchange Rate (USD to PKR): {result['exchange_rate']:.2f}")
print(f"Per Person: {result['per_person_cost']:,.2f} PKR")
print(f"Per Day: {result['daily_cost']:,.2f} PKR")
print(f"\nBreakdown:")
for category, amount in result['breakdown'].items():
    print(f"  {category}: {amount:,.2f} PKR")
print(f"\nCountry Category: {result['country_category']}")
