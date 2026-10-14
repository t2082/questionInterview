# Riverpod - Modern Provider Alternative

## Table of Contents
- [What is Riverpod?](#what-is-riverpod)
- [Why Use Riverpod?](#why-use-riverpod)
- [How Does Riverpod Work?](#how-does-riverpod-work)
- [Basic Example](#basic-example)
- [Intermediate Example](#intermediate-example)
- [Advanced Example](#advanced-example)
- [Best Practices](#best-practices)
- [Common Mistakes](#common-mistakes)
- [When to Use vs When Not to Use](#when-to-use-vs-when-not-to-use)
- [Comparison with Other Approaches](#comparison-with-other-approaches)
- [Interview Questions & Answers](#interview-questions--answers)

## What is Riverpod?

**Simple Explanation:**

Riverpod is like Provider 2.0 - it's Provider but with a safety net. It provides compile-time safety, meaning errors are caught before your app runs, not after.

**Simple Analogy:**

Think of Riverpod like a smart security system:
- **Provider** = A regular lock (works, but can have issues)
- **Riverpod** = A smart lock with alarms (safer, catches problems early)

**Key Concepts:**

- **Provider**: A value that can be accessed anywhere
- **StateProvider**: Simple state management
- **StateNotifierProvider**: Complex state management
- **ref**: Reference to access providers
- **watch**: Listen to provider changes
- **read**: Read provider without listening

## Why Use Riverpod?

**Benefits:**

1. **Compile-time Safety**: Errors caught before runtime
2. **No BuildContext Needed**: Access providers anywhere
3. **Better Testing**: Easier to test providers
4. **No Dependency on Widget Tree**: More flexible
5. **Modern**: Built for modern Flutter development

**When It's Perfect:**

- New projects
- Want compile-time safety
- Need better testing
- Want to avoid Provider's limitations

## How Does Riverpod Work?

**The Mechanism:**

1. Create providers (StateProvider, StateNotifierProvider, etc.)
2. Wrap app with ProviderScope
3. Access providers using `ref.watch()` or `ref.read()`
4. Providers automatically update when state changes

**Simple Flow:**

```
Provider → ProviderScope → Widgets Access via ref → State Changes → Auto Rebuild
```

## Basic Example

**Simple Counter with Riverpod:**

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Step 1: Create a StateProvider
// This is like a simple box that holds a value
// Think of it as a container that can change its contents
final counterProvider = StateProvider<int>((ref) {
  // This is the initial value
  // Think of it as what's in the box when you first open it
  return 0;
});

// Step 2: Wrap your app with ProviderScope
// This is like creating a room where all providers live
// Think of it as a container that holds all your state
void main() {
  runApp(
    ProviderScope(
      // ProviderScope makes all providers available to the app
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Riverpod Counter',
      home: CounterScreen(),
    );
  }
}

// Step 3: Use ConsumerWidget to access providers
// ConsumerWidget is like a widget that can look into the provider room
// Think of it as a widget that has a key to access providers
class CounterScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // ref is like a key that gives you access to all providers
    // Think of it as a remote control for your providers
    
    // watch() listens to the provider and rebuilds when it changes
    // Think of it as watching a TV channel - you see updates automatically
    final count = ref.watch(counterProvider);
    
    return Scaffold(
      appBar: AppBar(title: Text('Riverpod Counter')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Display the count
            // This automatically updates when count changes
            Text(
              'Count: $count',
              style: TextStyle(fontSize: 48),
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Decrement button
                ElevatedButton(
                  onPressed: () {
                    // read() gets the provider without listening
                    // Think of it as checking the value once without watching
                    // We use read() here because we don't need to rebuild
                    ref.read(counterProvider.notifier).state--;
                  },
                  child: Text('-'),
                ),
                SizedBox(width: 20),
                // Increment button
                ElevatedButton(
                  onPressed: () {
                    // Update the state
                    // .notifier gives us access to change the state
                    // .state is the actual value we can modify
                    ref.read(counterProvider.notifier).state++;
                  },
                  child: Text('+'),
                ),
              ],
            ),
            SizedBox(height: 20),
            // Reset button
            ElevatedButton(
              onPressed: () {
                // Reset to 0
                ref.read(counterProvider.notifier).state = 0;
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
1. We create a `StateProvider` that holds an integer (the count)
2. We wrap the app with `ProviderScope` to make providers available
3. We use `ConsumerWidget` to access providers via `ref`
4. `ref.watch()` listens to changes and rebuilds automatically
5. `ref.read()` accesses the provider without listening (for actions)

**Why This Works:**
- Riverpod provides compile-time safety
- No need for BuildContext to access providers
- Automatic rebuilds when state changes
- Cleaner code than Provider

## Intermediate Example

**User Authentication with Riverpod:**

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

// User model
class User {
  final String id;
  final String name;
  final String email;
  
  User({required this.id, required this.name, required this.email});
}

// Auth state class
// This represents the different states of authentication
// Think of it as a box that can be empty (not logged in) or full (logged in)
@freezed
class AuthState {
  const factory AuthState.initial() = _Initial;
  const factory AuthState.loading() = _Loading;
  const factory AuthState.authenticated(User user) = _Authenticated;
  const factory AuthState.unauthenticated() = _Unauthenticated;
  const factory AuthState.error(String message) = _Error;
}

// Auth notifier
// This manages authentication state
// Think of it as a security guard that handles login/logout
class AuthNotifier extends StateNotifier<AuthState> {
  AuthNotifier() : super(const AuthState.initial());
  
  // Login method
  // Think of it as checking credentials and letting user in
  Future<void> login(String email, String password) async {
    state = const AuthState.loading(); // Show loading
    
    try {
      // Simulate API call
      await Future.delayed(Duration(seconds: 1));
      
      // For demo, accept any credentials
      final user = User(
        id: '1',
        name: 'John Doe',
        email: email,
      );
      
      state = AuthState.authenticated(user); // Set authenticated state
    } catch (e) {
      state = AuthState.error('Login failed: $e'); // Set error state
    }
  }
  
  // Logout method
  void logout() {
    state = const AuthState.unauthenticated(); // Set unauthenticated state
  }
}

// Auth provider
// This provides the AuthNotifier to the app
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier();
});

// App setup
void main() {
  runApp(
    ProviderScope(
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Auth App',
      home: AuthWrapper(),
    );
  }
}

// Auth wrapper that checks authentication state
class AuthWrapper extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Watch the auth state
    // This automatically rebuilds when auth state changes
    final authState = ref.watch(authProvider);
    
    // Handle different states
    return authState.when(
      initial: () => LoginScreen(),
      loading: () => Scaffold(
        body: Center(child: CircularProgressIndicator()),
      ),
      authenticated: (user) => HomeScreen(user: user),
      unauthenticated: () => LoginScreen(),
      error: (message) => LoginScreen(error: message),
    );
  }
}

// Login screen
class LoginScreen extends ConsumerStatefulWidget {
  final String? error;
  LoginScreen({this.error});
  
  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  
  Future<void> _handleLogin() async {
    // Get auth notifier and call login
    await ref.read(authProvider.notifier).login(
      _emailController.text,
      _passwordController.text,
    );
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
            if (widget.error != null)
              Text(
                widget.error!,
                style: TextStyle(color: Colors.red),
              ),
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
            ElevatedButton(
              onPressed: _handleLogin,
              child: Text('Login'),
            ),
          ],
        ),
      ),
    );
  }
}

// Home screen
class HomeScreen extends ConsumerWidget {
  final User user;
  HomeScreen({required this.user});
  
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Home'),
        actions: [
          IconButton(
            icon: Icon(Icons.logout),
            onPressed: () {
              ref.read(authProvider.notifier).logout();
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
1. We create an `AuthNotifier` that extends `StateNotifier`
2. It manages different auth states (initial, loading, authenticated, etc.)
3. We create a provider that provides the notifier
4. `AuthWrapper` watches the auth state and shows appropriate screen
5. When login succeeds, state changes and UI updates automatically

**Why This Works:**
- StateNotifier provides structured state management
- Freezed classes provide type-safe state
- Automatic UI updates when state changes
- No BuildContext needed to access providers

## Advanced Example

**Shopping Cart with Riverpod:**

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Product model
class Product {
  final String id;
  final String name;
  final double price;
  
  Product({required this.id, required this.name, required this.price});
}

// Cart item model
class CartItem {
  final Product product;
  int quantity;
  
  CartItem({required this.product, this.quantity = 1});
  
  double get total => product.price * quantity;
}

// Cart state
class CartState {
  final List<CartItem> items;
  
  CartState(this.items);
  
  int get itemCount => items.fold(0, (sum, item) => sum + item.quantity);
  double get totalPrice => items.fold(0.0, (sum, item) => sum + item.total);
  
  CartState copyWith({List<CartItem>? items}) {
    return CartState(items ?? this.items);
  }
}

// Cart notifier
class CartNotifier extends StateNotifier<CartState> {
  CartNotifier() : super(CartState([]));
  
  void addProduct(Product product) {
    final items = List<CartItem>.from(state.items);
    final existingIndex = items.indexWhere(
      (item) => item.product.id == product.id,
    );
    
    if (existingIndex >= 0) {
      items[existingIndex].quantity++;
    } else {
      items.add(CartItem(product: product));
    }
    
    state = CartState(items);
  }
  
  void removeProduct(String productId) {
    final items = state.items.where((item) => item.product.id != productId).toList();
    state = CartState(items);
  }
  
  void updateQuantity(String productId, int quantity) {
    if (quantity <= 0) {
      removeProduct(productId);
      return;
    }
    
    final items = List<CartItem>.from(state.items);
    final item = items.firstWhere((item) => item.product.id == productId);
    item.quantity = quantity;
    state = CartState(items);
  }
  
  void clearCart() {
    state = CartState([]);
  }
}

// Cart provider
final cartProvider = StateNotifierProvider<CartNotifier, CartState>((ref) {
  return CartNotifier();
});

// Computed provider for item count
final cartItemCountProvider = Provider<int>((ref) {
  return ref.watch(cartProvider).itemCount;
});

// Computed provider for total price
final cartTotalPriceProvider = Provider<double>((ref) {
  return ref.watch(cartProvider).totalPrice;
});
```

## Best Practices

1. **Use StateProvider for Simple State**
```dart
final countProvider = StateProvider<int>((ref) => 0);
```

2. **Use StateNotifierProvider for Complex State**
```dart
final cartProvider = StateNotifierProvider<CartNotifier, CartState>((ref) {
  return CartNotifier();
});
```

3. **Use Computed Providers for Derived State**
```dart
final totalProvider = Provider<double>((ref) {
  return ref.watch(cartProvider).totalPrice;
});
```

4. **Use ref.watch() for Listening**
```dart
final count = ref.watch(counterProvider);
```

5. **Use ref.read() for Actions**
```dart
ref.read(counterProvider.notifier).state++;
```

## Common Mistakes

1. **Forgetting ProviderScope**
```dart
// BAD:
runApp(MyApp()); // Providers won't work!

// GOOD:
runApp(ProviderScope(child: MyApp()));
```

2. **Using ref.watch() in Actions**
```dart
// BAD:
onPressed: () {
  ref.watch(counterProvider.notifier).state++; // Unnecessary rebuild
}

// GOOD:
onPressed: () {
  ref.read(counterProvider.notifier).state++; // No rebuild
}
```

## When to Use vs When Not to Use

**Use Riverpod when:**
- New projects
- Want compile-time safety
- Need better testing
- Want modern state management

**Don't use Riverpod when:**
- Already using Provider extensively
- Team not familiar with Riverpod
- Need simpler solution (use Provider)

## Comparison with Other Approaches

**Riverpod vs Provider:**
- Riverpod: Compile-time safe, no BuildContext needed
- Provider: Runtime-based, needs BuildContext

**Riverpod vs BLoC:**
- Riverpod: Less boilerplate, easier to use
- BLoC: More structured, better for complex logic

## Interview Questions & Answers

### Q1: What is Riverpod and how does it differ from Provider?

**Answer:**

Riverpod is Provider 2.0 with compile-time safety. It's like Provider but catches errors before your app runs.

**Key Differences:**
- **Compile-time Safety**: Errors caught before runtime
- **No BuildContext**: Access providers anywhere
- **Better Testing**: Easier to test
- **No Widget Tree Dependency**: More flexible

```dart
// Provider (runtime):
Provider.of<CounterProvider>(context).count

// Riverpod (compile-time safe):
ref.watch(counterProvider)
```

### Q2: Explain StateProvider vs StateNotifierProvider.

**Answer:**

**StateProvider**: For simple state (single value)
**StateNotifierProvider**: For complex state (objects with methods)

```dart
// StateProvider - simple:
final countProvider = StateProvider<int>((ref) => 0);

// StateNotifierProvider - complex:
final cartProvider = StateNotifierProvider<CartNotifier, CartState>((ref) {
  return CartNotifier();
});
```

### Q3: What is the difference between ref.watch() and ref.read()?

**Answer:**

**ref.watch()**: Listens to changes, rebuilds widget
**ref.read()**: Reads value once, no rebuild

```dart
// watch() - for displaying data:
final count = ref.watch(counterProvider);

// read() - for actions:
ref.read(counterProvider.notifier).state++;
```

### Q4: How do you create computed providers in Riverpod?

**Answer:**

**Use Provider** to create computed values from other providers.

```dart
final totalProvider = Provider<double>((ref) {
  return ref.watch(cartProvider).totalPrice;
});
```

### Q5: Explain ProviderScope in Riverpod.

**Answer:**

**ProviderScope** makes providers available to the app. It's like a container that holds all providers.

```dart
runApp(
  ProviderScope(
    child: MyApp(),
  ),
);
```

### Q6: How do you handle async operations in Riverpod?

**Answer:**

**Use FutureProvider or AsyncNotifierProvider** for async operations.

```dart
final userProvider = FutureProvider<User>((ref) async {
  return await api.getUser();
});
```

### Q7: What are the advantages of Riverpod over Provider?

**Answer:**

**Advantages:**
- Compile-time safety
- No BuildContext needed
- Better testing
- No widget tree dependency
- More modern API

### Q8: How do you test Riverpod providers?

**Answer:**

**Use ProviderContainer** to test providers in isolation.

```dart
test('counter increments', () {
  final container = ProviderContainer();
  final counter = container.read(counterProvider.notifier);
  
  expect(container.read(counterProvider), 0);
  counter.state++;
  expect(container.read(counterProvider), 1);
});
```

### Q9: Explain freezed with Riverpod.

**Answer:**

**Freezed** creates immutable classes with pattern matching, perfect for state management.

```dart
@freezed
class AuthState {
  const factory AuthState.authenticated(User user) = _Authenticated;
  const factory AuthState.unauthenticated() = _Unauthenticated;
}
```

### Q10: When should you migrate from Provider to Riverpod?

**Answer:**

**Migrate when:**
- Starting new project
- Need compile-time safety
- Want better testing
- Experiencing Provider limitations

---

## Navigation

**Previous:** [Provider](state-management-provider.md)

**Next:** [BLoC](state-management-bloc.md)

