# Navigation

## Table of Contents
- [Navigator 1.0 vs Navigator 2.0](#navigator-10-vs-navigator-20)
- [GoRouter](#gorouter)
- [Deep Linking](#deep-linking)
- [Named Routes](#named-routes)
- [Passing Data Between Screens](#passing-data-between-screens)
- [Interview Questions & Answers](#interview-questions--answers)

## Navigator 1.0 vs Navigator 2.0

**Navigator 1.0 - Imperative Navigation:**

```dart
// Simple navigation
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => NextScreen()),
);

// Named routes
Navigator.pushNamed(context, '/details');
```

**Navigator 2.0 - Declarative Navigation:**

```dart
// Declarative navigation with Router
class MyRouterDelegate extends RouterDelegate<RouteInformation>
    with ChangeNotifier, PopNavigatorRouterDelegateMixin<RouteInformation> {
  @override
  Widget build(BuildContext context) {
    return Navigator(
      pages: [
        MaterialPage(child: HomeScreen()),
        if (showDetails)
          MaterialPage(child: DetailsScreen()),
      ],
      onPopPage: (route, result) {
        if (!route.didPop(result)) return false;
        showDetails = false;
        notifyListeners();
        return true;
      },
    );
  }
}
```

## GoRouter

**Modern Navigation Solution:**

```dart
import 'package:go_router/go_router.dart';

final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => HomeScreen(),
    ),
    GoRoute(
      path: '/details/:id',
      builder: (context, state) {
        final id = state.pathParameters['id']!;
        return DetailsScreen(id: id);
      },
    ),
  ],
);

// Usage:
context.go('/details/123');
```

## Deep Linking

**Handling Deep Links:**

```dart
// Configure deep links
final router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/product/:id',
      builder: (context, state) {
        final id = state.pathParameters['id']!;
        return ProductScreen(id: id);
      },
    ),
  ],
);
```

## Named Routes

**Using Named Routes:**

```dart
MaterialApp(
  routes: {
    '/': (context) => HomeScreen(),
    '/details': (context) => DetailsScreen(),
  },
);

// Navigate:
Navigator.pushNamed(context, '/details');
```

## Passing Data Between Screens

**Methods to Pass Data:**

```dart
// Method 1: Constructor
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (context) => DetailsScreen(data: myData),
  ),
);

// Method 2: Arguments
Navigator.pushNamed(
  context,
  '/details',
  arguments: myData,
);

// Method 3: Route parameters (GoRouter)
context.go('/details/$id');
```

## Interview Questions & Answers

### Q1: Explain Navigator 1.0 vs Navigator 2.0.

**Answer:**

**Navigator 1.0** uses an imperative, stack-based approach where you explicitly push and pop routes using methods like `Navigator.push()` and `Navigator.pop()`. It's simpler to use and works well for basic navigation needs, but it doesn't provide deep linking support or URL-based routing. Navigator 1.0 maintains a stack of routes and you manipulate this stack directly through method calls.

**Navigator 2.0** uses a declarative, URL-based approach where you describe your app's navigation state and Flutter builds the route stack accordingly. It provides better support for deep linking, web URLs, and complex navigation scenarios. Navigator 2.0 requires more setup with RouterDelegate and RouteInformationParser, but offers more control and better integration with web platforms and deep linking.

### Q2: How does GoRouter work?

**Answer:**

**GoRouter** is a declarative routing package built on top of Navigator 2.0 that simplifies URL-based navigation and deep linking. It allows you to define routes with paths, parameters, and query strings, making it easy to handle web URLs and deep links. GoRouter automatically manages the navigation stack based on the current route, provides navigation guards for authentication checks, and supports nested routing. It's particularly useful for apps that need to work on web platforms or require complex navigation scenarios with deep linking support.

### Q3: How do you handle deep linking in Flutter?

**Answer:**

To handle deep linking in Flutter, you can use **GoRouter** which provides built-in support for parsing URLs and routing to appropriate screens based on the URL path and parameters. Alternatively, you can use **Navigator 2.0** with RouterDelegate and RouteInformationParser to manually parse incoming URLs and build the appropriate route stack. Both approaches require configuring URL handling in your app's platform-specific code (AndroidManifest.xml for Android, Info.plist for iOS) to register your app as a handler for specific URL schemes. Deep linking allows users to navigate directly to specific content within your app from external sources like web links, notifications, or other apps.

### Q4: Explain named routes vs anonymous routes.

**Answer:**

**Named routes** are predefined routes registered with the MaterialApp or CupertinoApp using a routes map, where each route has a name (like '/home' or '/details') that you can use to navigate. They're useful when you have a fixed set of screens and want type-safe navigation with compile-time route checking. Named routes make navigation code more readable and maintainable, especially in larger apps with many screens.

**Anonymous routes** are created on-the-fly using `MaterialPageRoute` or `CupertinoPageRoute` without pre-registration. They're useful when you need to pass complex data to a screen, create routes dynamically based on runtime conditions, or navigate to screens that aren't part of your main navigation structure. Anonymous routes offer more flexibility but don't provide the same level of organization and type safety as named routes.

### Q5: How do you pass data between screens?

**Answer:**

There are several ways to pass data between screens in Flutter. **Constructor parameters** are the most straightforward approach - you pass data directly when creating the destination screen widget, which provides type safety and compile-time checking. **Route arguments** allow you to pass data through the Navigator using the `arguments` parameter, which is useful with named routes but requires type casting. **Route parameters** (with GoRouter or Navigator 2.0) allow you to pass data through URL parameters, making it ideal for deep linking scenarios. Additionally, you can use state management solutions like Provider or BLoC to share data across screens without explicitly passing it through navigation.

### Q6: Explain navigation guards and middleware.

**Answer:**

**Navigation guards** (also called route guards or navigation middleware) are mechanisms that intercept navigation attempts and check certain conditions before allowing navigation to proceed. They're commonly used to protect routes that require authentication, verify user permissions, or validate navigation prerequisites. For example, a navigation guard might check if a user is logged in before allowing access to a profile screen, redirecting to a login screen if authentication is required. GoRouter provides `redirect` callbacks that act as navigation guards, while Navigator 2.0 requires manual implementation in RouterDelegate. Navigation guards help maintain app security and ensure users can only access screens they're authorized to view.

### Q7: How do you handle nested navigation?

**Answer:**

To handle nested navigation in Flutter, you can use **nested routers** with GoRouter which allows you to define child routes within parent routes, creating a hierarchical navigation structure. Alternatively, you can use **nested Navigator widgets** where you place a Navigator widget inside a screen, allowing that screen to manage its own navigation stack independently. This is commonly used in scenarios like bottom navigation bars where each tab has its own navigation stack, or in master-detail layouts where the detail section has its own navigation. Nested navigation allows different parts of your app to maintain their own navigation state independently.

### Q8: What are the best practices for navigation in Flutter?

**Answer:**

**Best Practices for Navigation:**
- **Use GoRouter for modern apps** that need URL support, deep linking, or web compatibility, as it simplifies complex navigation scenarios and provides better developer experience than Navigator 2.0.
- **Handle deep links properly** by configuring URL schemes in platform-specific files and ensuring your routing logic can parse and handle incoming URLs correctly.
- **Pass data explicitly** through constructor parameters when possible for type safety, or use route arguments/parameters when necessary, avoiding global state for navigation data.
- **Use named routes for clarity** in apps with a fixed navigation structure, as they make navigation code more readable and maintainable.
- **Handle back button properly** by implementing `WillPopScope` or `PopScope` when you need to intercept back navigation, such as showing confirmation dialogs or preventing navigation in certain states.
- **Implement navigation guards** to protect routes that require authentication or specific permissions, ensuring users can only access authorized screens.

---

## Navigation

**Previous:** [Widgets & Layouts](widgets-and-layouts.md)

**Next:** [Networking](networking.md)

