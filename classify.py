def classify_number_interactive():
    """
    Interactive number guessing game that asks questions to classify a number (1-9)
    """
    print("=" * 50)
    print("Think of a number between 1 and 9!")
    print("I'll ask you some questions to guess it.")
    print("=" * 50)
    print()
    
    # Question 1: Is it 5?
    response = input("Is your number 5? (yes/no): ").strip().lower()
    if response in ['yes', 'y']:
        print("\n🎉 Your number is: 5")
        return 5
    
    # Question 2: Is it even?
    response = input("Is your number even? (yes/no): ").strip().lower()
    is_even = response in ['yes', 'y']
    
    if is_even:
        # Even numbers: 2, 4, 6, 8
        response = input("Is your number a prime number? (yes/no): ").strip().lower()
        is_prime = response in ['yes', 'y']
        
        if is_prime:
            # Only even prime is 2
            print("\n🎉 Your number is: 2")
            return 2
        else:
            # Not prime: 4, 6, 8
            response = input("Is your number divisible by 3? (yes/no): ").strip().lower()
            div_by_3 = response in ['yes', 'y']
            
            if div_by_3:
                print("\n🎉 Your number is: 6")
                return 6
            else:
                # 4 or 8
                response = input("Is your number a perfect square? (yes/no): ").strip().lower()
                is_perfect_square = response in ['yes', 'y']
                
                if is_perfect_square:
                    print("\n🎉 Your number is: 4")
                    return 4
                else:
                    print("\n🎉 Your number is: 8")
                    return 8
    else:
        # Odd numbers: 1, 3, 7, 9
        response = input("Is your number a prime number? (yes/no): ").strip().lower()
        is_prime = response in ['yes', 'y']
        
        if is_prime:
            # Odd primes: 3, 7
            response = input("Is your number divisible by 3? (yes/no): ").strip().lower()
            div_by_3 = response in ['yes', 'y']
            
            if div_by_3:
                print("\n🎉 Your number is: 3")
                return 3
            else:
                print("\n🎉 Your number is: 7")
                return 7
        else:
            # Not prime odd: 1, 9
            response = input("Is your number a perfect square? (yes/no): ").strip().lower()
            is_perfect_square = response in ['yes', 'y']
            
            if is_perfect_square:
                print("\n🎉 Your number is: 9")
                return 9
            else:
                print("\n🎉 Your number is: 1")
                return 1


def classify_number_direct(num):
    """
    Direct classification for numbers 1-9
    """
    if num < 1 or num > 9:
        return "Number must be between 1 and 9"
    
    # Direct mapping
    classifications = {
        1: 1, 2: 2, 3: 3, 4: 4, 5: 5,
        6: 6, 7: 7, 8: 8, 9: 9
    }
    return classifications[num]


def show_menu():
    """
    Show menu and handle user choice
    """
    print("\n" + "=" * 50)
    print("NUMBER CLASSIFICATION SYSTEM (1-9)")
    print("=" * 50)
    print("1. Interactive Mode (I'll guess your number)")
    print("2. Direct Classification (Enter a number)")
    print("3. Show All Classifications")
    print("4. Exit")
    print("=" * 50)
    
    choice = input("\nEnter your choice (1-4): ").strip()
    return choice


def show_all_classifications():
    """
    Display classification for all numbers 1-9
    """
    print("\n" + "=" * 50)
    print("ALL NUMBER CLASSIFICATIONS (1-9)")
    print("=" * 50)
    
    for num in range(1, 10):
        is_prime = num in [2, 3, 5, 7]
        is_even = num % 2 == 0
        is_perfect_square = num in [1, 4, 9]
        div_by_2 = num % 2 == 0
        div_by_3 = num % 3 == 0
        
        print(f"\nNumber: {num} → Classified as: {num}")
        print(f"  Prime: {is_prime} | Even: {is_even} | Perfect Square: {is_perfect_square}")
        print(f"  Divisible by 2: {div_by_2} | Divisible by 3: {div_by_3}")


if __name__ == "__main__":
    while True:
        choice = show_menu()
        
        if choice == '1':
            # Interactive mode
            result = classify_number_interactive()
            print(f"\nClassification Result: {result}")
            
        elif choice == '2':
            # Direct classification
            try:
                num = int(input("\nEnter a number (1-9): ").strip())
                result = classify_number_direct(num)
                print(f"\n🎯 Number {num} is classified as: {result}")
            except ValueError:
                print("\n❌ Please enter a valid number!")
                
        elif choice == '3':
            # Show all
            show_all_classifications()
            
        elif choice == '4':
            # Exit
            print("\n👋 Goodbye!")
            break
            
        else:
            print("\n❌ Invalid choice! Please enter 1-4.")
        
        input("\nPress Enter to continue...")
