# Provider - Popular State Management Solution

## Table of Contents
- [What is Provider?](#what-is-provider)
- [Why Use Provider?](#why-use-provider)
- [How Does Provider Work?](#how-does-provider-work)
- [Basic Example](#basic-example)
- [Intermediate Example](#intermediate-example)
- [Advanced Example](#advanced-example)
- [Best Practices](#best-practices)
- [Common Mistakes](#common-mistakes)
- [When to Use vs When Not to Use](#when-to-use-vs-when-not-to-use)
- [Comparison with Other Approaches](#comparison-with-other-approaches)
- [Interview Questions & Answers](#interview-questions--answers)

## What is Provider?

**Simple Explanation:**

Provider is like a shared box that multiple widgets can access. When something changes in the box, all widgets watching it are automatically updated.

**Simple Analogy:**

Think of Provider like a shared bulletin board:
- **Provider** = The bulletin board
- **State** = The messages on the board
- **Widgets** = People watching the board
- When a new message is posted (state changes), everyone watching sees it immediately

**Key Concepts:**

- **ChangeNotifier**: Class that holds state and notifies listeners
- **Provider**: Widget that provides state to child widgets
- **Consumer**: Widget that listens to state changes
- **notifyListeners()**: Method that tells all listeners "state changed!"

## Why Use Provider?

**Benefits:**

1. **Simple**: Easy to understand and use
2. **Popular**: Widely used in Flutter community
3. **Efficient**: Only rebuilds widgets that need updating
4. **Flexible**: Works for simple to medium complexity apps
5. **Well Documented**: Lots of resources and examples

**When It's Perfect:**

- Medium-sized apps
- Need to share state across widgets
- Want simple state management
- Team familiar with Provider pattern

## How Does Provider Work?

**The Mechanism:**

1. Create a ChangeNotifier class to hold state
2. Wrap your app/widget tree with Provider
3. Widgets access state using `Provider.of()` or `Consumer`
4. When state changes, call `notifyListeners()`
5. All listening widgets rebuild automatically

**Simple Flow:**

```
ChangeNotifier → Provider → Widgets Access → State Changes → notifyListeners() → Widgets Rebuild
```

## Basic Example

**Simple Counter with Provider:**

```dart
// Step 1: Create a ChangeNotifier class
// This is like creating a box that can hold state and notify others when it changes
// Think of it as a smart container that can ring a bell when contents change
class CounterProvider extends ChangeNotifier {
  // This is our state - the data we want to share
  // Think of it as the contents of our box
  int _count = 0;
  
  // Getter to read the count
  // Think of it as a window to look at the count
  // The get keyword makes this a read-only property
  int get count => _count;
  
  // Method to update the count
  // Think of it as changing what's in the box
  void increment() {
    _count = _count + 1; // Increase count by 1
    // notifyListeners() is like ringing a bell
    // It tells all widgets watching this provider: "Hey, something changed!"
    // Without this, widgets wouldn't know to update
    notifyListeners();
  }
  
  // Method to decrease the count
  void decrement() {
    _count = _count - 1; // Decrease count by 1
    notifyListeners(); // Tell everyone who's watching
  }
  
  // Method to reset the count
  void reset() {
    _count = 0; // Set count back to zero
    notifyListeners(); // Notify all listeners
  }
}

// Step 2: Provide the provider to your app
// This is like putting the box in a place where everyone can access it
void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      // ChangeNotifierProvider creates and provides the CounterProvider
      // Think of it as creating the box and making it available
      create: (context) => CounterProvider(),
      child: MaterialApp(
        title: 'Provider Counter',
        home: CounterScreen(),
      ),
    );
  }
}

// Step 3: Use the provider in widgets
// This is like accessing the box to read or change its contents
class CounterScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Method 1: Using Provider.of()
    // This gets the CounterProvider from the widget tree
    // Think of it as reaching into the box
    final counterProvider = Provider.of<CounterProvider>(context);
    
    return Scaffold(
      appBar: AppBar(title: Text('Provider Counter')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Display the count
            // The count comes from the provider
            Text(
              'Count: ${counterProvider.count}',
              style: TextStyle(fontSize: 48),
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Decrement button
                ElevatedButton(
                  onPressed: () {
                    // Call decrement on the provider
                    // This will update state and notify listeners
                    counterProvider.decrement();
                  },
                  child: Text('-'),
                ),
                SizedBox(width: 20),
                // Increment button
                ElevatedButton(
                  onPressed: () {
                    // Call increment on the provider
                    counterProvider.increment();
                  },
                  child: Text('+'),
                ),
              ],
            ),
            SizedBox(height: 20),
            // Reset button
            ElevatedButton(
              onPressed: () {
                counterProvider.reset();
              },
              child: Text('Reset'),
            ),
          ],
        ),
      ),
    );
  }
}
```

**Step-by-Step Explanation:**
1. We create a `CounterProvider` class that extends `ChangeNotifier`
2. It holds the state (`_count`) and provides methods to change it
3. We wrap the app with `ChangeNotifierProvider` to make it available
4. Widgets use `Provider.of()` to access the provider
5. When state changes, `notifyListeners()` tells all widgets to update
6. Widgets automatically rebuild with new state

**Why This Works:**
- Provider makes state available to all widgets in the tree
- `notifyListeners()` triggers rebuilds only for listening widgets
- No need to pass data through multiple widget layers

## Intermediate Example

**User Authentication with Provider:**

```dart
// User model
// Think of it as a blueprint for user data
class User {
  final String id;
  final String name;
  final String email;
  
  User({
    required this.id,
    required this.name,
    required this.email,
  });
}

// Authentication provider
// This manages user authentication state
// Think of it as a security guard that knows who's logged in
class AuthProvider extends ChangeNotifier {
  // Current user - null if not logged in
  // Think of it as the ID card of the logged-in user
  User? _user;
  
  // Getter to check if user is logged in
  bool get isAuthenticated => _user != null;
  
  // Getter to get current user
  User? get user => _user;
  
  // Method to log in
  // Think of it as checking the user's credentials and letting them in
  Future<void> login(String email, String password) async {
    try {
      // Simulate API call
      // In real app, this would call your authentication API
      await Future.delayed(Duration(seconds: 1));
      
      // For demo, accept any email/password
      // In real app, verify credentials with server
      _user = User(
        id: '1',
        name: 'John Doe',
        email: email,
      );
      
      // Notify all listeners that login state changed
      notifyListeners();
    } catch (e) {
      // Handle error
      throw Exception('Login failed: $e');
    }
  }
  
  // Method to log out
  // Think of it as removing the user's access
  void logout() {
    _user = null; // Clear the user
    notifyListeners(); // Notify all listeners
  }
  
  // Method to update user profile
  void updateUser(User updatedUser) {
    _user = updatedUser; // Update user data
    notifyListeners(); // Notify listeners
  }
}

// App setup with provider
void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => AuthProvider(),
      child: MaterialApp(
        title: 'Auth App',
        home: AuthWrapper(), // Wrapper to check auth state
      ),
    );
  }
}

// Wrapper widget that checks authentication
// Think of it as a gatekeeper that decides which screen to show
class AuthWrapper extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Watch the auth provider
    // Consumer rebuilds when auth state changes
    return Consumer<AuthProvider>(
      builder: (context, authProvider, child) {
        // If user is logged in, show home screen
        if (authProvider.isAuthenticated) {
          return HomeScreen();
        }
        // Otherwise, show login screen
        return LoginScreen();
      },
    );
  }
}

// Login screen
class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;
  
  Future<void> _handleLogin() async {
    setState(() {
      _isLoading = true;
    });
    
    try {
      // Get the auth provider and call login
      final authProvider = Provider.of<AuthProvider>(context, listen: false);
      await authProvider.login(
        _emailController.text,
        _passwordController.text,
      );
      // If login succeeds, AuthWrapper will automatically show HomeScreen
    } catch (e) {
      // Show error
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Login failed: $e')),
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Login')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _emailController,
              decoration: InputDecoration(labelText: 'Email'),
            ),
            SizedBox(height: 16),
            TextField(
              controller: _passwordController,
              obscureText: true,
              decoration: InputDecoration(labelText: 'Password'),
            ),
            SizedBox(height: 24),
            _isLoading
                ? CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: _handleLogin,
                    child: Text('Login'),
                  ),
          ],
        ),
      ),
    );
  }
}

// Home screen (shown after login)
class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Get the auth provider
    final authProvider = Provider.of<AuthProvider>(context);
    final user = authProvider.user!; // We know user is not null here
    
    return Scaffold(
      appBar: AppBar(
        title: Text('Home'),
        actions: [
          // Logout button
          IconButton(
            icon: Icon(Icons.logout),
            onPressed: () {
              authProvider.logout();
              // AuthWrapper will automatically show LoginScreen
            },
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Welcome, ${user.name}!'),
            SizedBox(height: 8),
            Text('Email: ${user.email}'),
          ],
        ),
      ),
    );
  }
}
```

**Step-by-Step Explanation:**
1. We create an `AuthProvider` that manages user authentication state
2. It has methods to login, logout, and update user
3. We use `Consumer` to watch auth state and show appropriate screen
4. When login succeeds, `notifyListeners()` triggers `AuthWrapper` to rebuild
5. `AuthWrapper` sees user is authenticated and shows `HomeScreen`

**Why This Works:**
- Provider manages app-wide authentication state
- `Consumer` automatically rebuilds when state changes
- No need to manually navigate - UI updates based on state

## Advanced Example

**Shopping Cart with Provider:**

```dart
// Product model
class Product {
  final String id;
  final String name;
  final double price;
  final String imageUrl;
  
  Product({
    required this.id,
    required this.name,
    required this.price,
    required this.imageUrl,
  });
}

// Cart item model
class CartItem {
  final Product product;
  int quantity;
  
  CartItem({
    required this.product,
    this.quantity = 1,
  });
  
  double get total => product.price * quantity;
}

// Shopping cart provider
// This manages the shopping cart state
// Think of it as a shopping basket that remembers what you added
class CartProvider extends ChangeNotifier {
  // List of items in cart
  // Think of it as the items in your shopping basket
  List<CartItem> _items = [];
  
  // Getter to get all items
  List<CartItem> get items => _items;
  
  // Getter to get total number of items
  // Think of it as counting all items (including quantities)
  int get itemCount {
    return _items.fold(0, (sum, item) => sum + item.quantity);
  }
  
  // Getter to get total price
  // Think of it as calculating the total cost of all items
  double get totalPrice {
    return _items.fold(0.0, (sum, item) => sum + item.total);
  }
  
  // Method to add product to cart
  // Think of it as putting an item in your shopping basket
  void addProduct(Product product) {
    // Check if product already in cart
    final existingIndex = _items.indexWhere(
      (item) => item.product.id == product.id,
    );
    
    if (existingIndex >= 0) {
      // If already in cart, increase quantity
      _items[existingIndex].quantity++;
    } else {
      // If not in cart, add new item
      _items.add(CartItem(product: product));
    }
    
    notifyListeners(); // Tell all widgets that cart changed
  }
  
  // Method to remove product from cart
  void removeProduct(String productId) {
    _items.removeWhere((item) => item.product.id == productId);
    notifyListeners();
  }
  
  // Method to update quantity
  void updateQuantity(String productId, int quantity) {
    if (quantity <= 0) {
      // If quantity is 0 or less, remove item
      removeProduct(productId);
      return;
    }
    
    final item = _items.firstWhere(
      (item) => item.product.id == productId,
    );
    item.quantity = quantity;
    notifyListeners();
  }
  
  // Method to clear cart
  void clearCart() {
    _items.clear();
    notifyListeners();
  }
}

// App setup
void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => CartProvider(),
      child: MaterialApp(
        title: 'Shopping App',
        home: ProductListScreen(),
      ),
    );
  }
}

// Product list screen
class ProductListScreen extends StatelessWidget {
  final List<Product> products = [
    Product(id: '1', name: 'Laptop', price: 999.99, imageUrl: ''),
    Product(id: '2', name: 'Phone', price: 699.99, imageUrl: ''),
    Product(id: '3', name: 'Tablet', price: 499.99, imageUrl: ''),
  ];
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Products'),
        actions: [
          // Cart icon with item count
          Consumer<CartProvider>(
            builder: (context, cartProvider, child) {
              return Stack(
                children: [
                  IconButton(
                    icon: Icon(Icons.shopping_cart),
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => CartScreen()),
                      );
                    },
                  ),
                  // Badge showing item count
                  if (cartProvider.itemCount > 0)
                    Positioned(
                      right: 8,
                      top: 8,
                      child: Container(
                        padding: EdgeInsets.all(4),
                        decoration: BoxDecoration(
                          color: Colors.red,
                          shape: BoxShape.circle,
                        ),
                        child: Text(
                          '${cartProvider.itemCount}',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 12,
                          ),
                        ),
                      ),
                    ),
                ],
              );
            },
          ),
        ],
      ),
      body: ListView.builder(
        itemCount: products.length,
        itemBuilder: (context, index) {
          final product = products[index];
          return ListTile(
            title: Text(product.name),
            subtitle: Text('\$${product.price}'),
            trailing: ElevatedButton(
              onPressed: () {
                // Add product to cart
                Provider.of<CartProvider>(context, listen: false)
                    .addProduct(product);
              },
              child: Text('Add to Cart'),
            ),
          );
        },
      ),
    );
  }
}

// Cart screen
class CartScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Shopping Cart')),
      body: Consumer<CartProvider>(
        builder: (context, cartProvider, child) {
          if (cartProvider.items.isEmpty) {
            return Center(child: Text('Cart is empty'));
          }
          
          return Column(
            children: [
              // List of cart items
              Expanded(
                child: ListView.builder(
                  itemCount: cartProvider.items.length,
                  itemBuilder: (context, index) {
                    final item = cartProvider.items[index];
                    return ListTile(
                      title: Text(item.product.name),
                      subtitle: Text('\$${item.product.price} x ${item.quantity}'),
                      trailing: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          // Decrease quantity
                          IconButton(
                            icon: Icon(Icons.remove),
                            onPressed: () {
                              cartProvider.updateQuantity(
                                item.product.id,
                                item.quantity - 1,
                              );
                            },
                          ),
                          Text('${item.quantity}'),
                          // Increase quantity
                          IconButton(
                            icon: Icon(Icons.add),
                            onPressed: () {
                              cartProvider.updateQuantity(
                                item.product.id,
                                item.quantity + 1,
                              );
                            },
                          ),
                          // Remove item
                          IconButton(
                            icon: Icon(Icons.delete),
                            onPressed: () {
                              cartProvider.removeProduct(item.product.id);
                            },
                          ),
                        ],
                      ),
                    );
                  },
                ),
              ),
              // Total and checkout
              Container(
                padding: EdgeInsets.all(16),
                child: Column(
                  children: [
                    Text(
                      'Total: \$${cartProvider.totalPrice.toStringAsFixed(2)}',
                      style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                    ),
                    SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: () {
                        // Checkout logic
                        cartProvider.clearCart();
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text('Order placed!')),
                        );
                      },
                      child: Text('Checkout'),
                    ),
                  ],
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}
```

**Step-by-Step Explanation:**
1. We create a `CartProvider` that manages shopping cart state
2. It tracks items, quantities, and calculates totals
3. Multiple screens access the same cart provider
4. When items are added/removed, `notifyListeners()` updates all widgets
5. `Consumer` widgets automatically rebuild when cart changes

**Why This Works:**
- Single source of truth for cart state
- All screens see the same cart
- Automatic updates when cart changes
- Easy to maintain and test

## Best Practices

1. **Use Private Variables for State**
```dart
// GOOD:
int _count = 0; // Private

// BAD:
int count = 0; // Public
```

2. **Call notifyListeners() After State Changes**
```dart
void increment() {
  _count++;
  notifyListeners(); // Always call this!
}
```

3. **Use Consumer for Selective Rebuilds**
```dart
// GOOD - only rebuilds this widget:
Consumer<CounterProvider>(
  builder: (context, provider, child) => Text('${provider.count}'),
)

// BAD - rebuilds entire widget tree:
Provider.of<CounterProvider>(context).count
```

4. **Use listen: false When You Don't Need Rebuilds**
```dart
// When you only need to call a method, not listen:
Provider.of<CounterProvider>(context, listen: false).increment();
```

5. **Dispose Resources Properly**
```dart
@override
void dispose() {
  _controller.dispose();
  super.dispose();
}
```

## Common Mistakes

1. **Forgetting notifyListeners()**
```dart
// BAD - UI won't update:
void increment() {
  _count++;
  // Missing notifyListeners()!
}

// GOOD:
void increment() {
  _count++;
  notifyListeners();
}
```

2. **Using Provider.of() When You Don't Need Rebuilds**
```dart
// BAD - causes unnecessary rebuilds:
void onButtonPressed() {
  Provider.of<CounterProvider>(context).increment();
  // This rebuilds the entire widget!
}

// GOOD - use listen: false:
void onButtonPressed() {
  Provider.of<CounterProvider>(context, listen: false).increment();
  // No rebuild!
}
```

3. **Not Using Consumer for Selective Rebuilds**
```dart
// BAD - rebuilds everything:
Widget build(BuildContext context) {
  final count = Provider.of<CounterProvider>(context).count;
  return Scaffold(/* entire widget tree */);
}

// GOOD - only rebuilds what needs to:
Widget build(BuildContext context) {
  return Scaffold(
    body: Consumer<CounterProvider>(
      builder: (context, provider, child) => Text('${provider.count}'),
    ),
  );
}
```

## When to Use vs When Not to Use

**Use Provider when:**
- Medium-sized apps
- Need to share state across widgets
- Want simple state management
- Team familiar with Provider
- Don't need compile-time safety

**Don't use Provider when:**
- Need compile-time safety (use Riverpod)
- Very complex state management (use BLoC)
- Want all-in-one solution (use GetX)
- Need advanced features (time-travel, etc.)

## Comparison with Other Approaches

**Provider vs setState():**
- Provider: Shared state across widgets
- setState(): Local state only

**Provider vs Riverpod:**
- Provider: Runtime-based, simpler
- Riverpod: Compile-time safe, more modern

**Provider vs BLoC:**
- Provider: Simpler, less boilerplate
- BLoC: More structured, better for complex logic

## Interview Questions & Answers

### Q1: What is Provider and how does it work?

**Answer:**

Provider is a state management solution that uses ChangeNotifier to share state across widgets. Think of it like a shared bulletin board that widgets can read and update.

```dart
class CounterProvider extends ChangeNotifier {
  int _count = 0;
  int get count => _count;
  
  void increment() {
    _count++;
    notifyListeners(); // Tells all listeners to update
  }
}

// Usage:
ChangeNotifierProvider(
  create: (_) => CounterProvider(),
  child: MyApp(),
)

// In widget:
Provider.of<CounterProvider>(context).count
```

**How it works:**
1. Create ChangeNotifier class
2. Wrap app with Provider
3. Widgets access state via Provider.of()
4. Call notifyListeners() when state changes
5. Listening widgets rebuild automatically

### Q2: What is the difference between Provider.of() and Consumer?

**Answer:**

**Provider.of()**: Gets provider, can cause full widget rebuild
**Consumer**: Only rebuilds the builder function

```dart
// Provider.of() - can rebuild entire widget:
Widget build(BuildContext context) {
  final count = Provider.of<CounterProvider>(context).count;
  return Scaffold(/* rebuilds everything */);
}

// Consumer - only rebuilds builder:
Widget build(BuildContext context) {
  return Scaffold(
    body: Consumer<CounterProvider>(
      builder: (context, provider, child) => Text('${provider.count}'),
      // Only this Text rebuilds, not Scaffold
    ),
  );
}
```

### Q3: When should you use listen: false?

**Answer:**

**Use `listen: false`** when you only need to call methods, not listen to changes.

```dart
// When you need to call a method but don't need to rebuild:
ElevatedButton(
  onPressed: () {
    Provider.of<CounterProvider>(context, listen: false).increment();
    // listen: false prevents unnecessary rebuild
  },
  child: Text('Increment'),
)
```

### Q4: Explain ChangeNotifier in Provider.

**Answer:**

**ChangeNotifier** is a class that can notify listeners when state changes. It's the foundation of Provider.

```dart
class CounterProvider extends ChangeNotifier {
  int _count = 0;
  
  void increment() {
    _count++;
    notifyListeners(); // Notifies all listeners
  }
}
```

**Key points:**
- Extends ChangeNotifier
- Holds state
- Calls notifyListeners() when state changes
- Widgets listen via Provider

### Q5: How do you handle multiple providers?

**Answer:**

**Use MultiProvider** to provide multiple providers.

```dart
MultiProvider(
  providers: [
    ChangeNotifierProvider(create: (_) => CounterProvider()),
    ChangeNotifierProvider(create: (_) => AuthProvider()),
    ChangeNotifierProvider(create: (_) => CartProvider()),
  ],
  child: MyApp(),
)
```

### Q6: What is the difference between Provider and ChangeNotifierProvider?

**Answer:**

**Provider**: Generic provider for any value
**ChangeNotifierProvider**: Specific provider for ChangeNotifier

```dart
// Provider - for any value:
Provider<String>(
  create: (_) => 'Hello',
  child: MyApp(),
)

// ChangeNotifierProvider - for ChangeNotifier:
ChangeNotifierProvider<CounterProvider>(
  create: (_) => CounterProvider(),
  child: MyApp(),
)
```

### Q7: How do you test Provider?

**Answer:**

**Create provider in tests** and verify state changes.

```dart
test('increment increases count', () {
  final provider = CounterProvider();
  expect(provider.count, 0);
  
  provider.increment();
  expect(provider.count, 1);
});
```

### Q8: Explain Selector in Provider.

**Answer:**

**Selector** rebuilds only when specific part of state changes.

```dart
Selector<CounterProvider, int>(
  selector: (_, provider) => provider.count,
  builder: (context, count, child) => Text('$count'),
  // Only rebuilds when count changes, not other state
)
```

### Q9: What are the limitations of Provider?

**Answer:**

**Limitations:**
- Runtime-based (not compile-time safe)
- Can have issues with widget tree
- No built-in dependency injection
- Can be verbose for complex state

### Q10: How do you handle async operations in Provider?

**Answer:**

**Use async/await** and call notifyListeners() after state updates.

```dart
Future<void> loadData() async {
  _isLoading = true;
  notifyListeners();
  
  try {
    _data = await api.getData();
  } catch (e) {
    _error = e.toString();
  } finally {
    _isLoading = false;
    notifyListeners();
  }
}
```

---

## Navigation

**Previous:** [setState()](state-management-setstate.md)

**Next:** [Riverpod](state-management-riverpod.md)

