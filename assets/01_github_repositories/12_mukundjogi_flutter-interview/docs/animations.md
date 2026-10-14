# Animations

## Table of Contents
- [Implicit vs Explicit Animations](#implicit-vs-explicit-animations)
- [AnimationController](#animationcontroller)
- [Custom Animations](#custom-animations)
- [Hero Animations](#hero-animations)
- [Interview Questions & Answers](#interview-questions--answers)

## Implicit vs Explicit Animations

**Implicit Animations - Simple:**

```dart
AnimatedContainer(
  duration: Duration(seconds: 1),
  width: isExpanded ? 200 : 100,
  height: isExpanded ? 200 : 100,
  color: Colors.blue,
);
```

**Explicit Animations - Control:**

```dart
class MyAnimation extends StatefulWidget {
  @override
  _MyAnimationState createState() => _MyAnimationState();
}

class _MyAnimationState extends State<MyAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;
  
  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Duration(seconds: 1),
      vsync: this,
    );
    _animation = Tween<double>(begin: 0, end: 1).animate(_controller);
    _controller.forward();
  }
  
  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _animation,
      child: Text('Hello'),
    );
  }
  
  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
```

## AnimationController

**Using AnimationController:**

```dart
_controller = AnimationController(
  duration: Duration(seconds: 1),
  vsync: this,
);

_controller.forward(); // Start animation
_controller.reverse(); // Reverse animation
_controller.stop(); // Stop animation
_controller.reset(); // Reset to beginning
```

## Custom Animations

**Creating Custom Animations:**

```dart
class CustomAnimation extends StatefulWidget {
  @override
  _CustomAnimationState createState() => _CustomAnimationState();
}

class _CustomAnimationState extends State<CustomAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _rotation;
  
  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Duration(seconds: 2),
      vsync: this,
    );
    _rotation = Tween<double>(begin: 0, end: 2 * pi).animate(_controller);
    _controller.repeat();
  }
  
  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _rotation,
      builder: (context, child) {
        return Transform.rotate(
          angle: _rotation.value,
          child: Icon(Icons.refresh),
        );
      },
    );
  }
}
```

## Hero Animations

**Hero Animation:**

```dart
// First screen
Hero(
  tag: 'avatar',
  child: CircleAvatar(backgroundImage: NetworkImage(url)),
)

// Second screen
Hero(
  tag: 'avatar',
  child: Image.network(url),
)
```

## Interview Questions & Answers

### Q1: Explain implicit vs explicit animations.

**Answer:**

**Implicit animations** are simple, declarative animations where you specify the start and end values, and Flutter automatically animates the transition between them. Widgets like `AnimatedContainer`, `AnimatedOpacity`, `AnimatedPadding` handle the animation automatically when their properties change. They're easy to use - just change a property and the widget animates to the new value. Implicit animations are perfect for simple transitions like fading, scaling, or color changes, and they require minimal code. However, they offer limited control over the animation curve, duration, or intermediate states.

**Explicit animations** provide full control over the animation using `AnimationController` and `Animation` objects. You manually start, stop, reverse, and control the animation, and you can customize the animation curve, duration, and behavior. Explicit animations are more complex but offer complete control, making them ideal for complex animations, coordinated animations, or when you need precise control over animation timing. They're used with widgets like `AnimatedBuilder`, `FadeTransition`, or `RotationTransition` to create custom animation effects.

### Q2: How do you create custom animations?

**Answer:**

To create custom animations, use **AnimationController** to control the animation timing and lifecycle (start, stop, reverse, repeat). Create **Tween** objects to define the range of values for your animation (like Tween<double>(begin: 0, end: 360) for rotation). Combine the Tween with the AnimationController using `tween.animate(controller)` to create an Animation object. Use **AnimatedBuilder** to rebuild widgets based on animation values, or use transition widgets like `FadeTransition`, `ScaleTransition`, or `RotationTransition` for common effects. For complex custom animations, you can use `CustomPainter` with animation values to draw custom graphics. The key is to listen to the animation's value changes and update your UI accordingly, creating smooth, controlled animations that enhance user experience.

### Q3: Explain AnimationController and Tween.

**Answer:**

**AnimationController** is the core component that controls animation timing and lifecycle. It manages the animation's progress (from 0.0 to 1.0), provides methods to start (`forward()`), stop (`stop()`), reverse (`reverse()`), and repeat animations. The controller requires a `vsync` parameter (typically `this` when using `SingleTickerProviderStateMixin`) to synchronize with the screen refresh rate, ensuring smooth 60fps animations. You specify the animation duration when creating the controller, and it fires callbacks as the animation progresses. The controller is essential for any explicit animation and must be disposed when no longer needed to prevent memory leaks.

**Tween** defines the range of values for an animation, specifying the beginning value and ending value. For example, `Tween<double>(begin: 0, end: 360)` defines a range from 0 to 360 degrees for a rotation animation. Tween works with AnimationController to create an Animation object that interpolates between the begin and end values based on the controller's progress. You can use different types of Tweens (ColorTween, SizeTween, etc.) for animating different properties. Tween also supports custom interpolation curves to create non-linear animations like easing in/out effects.

### Q4: How do you optimize animations for performance?

**Answer:**

To optimize animations for performance, **use appropriate durations** (typically 200-500ms for most UI animations) to ensure animations feel responsive without being too slow. **Always dispose AnimationControllers** in the `dispose()` method to prevent memory leaks and ensure controllers are properly cleaned up. **Avoid heavy computations during animations** - perform expensive operations before or after animations, not during each frame update. **Use RepaintBoundary** around animated widgets to isolate repaints and prevent unnecessary repaints of parent widgets. **Prefer implicit animations** when possible as they're optimized by Flutter, and only use explicit animations when you need the additional control. **Limit the number of simultaneous animations** to avoid overloading the rendering pipeline. **Use hardware acceleration** by ensuring animations don't trigger layout recalculations - prefer transforms (translate, scale, rotate) over layout changes. Profile animations using Flutter DevTools to identify performance issues.

### Q5: Explain Hero animations.

**Answer:**

**Hero animations** create smooth, visually connected transitions between screens by animating a widget from one screen to another. When you wrap a widget with a `Hero` widget and give it a unique `tag`, Flutter automatically creates an animation that "flies" the widget from its position on the source screen to its position on the destination screen. This creates a seamless visual connection that helps users understand the relationship between screens. Hero animations are commonly used for images, avatars, or cards that appear on multiple screens - when navigating, the widget appears to move from one screen to the next. Both the source and destination screens must have Hero widgets with the same tag for the animation to work. Hero animations enhance user experience by providing visual continuity and making navigation feel more natural and polished.

### Q6: How do you create page transitions?

**Answer:**

To create custom page transitions, use **PageRouteBuilder** which allows you to define custom transition animations by providing `transitionsBuilder` and `transitionDuration` parameters. The `transitionsBuilder` receives the context, animation, secondary animation, and child widget, allowing you to create custom effects like slide, fade, scale, or rotation transitions. You can combine multiple transitions (like fade + slide) for more complex effects. Alternatively, use packages like **page_transition** which provides pre-built transition effects that you can use with minimal code. Common transition types include slide transitions (from left, right, top, bottom), fade transitions, scale transitions, or rotation transitions. Custom page transitions help create a unique app identity and improve the perceived quality of your app by making navigation feel smooth and polished.

### Q7: What are the best practices for animations?

**Answer:**

**Best Practices for Animations:**
- **Use implicit animations when possible** as they're simpler, require less code, and are optimized by Flutter, only using explicit animations when you need additional control.
- **Dispose controllers properly** by calling `controller.dispose()` in the `dispose()` method to prevent memory leaks and ensure resources are cleaned up.
- **Keep animations smooth (60fps)** by avoiding heavy computations during animations, using appropriate durations, and ensuring animations don't cause layout recalculations.
- **Test on different devices** to ensure animations perform well on both high-end and low-end devices, as performance can vary significantly.
- **Consider accessibility** by respecting system animation preferences (users may have reduced motion enabled), and ensure animations don't interfere with screen readers or accessibility features.
- **Use meaningful animations** that enhance user understanding rather than decorative animations that distract or slow down the user experience.
- **Provide animation feedback** for user actions to confirm interactions, but keep animations subtle and purposeful.
- **Profile animations** using Flutter DevTools to identify performance issues and ensure animations don't cause jank.

---

## Navigation

**Previous:** [Performance](performance.md)

**Next:** [Platform Channels](platform-channels.md)

