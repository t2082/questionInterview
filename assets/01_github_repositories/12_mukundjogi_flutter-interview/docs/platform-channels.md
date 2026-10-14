# Platform Channels

## Table of Contents
- [What are Platform Channels?](#what-are-platform-channels)
- [Method Channels](#method-channels)
- [Event Channels](#event-channels)
- [Native Code Integration](#native-code-integration)
- [Interview Questions & Answers](#interview-questions--answers)

## What are Platform Channels?

**Simple Explanation:**

Platform Channels are like a bridge between Flutter and native code. They let Flutter talk to iOS/Android code.

**Simple Analogy:**

Think of Platform Channels like a translator:
- **Flutter** = English speaker
- **Native Code** = Spanish speaker
- **Platform Channel** = Translator

## Method Channels

**Calling Native Code:**

```dart
// Flutter side
static const platform = MethodChannel('com.example/battery');

Future<int> getBatteryLevel() async {
  try {
    final result = await platform.invokeMethod('getBatteryLevel');
    return result as int;
  } on PlatformException catch (e) {
    print('Error: ${e.message}');
    return -1;
  }
}
```

**Native Side (Android):**

```kotlin
// MainActivity.kt
class MainActivity: FlutterActivity() {
    private val CHANNEL = "com.example/battery"
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        MethodChannel(flutterEngine!!.dartExecutor.binaryMessenger, CHANNEL)
            .setMethodCallHandler { call, result ->
                if (call.method == "getBatteryLevel") {
                    val batteryLevel = getBatteryLevel()
                    result.success(batteryLevel)
                } else {
                    result.notImplemented()
                }
            }
    }
}
```

## Event Channels

**Streaming Data from Native:**

```dart
// Flutter side
static const eventChannel = EventChannel('com.example/events');

Stream<int> getEvents() {
  return eventChannel.receiveBroadcastStream().map((event) => event as int);
}
```

## Native Code Integration

**Best Practices:**

```dart
// Error handling
try {
  final result = await platform.invokeMethod('method');
} on PlatformException catch (e) {
  // Handle error
}

// Type safety
final result = await platform.invokeMethod<int>('method');
```

## Interview Questions & Answers

### Q1: What are platform channels in Flutter?

**Answer:**

**Platform Channels** are a mechanism that enables bidirectional communication between Flutter (Dart) code and native platform code (Swift/Kotlin for iOS, Java/Kotlin for Android). They act as a bridge that allows Flutter apps to access platform-specific features that aren't available in Flutter's cross-platform APIs, such as device sensors, platform-specific UI components, or native libraries. Platform channels use message passing to send data between Flutter and native code, with type-safe serialization of basic data types. They're essential when you need to integrate with native SDKs, access platform-specific APIs, or implement features that require native code. Platform channels enable Flutter apps to leverage the full power of native platforms while maintaining a primarily Flutter codebase.

### Q2: Explain method channels vs event channels.

**Answer:**

**Method Channels** are used for one-time, request-response style communication between Flutter and native code. You invoke a method on the native side, wait for a result, and receive a response. Method channels are ideal for operations like getting device information, performing a calculation, or executing a single native operation. The communication is synchronous from Flutter's perspective (using async/await), but the native side can perform async operations. Method channels are the most common type of platform channel and are used for most platform integrations.

**Event Channels** are used for continuous, streaming data from native code to Flutter. They establish a persistent connection that allows native code to send multiple events over time, rather than just a single response. Event channels are ideal for scenarios like listening to sensor data, receiving location updates, monitoring battery level changes, or any situation where you need to receive ongoing updates from the native platform. Event channels use Dart Streams, allowing Flutter to listen to events as they occur, making them perfect for real-time data scenarios.

### Q3: How do you call native code from Flutter?

**Answer:**

To call native code from Flutter, create a **MethodChannel** with a unique channel name (like `'com.example/battery'`) that matches the name used in native code. Use `platform.invokeMethod('methodName', arguments)` to call a method on the native side, passing optional arguments as a Map. The method returns a Future that resolves with the result from native code. Wrap the call in a try-catch block to handle `PlatformException` which is thrown if the method isn't implemented or encounters an error. On the native side (Android/iOS), you register a method call handler that receives the method name and arguments, performs the operation, and returns a result. This allows Flutter to seamlessly call platform-specific functionality while maintaining type safety through the channel's serialization mechanism.

### Q4: How do you call Flutter from native code?

**Answer:**

To call Flutter from native code, use **MethodChannel** on the native side (Android/iOS) with the same channel name used in Flutter. On the native side, you can invoke methods on the Flutter side using the channel's `invokeMethod()` method, passing a method name and optional arguments. However, the more common pattern is for Flutter to set up method call handlers on the Flutter side that native code can invoke. Alternatively, use **Event Channels** or **BasicMessageChannel** for more complex communication patterns. For one-way communication from native to Flutter, Event Channels are typically preferred as they provide a streaming interface. The key is ensuring both sides use the same channel name and handle the communication protocol consistently, with proper error handling on both sides.

### Q5: Explain platform-specific implementations.

**Answer:**

Platform-specific implementations involve writing native code (Swift/Kotlin for iOS, Java/Kotlin for Android) to access features that aren't available through Flutter's cross-platform APIs. You use **platform channels** to bridge between Flutter and this native code, allowing your Flutter app to call platform-specific functionality. Common use cases include accessing device sensors, integrating with native SDKs (like payment processors, analytics tools, or social media SDKs), using platform-specific UI components, accessing system services, or implementing features that require native performance. The implementation typically involves creating a Flutter plugin that encapsulates the platform channel communication, making it reusable across projects. This approach allows Flutter apps to leverage native platform capabilities while maintaining a primarily Dart codebase, giving you the best of both worlds - Flutter's cross-platform development with native platform power when needed.

### Q6: How do you handle errors in platform channels?

**Answer:**

To handle errors in platform channels, wrap platform channel calls in **try-catch blocks** to catch `PlatformException`, which is the exception type thrown when platform channel communication fails. PlatformException provides error details including `code` (error type), `message` (error description), and `details` (additional error information). Check the error code to determine the type of error (like 'not_implemented' if the method doesn't exist on native side, or custom error codes for your specific errors). Provide fallback behavior or user-friendly error messages based on the error type. On the native side, use `result.error()` to send errors back to Flutter with appropriate error codes and messages. Always handle the case where the platform channel method might not be implemented, especially when supporting multiple platforms where a feature might only be available on one platform. Proper error handling ensures your app gracefully handles platform communication failures.

### Q7: What are the best practices for platform channels?

**Answer:**

**Best Practices for Platform Channels:**
- **Handle errors properly** by wrapping all platform channel calls in try-catch blocks, checking for PlatformException, and providing appropriate error handling and user feedback.
- **Use type-safe methods** by defining clear interfaces for platform channel communication, using consistent data types, and validating data on both Flutter and native sides.
- **Document channel names** and method signatures clearly, as channel names must match exactly between Flutter and native code, and mismatches cause silent failures.
- **Test on both platforms** (iOS and Android) since platform channel implementations are platform-specific and can behave differently or have platform-specific bugs.
- **Keep native code minimal** by only implementing what's necessary in native code, keeping business logic in Flutter/Dart, and using native code only for platform-specific APIs.
- **Use meaningful channel and method names** that clearly indicate their purpose, following a consistent naming convention (like 'package_name/feature_name').
- **Create Flutter plugins** to encapsulate platform channel code, making it reusable, testable, and easier to maintain.
- **Version your platform channel API** if you need to support multiple versions or handle breaking changes gracefully.

---

## Navigation

**Previous:** [Animations](animations.md)

**Next:** [Publishing](publishing.md)

