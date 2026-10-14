# BLoC - Business Logic Component Pattern

## Table of Contents
- [What is BLoC?](#what-is-bloc)
- [Why Use BLoC?](#why-use-bloc)
- [How Does BLoC Work?](#how-does-bloc-work)
- [Basic Example](#basic-example)
- [Intermediate Example](#intermediate-example)
- [Advanced Example](#advanced-example)
- [Best Practices](#best-practices)
- [Common Mistakes](#common-mistakes)
- [When to Use vs When Not to Use](#when-to-use-vs-when-not-to-use)
- [Comparison with Other Approaches](#comparison-with-other-approaches)
- [Interview Questions & Answers](#interview-questions--answers)

## What is BLoC?

**Simple Explanation:**

BLoC (Business Logic Component) is like a vending machine. You put in an event (like pressing a button), it processes it, and gives you a state (like dispensing a snack).

**Simple Analogy:**

Think of BLoC like a restaurant:
- **Events** = Customer orders (what you want to do)
- **BLoC** = The kitchen (processes the orders)
- **States** = The food served (the result)
- Everything flows in one direction: Events → BLoC → States

**Key Concepts:**

- **Events**: User actions or triggers (button press, data load)
- **States**: The current situation (loading, success, error)
- **BLoC**: Processes events and emits states
- **Stream**: Flow of states over time
- **Unidirectional Data Flow**: Events go in, states come out

## Why Use BLoC?

**Benefits:**

1. **Separation of Concerns**: Business logic separate from UI
2. **Testable**: Easy to test business logic
3. **Predictable**: Clear flow of data
4. **Reusable**: BLoC can be used in multiple widgets
5. **Scalable**: Works well for large apps

**When It's Perfect:**

- Complex business logic
- Large team projects
- Need strict separation of concerns
- Want predictable state management
- Need testable architecture

## How Does BLoC Work?

**The Mechanism:**

1. User action creates an Event
2. Event is added to BLoC
3. BLoC processes event and emits new State
4. Widget listens to state stream
5. Widget rebuilds with new state

**Simple Flow:**

```
User Action → Event → BLoC → State → Widget Rebuilds
```

## Basic Example

**Simple Counter with BLoC:**

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

// Step 1: Define Events
// Events are like commands - they tell BLoC what to do
// Think of them as buttons on a remote control
abstract class CounterEvent {}

// Increment event - tells BLoC to increase count
// Think of it as pressing the "+" button
class Increment extends CounterEvent {}

// Decrement event - tells BLoC to decrease count
// Think of it as pressing the "-" button
class Decrement extends CounterEvent {}

// Reset event - tells BLoC to reset count
// Think of it as pressing the "Reset" button
class Reset extends CounterEvent {}

// Step 2: Define States
// States represent the current situation
// Think of them as the current status of a machine
abstract class CounterState {
  // This is the count value
  // Think of it as the number displayed on a counter
  final int count;
  
  CounterState(this.count);
}

// Initial state - when counter starts
// Think of it as the counter showing 0
class CounterInitial extends CounterState {
  CounterInitial(int count) : super(count);
}

// Step 3: Create BLoC
// BLoC is like a machine that processes events and produces states
// Think of it as a vending machine: you put in an event, you get a state
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  // Constructor - sets initial state
  // Think of it as setting up the machine with starting value
  CounterBloc() : super(CounterInitial(0)) {
    // Register event handlers
    // on() tells BLoC: "When this event happens, do this"
    // Think of it as programming buttons on the machine
    
    // When Increment event comes, increase count
    on<Increment>((event, emit) {
      // emit() sends a new state
      // Think of it as displaying a new number on the counter
      emit(CounterInitial(state.count + 1));
    });
    
    // When Decrement event comes, decrease count
    on<Decrement>((event, emit) {
      emit(CounterInitial(state.count - 1));
    });
    
    // When Reset event comes, reset to 0
    on<Reset>((event, emit) {
      emit(CounterInitial(0));
    });
  }
}

// Step 4: Use BLoC in Widget
void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BLoC Counter',
      home: BlocProvider(
        // BlocProvider makes BLoC available to child widgets
        // Think of it as putting the machine where everyone can use it
        create: (context) => CounterBloc(),
        child: CounterScreen(),
      ),
    );
  }
}

// Counter screen that uses BLoC
class CounterScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // BlocBuilder listens to state changes and rebuilds
    // Think of it as watching the counter display
    return BlocBuilder<CounterBloc, CounterState>(
      builder: (context, state) {
        return Scaffold(
          appBar: AppBar(title: Text('BLoC Counter')),
          body: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Display the count from state
                // This automatically updates when state changes
                Text(
                  'Count: ${state.count}',
                  style: TextStyle(fontSize: 48),
                ),
                SizedBox(height: 20),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // Decrement button
                    ElevatedButton(
                      onPressed: () {
                        // Add event to BLoC
                        // Think of it as pressing a button on the machine
                        context.read<CounterBloc>().add(Decrement());
                      },
                      child: Text('-'),
                    ),
                    SizedBox(width: 20),
                    // Increment button
                    ElevatedButton(
                      onPressed: () {
                        // Add event to BLoC
                        context.read<CounterBloc>().add(Increment());
                      },
                      child: Text('+'),
                    ),
                  ],
                ),
                SizedBox(height: 20),
                // Reset button
                ElevatedButton(
                  onPressed: () {
                    context.read<CounterBloc>().add(Reset());
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
1. We define Events (Increment, Decrement, Reset) - these are user actions
2. We define States (CounterInitial with count) - these represent the current situation
3. We create CounterBloc that processes events and emits states
4. We wrap the app with BlocProvider to make BLoC available
5. We use BlocBuilder to listen to state changes and rebuild UI
6. When user presses button, we add an event to BLoC
7. BLoC processes event and emits new state
8. BlocBuilder rebuilds with new state

**Why This Works:**
- Clear separation: Events (what) → BLoC (how) → States (result)
- Unidirectional flow makes it predictable
- Easy to test: test events and states separately
- Reusable: same BLoC can be used in multiple widgets

## Intermediate Example

**User Authentication with BLoC:**

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

// User model
class User {
  final String id;
  final String name;
  final String email;
  
  User({required this.id, required this.name, required this.email});
}

// Events
abstract class AuthEvent {}

class LoginRequested extends AuthEvent {
  final String email;
  final String password;
  LoginRequested(this.email, this.password);
}

class LogoutRequested extends AuthEvent {}

// States
abstract class AuthState {}

class AuthInitial extends AuthState {}

class AuthLoading extends AuthState {}

class AuthAuthenticated extends AuthState {
  final User user;
  AuthAuthenticated(this.user);
}

class AuthUnauthenticated extends AuthState {}

class AuthError extends AuthState {
  final String message;
  AuthError(this.message);
}

// BLoC
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  AuthBloc() : super(AuthInitial()) {
    // Handle login
    on<LoginRequested>((event, emit) async {
      emit(AuthLoading()); // Show loading
      
      try {
        // Simulate API call
        await Future.delayed(Duration(seconds: 1));
        
        // For demo, accept any credentials
        final user = User(
          id: '1',
          name: 'John Doe',
          email: event.email,
        );
        
        emit(AuthAuthenticated(user)); // Success
      } catch (e) {
        emit(AuthError('Login failed: $e')); // Error
      }
    });
    
    // Handle logout
    on<LogoutRequested>((event, emit) {
      emit(AuthUnauthenticated());
    });
  }
}

// App setup
void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => AuthBloc(),
      child: MaterialApp(
        title: 'Auth App',
        home: AuthWrapper(),
      ),
    );
  }
}

// Auth wrapper
class AuthWrapper extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocBuilder<AuthBloc, AuthState>(
      builder: (context, state) {
        // Handle different states
        if (state is AuthLoading) {
          return Scaffold(
            body: Center(child: CircularProgressIndicator()),
          );
        } else if (state is AuthAuthenticated) {
          return HomeScreen(user: state.user);
        } else {
          return LoginScreen();
        }
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
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Login')),
      body: BlocListener<AuthBloc, AuthState>(
        // BlocListener listens to state changes but doesn't rebuild
        // Use it for side effects like navigation, showing dialogs
        listener: (context, state) {
          if (state is AuthError) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text(state.message)),
            );
          }
        },
        child: Padding(
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
              ElevatedButton(
                onPressed: () {
                  // Dispatch login event
                  context.read<AuthBloc>().add(
                    LoginRequested(
                      _emailController.text,
                      _passwordController.text,
                    ),
                  );
                },
                child: Text('Login'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// Home screen
class HomeScreen extends StatelessWidget {
  final User user;
  HomeScreen({required this.user});
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Home'),
        actions: [
          IconButton(
            icon: Icon(Icons.logout),
            onPressed: () {
              context.read<AuthBloc>().add(LogoutRequested());
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
1. We define AuthEvents (LoginRequested, LogoutRequested)
2. We define AuthStates (Initial, Loading, Authenticated, Unauthenticated, Error)
3. AuthBloc processes events and emits appropriate states
4. AuthWrapper uses BlocBuilder to show appropriate screen based on state
5. LoginScreen uses BlocListener to show errors
6. When login succeeds, state changes and UI updates automatically

**Why This Works:**
- Clear state management for authentication flow
- Easy to handle loading, success, and error states
- BlocListener handles side effects (snackbars, navigation)
- Testable: can test events and states separately

## Advanced Example

**Todo List with BLoC:**

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

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

// Events
abstract class TodoEvent {}

class LoadTodos extends TodoEvent {}

class AddTodo extends TodoEvent {
  final String title;
  AddTodo(this.title);
}

class ToggleTodo extends TodoEvent {
  final String id;
  ToggleTodo(this.id);
}

class DeleteTodo extends TodoEvent {
  final String id;
  DeleteTodo(this.id);
}

// States
abstract class TodoState {}

class TodoInitial extends TodoState {}

class TodoLoading extends TodoState {}

class TodoLoaded extends TodoState {
  final List<Todo> todos;
  TodoLoaded(this.todos);
}

class TodoError extends TodoState {
  final String message;
  TodoError(this.message);
}

// BLoC
class TodoBloc extends Bloc<TodoEvent, TodoState> {
  TodoBloc() : super(TodoInitial()) {
    on<LoadTodos>((event, emit) async {
      emit(TodoLoading());
      try {
        // Simulate loading todos
        await Future.delayed(Duration(seconds: 1));
        emit(TodoLoaded([]));
      } catch (e) {
        emit(TodoError('Failed to load todos'));
      }
    });
    
    on<AddTodo>((event, emit) {
      if (state is TodoLoaded) {
        final currentState = state as TodoLoaded;
        final newTodo = Todo(
          id: DateTime.now().millisecondsSinceEpoch.toString(),
          title: event.title,
        );
        emit(TodoLoaded([...currentState.todos, newTodo]));
      }
    });
    
    on<ToggleTodo>((event, emit) {
      if (state is TodoLoaded) {
        final currentState = state as TodoLoaded;
        final updatedTodos = currentState.todos.map((todo) {
          if (todo.id == event.id) {
            return todo.copyWith(isCompleted: !todo.isCompleted);
          }
          return todo;
        }).toList();
        emit(TodoLoaded(updatedTodos));
      }
    });
    
    on<DeleteTodo>((event, emit) {
      if (state is TodoLoaded) {
        final currentState = state as TodoLoaded;
        final updatedTodos = currentState.todos
            .where((todo) => todo.id != event.id)
            .toList();
        emit(TodoLoaded(updatedTodos));
      }
    });
  }
}
```

## Best Practices

1. **Use Sealed Classes for States**
```dart
sealed class AuthState {}
class AuthLoading extends AuthState {}
class AuthSuccess extends AuthState {}
```

2. **One BLoC per Feature**
```dart
// GOOD: Separate BLoCs
AuthBloc, TodoBloc, CartBloc

// BAD: One giant BLoC
AppBloc // Too complex!
```

3. **Use BlocListener for Side Effects**
```dart
BlocListener<AuthBloc, AuthState>(
  listener: (context, state) {
    if (state is AuthSuccess) {
      Navigator.push(...);
    }
  },
  child: ...,
)
```

4. **Use BlocBuilder for UI Updates**
```dart
BlocBuilder<CounterBloc, CounterState>(
  builder: (context, state) {
    return Text('${state.count}');
  },
)
```

5. **Test BLoCs Thoroughly**
```dart
test('increment increases count', () {
  final bloc = CounterBloc();
  bloc.add(Increment());
  expect(bloc.state.count, 1);
});
```

## Common Mistakes

1. **Emitting States Outside BLoC**
```dart
// BAD:
void increment() {
  bloc.emit(NewState()); // Don't do this!
}

// GOOD:
bloc.add(Increment()); // Let BLoC handle it
```

2. **Not Handling All States**
```dart
// BAD:
BlocBuilder<AuthBloc, AuthState>(
  builder: (context, state) {
    if (state is AuthSuccess) {
      return HomeScreen();
    }
    return LoginScreen(); // What about loading/error?
  },
)

// GOOD:
BlocBuilder<AuthBloc, AuthState>(
  builder: (context, state) {
    return state.when(
      loading: () => LoadingScreen(),
      success: (user) => HomeScreen(user),
      error: (message) => ErrorScreen(message),
      initial: () => LoginScreen(),
    );
  },
)
```

## When to Use vs When Not to Use

**Use BLoC when:**
- Complex business logic
- Large team projects
- Need strict separation
- Want testable architecture
- Need predictable flow

**Don't use BLoC when:**
- Simple apps
- Quick prototypes
- Team not familiar with BLoC
- Too much boilerplate for needs

## Comparison with Other Approaches

**BLoC vs Provider:**
- BLoC: More structured, better for complex logic
- Provider: Simpler, less boilerplate

**BLoC vs Riverpod:**
- BLoC: Pattern-based, more boilerplate
- Riverpod: Less boilerplate, compile-time safe

## Interview Questions & Answers

### Q1: What is BLoC pattern and how does it work?

**Answer:**

BLoC (Business Logic Component) is a pattern that separates business logic from UI using events and states.

**How it works:**
1. User actions create Events
2. Events are processed by BLoC
3. BLoC emits States
4. Widgets listen to states and rebuild

```dart
// Event → BLoC → State
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  CounterBloc() : super(CounterInitial(0)) {
    on<Increment>((event, emit) {
      emit(CounterInitial(state.count + 1));
    });
  }
}
```

### Q2: Explain Events, States, and BLoC in detail.

**Answer:**

**Events**: User actions or triggers
**States**: Current situation
**BLoC**: Processes events and emits states

```dart
// Events
class Increment extends CounterEvent {}

// States
class CounterInitial extends CounterState {
  final int count;
  CounterInitial(this.count);
}

// BLoC
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  on<Increment>((event, emit) {
    emit(CounterInitial(state.count + 1));
  });
}
```

### Q3: What is the difference between BLoC and Cubit?

**Answer:**

**BLoC**: Uses events and states
**Cubit**: Simpler, uses methods instead of events

```dart
// BLoC - uses events:
bloc.add(Increment());

// Cubit - uses methods:
cubit.increment();
```

### Q4: How do you handle side effects in BLoC?

**Answer:**

**Use BlocListener** for side effects like navigation, showing dialogs.

```dart
BlocListener<AuthBloc, AuthState>(
  listener: (context, state) {
    if (state is AuthSuccess) {
      Navigator.push(...);
    }
  },
  child: ...,
)
```

### Q5: Explain Streams in the context of BLoC.

**Answer:**

**BLoC uses Streams** to emit states over time. Widgets listen to the stream.

```dart
// BLoC emits states through stream
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  // States are emitted through stream
}

// Widget listens to stream
BlocBuilder<CounterBloc, CounterState>(
  builder: (context, state) {
    return Text('${state.count}');
  },
)
```

### Q6: How do you test BLoC?

**Answer:**

**Test events and states** separately.

```dart
test('increment increases count', () {
  final bloc = CounterBloc();
  expect(bloc.state.count, 0);
  
  bloc.add(Increment());
  expect(bloc.state.count, 1);
});
```

### Q7: When should you use BLoC over other state management solutions?

**Answer:**

**Use BLoC when:**
- Complex business logic
- Large team projects
- Need strict separation
- Want testable architecture

**Use others when:**
- Simple apps (Provider)
- Quick prototypes (setState)
- Want less boilerplate (GetX)

### Q8: Explain BLoC architecture with examples.

**Answer:**

**BLoC architecture:**
- UI Layer → Events → BLoC → States → UI Layer

```dart
// UI dispatches event
ElevatedButton(
  onPressed: () {
    bloc.add(Increment());
  },
)

// BLoC processes event
on<Increment>((event, emit) {
  emit(NewState());
});

// UI rebuilds with new state
BlocBuilder<CounterBloc, CounterState>(
  builder: (context, state) {
    return Text('${state.count}');
  },
)
```

### Q9: How do you handle errors in BLoC?

**Answer:**

**Create error states** and handle them in UI.

```dart
// Error state
class AuthError extends AuthState {
  final String message;
  AuthError(this.message);
}

// Handle in BLoC
on<LoginRequested>((event, emit) async {
  try {
    // Login logic
  } catch (e) {
    emit(AuthError(e.toString()));
  }
});

// Handle in UI
BlocBuilder<AuthBloc, AuthState>(
  builder: (context, state) {
    if (state is AuthError) {
      return ErrorWidget(state.message);
    }
  },
)
```

### Q10: What are the best practices for using BLoC?

**Answer:**

**Best Practices:**
1. One BLoC per feature
2. Use sealed classes for states
3. Use BlocListener for side effects
4. Use BlocBuilder for UI updates
5. Test thoroughly
6. Keep BLoCs focused and small

---

## Navigation

**Previous:** [Riverpod](state-management-riverpod.md)

**Next:** [GetX](state-management-getx.md)

