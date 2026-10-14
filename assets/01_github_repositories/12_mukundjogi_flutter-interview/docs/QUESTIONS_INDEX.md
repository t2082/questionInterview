# Questions Index

Complete index of all interview questions across topics.

## Topics

- [Introduction](#introduction-7-questions)
- [Flutter Basics](#flutter-basics-10-questions)
- [Dart Programming](#dart-programming-10-questions)
- [State Management Overview](#state-management-overview-7-questions)
- [setState()](#setstate-8-questions)
- [Provider](#provider-10-questions)
- [Riverpod](#riverpod-10-questions)
- [BLoC](#bloc-10-questions)
- [GetX](#getx-9-questions)
- [Redux](#redux-9-questions)
- [MobX](#mobx-8-questions)
- [State Management Comparison](#state-management-comparison-12-questions)
- [Widgets & Layouts](#widgets--layouts-9-questions)
- [Navigation](#navigation-8-questions)
- [Networking](#networking-8-questions)
- [Data Persistence](#data-persistence-8-questions)
- [Dependency Injection](#dependency-injection-7-questions)
- [Testing](#testing-7-questions)
- [Performance](#performance-7-questions)
- [Animations](#animations-7-questions)
- [Platform Channels](#platform-channels-7-questions)
- [Publishing](#publishing-9-questions)
- [Architecture Patterns](#architecture-patterns-8-questions)
- [Advanced Topics](#advanced-topics-7-questions)

## Introduction (7 Questions)

1. How should I approach a Flutter interview?
2. What topics are most frequently asked in Flutter interviews?
3. How long does interview preparation take?
4. What should I focus on: theory or practice?
5. How do I handle questions I don't know?
6. Should I only prepare for Flutter-specific topics?
7. What projects should I build for my portfolio?

## Flutter Basics (10 Questions)

1. What is Flutter and how does it work?
2. Explain the difference between StatelessWidget and StatefulWidget.
3. What is BuildContext and why is it important?
4. Explain the widget lifecycle in Flutter.
5. What is the difference between Hot Reload and Hot Restart?
6. What does the build() method do?
7. How does Flutter render widgets?
8. What is a widget tree?
9. Explain setState() in detail.
10. What is the difference between const and final in Flutter?

## Dart Programming (10 Questions)

1. Explain null safety in Dart with examples.
2. What is the difference between async and await?
3. Explain Streams in Dart.
4. What are generics and why use them?
5. Explain mixins in Dart.
6. What are extension methods?
7. Explain Future vs Stream.
8. What is the difference between const and final?
9. Explain the cascade operator (..).
10. What are named parameters vs positional parameters?

## State Management Overview (7 Questions)

1. What is state management and why is it important?
2. When should I use setState() vs a state management solution?
3. Compare Provider vs Riverpod.
4. When would you choose BLoC over Provider?
5. Explain the concept of "single source of truth" in state management.
6. What are the main state management approaches in Flutter?
7. How do you decide which state management to use for a project?

## setState() (8 Questions)

1. What is setState() and how does it work?
2. When should you use setState() vs a state management solution?
3. What happens if you forget to call setState()?
4. Can you call setState() in build() method?
5. How do you handle async operations with setState()?
6. What is the difference between setState() and notifyListeners()?
7. Explain the widget rebuild process with setState().
8. When would you move away from setState() to a state management solution?

## Provider (10 Questions)

1. What is Provider and how does it work?
2. What is the difference between Provider.of() and Consumer?
3. When should you use listen: false?
4. Explain ChangeNotifier in Provider.
5. How do you handle multiple providers?
6. What is the difference between Provider and ChangeNotifierProvider?
7. How do you test Provider?
8. Explain Selector in Provider.
9. What are the limitations of Provider?
10. How do you handle async operations in Provider?

## Riverpod (10 Questions)

1. What is Riverpod and how does it differ from Provider?
2. Explain StateProvider vs StateNotifierProvider.
3. What is the difference between ref.watch() and ref.read()?
4. How do you create computed providers in Riverpod?
5. Explain ProviderScope in Riverpod.
6. How do you handle async operations in Riverpod?
7. What are the advantages of Riverpod over Provider?
8. How do you test Riverpod providers?
9. Explain freezed with Riverpod.
10. When should you migrate from Provider to Riverpod?

## BLoC (10 Questions)

1. What is BLoC pattern and how does it work?
2. Explain Events, States, and BLoC in detail.
3. What is the difference between BLoC and Cubit?
4. How do you handle side effects in BLoC?
5. Explain Streams in the context of BLoC.
6. How do you test BLoC?
7. When should you use BLoC over other state management solutions?
8. Explain BLoC architecture with examples.
9. How do you handle errors in BLoC?
10. What are the best practices for using BLoC?

## GetX (9 Questions)

1. What is GetX and what are its main features?
2. Explain state management in GetX.
3. How does GetX differ from other state management solutions?
4. Explain GetX navigation.
5. How do you handle dependency injection in GetX?
6. What are the pros and cons of GetX?
7. When should you use GetX?
8. How do you test GetX controllers?
9. Explain GetX reactive programming.

## Redux (9 Questions)

1. What is Redux and how does it work in Flutter?
2. Explain Redux principles (Single Source of Truth, etc.).
3. What are Actions, Reducers, and Store in Redux?
4. How does Redux differ from other state management solutions?
5. Explain middleware in Redux.
6. When should you use Redux?
7. How do you handle async operations in Redux?
8. How do you test Redux reducers?
9. Explain Redux DevTools and time-travel debugging.

## MobX (8 Questions)

1. What is MobX and how does it work?
2. Explain Observable, Action, and Computed in MobX.
3. How does MobX differ from other state management solutions?
4. When should you use MobX?
5. How do you handle async operations in MobX?
6. How do you test MobX stores?
7. Explain MobX reactive programming.
8. What are the best practices for using MobX?

## State Management Comparison (12 Questions)

1. Compare setState() vs Provider vs Riverpod vs BLoC.
2. When should you use Provider vs Riverpod?
3. Compare BLoC vs GetX for state management.
4. Explain the trade-offs between different state management solutions.
5. How do you migrate from setState() to Provider?
6. How do you migrate from Provider to Riverpod?
7. Compare Redux vs BLoC for complex state management.
8. What are the performance implications of different state management solutions?
9. How do you choose the right state management for your project?
10. Explain the learning curve for each state management approach.
11. Compare boilerplate code in different state management solutions.
12. What are real-world examples of each state management approach?

## Widgets & Layouts (9 Questions)

1. Explain Row, Column, and Stack widgets.
2. What is the difference between Expanded and Flexible?
3. Explain Container vs SizedBox vs Padding.
4. How do you create custom widgets?
5. Explain widget composition in Flutter.
6. What are Material vs Cupertino widgets?
7. How do you handle responsive layouts?
8. Explain ConstrainedBox and UnconstrainedBox.
9. How do you optimize widget rebuilds?

## Navigation (8 Questions)

1. Explain Navigator 1.0 vs Navigator 2.0.
2. How does GoRouter work?
3. How do you handle deep linking in Flutter?
4. Explain named routes vs anonymous routes.
5. How do you pass data between screens?
6. Explain navigation guards and middleware.
7. How do you handle nested navigation?
8. What are the best practices for navigation in Flutter?

## Networking (8 Questions)

1. Compare HTTP package vs Dio.
2. How do you handle API errors in Flutter?
3. Explain interceptors in Dio.
4. How do you implement retry logic?
5. How do you handle authentication tokens?
6. Explain caching strategies for network requests.
7. How do you handle file uploads with progress?
8. What are the best practices for networking in Flutter?

## Data Persistence (8 Questions)

1. Compare SharedPreferences vs Hive vs SQLite.
2. How do you use Hive for local storage?
3. Explain Room database in Flutter (sqflite).
4. How do you handle database migrations?
5. How do you implement offline-first architecture?
6. Explain encryption for local storage.
7. How do you sync local and remote data?
8. What are the best practices for data persistence?

## Dependency Injection (7 Questions)

1. What is dependency injection and why is it important?
2. Compare GetIt vs Injectable vs Manual DI.
3. How do you implement dependency injection in Flutter?
4. Explain DI scopes (Singleton, Factory, etc.).
5. How do you test with dependency injection?
6. What are the best practices for DI in Flutter?
7. How do you handle DI in multi-module projects?

## Testing (7 Questions)

1. What are unit tests, widget tests, and integration tests?
2. How do you test StatefulWidget?
3. How do you test state management (Provider, BLoC, etc.)?
4. Explain mocking in Flutter tests.
5. How do you test async operations?
6. What are the best practices for testing in Flutter?
7. How do you achieve high test coverage?

## Performance (7 Questions)

1. How do you optimize Flutter app performance?
2. Explain build optimization techniques.
3. How do you optimize list rendering?
4. Explain image optimization in Flutter.
5. How do you profile Flutter apps?
6. How do you reduce app size?
7. What are common performance bottlenecks?

## Animations (7 Questions)

1. Explain implicit vs explicit animations.
2. How do you create custom animations?
3. Explain AnimationController and Tween.
4. How do you optimize animations for performance?
5. Explain Hero animations.
6. How do you create page transitions?
7. What are the best practices for animations?

## Platform Channels (7 Questions)

1. What are platform channels in Flutter?
2. Explain method channels vs event channels.
3. How do you call native code from Flutter?
4. How do you call Flutter from native code?
5. Explain platform-specific implementations.
6. How do you handle errors in platform channels?
7. What are the best practices for platform channels?

## Publishing (9 Questions)

1. How do you prepare an app for App Store publishing?
2. How do you prepare an app for Play Store publishing?
3. Explain app signing for iOS and Android.
4. How do you manage app versions?
5. Explain release tracks (internal, alpha, beta, production).
6. How do you handle app updates?
7. What are common app rejection reasons?
8. How do you optimize app store listings?
9. What are the best practices for app publishing?

## Architecture Patterns (8 Questions)

1. Explain Clean Architecture in Flutter.
2. What is MVVM pattern in Flutter?
3. Explain Repository pattern.
4. How do you implement SOLID principles in Flutter?
5. Explain multi-module architecture.
6. How do you structure a large Flutter project?
7. What are the best practices for Flutter architecture?
8. How do you handle error handling in architecture?

## Advanced Topics (7 Questions)

1. Explain Isolates in Flutter.
2. What are custom renderers?
3. Explain platform views in Flutter.
4. How do you implement custom paint?
5. What are compute functions?
6. How do you handle background processing?
7. Explain advanced Flutter concepts.

---

**Return to:** [Home](/)

