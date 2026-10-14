# Redux - Predictable State Container

## Table of Contents
- [What is Redux?](#what-is-redux)
- [Why Use Redux?](#why-use-redux)
- [How Does Redux Work?](#how-does-redux-work)
- [Basic Example](#basic-example)
- [Intermediate Example](#intermediate-example)
- [Advanced Example](#advanced-example)
- [Best Practices](#best-practices)
- [Common Mistakes](#common-mistakes)
- [When to Use vs When Not to Use](#when-to-use-vs-when-not-to-use)
- [Comparison with Other Approaches](#comparison-with-other-approaches)
- [Interview Questions & Answers](#interview-questions--answers)

## What is Redux?

**Simple Explanation:**

Redux is like a library system. You submit an action (like checking out a book), the librarian (reducer) processes it, and updates the library catalog (store).

**Simple Analogy:**

Think of Redux like a library:
- **Actions** = Requests (check out book, return book)
- **Reducers** = Librarian (processes requests)
- **Store** = Library catalog (holds all books/state)
- **Single Source of Truth** = One catalog for everything

**Key Concepts:**

- **Actions**: Describe what happened (plain objects)
- **Reducers**: Pure functions that update state
- **Store**: Holds the entire app state
- **Dispatch**: Send actions to store
- **Single Source of Truth**: One store for all state

## Why Use Redux?

**Benefits:**

1. **Predictable**: Same input always produces same output
2. **Time-Travel Debugging**: Can replay actions
3. **Single Source of Truth**: All state in one place
4. **Testable**: Pure functions are easy to test
5. **Familiar**: If you know React Redux, Flutter Redux is similar

**When It's Perfect:**

- Complex state management
- Need time-travel debugging
- Coming from React background
- Want predictable state flow
- Large applications

## How Does Redux Work?

**The Mechanism:**

1. User action creates an Action
2. Action is dispatched to Store
3. Store sends action to Reducer
4. Reducer returns new state
5. Store updates and notifies listeners
6. UI rebuilds with new state

**Simple Flow:**

```
Action → Dispatch → Store → Reducer → New State → UI Update
```

## Basic Example

**Simple Counter with Redux:**

```dart
import 'package:flutter_redux/flutter_redux.dart';
import 'package:redux/redux.dart';

// Step 1: Define Actions
// Actions are like commands - they describe what should happen
// Think of them as messages sent to the store
class IncrementAction {}

class DecrementAction {}

class ResetAction {}

// Step 2: Define State
// State is the data structure that holds your app's state
// Think of it as a box that holds all your data
class AppState {
  final int count;
  
  AppState({required this.count});
  
  // CopyWith creates a new state with updated values
  // Think of it as creating a new box with some items changed
  AppState copyWith({int? count}) {
    return AppState(count: count ?? this.count);
  }
}

// Step 3: Create Reducer
// Reducer is a pure function that takes current state and action,
// and returns new state
// Think of it as a machine that processes actions and produces new state
AppState counterReducer(AppState state, dynamic action) {
  // Check what action was dispatched
  // Think of it as checking what command was received
  if (action is IncrementAction) {
    // Return new state with incremented count
    // Important: Don't modify old state, create new one!
    return state.copyWith(count: state.count + 1);
  } else if (action is DecrementAction) {
    return state.copyWith(count: state.count - 1);
  } else if (action is ResetAction) {
    return state.copyWith(count: 0);
  }
  
  // If action doesn't match, return current state unchanged
  return state;
}

// Step 4: Create Store
// Store holds the state and handles actions
// Think of it as the central hub for your app's state
final store = Store<AppState>(
  counterReducer,
  initialState: AppState(count: 0), // Starting state
);

// Step 5: Use Store in App
void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return StoreProvider<AppState>(
      // StoreProvider makes store available to child widgets
      // Think of it as putting the store where everyone can access it
      store: store,
      child: MaterialApp(
        title: 'Redux Counter',
        home: CounterScreen(),
      ),
    );
  }
}

// Step 6: Use Store in Widget
class CounterScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return StoreConnector<AppState, int>(
      // StoreConnector connects widget to store
      // It converts store state to widget data
      // Think of it as a translator between store and widget
      converter: (store) => store.state.count, // Get count from store
      builder: (context, count) {
        // builder is called whenever count changes
        // Think of it as rebuilding the widget when data changes
        return Scaffold(
          appBar: AppBar(title: Text('Redux Counter')),
          body: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Display count from store
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
                        // Dispatch action to store
                        // Think of it as sending a command to the store
                        StoreProvider.of<AppState>(context)
                            .dispatch(DecrementAction());
                      },
                      child: Text('-'),
                    ),
                    SizedBox(width: 20),
                    // Increment button
                    ElevatedButton(
                      onPressed: () {
                        // Dispatch action to store
                        StoreProvider.of<AppState>(context)
                            .dispatch(IncrementAction());
                      },
                      child: Text('+'),
                    ),
                  ],
                ),
                SizedBox(height: 20),
                // Reset button
                ElevatedButton(
                  onPressed: () {
                    StoreProvider.of<AppState>(context)
                        .dispatch(ResetAction());
                  },
                  child: Text('Reset'),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
```

**Step-by-Step Explanation:**
1. We define Actions (IncrementAction, DecrementAction, ResetAction)
2. We define AppState to hold our state (count)
3. We create a reducer that processes actions and returns new state
4. We create a Store with the reducer and initial state
5. We wrap the app with StoreProvider to make store available
6. We use StoreConnector to connect widgets to store
7. When user presses button, we dispatch an action
8. Reducer processes action and returns new state
9. Store updates and StoreConnector rebuilds widget

**Why This Works:**
- Single source of truth (one store)
- Predictable: same action always produces same result
- Pure functions (reducers) are easy to test
- Time-travel debugging possible
- Clear data flow

## Intermediate Example

**Todo List with Redux:**

```dart
import 'package:flutter_redux/flutter_redux.dart';
import 'package:redux/redux.dart';

// Models
class Todo {
  final String id;
  final String title;
  final bool isCompleted;
  
  Todo({required this.id, required this.title, this.isCompleted = false});
  
  Todo copyWith({String? id, String? title, bool? isCompleted}) {
    return Todo(
      id: id ?? this.id,
      title: title ?? this.title,
      isCompleted: isCompleted ?? this.isCompleted,
    );
  }
}

// Actions
class AddTodoAction {
  final String title;
  AddTodoAction(this.title);
}

class ToggleTodoAction {
  final String id;
  ToggleTodoAction(this.id);
}

class DeleteTodoAction {
  final String id;
  DeleteTodoAction(this.id);
}

// State
class AppState {
  final List<Todo> todos;
  
  AppState({required this.todos});
  
  AppState copyWith({List<Todo>? todos}) {
    return AppState(todos: todos ?? this.todos);
  }
}

// Reducer
AppState todoReducer(AppState state, dynamic action) {
  if (action is AddTodoAction) {
    final newTodo = Todo(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      title: action.title,
    );
    return state.copyWith(todos: [...state.todos, newTodo]);
  } else if (action is ToggleTodoAction) {
    final updatedTodos = state.todos.map((todo) {
      if (todo.id == action.id) {
        return todo.copyWith(isCompleted: !todo.isCompleted);
      }
      return todo;
    }).toList();
    return state.copyWith(todos: updatedTodos);
  } else if (action is DeleteTodoAction) {
    final updatedTodos = state.todos
        .where((todo) => todo.id != action.id)
        .toList();
    return state.copyWith(todos: updatedTodos);
  }
  return state;
}

// Store
final store = Store<AppState>(
  todoReducer,
  initialState: AppState(todos: []),
);
```

## Advanced Example

**Redux with Middleware:**

```dart
import 'package:redux/redux.dart';

// Middleware for logging actions
// Middleware intercepts actions before they reach reducer
// Think of it as a security checkpoint
List<Middleware<AppState>> loggingMiddleware() {
  return [
    // TypedMiddleware logs every action
    TypedMiddleware<AppState, dynamic>(
      (store, action, next) {
        print('Action: $action');
        print('State before: ${store.state}');
        next(action); // Continue to reducer
        print('State after: ${store.state}');
      },
    ),
  ];
}

// Store with middleware
final store = Store<AppState>(
  todoReducer,
  initialState: AppState(todos: []),
  middleware: loggingMiddleware(), // Add middleware
);
```

## Best Practices

1. **Keep Reducers Pure**
```dart
// GOOD - pure function:
AppState reducer(AppState state, dynamic action) {
  return state.copyWith(count: state.count + 1);
}

// BAD - side effects:
AppState reducer(AppState state, dynamic action) {
  print('Updating'); // Side effect!
  return state.copyWith(count: state.count + 1);
}
```

2. **Don't Mutate State**
```dart
// BAD - mutates state:
state.todos.add(newTodo); // Don't do this!

// GOOD - creates new state:
return state.copyWith(todos: [...state.todos, newTodo]);
```

3. **Use Middleware for Side Effects**
```dart
// Use middleware for API calls, logging, etc.
middleware: [
  thunkMiddleware, // For async actions
  loggingMiddleware,
]
```

4. **Combine Reducers for Large Apps**
```dart
final appReducer = combineReducers<AppState>([
  TypedReducer<AppState, IncrementAction>(counterReducer),
  TypedReducer<AppState, AddTodoAction>(todoReducer),
]);
```

## Common Mistakes

1. **Mutating State**
```dart
// BAD:
state.todos.add(newTodo);

// GOOD:
return state.copyWith(todos: [...state.todos, newTodo]);
```

2. **Side Effects in Reducers**
```dart
// BAD:
AppState reducer(AppState state, dynamic action) {
  api.call(); // Side effect!
  return state;
}

// GOOD - use middleware:
middleware: [apiMiddleware]
```

## When to Use vs When Not to Use

**Use Redux when:**
- Complex state management
- Need time-travel debugging
- Coming from React background
- Want predictable state flow
- Large applications

**Don't use Redux when:**
- Simple apps
- Don't need time-travel
- Team not familiar with Redux
- Too much boilerplate for needs

## Comparison with Other Approaches

**Redux vs BLoC:**
- Redux: Action-based, single store
- BLoC: Event-based, multiple BLoCs

**Redux vs Provider:**
- Redux: More structured, time-travel
- Provider: Simpler, less boilerplate

## Interview Questions & Answers

### Q1: What is Redux and how does it work in Flutter?

**Answer:**

Redux is a predictable state container. It uses actions, reducers, and a store.

**How it works:**
1. Actions describe what happened
2. Reducers process actions and return new state
3. Store holds state and dispatches actions
4. UI connects to store and updates automatically

```dart
// Action
class IncrementAction {}

// Reducer
AppState reducer(AppState state, dynamic action) {
  if (action is IncrementAction) {
    return state.copyWith(count: state.count + 1);
  }
  return state;
}

// Store
final store = Store<AppState>(reducer, initialState: AppState(count: 0));
```

### Q2: Explain Redux principles (Single Source of Truth, etc.).

**Answer:**

**Redux Principles:**
1. **Single Source of Truth**: All state in one store
2. **State is Read-Only**: Can't modify directly, only through actions
3. **Changes via Pure Functions**: Reducers are pure functions

```dart
// Single source of truth
final store = Store<AppState>(...);

// State is read-only - can't modify directly
// Must dispatch actions
store.dispatch(IncrementAction());

// Pure reducer
AppState reducer(AppState state, dynamic action) {
  return state.copyWith(...); // Pure function
}
```

### Q3: What are Actions, Reducers, and Store in Redux?

**Answer:**

**Actions**: Describe what happened (plain objects)
**Reducers**: Pure functions that update state
**Store**: Holds state and handles actions

```dart
// Action
class IncrementAction {}

// Reducer
AppState reducer(AppState state, dynamic action) {
  if (action is IncrementAction) {
    return state.copyWith(count: state.count + 1);
  }
  return state;
}

// Store
final store = Store<AppState>(reducer, initialState: AppState(count: 0));
```

### Q4: How does Redux differ from other state management solutions?

**Answer:**

**Redux:**
- Single store
- Action-based
- Time-travel debugging
- Predictable flow

**Others:**
- Multiple stores/BLoCs
- Event-based or reactive
- No time-travel
- Different patterns

### Q5: Explain middleware in Redux.

**Answer:**

**Middleware** intercepts actions before they reach reducers. Use for logging, API calls, etc.

```dart
List<Middleware<AppState>> loggingMiddleware() {
  return [
    TypedMiddleware<AppState, dynamic>(
      (store, action, next) {
        print('Action: $action');
        next(action);
      },
    ),
  ];
}
```

### Q6: When should you use Redux?

**Answer:**

**Use Redux when:**
- Complex state management
- Need time-travel debugging
- Coming from React background
- Want predictable state flow
- Large applications

### Q7: How do you handle async operations in Redux?

**Answer:**

**Use middleware** like redux_thunk for async operations.

```dart
// Async action
ThunkAction<AppState> loadData() {
  return (Store<AppState> store) async {
    final data = await api.getData();
    store.dispatch(DataLoadedAction(data));
  };
}
```

### Q8: How do you test Redux reducers?

**Answer:**

**Test reducers** as pure functions.

```dart
test('increment increases count', () {
  final state = AppState(count: 0);
  final newState = reducer(state, IncrementAction());
  expect(newState.count, 1);
});
```

### Q9: Explain Redux DevTools and time-travel debugging.

**Answer:**

**Redux DevTools** allows you to replay actions and see state at any point in time.

```dart
// Enable DevTools
final store = Store<AppState>(
  reducer,
  initialState: AppState(count: 0),
  middleware: [redux_logging],
);
```

---

## Navigation

**Previous:** [GetX](state-management-getx.md)

**Next:** [MobX](state-management-mobx.md)

