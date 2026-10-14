# Testing

## Table of Contents
- [Types of Tests](#types-of-tests)
- [Unit Tests](#unit-tests)
- [Widget Tests](#widget-tests)
- [Integration Tests](#integration-tests)
- [Mocking](#mocking)
- [Interview Questions & Answers](#interview-questions--answers)

## Types of Tests

**Unit Tests:**
- Test individual functions/classes
- Fast, isolated
- No UI involved

**Widget Tests:**
- Test individual widgets
- Render widgets in test environment
- Check widget behavior

**Integration Tests:**
- Test entire app flow
- Real device/emulator
- End-to-end testing

## Unit Tests

**Writing Unit Tests:**

```dart
void main() {
  group('Counter tests', () {
    test('increment increases count', () {
      final counter = Counter();
      expect(counter.count, 0);
      
      counter.increment();
      expect(counter.count, 1);
    });
    
    test('decrement decreases count', () {
      final counter = Counter();
      counter.increment();
      counter.decrement();
      
      expect(counter.count, 0);
    });
  });
}
```

## Widget Tests

**Testing Widgets:**

```dart
void main() {
  testWidgets('Counter widget test', (WidgetTester tester) async {
    await tester.pumpWidget(CounterWidget());
    
    expect(find.text('0'), findsOneWidget);
    
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();
    
    expect(find.text('1'), findsOneWidget);
  });
}
```

## Integration Tests

**Integration Testing:**

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  
  testWidgets('Login flow', (WidgetTester tester) async {
    await tester.pumpWidget(MyApp());
    
    await tester.enterText(find.byKey(Key('email')), 'test@example.com');
    await tester.enterText(find.byKey(Key('password')), 'password');
    await tester.tap(find.byKey(Key('login')));
    await tester.pumpAndSettle();
    
    expect(find.text('Home'), findsOneWidget);
  });
}
```

## Mocking

**Using Mocks:**

```dart
class MockApiService extends Mock implements ApiService {}

void main() {
  test('user repository test', () {
    final mockApi = MockApiService();
    when(mockApi.getUser()).thenAnswer((_) async => User(id: '1'));
    
    final repo = UserRepository(mockApi);
    final user = await repo.getUser();
    
    expect(user.id, '1');
    verify(mockApi.getUser()).called(1);
  });
}
```

## Interview Questions & Answers

### Q1: What are unit, widget, and integration tests?

**Answer:**

**Unit tests** test individual functions, methods, or classes in isolation without any UI or external dependencies. They're fast, run frequently during development, and help ensure that your business logic works correctly. Unit tests typically use mocks to isolate the code being tested from dependencies like databases, network calls, or file systems. They're the foundation of a good test suite and should cover the majority of your code.

**Widget tests** (also called component tests) test individual widgets in isolation by rendering them in a test environment. They verify that widgets display correctly, handle user interactions properly, and update their UI based on state changes. Widget tests are faster than integration tests but slower than unit tests, and they help ensure your UI components work as expected without running the entire app.

**Integration tests** (also called end-to-end tests) test the entire app flow by running the app on a real device or emulator and simulating user interactions. They verify that different parts of your app work together correctly, including navigation, state management, and integration with external services. Integration tests are slower and more complex but provide confidence that your app works as a whole.

### Q2: How do you test StatefulWidget?

**Answer:**

To test StatefulWidget, use **testWidgets** from the Flutter test package, which provides a `WidgetTester` that can render widgets and simulate user interactions. Use `tester.pumpWidget()` to render your StatefulWidget, then use `tester.find()` to locate widgets in the widget tree and `tester.tap()`, `tester.enterText()`, or other interaction methods to simulate user actions. After interactions, call `tester.pump()` or `tester.pumpAndSettle()` to trigger rebuilds and verify the widget's state changes correctly. You can access the widget's state using `tester.state()` to verify internal state values. Test that the widget initializes correctly, responds to user interactions, updates its state properly, and handles edge cases.

### Q3: How do you test state management (Provider, BLoC, etc.)?

**Answer:**

To test state management solutions, you can **test providers/BLoCs directly** by instantiating them and calling their methods, then verifying that state changes correctly. For **Provider**, create a ChangeNotifier instance, call its methods, and verify that state updates and `notifyListeners()` is called. For **BLoC**, use the `blocTest` utility from `bloc_test` package which provides a convenient way to test BLoCs by sending events and verifying emitted states. For **Riverpod**, use `ProviderContainer` to create an isolated test environment. Most state management packages provide test utilities that make testing easier - use `ProviderTester` for Provider, `blocTest` for BLoC, or `ProviderContainer` for Riverpod. Test that state initializes correctly, state changes when methods are called, and error states are handled properly.

### Q4: Explain mocking in Flutter tests.

**Answer:**

**Mocking** in Flutter tests involves creating fake implementations of dependencies (like API services, databases, or repositories) that you can control during testing. Use mock packages like **mockito** or **mocktail** to generate mock classes from your interfaces or classes. Mocks allow you to define what methods return when called (using `when().thenReturn()`), verify that methods were called with correct parameters (using `verify()`), and simulate different scenarios like success responses, errors, or edge cases. Mocking is essential for unit tests because it isolates the code being tested from external dependencies, making tests fast, reliable, and independent. For example, you might mock an API service to return specific data without making actual network calls, allowing you to test your code's behavior with different API responses.

### Q5: How do you test async operations?

**Answer:**

To test async operations, use **await** in your test functions to wait for Futures to complete, ensuring that async operations finish before assertions are made. For widget tests with async operations, use **`tester.pumpAndSettle()`** which repeatedly calls `pump()` until all animations and async operations complete, or use `tester.pump()` with a duration to advance time for testing time-based operations. For unit tests, simply await the async function and then make assertions. Use `Future.value()` or `Future.error()` to create test futures, and `Completer` for more complex async scenarios. Be careful with timeouts in tests - use `fakeAsync` from the test package to control time in tests, or increase timeout duration for slow operations. Always ensure that async operations complete before your test finishes.

### Q6: What are the best practices for testing in Flutter?

**Answer:**

**Best Practices for Testing:**
- **Write tests for critical logic** including business logic, state management, and user-facing features that are important for app functionality.
- **Use mocks for external dependencies** like API calls, databases, or file systems to isolate code being tested and make tests fast and reliable.
- **Test edge cases** including error scenarios, boundary conditions, empty states, and invalid inputs to ensure your app handles all situations gracefully.
- **Maintain high coverage** by aiming for at least 80% code coverage, focusing on critical paths and business logic rather than just achieving a number.
- **Keep tests fast and isolated** by avoiding real network calls, database operations, or file I/O, and ensuring tests don't depend on each other or external state.
- **Use descriptive test names** that clearly explain what is being tested and what the expected outcome is.
- **Follow the AAA pattern** (Arrange, Act, Assert) to structure tests clearly: set up test data, perform the action, verify the result.
- **Test user interactions** in widget tests to ensure your UI responds correctly to taps, text input, and other user actions.

### Q7: How do you achieve high test coverage?

**Answer:**

To achieve high test coverage, **write comprehensive tests** that cover all code paths including happy paths, error cases, edge cases, and boundary conditions. Use **coverage tools** like `flutter test --coverage` to generate coverage reports that show which lines of code are executed during tests, helping you identify untested code. Focus on testing critical business logic, state management, and user-facing features first, then expand to less critical code. Use code coverage as a guide but not the only metric - aim for meaningful tests that verify correctness rather than just hitting coverage numbers. Regularly review coverage reports to identify gaps and add tests for uncovered code. Remember that 100% coverage doesn't guarantee bug-free code, but high coverage with good tests significantly reduces the likelihood of bugs.

---

## Navigation

**Previous:** [Dependency Injection](dependency-injection.md)

**Next:** [Performance](performance.md)

