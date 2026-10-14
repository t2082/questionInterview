# Dart Programming

## Table of Contents
- [Null Safety](#null-safety)
- [Async/Await](#asyncawait)
- [Streams](#streams)
- [Generics](#generics)
- [Mixins](#mixins)
- [Extension Methods](#extension-methods)
- [Interview Questions & Answers](#interview-questions--answers)

## Null Safety

**What is Null Safety?**

Null safety is like having a safety net. It prevents your app from crashing when you try to use something that doesn't exist (is null).

**Simple Analogy:**

Think of null safety like a guard at a door:
- **Without null safety**: Anyone can enter, even if they don't exist (crash!)
- **With null safety**: The guard checks if someone exists before letting them in (safe!)

**How Null Safety Works:**

```dart
// Before null safety (Dart 2.0):
String name; // Could be null, could cause crashes
name.length; // Might crash if name is null!

// With null safety (Dart 2.12+):
String name; // ERROR: Must be initialized or nullable
String? nullableName; // OK: Can be null (the ? means nullable)
String nonNullableName = 'John'; // OK: Cannot be null

// Using nullable values safely:
String? name;
if (name != null) {
  print(name.length); // Safe: We checked it's not null
}

// Or use null-aware operators:
String? name;
print(name?.length ?? 0); // If name is null, use 0 instead
```

**Step-by-Step Explanation:**
1. `String?` means "String that can be null"
2. `String` means "String that cannot be null"
3. Before using nullable values, we must check if they're null
4. Use `?.` to safely access properties (won't crash if null)
5. Use `??` to provide a default value if null

**Why This Works:**
- Null safety prevents null pointer exceptions
- The compiler catches errors before runtime
- Makes code safer and more predictable

## Async/Await

**What is Async/Await?**

Async/await is like ordering food at a restaurant. You place your order (start an async operation), wait for it (await), and then eat when it arrives (use the result).

**Simple Analogy:**

Think of async/await like waiting for a package:
- **Synchronous**: You wait at the door until it arrives (blocks everything)
- **Asynchronous**: You do other things while waiting, then check when it arrives (non-blocking)

**How Async/Await Works:**

```dart
// Synchronous function (blocks):
String fetchData() {
  // This blocks - nothing else can happen until this finishes
  return 'Data';
}

// Asynchronous function (non-blocking):
Future<String> fetchDataAsync() async {
  // This doesn't block - other code can run while waiting
  await Future.delayed(Duration(seconds: 2)); // Simulate network delay
  return 'Data';
}

// Using async/await:
void loadData() async {
  print('Starting to load...');
  
  // await pauses here until fetchDataAsync() completes
  // But other code in your app can still run
  String data = await fetchDataAsync();
  
  print('Data loaded: $data');
}

// Error handling with async/await:
void loadDataSafely() async {
  try {
    String data = await fetchDataAsync();
    print('Success: $data');
  } catch (e) {
    print('Error: $e');
  }
}
```

**Step-by-Step Explanation:**
1. `async` keyword makes a function asynchronous
2. `await` pauses execution until the Future completes
3. While waiting, other code can run (non-blocking)
4. Use try-catch to handle errors
5. The function returns a Future automatically

**Why This Works:**
- Prevents UI from freezing during long operations
- Makes asynchronous code look like synchronous code
- Easier to read and understand than callbacks

## Streams

**What are Streams?**

Streams are like a river of data. Data flows continuously, and you can listen to it as it comes.

**Simple Analogy:**

Think of streams like a TV channel:
- Data flows continuously (like a TV show)
- You can subscribe to listen (like tuning in)
- You can unsubscribe when done (like changing channels)

**How Streams Work:**

```dart
// Creating a stream:
Stream<int> countStream() async* {
  // async* means this function returns a stream
  for (int i = 1; i <= 5; i++) {
    await Future.delayed(Duration(seconds: 1));
    yield i; // Send value to stream (like adding water to river)
  }
}

// Listening to a stream:
void listenToStream() {
  countStream().listen(
    (value) {
      // This is called each time a new value arrives
      print('Received: $value');
    },
    onError: (error) {
      print('Error: $error');
    },
    onDone: () {
      print('Stream finished');
    },
  );
}

// Using StreamBuilder in Flutter:
StreamBuilder<int>(
  stream: countStream(),
  builder: (context, snapshot) {
    if (snapshot.hasData) {
      return Text('Count: ${snapshot.data}');
    } else if (snapshot.hasError) {
      return Text('Error: ${snapshot.error}');
    } else {
      return CircularProgressIndicator();
    }
  },
)
```

**Step-by-Step Explanation:**
1. `async*` creates a function that returns a Stream
2. `yield` sends a value to the stream
3. `listen()` subscribes to the stream
4. Callback is called for each value
5. StreamBuilder automatically rebuilds when new data arrives

**Why This Works:**
- Streams handle continuous data flow
- Perfect for real-time updates (chat, notifications)
- StreamBuilder makes it easy to use in Flutter

## Generics

**What are Generics?**

Generics are like a reusable container. You can put different types of things in it, but you specify what type when you create it.

**Simple Analogy:**

Think of generics like a labeled box:
- A box labeled "Apples" can only hold apples
- A box labeled "Oranges" can only hold oranges
- But the box itself is the same - just the label changes

**How Generics Work:**

```dart
// Without generics (not flexible):
class IntBox {
  int value;
  IntBox(this.value);
}

class StringBox {
  String value;
  StringBox(this.value);
}
// Need separate class for each type!

// With generics (flexible):
class Box<T> {
  // T is a type parameter - like a placeholder
  // Think of T as "whatever type you want"
  T value;
  Box(this.value);
  
  T getValue() {
    return value;
  }
}

// Using generics:
Box<int> intBox = Box<int>(5); // Box for integers
Box<String> stringBox = Box<String>('Hello'); // Box for strings
Box<bool> boolBox = Box<bool>(true); // Box for booleans

// Generic methods:
T getFirst<T>(List<T> list) {
  return list[0];
}

int firstInt = getFirst<int>([1, 2, 3]);
String firstString = getFirst<String>(['a', 'b', 'c']);
```

**Step-by-Step Explanation:**
1. `<T>` declares a type parameter (generic type)
2. `T` can be replaced with any type when using the class
3. One class works for multiple types
4. Type safety is maintained (can't put wrong type)

**Why This Works:**
- Reduces code duplication
- Maintains type safety
- Makes code more flexible and reusable

## Mixins

**What are Mixins?**

Mixins are like adding extra features to a class without inheritance. Think of it like adding apps to your phone - you get new features without changing the phone itself.

**Simple Analogy:**

Think of mixins like adding skills to a character in a game:
- Base class: A warrior
- Mixin: Add "flying" skill
- Result: A warrior who can fly

**How Mixins Work:**

```dart
// Define a mixin:
mixin Flyable {
  // Mixins contain methods that can be added to classes
  void fly() {
    print('Flying!');
  }
}

mixin Swimmable {
  void swim() {
    print('Swimming!');
  }
}

// Use mixins in a class:
class Bird with Flyable {
  // Bird class now has fly() method from Flyable mixin
  void chirp() {
    print('Chirp!');
  }
}

class Duck with Flyable, Swimmable {
  // Duck can both fly and swim!
  void quack() {
    print('Quack!');
  }
}

// Using the classes:
Bird bird = Bird();
bird.fly(); // From Flyable mixin
bird.chirp(); // From Bird class

Duck duck = Duck();
duck.fly(); // From Flyable mixin
duck.swim(); // From Swimmable mixin
duck.quack(); // From Duck class
```

**Step-by-Step Explanation:**
1. `mixin` keyword creates a mixin
2. Mixins contain methods that can be reused
3. `with` keyword adds mixin to a class
4. A class can use multiple mixins
5. Mixins provide code reuse without inheritance

**Why This Works:**
- Avoids multiple inheritance issues
- Provides code reuse
- Makes classes more flexible
- Common in Flutter for adding functionality

## Extension Methods

**What are Extension Methods?**

Extension methods let you add new methods to existing classes without modifying them. Think of it like adding a new button to someone else's remote control without opening it.

**Simple Analogy:**

Think of extension methods like adding a new feature to a tool:
- Original tool: A hammer
- Extension: Add a "measure" feature
- Result: A hammer that can also measure

**How Extension Methods Work:**

```dart
// Extending String class:
extension StringExtensions on String {
  // Add a method to check if string is a valid email
  bool isValidEmail() {
    return contains('@') && contains('.');
  }
  
  // Add a method to capitalize first letter
  String capitalizeFirst() {
    if (isEmpty) return this;
    return this[0].toUpperCase() + substring(1);
  }
}

// Using the extension:
void useExtensions() {
  String email = 'user@example.com';
  print(email.isValidEmail()); // true - method added to String!
  
  String name = 'john';
  print(name.capitalizeFirst()); // 'John' - method added to String!
}

// Extending int class:
extension IntExtensions on int {
  // Add a method to check if number is even
  bool isEven() {
    return this % 2 == 0;
  }
  
  // Add a method to convert seconds to minutes
  double toMinutes() {
    return this / 60.0;
  }
}

// Using int extensions:
void useIntExtensions() {
  int number = 4;
  print(number.isEven()); // true
  
  int seconds = 120;
  print(seconds.toMinutes()); // 2.0
}
```

**Step-by-Step Explanation:**
1. `extension` keyword creates an extension
2. `on Type` specifies which type to extend
3. Add methods inside the extension
4. Methods become available on that type
5. Can extend any type (even built-in types)

**Why This Works:**
- Add functionality without modifying original class
- Makes code more readable
- Common in Flutter for utility methods
- Type-safe (only works on specified type)

## Interview Questions & Answers

### Q1: Explain null safety in Dart with examples.

**Answer:**

**Null safety** is a feature in Dart that prevents crashes from trying to use null values by making nullability explicit in the type system. By default, variables cannot be null unless you explicitly mark them with `?` (like `String?`), which tells the compiler that this variable might be null. This forces developers to handle null cases before using values, preventing common runtime errors like "null pointer exceptions". Null safety uses operators like `?.` (null-aware access), `??` (null coalescing), and `!` (null assertion) to safely work with potentially null values, making code more robust and preventing unexpected crashes.

```dart
// Nullable types (can be null):
String? name; // The ? means this can be null
name = null; // OK
name = 'John'; // OK

// Non-nullable types (cannot be null):
String title = 'Hello'; // Cannot be null
// title = null; // ERROR: Cannot assign null

// Null-aware operators:
String? name;
print(name?.length ?? 0); // If name is null, use 0

// Null assertion (use carefully):
String? name;
String nonNullName = name!; // Force unwrap (crashes if null)
```

**Key Points:**
- `?` makes a type nullable
- `?.` safely accesses properties
- `??` provides default values
- `!` force unwraps (dangerous)

### Q2: What is the difference between async and await?

**Answer:**

**async** is a keyword that marks a function as asynchronous, automatically wrapping its return value in a `Future` and allowing the function to use `await`. **await** is used inside async functions to pause execution until a `Future` completes, making asynchronous code look and read like synchronous code. When you use `await`, the function waits for the Future to complete, but it doesn't block the entire program - other code can still run while waiting. This combination allows you to write clean, readable asynchronous code without nested callbacks, making it easier to handle network requests, file I/O, and other time-consuming operations.

```dart
// async makes function return Future
Future<String> fetchData() async {
  await Future.delayed(Duration(seconds: 1));
  return 'Data';
}

// await pauses until Future completes
void loadData() async {
  String data = await fetchData(); // Waits here
  print(data);
}
```

**Key Points:**
- `async` function returns Future automatically
- `await` pauses execution (non-blocking)
- Other code can run while waiting

### Q3: Explain Streams in Dart.

**Answer:**

**Streams** provide a continuous flow of data over time, like a river that keeps flowing with new values. Unlike `Future` which returns a single value once, streams can emit multiple values asynchronously, making them perfect for real-time data like user input, sensor readings, or live updates from a server. You create streams using `async*` functions with `yield` to emit values, and listen to them using `.listen()` to receive each value as it arrives. Streams are essential for reactive programming in Flutter, enabling features like real-time chat, live data feeds, and continuous user interactions.

```dart
Stream<int> countStream() async* {
  for (int i = 1; i <= 5; i++) {
    await Future.delayed(Duration(seconds: 1));
    yield i; // Send value to stream
  }
}

// Listen to stream:
countStream().listen((value) {
  print('Received: $value');
});
```

**Key Points:**
- `async*` creates a stream
- `yield` sends values
- `listen()` subscribes to stream
- Perfect for real-time data

### Q4: What are generics and why use them?

**Answer:**

**Generics** allow you to write code that works with multiple types while maintaining type safety, using type parameters (like `<T>`) as placeholders for actual types. Instead of creating separate classes for each type (like `IntBox`, `StringBox`), you create one generic class (like `Box<T>`) that works with any type. Generics eliminate code duplication by allowing you to write reusable code that's type-safe - the compiler ensures you use the correct types, preventing runtime errors. They're used extensively in Flutter collections (like `List<T>`, `Map<K, V>`) and are essential for creating flexible, reusable components.

```dart
class Box<T> {
  T value;
  Box(this.value);
}

Box<int> intBox = Box<int>(5);
Box<String> stringBox = Box<String>('Hello');
```

**Key Points:**
- `<T>` is type parameter
- One class for multiple types
- Maintains type safety
- Reduces code duplication

### Q5: Explain mixins in Dart.

**Answer:**

**Mixins** are a way to add functionality to classes without using inheritance, allowing you to share code across multiple class hierarchies. You define a mixin using the `mixin` keyword, and then add it to a class using the `with` keyword - a class can use multiple mixins, which isn't possible with single inheritance. Mixins are perfect for adding specific behaviors (like `Flyable`, `Swimmable`) to different classes without creating complex inheritance chains. They're commonly used in Flutter to add functionality to widgets or services, providing a flexible way to compose classes with reusable behaviors while avoiding the limitations and complexity of multiple inheritance.

```dart
mixin Flyable {
  void fly() => print('Flying');
}

class Bird with Flyable {
  // Now has fly() method
}
```

**Key Points:**
- `mixin` keyword creates mixin
- `with` adds mixin to class
- Multiple mixins allowed
- Avoids inheritance issues

### Q6: What are extension methods?

**Answer:**

**Extension methods** allow you to add new methods to existing classes (even built-in types like `String` or `int`) without modifying the original class or creating a subclass. You define an extension using the `extension` keyword, specify the target type with `on Type`, and then add methods that become available on that type. This is particularly useful for adding utility methods to types you don't own, like adding `isValidEmail()` to `String` or `toMinutes()` to `int`. Extension methods maintain type safety and make code more readable by allowing you to call methods directly on types, making your code feel more natural and expressive.

```dart
extension StringExtensions on String {
  bool isValidEmail() => contains('@');
}

'user@example.com'.isValidEmail(); // true
```

**Key Points:**
- `extension` keyword
- `on Type` specifies target
- Add methods without modifying original
- Type-safe

### Q7: Explain Future vs Stream.

**Answer:**

**Future** represents a single asynchronous value that will be available at some point in the future - it's like ordering a pizza and getting it once. **Stream** represents a sequence of asynchronous values that arrive over time - it's like a subscription that keeps delivering pizzas. Use `Future` when you need a one-time result (like fetching a user profile or loading a file), and use `Stream` when you need continuous updates (like real-time chat messages, live location updates, or user input). Both are essential for asynchronous programming in Dart, with `Future` for single operations and `Stream` for continuous data flows.

```dart
// Future: One value, one time
Future<String> fetchUser() async {
  return 'User data';
}

// Stream: Multiple values over time
Stream<int> countStream() async* {
  for (int i = 1; i <= 5; i++) {
    yield i;
  }
}
```

**Key Points:**
- Future: One result
- Stream: Continuous data
- Use Future for single operations
- Use Stream for real-time updates

### Q8: What is the difference between const and final?

**Answer:**

**const** creates a compile-time constant - the value must be known when you write the code and cannot change, and the compiler can optimize it by reusing the same instance. **final** creates a runtime constant - the value is set once when the code runs and cannot be reassigned, but it can be calculated at runtime. Use `const` for values that are known at compile time (like `const int maxItems = 100`), which is more efficient. Use `final` for values that need to be calculated or assigned at runtime (like `final user = await fetchUser()`). In Flutter, `const` widgets are particularly important for performance optimization, as they're created once and reused.

```dart
const int compileTime = 5; // Known when writing code
final int runtime = calculate(); // Known when code runs
```

**Key Points:**
- `const`: Compile-time constant
- `final`: Runtime constant
- `const` more efficient
- `final` more flexible

### Q9: Explain the cascade operator (..).

**Answer:**

**Cascade operator (`..`)** allows you to perform multiple operations on the same object in sequence, returning the original object after each operation instead of the operation's result. This lets you chain method calls and property assignments without repeatedly referencing the object variable. Instead of writing `list.add(4); list.add(5); list.sort();`, you can write `list..add(4)..add(5)..sort();`. The cascade operator is particularly useful in Flutter for configuring widgets, where you might set multiple properties on the same widget, making the code more concise and readable while clearly showing that all operations are on the same object.

```dart
// Without cascade:
var list = [1, 2, 3];
list.add(4);
list.add(5);
list.sort();

// With cascade:
var list = [1, 2, 3]
  ..add(4)
  ..add(5)
  ..sort();
```

**Key Points:**
- `..` returns same object
- Chains multiple operations
- More readable
- Common in Flutter

### Q10: What are named parameters vs positional parameters?

**Answer:**

**Positional parameters** are passed in a specific order and are required by their position in the function signature - the order matters, and you must provide them in the correct sequence. **Named parameters** are passed by name using curly braces `{}` and can be provided in any order - they're optional by default unless marked with `required`, making function calls more readable and self-documenting. Flutter extensively uses named parameters for widget constructors (like `Text('Hello', style: TextStyle(), textAlign: TextAlign.center)`), which makes code more readable and maintainable, especially when functions have many parameters. Named parameters make it clear what each value represents, reducing errors from passing arguments in the wrong order.

```dart
// Positional:
void greet(String name, int age) {}
greet('John', 25); // Order matters

// Named:
void greet({String? name, int? age}) {}
greet(age: 25, name: 'John'); // Order doesn't matter
```

**Key Points:**
- Positional: Order matters
- Named: Order doesn't matter
- Named more readable
- Flutter uses named extensively

---

## Navigation

**Previous:** [Flutter Basics](flutter-basics.md)

**Next:** [State Management Overview](state-management-overview.md)

