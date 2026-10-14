# Dependency Injection

## Table of Contents
- [What is Dependency Injection?](#what-is-dependency-injection)
- [GetIt vs Injectable vs Manual DI](#getit-vs-injectable-vs-manual-di)
- [Implementing DI](#implementing-di)
- [DI Scopes](#di-scopes)
- [Testing with DI](#testing-with-di)
- [Interview Questions & Answers](#interview-questions--answers)

## What is Dependency Injection?

**Simple Explanation:**

Dependency Injection is like ordering food at a restaurant. Instead of going to the kitchen yourself (creating dependencies), the waiter (DI system) brings you what you need.

**Simple Analogy:**

Think of DI like a vending machine:
- **Without DI**: You build the machine yourself
- **With DI**: The machine is already built, you just use it

## GetIt vs Injectable vs Manual DI

**GetIt - Service Locator:**

```dart
final getIt = GetIt.instance;

// Register
getIt.registerSingleton<ApiService>(ApiService());
getIt.registerFactory<UserRepository>(() => UserRepository(getIt()));

// Get
final api = getIt<ApiService>();
```

**Injectable - Code Generation:**

```dart
@injectable
class UserRepository {
  final ApiService api;
  UserRepository(this.api);
}

// Auto-generated code handles registration
```

**Manual DI - Constructor Injection:**

```dart
class UserRepository {
  final ApiService api;
  UserRepository(this.api); // Injected via constructor
}
```

## Implementing DI

**GetIt Example:**

```dart
// Setup
void setupDI() {
  getIt.registerSingleton<ApiService>(ApiService());
  getIt.registerFactory<UserRepository>(
    () => UserRepository(getIt<ApiService>()),
  );
}

// Usage
class MyWidget extends StatelessWidget {
  final userRepo = getIt<UserRepository>();
  
  @override
  Widget build(BuildContext context) {
    return Container();
  }
}
```

## DI Scopes

**Understanding Scopes:**

```dart
// Singleton - one instance for entire app
getIt.registerSingleton<ApiService>(ApiService());

// Factory - new instance each time
getIt.registerFactory<UserRepository>(() => UserRepository());

// Lazy Singleton - created when first accessed
getIt.registerLazySingleton<Database>(() => Database());
```

## Testing with DI

**Testing with DI:**

```dart
// Register mock in tests
getIt.registerSingleton<ApiService>(MockApiService());

// Test
test('user repository test', () {
  final repo = getIt<UserRepository>();
  // Test with mock
});
```

## Interview Questions & Answers

### Q1: What is dependency injection and why is it important?

**Answer:**

**Dependency Injection (DI)** is a design pattern where dependencies (objects that a class needs) are provided to the class from outside rather than the class creating them internally. Instead of a class instantiating its own dependencies (which creates tight coupling), dependencies are "injected" through constructors, setters, or DI frameworks. DI is important because it makes code **testable** - you can easily replace real dependencies with mocks in tests. It makes code **maintainable** - changes to dependencies don't require modifying classes that use them. It promotes **loose coupling** - classes depend on abstractions (interfaces) rather than concrete implementations, making the code more flexible and easier to modify.

### Q2: Compare GetIt vs Injectable vs Manual DI.

**Answer:**

**GetIt** is a service locator pattern where you manually register dependencies using methods like `registerSingleton()`, `registerFactory()`, or `registerLazySingleton()`, and retrieve them using `getIt<Type>()`. It provides flexibility in registration and supports different lifecycle scopes, but requires manual setup and can lead to runtime errors if dependencies aren't registered. GetIt is popular in Flutter for its simplicity and performance.

**Injectable** uses code generation (via build_runner) to automatically generate dependency registration code based on annotations like `@injectable` and `@module`. It reduces boilerplate and provides compile-time safety, but requires running code generation and has a learning curve. Injectable is ideal for larger projects where automatic DI setup saves significant time.

**Manual DI** (constructor injection) involves passing dependencies directly through constructors without any DI framework. It's the simplest approach with no dependencies, provides compile-time safety, and is easy to understand. However, it can become verbose in large apps and requires manually wiring dependencies throughout your app. Manual DI is perfect for small projects or when you want to avoid external dependencies.

### Q3: How do you implement dependency injection in Flutter?

**Answer:**

To implement dependency injection in Flutter, you can use **GetIt** by creating a setup function that registers all dependencies (like `getIt.registerSingleton<ApiService>(ApiService())`) and calling it during app initialization. Alternatively, use **Injectable** by annotating classes with `@injectable` and running code generation to automatically create the registration code. For **manual constructor injection**, simply pass dependencies through constructors when creating objects. With GetIt or Injectable, you typically create a setup function that registers all dependencies in one place, then use `getIt<Type>()` or constructor injection to retrieve dependencies throughout your app. The key is to register dependencies before they're needed and use the same instance (singleton) or create new instances (factory) based on your requirements.

### Q4: Explain DI scopes (Singleton, Factory, etc.).

**Answer:**

**Singleton** scope creates one instance of a dependency that is shared across the entire app lifetime. Once created, the same instance is returned every time the dependency is requested. Singletons are ideal for services that maintain state, hold configuration, or are expensive to create (like database connections, API clients, or repositories). They help conserve memory and ensure consistent state across your app.

**Factory** scope creates a new instance of the dependency every time it's requested. Each call to get the dependency returns a fresh instance. Factories are ideal for objects that should be independent, don't maintain shared state, or need to be recreated for each use (like ViewModels, Controllers, or data models). They ensure that each consumer gets its own isolated instance.

**Lazy Singleton** scope creates a singleton instance, but only when it's first accessed (lazy initialization). The instance is then cached and reused for subsequent requests. Lazy singletons are useful when you want singleton behavior but don't want to create the instance during app startup, deferring creation until it's actually needed. This can improve app startup time.

### Q5: How do you test with dependency injection?

**Answer:**

To test with dependency injection, **register mock implementations** in your test setup instead of real dependencies. Before running tests, reset your DI container and register mock versions of dependencies (using packages like `mockito` or `mocktail` to create mocks). This allows you to control the behavior of dependencies during tests, verify that methods are called with correct parameters, and test your code in isolation without relying on external services. For example, you might register a `MockApiService` instead of the real `ApiService`, allowing you to simulate different API responses and error scenarios. After tests complete, clean up by resetting the DI container. This approach makes unit testing much easier and faster since you don't need real network calls, database connections, or other external dependencies.

### Q6: What are the best practices for DI in Flutter?

**Answer:**

**Best Practices for Dependency Injection:**
- **Use DI for testability** by injecting dependencies rather than creating them internally, making it easy to replace with mocks in tests.
- **Register dependencies in setup** by creating a centralized setup function that registers all dependencies in one place, making it easy to see and manage all dependencies.
- **Use appropriate scopes** - singletons for shared services, factories for independent instances, lazy singletons for deferred initialization.
- **Keep dependencies minimal** by only injecting what a class actually needs, avoiding over-injection which can make code harder to understand.
- **Document dependencies** by using clear naming and comments to explain why certain dependencies are needed and what they provide.
- **Depend on abstractions** (interfaces) rather than concrete classes to promote loose coupling and make it easier to swap implementations.
- **Initialize DI early** in your app's lifecycle (typically in `main()` or app initialization) to ensure dependencies are available when needed.

### Q7: How do you handle DI in multi-module projects?

**Answer:**

To handle DI in multi-module projects, **create separate DI modules** for each feature or module, where each module registers its own dependencies. Each module should have its own setup function (like `setupAuthModule()`, `setupHomeModule()`) that registers dependencies specific to that module. In your main app setup, call all module setup functions to combine them. This approach keeps dependencies organized by feature, makes it easy to see what each module depends on, and allows modules to be developed independently. You can also use module-specific DI containers or namespaces if your DI framework supports it. This modular approach scales well as your project grows and makes it easier to add, remove, or modify features without affecting other modules.

---

## Navigation

**Previous:** [Data Persistence](data-persistence.md)

**Next:** [Testing](testing.md)

