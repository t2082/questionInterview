# Networking

## Table of Contents
- [HTTP Package vs Dio](#http-package-vs-dio)
- [API Error Handling](#api-error-handling)
- [Interceptors](#interceptors)
- [Retry Logic](#retry-logic)
- [Authentication](#authentication)
- [Interview Questions & Answers](#interview-questions--answers)

## HTTP Package vs Dio

**HTTP Package - Simple HTTP Client:**

```dart
import 'package:http/http.dart' as http;

Future<void> fetchData() async {
  final response = await http.get(
    Uri.parse('https://api.example.com/data'),
  );
  
  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    // Use data
  }
}
```

**Dio - Advanced HTTP Client:**

```dart
import 'package:dio/dio.dart';

final dio = Dio();

Future<void> fetchData() async {
  try {
    final response = await dio.get('https://api.example.com/data');
    final data = response.data;
    // Use data
  } on DioException catch (e) {
    // Handle error
  }
}
```

## API Error Handling

**Proper Error Handling:**

```dart
Future<Result<User>> fetchUser(String id) async {
  try {
    final response = await dio.get('/users/$id');
    return Result.success(User.fromJson(response.data));
  } on DioException catch (e) {
    if (e.response?.statusCode == 404) {
      return Result.error('User not found');
    } else if (e.response?.statusCode == 500) {
      return Result.error('Server error');
    }
    return Result.error('Network error');
  }
}
```

## Interceptors

**Using Interceptors:**

```dart
dio.interceptors.add(
  InterceptorsWrapper(
    onRequest: (options, handler) {
      // Add auth token
      options.headers['Authorization'] = 'Bearer $token';
      return handler.next(options);
    },
    onResponse: (response, handler) {
      // Handle response
      return handler.next(response);
    },
    onError: (error, handler) {
      // Handle error
      return handler.next(error);
    },
  ),
);
```

## Retry Logic

**Implementing Retry:**

```dart
Future<T> fetchWithRetry<T>(
  Future<T> Function() fetch, {
  int maxRetries = 3,
}) async {
  for (int i = 0; i < maxRetries; i++) {
    try {
      return await fetch();
    } catch (e) {
      if (i == maxRetries - 1) rethrow;
      await Future.delayed(Duration(seconds: i + 1));
    }
  }
  throw Exception('Max retries exceeded');
}
```

## Authentication

**Handling Auth Tokens:**

```dart
class AuthInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    final token = getAuthToken();
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }
  
  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (err.response?.statusCode == 401) {
      // Refresh token and retry
      refreshToken().then((_) {
        return handler.resolve(err.requestOptions);
      });
    } else {
      handler.next(err);
    }
  }
}
```

## Interview Questions & Answers

### Q1: Compare HTTP package vs Dio.

**Answer:**

**HTTP package** is a simple, lightweight HTTP client that provides basic functionality for making HTTP requests. It's maintained by the Dart team and is perfect for straightforward API calls without complex requirements. However, it lacks advanced features like interceptors, request/response transformers, and comprehensive error handling, making it less suitable for complex networking scenarios.

**Dio** is a powerful HTTP client that provides advanced features including interceptors for request/response modification, automatic request/response transformation, comprehensive error handling with DioException, request cancellation, timeout configuration, and support for file uploads with progress tracking. Dio is ideal for production apps that need robust networking capabilities, authentication handling, logging, and retry logic. While it's more complex than the HTTP package, it significantly reduces boilerplate code for common networking tasks.

### Q2: How do you handle API errors in Flutter?

**Answer:**

To handle API errors effectively, use **try-catch blocks** to catch exceptions and check **HTTP status codes** (like 400 for bad requests, 401 for unauthorized, 404 for not found, 500 for server errors) to determine the type of error. Create custom error classes or use Result types to represent different error states (network errors, server errors, parsing errors) and handle them appropriately in your UI. With Dio, you can use `DioException` which provides detailed error information including response data, status codes, and error types. Always provide user-friendly error messages and implement retry logic for transient failures like network timeouts.

### Q3: Explain interceptors in Dio.

**Answer:**

**Interceptors** in Dio are middleware functions that can modify requests before they're sent, transform responses before they're returned, or handle errors globally. There are three types: **Request interceptors** (onRequest) allow you to add headers, modify request data, or add authentication tokens to every request. **Response interceptors** (onResponse) let you transform response data, handle successful responses, or perform logging. **Error interceptors** (onError) provide centralized error handling, allowing you to retry failed requests, refresh tokens, or log errors. Interceptors help you implement cross-cutting concerns like authentication, logging, and error handling without duplicating code in every API call.

### Q4: How do you implement retry logic?

**Answer:**

To implement retry logic, you can use **loops with exponential backoff delays** where you retry a request multiple times with increasing delays between attempts (e.g., 1 second, 2 seconds, 4 seconds). Alternatively, you can use **Dio's retry interceptor** (like `dio_retry` package) which automatically retries failed requests based on configurable conditions such as specific error types, maximum retry count, and retry delays. Retry logic should only retry transient failures (network timeouts, 5xx server errors) and not permanent failures (4xx client errors like 401 unauthorized). Always set a maximum retry limit to prevent infinite retry loops and provide user feedback about retry attempts.

### Q5: How do you handle authentication tokens?

**Answer:**

To handle authentication tokens, use **Dio interceptors** to automatically add tokens to request headers (typically in the Authorization header as "Bearer {token}") for every API call. Implement token refresh logic in the error interceptor that detects 401 (Unauthorized) responses, automatically refreshes the token using a refresh token, and retries the original request with the new token. Store tokens securely using packages like `flutter_secure_storage` or `shared_preferences` with encryption. The interceptor approach centralizes authentication logic, ensuring all requests are properly authenticated without duplicating code across your app.

### Q6: Explain caching strategies for network requests.

**Answer:**

Caching strategies help reduce network calls and improve app performance by storing API responses locally. You can use packages like **dio_cache_interceptor** which provides HTTP caching with configurable cache policies (cache-first, network-first, cache-only, network-only) and automatic cache invalidation. Alternatively, implement **custom caching** using packages like `hive` or `shared_preferences` to store responses with expiration times and cache keys. Common strategies include: **Cache-First** (check cache, use if available, otherwise fetch from network), **Network-First** (fetch from network, fall back to cache if network fails), and **Stale-While-Revalidate** (return cached data immediately while fetching fresh data in background). Always implement cache expiration and invalidation to ensure data freshness.

### Q7: How do you handle file uploads with progress?

**Answer:**

To handle file uploads with progress tracking, use **Dio's FormData** to create multipart/form-data requests that can include files along with other form fields. Use the **onSendProgress callback** in Dio's request options to receive progress updates (bytes sent and total bytes) which you can use to update a progress indicator in your UI. The callback provides both the number of bytes sent and the total bytes, allowing you to calculate and display upload percentage. For large files, consider implementing chunked uploads or resumable uploads. Always handle upload errors gracefully and provide user feedback about upload status.

### Q8: What are the best practices for networking in Flutter?

**Answer:**

**Best Practices for Networking:**
- **Use Dio for complex needs** like authentication, interceptors, and advanced error handling, while HTTP package is sufficient for simple API calls.
- **Handle errors properly** by creating custom error classes, checking status codes, and providing user-friendly error messages with appropriate error states in your UI.
- **Use interceptors for common logic** like adding authentication headers, logging requests/responses, and centralized error handling to avoid code duplication.
- **Implement retry logic** for transient failures with exponential backoff, but avoid retrying permanent failures like 4xx client errors.
- **Cache responses when appropriate** using cache-first or network-first strategies to reduce network calls and improve performance, especially for data that doesn't change frequently.
- **Handle authentication properly** by automatically adding tokens to requests, refreshing expired tokens, and securely storing credentials.
- **Implement timeout configuration** to prevent requests from hanging indefinitely and provide better user experience.
- **Use proper data models** with JSON serialization/deserialization for type-safe API responses.

---

## Navigation

**Previous:** [Navigation](navigation.md)

**Next:** [Data Persistence](data-persistence.md)

