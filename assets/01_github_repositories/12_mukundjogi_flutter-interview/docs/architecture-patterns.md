# Architecture Patterns

## Table of Contents
- [Clean Architecture](#clean-architecture)
- [MVVM Pattern](#mvvm-pattern)
- [Repository Pattern](#repository-pattern)
- [SOLID Principles](#solid-principles)
- [Multi-Module Architecture](#multi-module-architecture)
- [Interview Questions & Answers](#interview-questions--answers)

## Clean Architecture

**Layers:**

```
Presentation Layer (UI)
    ↓
Domain Layer (Business Logic)
    ↓
Data Layer (Data Sources)
```

**Example:**

```dart
// Domain Layer
class User {
  final String id;
  final String name;
}

abstract class UserRepository {
  Future<User> getUser(String id);
}

// Data Layer
class UserRepositoryImpl implements UserRepository {
  final ApiService api;
  UserRepositoryImpl(this.api);
  
  @override
  Future<User> getUser(String id) async {
    final data = await api.getUser(id);
    return User.fromJson(data);
  }
}

// Presentation Layer
class UserViewModel extends ChangeNotifier {
  final UserRepository repository;
  UserViewModel(this.repository);
  
  User? user;
  
  Future<void> loadUser(String id) async {
    user = await repository.getUser(id);
    notifyListeners();
  }
}
```

## MVVM Pattern

**Model-View-ViewModel:**

```dart
// Model
class User {
  final String name;
  User(this.name);
}

// ViewModel
class UserViewModel extends ChangeNotifier {
  User? _user;
  User? get user => _user;
  
  void loadUser() {
    _user = User('John');
    notifyListeners();
  }
}

// View
class UserView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<UserViewModel>(
      builder: (context, viewModel, child) {
        return Text(viewModel.user?.name ?? 'Loading');
      },
    );
  }
}
```

## Repository Pattern

**Repository Implementation:**

```dart
abstract class UserRepository {
  Future<User> getUser(String id);
  Future<void> saveUser(User user);
}

class UserRepositoryImpl implements UserRepository {
  final ApiService api;
  final LocalDatabase db;
  
  UserRepositoryImpl(this.api, this.db);
  
  @override
  Future<User> getUser(String id) async {
    // Try local first
    final localUser = await db.getUser(id);
    if (localUser != null) return localUser;
    
    // Fetch from API
    final user = await api.getUser(id);
    await db.saveUser(user);
    return user;
  }
}
```

## SOLID Principles

**What is SOLID?**

SOLID is an acronym for five design principles that make code more maintainable, flexible, and easier to understand. Think of SOLID like building a house - each principle is like a rule that ensures the house is well-built and won't collapse.

**Simple Analogy:**

Think of SOLID principles like rules for a restaurant:
- **Single Responsibility**: Each chef has one job (one chef for desserts, one for main courses)
- **Open/Closed**: You can add new menu items without changing existing recipes
- **Liskov Substitution**: Any dessert chef can replace another dessert chef
- **Interface Segregation**: Chefs only learn what they need (dessert chef doesn't need to know main course recipes)
- **Dependency Inversion**: Restaurant depends on "chef" concept, not specific chefs

### S - Single Responsibility Principle (SRP)

**Simple Explanation:**

A class should have only one reason to change. Think of it like a worker who has one job - a plumber fixes pipes, an electrician fixes wires. They don't do each other's jobs.

**Simple Analogy:**

Think of Single Responsibility like a toolbox:
- **Bad**: One tool that tries to be a hammer, screwdriver, and wrench (doesn't work well)
- **Good**: Separate tools for each job (each tool does one thing perfectly)

**Bad Example (Violates SRP):**

```dart
// BAD: This class does too many things
// It handles user data, sends emails, and saves to database
// If email service changes, or database changes, this class needs to change
// That's multiple reasons to change - violates SRP!
class UserManager {
  // This class is doing too much!
  
  // Responsibility 1: User data management
  void createUser(String name, String email) {
    // Create user logic
  }
  
  // Responsibility 2: Email sending (should be separate!)
  void sendWelcomeEmail(String email) {
    // Email sending logic - this doesn't belong here!
  }
  
  // Responsibility 3: Database operations (should be separate!)
  void saveToDatabase(User user) {
    // Database logic - this doesn't belong here either!
  }
}
```

**Good Example (Follows SRP):**

```dart
// GOOD: Each class has one responsibility
// Think of it as having separate workers for separate jobs

// Class 1: Only handles user data
// This class only changes if user data structure changes
class UserService {
  // Single responsibility: Manage user data
  // Think of it as a worker who only handles user information
  User createUser(String name, String email) {
    // Only user creation logic here
    return User(name: name, email: email);
  }
  
  User updateUser(User user, String newName) {
    // Only user update logic here
    return user.copyWith(name: newName);
  }
}

// Class 2: Only handles email operations
// This class only changes if email service changes
class EmailService {
  // Single responsibility: Send emails
  // Think of it as a worker who only sends emails
  Future<void> sendWelcomeEmail(String email) async {
    // Only email sending logic here
    print('Sending welcome email to $email');
  }
  
  Future<void> sendPasswordResetEmail(String email) async {
    // Only email logic here
    print('Sending password reset email to $email');
  }
}

// Class 3: Only handles database operations
// This class only changes if database structure changes
class UserRepository {
  // Single responsibility: Save/load users from database
  // Think of it as a worker who only handles database
  Future<void> saveUser(User user) async {
    // Only database save logic here
    print('Saving user to database: ${user.name}');
  }
  
  Future<User?> getUser(String id) async {
    // Only database load logic here
    return null; // Simplified
  }
}

// Now we can use them together
class UserController {
  // This class coordinates the three services
  // But each service has its own single responsibility
  final UserService userService;
  final EmailService emailService;
  final UserRepository userRepository;
  
  UserController({
    required this.userService,
    required this.emailService,
    required this.userRepository,
  });
  
  Future<void> registerUser(String name, String email) async {
    // Use each service for its specific job
    final user = userService.createUser(name, email);
    await userRepository.saveUser(user);
    await emailService.sendWelcomeEmail(email);
  }
}
```

**Step-by-Step Explanation:**
1. **Bad Example**: One class does user management, email sending, and database operations
2. **Problem**: If email service changes, or database changes, the UserManager class needs to change
3. **Good Example**: Split into three classes, each with one responsibility
4. **UserService**: Only handles user data
5. **EmailService**: Only handles emails
6. **UserRepository**: Only handles database
7. **UserController**: Coordinates them (but doesn't do their jobs)

**Why This Works:**
- Each class has one reason to change
- Easier to test (test email separately from database)
- Easier to maintain (change email logic without touching database code)
- Easier to understand (each class does one thing)

### O - Open/Closed Principle (OCP)

**Simple Explanation:**

Software entities should be open for extension but closed for modification. Think of it like a phone - you can add apps (extend) without changing the phone itself (closed for modification).

**Simple Analogy:**

Think of Open/Closed like a plugin system:
- **Closed**: The main system doesn't change
- **Open**: You can add new plugins without changing the system

**Bad Example (Violates OCP):**

```dart
// BAD: If we want to add a new payment method, we have to modify this class
// This violates "closed for modification"
class PaymentProcessor {
  // This class is closed for extension - we can't add new payment methods easily
  void processPayment(String method, double amount) {
    // If we want to add a new payment method, we have to modify this code
    // That's bad because we're changing existing, working code
    if (method == 'credit_card') {
      // Credit card processing
      print('Processing credit card: $amount');
    } else if (method == 'paypal') {
      // PayPal processing
      print('Processing PayPal: $amount');
    } else if (method == 'bitcoin') {
      // Bitcoin processing - we had to ADD this, modifying the class
      print('Processing Bitcoin: $amount');
    }
    // Every time we add a new payment method, we modify this class
    // This is dangerous because we might break existing code!
  }
}
```

**Good Example (Follows OCP):**

```dart
// GOOD: Open for extension, closed for modification
// We can add new payment methods without changing existing code

// Abstract class defines the contract
// Think of it as a blueprint for payment methods
abstract class PaymentMethod {
  // This is the interface that all payment methods must follow
  // Think of it as saying "all payment methods must be able to pay"
  Future<void> pay(double amount);
}

// Credit card implementation
// This extends the PaymentMethod (open for extension)
// But we didn't modify PaymentMethod (closed for modification)
class CreditCardPayment implements PaymentMethod {
  final String cardNumber;
  CreditCardPayment(this.cardNumber);
  
  @override
  Future<void> pay(double amount) async {
    // Credit card specific payment logic
    // Think of it as a specific way to pay using credit card
    print('Processing credit card $cardNumber: \$$amount');
    // In real app, this would call credit card API
  }
}

// PayPal implementation
// We can add this without modifying CreditCardPayment or PaymentMethod
// This is "open for extension"
class PayPalPayment implements PaymentMethod {
  final String email;
  PayPalPayment(this.email);
  
  @override
  Future<void> pay(double amount) async {
    // PayPal specific payment logic
    // Think of it as a specific way to pay using PayPal
    print('Processing PayPal $email: \$$amount');
    // In real app, this would call PayPal API
  }
}

// Bitcoin implementation
// We can add this NEW payment method without changing ANY existing code!
// This is the power of Open/Closed Principle
class BitcoinPayment implements PaymentMethod {
  final String walletAddress;
  BitcoinPayment(this.walletAddress);
  
  @override
  Future<void> pay(double amount) async {
    // Bitcoin specific payment logic
    // We added this new payment method without modifying old code
    print('Processing Bitcoin $walletAddress: \$$amount');
    // In real app, this would call Bitcoin API
  }
}

// Payment processor that uses the abstraction
// This class doesn't need to change when we add new payment methods!
// It's "closed for modification"
class PaymentProcessor {
  // This method accepts any PaymentMethod
  // Think of it as accepting any payment plugin
  Future<void> processPayment(PaymentMethod paymentMethod, double amount) async {
    // We don't care what type of payment it is
    // We just call pay() - polymorphism handles the rest
    // This code never needs to change, even if we add 100 new payment methods!
    await paymentMethod.pay(amount);
  }
}

// Usage:
void main() async {
  final processor = PaymentProcessor();
  
  // Use credit card - existing code works
  final creditCard = CreditCardPayment('1234-5678-9012-3456');
  await processor.processPayment(creditCard, 100.0);
  
  // Use PayPal - existing code works
  final paypal = PayPalPayment('user@example.com');
  await processor.processPayment(paypal, 100.0);
  
  // Use Bitcoin - NEW payment method, but NO changes to PaymentProcessor!
  // This is "open for extension"
  final bitcoin = BitcoinPayment('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa');
  await processor.processPayment(bitcoin, 100.0);
  
  // We can add as many payment methods as we want
  // Without ever modifying PaymentProcessor or existing payment classes!
}
```

**Step-by-Step Explanation:**
1. **Bad Example**: PaymentProcessor has if-else statements for each payment method
2. **Problem**: Adding a new payment method requires modifying the existing class
3. **Good Example**: Use abstract class PaymentMethod as interface
4. **Each payment method** implements PaymentMethod interface
5. **PaymentProcessor** uses the abstraction, not concrete classes
6. **To add new payment method**: Just create new class implementing PaymentMethod
7. **No modification needed** to PaymentProcessor or existing payment classes

**Why This Works:**
- Can add new features without changing existing code
- Reduces risk of breaking existing functionality
- Makes code more maintainable
- Follows polymorphism principles

### L - Liskov Substitution Principle (LSP)

**Simple Explanation:**

Objects of a superclass should be replaceable with objects of its subclasses without breaking the application. Think of it like batteries - any AA battery should work in any device that needs AA batteries.

**Simple Analogy:**

Think of Liskov Substitution like a parking lot:
- **Base class**: "Vehicle" (can park)
- **Subclasses**: Car, Motorcycle, Truck
- **Rule**: Any vehicle should be able to park in a parking spot
- **Violation**: If a "Vehicle" can't park, it breaks the rule

**Bad Example (Violates LSP):**

```dart
// BAD: Rectangle and Square violate Liskov Substitution
// A Square is a Rectangle, but they behave differently
// You can't always substitute Square for Rectangle

class Rectangle {
  double width;
  double height;
  
  Rectangle(this.width, this.height);
  
  void setWidth(double w) {
    width = w;
  }
  
  void setHeight(double h) {
    height = h;
  }
  
  double getArea() {
    return width * height;
  }
}

// This violates LSP because Square changes the behavior of setWidth/setHeight
// If code expects Rectangle behavior, Square will break it
class Square extends Rectangle {
  Square(double side) : super(side, side);
  
  // Problem: This changes the behavior!
  // For Rectangle, setWidth only changes width
  // For Square, setWidth changes both width AND height
  // This breaks the expectation that Square can replace Rectangle
  @override
  void setWidth(double w) {
    super.setWidth(w);
    super.setHeight(w); // This is unexpected behavior!
  }
  
  @override
  void setHeight(double h) {
    super.setWidth(h); // This is unexpected behavior!
    super.setHeight(h);
  }
}

// This function expects Rectangle behavior
// But Square breaks this expectation!
void testRectangle(Rectangle rectangle) {
  rectangle.setWidth(5);
  rectangle.setHeight(4);
  
  // We expect area to be 5 * 4 = 20
  // But if rectangle is actually a Square, area becomes 4 * 4 = 16
  // This breaks the function's expectations!
  assert(rectangle.getArea() == 20); // This will fail for Square!
}
```

**Good Example (Follows LSP):**

```dart
// GOOD: Proper inheritance that follows Liskov Substitution

// Base class defines the contract
// Think of it as defining what all shapes can do
abstract class Shape {
  // All shapes must be able to calculate area
  // Think of it as a requirement: "if you're a shape, you must have an area"
  double getArea();
}

// Rectangle implementation
// This can be used anywhere Shape is expected
class Rectangle implements Shape {
  double width;
  double height;
  
  Rectangle(this.width, this.height);
  
  @override
  double getArea() {
    return width * height;
  }
  
  // Rectangle-specific methods
  void setWidth(double w) {
    width = w;
  }
  
  void setHeight(double h) {
    height = h;
  }
}

// Square implementation
// This can ALSO be used anywhere Shape is expected
// It doesn't break any expectations
class Square implements Shape {
  double side;
  
  Square(this.side);
  
  @override
  double getArea() {
    return side * side;
  }
  
  // Square-specific methods
  void setSide(double s) {
    side = s;
  }
}

// This function works with ANY Shape
// It doesn't care if it's Rectangle or Square
// Both can substitute for Shape without breaking anything
double calculateTotalArea(List<Shape> shapes) {
  double total = 0;
  for (var shape in shapes) {
    // We can call getArea() on any Shape
    // Whether it's Rectangle or Square, it works the same way
    // This is Liskov Substitution in action!
    total += shape.getArea();
  }
  return total;
}

// Usage:
void main() {
  // Create different shapes
  final rectangle = Rectangle(5, 4);
  final square = Square(5);
  
  // Both can be used as Shapes
  // They're substitutable - this is Liskov Substitution!
  final shapes = [rectangle, square];
  
  // This function works with both
  // It doesn't need to know if it's Rectangle or Square
  final totalArea = calculateTotalArea(shapes);
  print('Total area: $totalArea'); // Works perfectly!
}
```

**Step-by-Step Explanation:**
1. **Bad Example**: Square extends Rectangle but changes behavior
2. **Problem**: Code expecting Rectangle behavior breaks with Square
3. **Good Example**: Both Rectangle and Square implement Shape interface
4. **Shape interface** defines common behavior (getArea)
5. **Both classes** can be used anywhere Shape is expected
6. **No breaking changes** when substituting one for another

**Why This Works:**
- Subclasses can replace base classes without breaking code
- Makes code more flexible and maintainable
- Prevents unexpected behavior
- Enables polymorphism safely

### I - Interface Segregation Principle (ISP)

**Simple Explanation:**

Clients should not be forced to depend on interfaces they don't use. Think of it like a remote control - you shouldn't need a TV remote with 100 buttons if you only need power and volume.

**Simple Analogy:**

Think of Interface Segregation like a restaurant menu:
- **Bad**: One giant menu with everything (hard to find what you want)
- **Good**: Separate menus for breakfast, lunch, dinner (easy to find what you need)

**Bad Example (Violates ISP):**

```dart
// BAD: One giant interface that forces classes to implement everything
// Think of it as a remote control with 100 buttons when you only need 5

// This interface has too many methods
// Any class that implements it must implement ALL methods
// Even if they don't need all of them!
abstract class Worker {
  // Some workers need all these, but most don't!
  void work();
  void eat();
  void sleep();
  void code(); // Only programmers need this
  void design(); // Only designers need this
  void manage(); // Only managers need this
}

// Programmer is forced to implement methods they don't use
class Programmer implements Worker {
  @override
  void work() {
    print('Programming...');
  }
  
  @override
  void eat() {
    print('Eating...');
  }
  
  @override
  void sleep() {
    print('Sleeping...');
  }
  
  @override
  void code() {
    print('Writing code...'); // This makes sense
  }
  
  @override
  void design() {
    // Programmer doesn't design, but forced to implement!
    throw UnimplementedError(); // Empty implementation - bad!
  }
  
  @override
  void manage() {
    // Programmer doesn't manage, but forced to implement!
    throw UnimplementedError(); // Empty implementation - bad!
  }
}
```

**Good Example (Follows ISP):**

```dart
// GOOD: Separate interfaces for different responsibilities
// Think of it as separate remotes for different devices

// Base interface - everyone needs this
// Think of it as basic human needs
abstract class Human {
  void eat();
  void sleep();
}

// Interface for workers
// Only workers need this
abstract class Worker extends Human {
  void work();
}

// Interface for programmers
// Only programmers need this
// They don't need to implement design or management
abstract class Programmer extends Worker {
  void code();
}

// Interface for designers
// Only designers need this
abstract class Designer extends Worker {
  void design();
}

// Interface for managers
// Only managers need this
abstract class Manager extends Worker {
  void manage();
}

// Now Programmer only implements what they need
// No empty methods, no throwing errors!
class ProgrammerImpl implements Programmer {
  @override
  void eat() {
    print('Eating...');
  }
  
  @override
  void sleep() {
    print('Sleeping...');
  }
  
  @override
  void work() {
    print('Working...');
  }
  
  @override
  void code() {
    print('Writing code...'); // Only what they need!
  }
  
  // No design() or manage() methods needed!
  // This is Interface Segregation - only implement what you need
}

// Designer only implements what they need
class DesignerImpl implements Designer {
  @override
  void eat() {
    print('Eating...');
  }
  
  @override
  void sleep() {
    print('Sleeping...');
  }
  
  @override
  void work() {
    print('Working...');
  }
  
  @override
  void design() {
    print('Designing...'); // Only what they need!
  }
  
  // No code() or manage() methods needed!
}

// Usage:
void main() {
  // Programmer only needs to implement Programmer interface
  // They don't need to know about design or management
  final programmer = ProgrammerImpl();
  programmer.code(); // Works!
  
  // Designer only needs to implement Designer interface
  // They don't need to know about coding or management
  final designer = DesignerImpl();
  designer.design(); // Works!
  
  // Each class only depends on interfaces they actually use
  // This is Interface Segregation Principle!
}
```

**Step-by-Step Explanation:**
1. **Bad Example**: One giant Worker interface with all methods
2. **Problem**: Classes forced to implement methods they don't use
3. **Good Example**: Split into smaller, focused interfaces
4. **Human**: Basic needs (eat, sleep)
5. **Worker**: Work-related (extends Human)
6. **Programmer, Designer, Manager**: Specific interfaces
7. **Each class** only implements what it needs

**Why This Works:**
- Classes only depend on what they use
- No empty implementations or errors
- Easier to understand and maintain
- More flexible and modular

### D - Dependency Inversion Principle (DIP)

**Simple Explanation:**

High-level modules should not depend on low-level modules. Both should depend on abstractions. Think of it like a power outlet - your devices (high-level) depend on the outlet interface (abstraction), not the specific wiring (low-level).

**Simple Analogy:**

Think of Dependency Inversion like a universal charger:
- **Bad**: Phone depends on specific charger brand (tightly coupled)
- **Good**: Phone depends on USB-C interface (abstraction), any USB-C charger works

**Bad Example (Violates DIP):**

```dart
// BAD: High-level module depends on low-level module directly
// Think of it as your app depending on a specific database

// Low-level module - specific implementation
// This is like a specific brand of database
class MySQLDatabase {
  // MySQL specific implementation
  void save(String data) {
    print('Saving to MySQL: $data');
    // MySQL specific code
  }
  
  String? load(String id) {
    print('Loading from MySQL: $id');
    return 'data from MySQL';
  }
}

// High-level module depends directly on low-level module
// This is bad because if we want to change database, we have to change this class
class UserRepository {
  // Direct dependency on MySQLDatabase
  // This is tightly coupled - bad!
  final MySQLDatabase database; // Depends on concrete class, not abstraction!
  
  UserRepository(this.database);
  
  void saveUser(User user) {
    // If we want to use PostgreSQL instead, we have to change this class
    // This violates Dependency Inversion Principle
    database.save(user.toJson());
  }
  
  User? getUser(String id) {
    final data = database.load(id);
    return data != null ? User.fromJson(data) : null;
  }
}

// Problem: If we want to use PostgreSQL, we have to modify UserRepository
// This breaks the principle - high-level depends on low-level
```

**Good Example (Follows DIP):**

```dart
// GOOD: Both high-level and low-level depend on abstraction
// Think of it as depending on a standard interface, not specific implementation

// Abstraction - this is the interface
// Think of it as a standard that all databases must follow
abstract class Database {
  // This defines what a database must be able to do
  // It doesn't care HOW it's done, just WHAT can be done
  void save(String data);
  String? load(String id);
}

// Low-level module 1 - MySQL implementation
// This implements the abstraction
// Think of it as one brand that follows the standard
class MySQLDatabase implements Database {
  @override
  void save(String data) {
    print('Saving to MySQL: $data');
    // MySQL specific implementation
    // But it follows the Database interface
  }
  
  @override
  String? load(String id) {
    print('Loading from MySQL: $id');
    return 'data from MySQL';
  }
}

// Low-level module 2 - PostgreSQL implementation
// This also implements the abstraction
// Think of it as another brand that follows the same standard
class PostgreSQLDatabase implements Database {
  @override
  void save(String data) {
    print('Saving to PostgreSQL: $data');
    // PostgreSQL specific implementation
    // But it follows the Database interface
  }
  
  @override
  String? load(String id) {
    print('Loading from PostgreSQL: $id');
    return 'data from PostgreSQL';
  }
}

// Low-level module 3 - In-memory database for testing
// This also implements the abstraction
// Think of it as a test version that follows the standard
class InMemoryDatabase implements Database {
  final Map<String, String> _storage = {};
  
  @override
  void save(String data) {
    _storage['key'] = data;
    print('Saving to memory: $data');
  }
  
  @override
  String? load(String id) {
    return _storage[id];
  }
}

// High-level module depends on abstraction, not concrete class
// This is Dependency Inversion - depends on Database interface, not MySQLDatabase
class UserRepository {
  // Depends on abstraction (Database), not concrete class (MySQLDatabase)
  // Think of it as depending on the standard, not a specific brand
  final Database database; // Depends on interface, not implementation!
  
  UserRepository(this.database);
  
  void saveUser(User user) {
    // This code doesn't care if it's MySQL, PostgreSQL, or in-memory
    // It just uses the Database interface
    // If we want to change database, we just pass a different implementation
    // No need to change this code!
    database.save(user.toJson());
  }
  
  User? getUser(String id) {
    final data = database.load(id);
    return data != null ? User.fromJson(data) : null;
  }
}

// Usage:
void main() {
  // We can use MySQL
  final mysqlDb = MySQLDatabase();
  final userRepo1 = UserRepository(mysqlDb);
  userRepo1.saveUser(User(name: 'John'));
  
  // We can use PostgreSQL - no changes to UserRepository needed!
  final postgresDb = PostgreSQLDatabase();
  final userRepo2 = UserRepository(postgresDb);
  userRepo2.saveUser(User(name: 'Jane'));
  
  // We can use in-memory for testing - no changes to UserRepository needed!
  final memoryDb = InMemoryDatabase();
  final userRepo3 = UserRepository(memoryDb);
  userRepo3.saveUser(User(name: 'Test'));
  
  // UserRepository doesn't care which database we use
  // It depends on the abstraction (Database interface)
  // This is Dependency Inversion Principle!
}
```

**Step-by-Step Explanation:**
1. **Bad Example**: UserRepository depends directly on MySQLDatabase
2. **Problem**: To change database, must modify UserRepository
3. **Good Example**: Create Database abstraction (interface)
4. **All databases** implement Database interface
5. **UserRepository** depends on Database interface, not concrete class
6. **Can switch databases** without changing UserRepository
7. **Both high and low level** depend on abstraction

**Why This Works:**
- High-level modules don't depend on low-level details
- Easy to swap implementations
- Better testability (can use mock databases)
- More flexible and maintainable
- Follows "program to interfaces, not implementations"

### Summary of SOLID Principles

**Remember SOLID:**

1. **S - Single Responsibility**: One class, one job
2. **O - Open/Closed**: Open for extension, closed for modification
3. **L - Liskov Substitution**: Subclasses must be substitutable
4. **I - Interface Segregation**: Don't force unused methods
5. **D - Dependency Inversion**: Depend on abstractions, not concretions

**Benefits of Following SOLID:**

- **Maintainable**: Easy to change and update
- **Testable**: Easy to test individual components
- **Flexible**: Easy to extend with new features
- **Reusable**: Components can be reused
- **Understandable**: Code is easier to understand

## Multi-Module Architecture

**Module Structure:**

```
app/
  features/
    auth/
    home/
    profile/
  core/
    network/
    database/
  shared/
    widgets/
    utils/
```

## Interview Questions & Answers

### Q1: Explain Clean Architecture in Flutter.

**Answer:**

**Clean Architecture** is a software design approach that separates code into distinct layers with clear responsibilities and dependencies. In Flutter, it typically consists of three main layers: **Presentation Layer** (UI, widgets, state management) handles user interface and user interactions, **Domain Layer** (business logic, entities, use cases) contains the core business rules and is independent of frameworks, and **Data Layer** (repositories, data sources, API services) handles data retrieval and storage. The key principle is dependency inversion - outer layers depend on inner layers, but inner layers (Domain) don't depend on outer layers. This separation makes code testable, maintainable, and allows you to change frameworks or data sources without affecting business logic. Clean Architecture promotes separation of concerns, making it easier to understand, test, and modify different parts of your application independently.

### Q2: What is MVVM pattern in Flutter?

**Answer:**

**MVVM (Model-View-ViewModel)** is an architectural pattern that separates concerns into three components: **Model** represents the data and business logic, **View** is the UI layer (Flutter widgets) that displays data and handles user input, and **ViewModel** acts as a bridge between View and Model, exposing data and commands to the View while handling presentation logic. The ViewModel is independent of the View, making it testable without UI dependencies. In Flutter, ViewModels are typically implemented using ChangeNotifier (with Provider), StateNotifier (with Riverpod), or similar state management solutions. The View observes the ViewModel and updates automatically when data changes. MVVM promotes separation of concerns, testability, and maintainability by keeping business logic separate from UI code, making it easier to modify the UI without affecting business logic or vice versa.

### Q3: Explain Repository pattern.

**Answer:**

**Repository pattern** is a design pattern that abstracts data sources (like APIs, databases, or local storage) and provides a clean, consistent API for data access to the rest of your application. Instead of having your business logic directly call API services or database methods, you create a Repository interface that defines data operations (like `getUser()`, `saveUser()`), and then implement this interface with concrete classes that handle the actual data retrieval and storage. This abstraction allows you to switch data sources (e.g., from API to local database) without changing the code that uses the repository. Repositories can implement strategies like "cache-first" (check local storage first, then API) or "network-first" (try API first, fall back to cache). The Repository pattern promotes testability (you can easily mock repositories), maintainability (data access logic is centralized), and flexibility (easy to change data sources or add caching layers).

### Q4: How do you implement SOLID principles in Flutter?

**Answer:**

To implement SOLID principles in Flutter, apply them through proper class design, interfaces, and dependency injection. **Single Responsibility Principle (SRP)**: Create classes with one clear purpose - separate UI widgets from business logic, data models from data access, etc. **Open/Closed Principle (OCP)**: Use abstract classes and interfaces so you can extend functionality without modifying existing code - create base widget classes or use composition. **Liskov Substitution Principle (LSP)**: Ensure subclasses can replace base classes without breaking functionality - when extending widgets or classes, maintain the same contract. **Interface Segregation Principle (ISP)**: Create focused interfaces rather than large ones - split large interfaces into smaller, specific ones that classes only implement what they need. **Dependency Inversion Principle (DIP)**: Depend on abstractions (interfaces) rather than concrete implementations - use dependency injection to provide implementations, making code testable and flexible. These principles help create maintainable, testable, and scalable Flutter applications.

### Q5: Explain multi-module architecture.

**Answer:**

**Multi-module architecture** organizes code into separate, independent modules (packages) where each module represents a feature or domain area of your application. Each module contains its own presentation layer, domain logic, and data layer, making it self-contained and independently developable. This approach improves maintainability by isolating features, making it easier to understand and modify specific parts of the app without affecting others. Modules can be developed by different team members in parallel, and they can be tested independently. Multi-module architecture also enables better code reuse, as modules can be shared across projects or used as libraries. In Flutter, you can create modules as separate packages using the `flutter create --template=package` command. This architecture is particularly beneficial for large applications with multiple features, as it prevents the codebase from becoming a monolithic structure that's difficult to navigate and maintain.

### Q6: How do you structure a large Flutter project?

**Answer:**

To structure a large Flutter project, use a **feature-based structure** where code is organized by features rather than by technical layers. Each feature module contains its own presentation (screens, widgets), domain (business logic, models), and data (repositories, data sources) layers. This makes it easy to locate code related to a specific feature and allows features to be developed independently. Common structure includes: `lib/features/` for feature modules, `lib/core/` for shared utilities and base classes, `lib/shared/` for reusable widgets and components, and `lib/config/` for app configuration. Within each feature, organize by layers (presentation, domain, data) or by component type (screens, widgets, models, services). Use dependency injection to wire features together, and keep features loosely coupled so they can be modified independently. This structure scales well as your project grows and makes onboarding new team members easier.

### Q7: What are the best practices for Flutter architecture?

**Answer:**

**Best Practices for Flutter Architecture:**
- **Separate concerns** by dividing your code into distinct layers (presentation, domain, data) with clear responsibilities, making each part easier to understand and modify.
- **Use dependency injection** to provide dependencies rather than creating them internally, promoting testability, flexibility, and loose coupling between components.
- **Follow SOLID principles** to create maintainable, extensible code that's easy to test and modify without breaking existing functionality.
- **Organize by features** rather than by technical layers, grouping related code together so features can be developed and maintained independently.
- **Keep layers independent** by ensuring that inner layers (like domain) don't depend on outer layers (like presentation or data), using dependency inversion to achieve this.
- **Write testable code** by designing classes and functions that can be easily tested in isolation, using interfaces and dependency injection to enable mocking.
- **Use consistent naming conventions** and project structure across the codebase to make it easier for team members to navigate and understand the code.
- **Document architecture decisions** to help team members understand why certain patterns or structures were chosen, making it easier to maintain consistency.

### Q8: How do you handle error handling in architecture?

**Answer:**

To handle errors effectively in architecture, use **Result types** (like `Result<T, E>`) that explicitly represent success or failure states, making error handling part of the type system and forcing developers to handle errors. Use **custom exceptions** for different error types (network errors, validation errors, business logic errors) that can be caught and handled appropriately at different layers. Implement **error states** in your state management (like ErrorState in BLoC or error fields in ViewModels) to represent error conditions in the UI layer. Handle errors at the appropriate layer - data layer errors (network failures, parsing errors) should be caught and converted to domain errors, domain layer should handle business logic errors, and presentation layer should display user-friendly error messages. Use **try-catch blocks** for expected errors and provide fallback behavior. Always log errors for debugging while showing user-friendly messages. This layered approach to error handling ensures errors are caught, handled appropriately, and users receive meaningful feedback without exposing technical details.

---

## Navigation

**Previous:** [Publishing](publishing.md)

**Next:** [Advanced Topics](advanced-topics.md)

