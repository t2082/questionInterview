# MobX - Observable State Management

## Table of Contents
- [What is MobX?](#what-is-mobx)
- [Why Use MobX?](#why-use-mobx)
- [How Does MobX Work?](#how-does-mobx-work)
- [Basic Example](#basic-example)
- [Intermediate Example](#intermediate-example)
- [Advanced Example](#advanced-example)
- [Best Practices](#best-practices)
- [Common Mistakes](#common-mistakes)
- [When to Use vs When Not to Use](#when-to-use-vs-when-not-to-use)
- [Comparison with Other Approaches](#comparison-with-other-approaches)
- [Interview Questions & Answers](#interview-questions--answers)

## What is MobX?

**Simple Explanation:**

MobX is like a smart mirror that automatically updates when something changes. You mark data as observable, and widgets automatically update when that data changes.

**Simple Analogy:**

Think of MobX like a smart home system:
- **Observable** = Sensors that detect changes
- **Actions** = Commands that change things
- **Computed** = Automatic calculations based on observables
- **Reactions** = Things that happen automatically when sensors detect changes

**Key Concepts:**

- **Observable**: Data that can be watched
- **Action**: Method that modifies observables
- **Computed**: Derived values that update automatically
- **Reaction**: Side effects that run when observables change
- **Automatic Updates**: UI updates automatically when observables change

## Why Use MobX?

**Benefits:**

1. **Automatic Reactivity**: UI updates automatically
2. **Minimal Boilerplate**: Less code needed
3. **Simple API**: Easy to understand
4. **Reactive Programming**: Natural reactive style
5. **Good Performance**: Efficient updates

**When It's Perfect:**

- Want automatic reactivity
- Prefer observable pattern
- Need minimal boilerplate
- Reactive programming style
- Small to medium apps

## How Does MobX Work?

**The Mechanism:**

1. Mark data as @observable
2. Create @action methods to modify observables
3. Use @computed for derived values
4. Wrap widgets with Observer
5. Widgets automatically rebuild when observables change

**Simple Flow:**

```
Observable → Action → Observable Changes → Observer Rebuilds
```

## Basic Example

**Simple Counter with MobX:**

```dart
import 'package:mobx/mobx.dart';
import 'package:flutter_mobx/flutter_mobx.dart';

part 'counter.g.dart'; // Generated file

// Step 1: Create Store with MobX
// Store holds observable state and actions
// Think of it as a smart container that can detect changes
class CounterStore = _CounterStore with _$CounterStore;

abstract class _CounterStore with Store {
  // @observable marks variable as observable
  // When this changes, widgets watching it will rebuild
  // Think of it as a variable with a bell that rings when it changes
  @observable
  int count = 0;
  
  // @action marks method that modifies observables
  // Think of it as a method that changes the observable and rings the bell
  @action
  void increment() {
    count++; // Modify observable - triggers automatic update!
  }
  
  @action
  void decrement() {
    count--;
  }
  
  @action
  void reset() {
    count = 0;
  }
  
  // @computed creates derived values
  // Think of it as a value that automatically calculates when observables change
  @computed
  String get countText => 'Count: $count';
}

// Step 2: Initialize Store
final counterStore = CounterStore();

// Step 3: Use Store in Widget
void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MobX Counter',
      home: CounterScreen(),
    );
  }
}

class CounterScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('MobX Counter')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Observer automatically rebuilds when observables change
            // Think of it as watching a TV - when the channel changes, you see it
            Observer(
              builder: (_) => Text(
                counterStore.countText, // Uses computed value
                style: TextStyle(fontSize: 48),
              ),
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Decrement button
                ElevatedButton(
                  onPressed: () {
                    counterStore.decrement(); // Call action
                  },
                  child: Text('-'),
                ),
                SizedBox(width: 20),
                // Increment button
                ElevatedButton(
                  onPressed: () {
                    counterStore.increment(); // Call action
                  },
                  child: Text('+'),
                ),
              ],
            ),
            SizedBox(height: 20),
            // Reset button
            ElevatedButton(
              onPressed: () {
                counterStore.reset(); // Call action
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
1. We create a `CounterStore` with `@observable` count
2. We mark methods as `@action` that modify observables
3. We create `@computed` values that derive from observables
4. We use `Observer` widget to watch observables
5. When action modifies observable, `Observer` automatically rebuilds

**Why This Works:**
- `@observable` makes variables reactive
- `@action` ensures changes are tracked
- `@computed` creates derived values automatically
- `Observer` listens to changes and rebuilds
- Minimal boilerplate needed

## Intermediate Example

**Todo List with MobX:**

```dart
import 'package:mobx/mobx.dart';
import 'package:flutter_mobx/flutter_mobx.dart';

part 'todo.g.dart';

// Todo model
class Todo {
  final String id;
  String title;
  bool isCompleted;
  
  Todo({required this.id, required this.title, this.isCompleted = false});
}

// Todo store
class TodoStore = _TodoStore with _$TodoStore;

abstract class _TodoStore with Store {
  // Observable list of todos
  @observable
  ObservableList<Todo> todos = ObservableList<Todo>();
  
  // Action to add todo
  @action
  void addTodo(String title) {
    if (title.trim().isEmpty) return;
    
    final todo = Todo(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      title: title,
    );
    todos.add(todo);
  }
  
  // Action to toggle todo
  @action
  void toggleTodo(String id) {
    final todo = todos.firstWhere((todo) => todo.id == id);
    todo.isCompleted = !todo.isCompleted;
  }
  
  // Action to delete todo
  @action
  void deleteTodo(String id) {
    todos.removeWhere((todo) => todo.id == id);
  }
  
  // Computed: total todos
  @computed
  int get totalTodos => todos.length;
  
  // Computed: completed todos
  @computed
  int get completedTodos => todos.where((todo) => todo.isCompleted).length;
  
  // Computed: pending todos
  @computed
  int get pendingTodos => totalTodos - completedTodos;
}

final todoStore = TodoStore();
```

## Advanced Example

**Shopping Cart with MobX:**

```dart
import 'package:mobx/mobx.dart';

part 'cart.g.dart';

class Product {
  final String id;
  final String name;
  final double price;
  
  Product({required this.id, required this.name, required this.price});
}

class CartItem {
  final Product product;
  int quantity;
  
  CartItem({required this.product, this.quantity = 1});
  
  double get total => product.price * quantity;
}

class CartStore = _CartStore with _$CartStore;

abstract class _CartStore with Store {
  @observable
  ObservableList<CartItem> items = ObservableList<CartItem>();
  
  @action
  void addProduct(Product product) {
    final existingIndex = items.indexWhere(
      (item) => item.product.id == product.id,
    );
    
    if (existingIndex >= 0) {
      items[existingIndex].quantity++;
    } else {
      items.add(CartItem(product: product));
    }
  }
  
  @action
  void removeProduct(String productId) {
    items.removeWhere((item) => item.product.id == productId);
  }
  
  @computed
  int get itemCount => items.fold(0, (sum, item) => sum + item.quantity);
  
  @computed
  double get totalPrice => items.fold(0.0, (sum, item) => sum + item.total);
}
```

## Best Practices

1. **Use @observable for State**
```dart
@observable
int count = 0;
```

2. **Use @action for Modifications**
```dart
@action
void increment() {
  count++;
}
```

3. **Use @computed for Derived Values**
```dart
@computed
int get doubleCount => count * 2;
```

4. **Use Observer for UI Updates**
```dart
Observer(
  builder: (_) => Text('$count'),
)
```

5. **Run Code Generation**
```bash
flutter pub run build_runner build
```

## Common Mistakes

1. **Forgetting @observable**
```dart
// BAD - won't update:
int count = 0;

// GOOD:
@observable
int count = 0;
```

2. **Not Using @action**
```dart
// BAD - changes might not be tracked:
void increment() {
  count++;
}

// GOOD:
@action
void increment() {
  count++;
}
```

3. **Forgetting Observer**
```dart
// BAD - won't rebuild:
Text('$count')

// GOOD:
Observer(builder: (_) => Text('$count'))
```

## When to Use vs When Not to Use

**Use MobX when:**
- Want automatic reactivity
- Prefer observable pattern
- Need minimal boilerplate
- Reactive programming style
- Small to medium apps

**Don't use MobX when:**
- Need compile-time safety (use Riverpod)
- Want pattern-based approach (use BLoC)
- Large enterprise apps
- Team not familiar with MobX

## Comparison with Other Approaches

**MobX vs Provider:**
- MobX: Automatic reactivity, less boilerplate
- Provider: More manual, more control

**MobX vs GetX:**
- MobX: Just state management
- GetX: All-in-one solution

## Interview Questions & Answers

### Q1: What is MobX and how does it work?

**Answer:**

MobX is observable state management. It uses observables, actions, and computed values.

**How it works:**
1. Mark data as @observable
2. Create @action methods to modify observables
3. Use @computed for derived values
4. Wrap widgets with Observer
5. Widgets automatically rebuild when observables change

```dart
class CounterStore = _CounterStore with _$CounterStore;

abstract class _CounterStore with Store {
  @observable
  int count = 0;
  
  @action
  void increment() {
    count++;
  }
}
```

### Q2: Explain Observable, Action, and Computed in MobX.

**Answer:**

**@observable**: Marks data that can be watched
**@action**: Methods that modify observables
**@computed**: Derived values that update automatically

```dart
@observable
int count = 0;

@action
void increment() {
  count++;
}

@computed
int get doubleCount => count * 2;
```

### Q3: How does MobX differ from other state management solutions?

**Answer:**

**MobX:**
- Automatic reactivity
- Observable pattern
- Minimal boilerplate
- Reactive programming

**Others:**
- Manual updates (Provider)
- Pattern-based (BLoC)
- More boilerplate
- Different patterns

### Q4: When should you use MobX?

**Answer:**

**Use MobX when:**
- Want automatic reactivity
- Prefer observable pattern
- Need minimal boilerplate
- Reactive programming style
- Small to medium apps

### Q5: How do you handle async operations in MobX?

**Answer:**

**Use @action with async/await.**

```dart
@action
Future<void> loadData() async {
  isLoading = true;
  try {
    data = await api.getData();
  } finally {
    isLoading = false;
  }
}
```

### Q6: How do you test MobX stores?

**Answer:**

**Test stores directly** like regular classes.

```dart
test('increment increases count', () {
  final store = CounterStore();
  expect(store.count, 0);
  
  store.increment();
  expect(store.count, 1);
});
```

### Q7: Explain MobX reactive programming.

**Answer:**

**MobX uses reactive programming** where observables automatically trigger updates.

```dart
@observable
int count = 0;

// When count changes, Observer automatically rebuilds
Observer(builder: (_) => Text('$count'))
```

### Q8: What are the best practices for using MobX?

**Answer:**

**Best Practices:**
1. Use @observable for state
2. Use @action for modifications
3. Use @computed for derived values
4. Use Observer for UI updates
5. Run code generation

---

## Navigation

**Previous:** [Redux](state-management-redux.md)

**Next:** [State Management Comparison](state-management-comparison.md)

