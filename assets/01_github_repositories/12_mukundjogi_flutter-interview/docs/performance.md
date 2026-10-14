# Performance

## Table of Contents
- [Build Optimization](#build-optimization)
- [List Optimization](#list-optimization)
- [Image Optimization](#image-optimization)
- [Memory Management](#memory-management)
- [Profiling](#profiling)
- [Interview Questions & Answers](#interview-questions--answers)

## Build Optimization

**Reducing Rebuilds:**

```dart
// Use const constructors
const Text('Hello');

// Use keys to preserve state
MyWidget(key: ValueKey('unique'));

// Split widgets to reduce rebuild scope
class OptimizedWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ExpensiveWidget(), // Only rebuilds if needed
        SimpleWidget(),
      ],
    );
  }
}
```

## List Optimization

**Optimizing Lists:**

```dart
// Use ListView.builder for long lists
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ListTile(title: Text(items[index]));
  },
);

// Use const constructors in lists
ListView.builder(
  itemBuilder: (context, index) {
    return const ListTile(title: Text('Item'));
  },
);
```

## Image Optimization

**Optimizing Images:**

```dart
// Use appropriate image formats
Image.asset('image.webp'); // WebP is smaller

// Cache images
CachedNetworkImage(
  imageUrl: url,
  placeholder: (context, url) => CircularProgressIndicator(),
);

// Resize images
Image.memory(
  imageBytes,
  width: 200,
  height: 200,
);
```

## Memory Management

**Managing Memory:**

```dart
// Dispose controllers
@override
void dispose() {
  _controller.dispose();
  super.dispose();
}

// Use weak references when needed
final weakRef = WeakReference(object);

// Clear large caches
imageCache.clear();
```

## Profiling

**Profiling Apps:**

```dart
// Use Flutter DevTools
// - Performance overlay
// - Memory profiler
// - CPU profiler

// Enable performance overlay
MaterialApp(
  showPerformanceOverlay: true,
);
```

## Interview Questions & Answers

### Q1: How do you optimize Flutter app performance?

**Answer:**

To optimize Flutter app performance, focus on several key areas: **optimize widget rebuilds** by using const constructors, keys, and selective rebuilds to minimize unnecessary widget reconstructions. **Optimize list rendering** by using ListView.builder for long lists, implementing itemExtent for fixed-height items, and using const constructors in list items. **Optimize images** by using appropriate formats (WebP), caching images, resizing images to required dimensions, and using image caching packages. **Manage memory usage** by disposing controllers and streams properly, clearing caches when appropriate, and avoiding memory leaks. **Profile your app** using Flutter DevTools to identify performance bottlenecks and measure improvements. Additionally, minimize expensive computations on the main thread by using isolates for heavy processing.

### Q2: Explain build optimization techniques.

**Answer:**

Build optimization techniques focus on reducing unnecessary widget rebuilds to maintain smooth 60fps performance. **Use const constructors** whenever possible for widgets that don't change, as const widgets are created at compile-time and never rebuild, saving CPU cycles. **Use keys** (ValueKey, ObjectKey, UniqueKey) to help Flutter identify which widgets have changed, allowing it to preserve state and reuse widgets efficiently. **Split large widgets into smaller widgets** so that only the parts that actually change get rebuilt, rather than rebuilding entire widget trees. **Use selective rebuild widgets** like Consumer in Provider or BlocBuilder in BLoC to rebuild only specific parts of the UI that depend on changed state. **Avoid calling setState() unnecessarily** and ensure state changes are batched when possible. These techniques help Flutter's rendering engine work efficiently by minimizing the amount of work needed during each frame.

### Q3: How do you optimize list rendering?

**Answer:**

To optimize list rendering, use **ListView.builder** instead of ListView with a children list, as ListView.builder lazily builds only visible items, dramatically improving performance for long lists. **Use const constructors** in list item widgets when the items don't change, allowing Flutter to reuse widget instances. **Provide itemExtent** when items have a fixed height, which helps Flutter calculate scroll positions more efficiently and improves scrolling performance. **Use RepaintBoundary** around expensive list items to isolate repaints and prevent unnecessary repaints of other items. **Implement proper keys** for list items to help Flutter identify which items have changed when the list updates. **Avoid heavy computations in itemBuilder** - perform expensive operations outside the builder and pass results as data. For very long lists, consider implementing pagination or virtual scrolling to limit the number of items rendered at once.

### Q4: Explain image optimization in Flutter.

**Answer:**

Image optimization is crucial for app performance and size. **Use appropriate formats** like WebP which provides better compression than PNG or JPEG, reducing both download time and storage space. **Cache images** using packages like `cached_network_image` which automatically caches network images, avoiding repeated downloads and improving load times. **Resize images** to the exact dimensions needed rather than loading full-resolution images and scaling them down, which wastes memory and bandwidth. **Use image placeholders** to show loading indicators while images load, improving perceived performance. **Lazy load images** in lists so images only load when they're about to become visible. **Compress images** before including them in your app bundle to reduce app size. Consider using different image resolutions for different screen densities (1x, 2x, 3x) to provide optimal quality without wasting resources on high-density displays when lower resolution would suffice.

### Q5: How do you profile Flutter apps?

**Answer:**

To profile Flutter apps, use **Flutter DevTools**, a suite of performance and debugging tools. The **Performance tab** shows frame rendering times, helping you identify jank (frames that take longer than 16ms) and see which widgets are causing performance issues. The **Memory tab** displays memory usage over time, helping you identify memory leaks, excessive memory consumption, or objects that aren't being garbage collected. The **CPU Profiler** shows which functions are consuming CPU time, helping you identify expensive operations that should be optimized or moved to isolates. Enable the **performance overlay** in your app (`showPerformanceOverlay: true`) to see real-time frame rendering statistics. Use **timeline events** to mark specific operations and measure their performance. Regularly profile your app during development to catch performance issues early and verify that optimizations are effective.

### Q6: How do you reduce app size?

**Answer:**

To reduce app size, **remove unused code** by enabling tree-shaking in release builds, which automatically removes unused code and dependencies. **Optimize assets** by compressing images, using WebP format, removing unused images and fonts, and providing assets only for the screen densities you support. **Use code splitting** and dynamic imports to load code only when needed, though Flutter's tree-shaking already does this to some extent. **Minimize dependencies** by only including packages you actually use and avoiding large packages when smaller alternatives exist. **Enable ProGuard/R8** for Android and strip unused code for iOS in release builds. **Use app bundles** (AAB for Android) instead of APKs, which allows Google Play to deliver optimized versions to different devices. **Analyze your app size** using `flutter build apk --analyze-size` or `flutter build ios --analyze-size` to see what's contributing to app size and identify optimization opportunities.

### Q7: What are common performance bottlenecks?

**Answer:**

**Common Performance Bottlenecks:**
- **Unnecessary rebuilds** occur when widgets rebuild even when their data hasn't changed, often caused by not using const constructors, missing keys, or rebuilding entire widget trees instead of selective parts. This leads to jank and wasted CPU cycles.
- **Large lists without optimization** can cause significant performance issues when rendering hundreds or thousands of items, especially if using ListView with a children list instead of ListView.builder, leading to memory issues and slow scrolling.
- **Unoptimized images** including loading full-resolution images when smaller versions would suffice, not caching network images, or using inefficient image formats, causing slow load times and high memory usage.
- **Memory leaks** happen when resources aren't properly disposed (controllers, streams, subscriptions), causing memory usage to grow over time and eventually leading to app crashes or device slowdown.
- **Heavy computations on main thread** block the UI thread, causing frame drops and jank. Expensive operations like image processing, data parsing, or complex calculations should be moved to isolates.
- **Excessive use of setState()** or notifyListeners() can trigger cascading rebuilds throughout the widget tree, causing performance degradation.

---

## Navigation

**Previous:** [Testing](testing.md)

**Next:** [Animations](animations.md)

