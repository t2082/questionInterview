# Widgets & Layouts

## Table of Contents
- [Layout Widgets](#layout-widgets)
- [Material vs Cupertino](#material-vs-cupertino)
- [Custom Widgets](#custom-widgets)
- [Widget Composition](#widget-composition)
- [Interview Questions & Answers](#interview-questions--answers)

## Layout Widgets

**Row, Column, Stack Explained:**

```dart
// Row - arranges widgets horizontally
Row(
  children: [
    Text('Left'),
    Text('Right'),
  ],
)

// Column - arranges widgets vertically
Column(
  children: [
    Text('Top'),
    Text('Bottom'),
  ],
)

// Stack - overlays widgets
Stack(
  children: [
    Container(color: Colors.blue),
    Text('On top'),
  ],
)
```

## Material vs Cupertino

**Material Design (Android style):**
- Material widgets
- Android look and feel
- MaterialApp

**Cupertino (iOS style):**
- Cupertino widgets
- iOS look and feel
- CupertinoApp

## Custom Widgets

**Creating Reusable Widgets:**

```dart
class CustomButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  
  CustomButton({required this.text, required this.onPressed});
  
  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      child: Text(text),
    );
  }
}
```

## Widget Composition

**Building Complex UIs from Simple Widgets:**

```dart
// Compose widgets together
Scaffold(
  appBar: AppBar(title: Text('App')),
  body: Column(
    children: [
      HeaderWidget(),
      ContentWidget(),
      FooterWidget(),
    ],
  ),
)
```

## Interview Questions & Answers

### Q1: Explain Row, Column, and Stack widgets.

**Answer:**

**Row** arranges widgets horizontally in a single line, similar to a horizontal shelf where items are placed side by side. It uses mainAxisAlignment to control horizontal alignment and crossAxisAlignment to control vertical alignment of children. Row is ideal for creating horizontal layouts like navigation bars, button groups, or any UI elements that need to be displayed side by side.

**Column** arranges widgets vertically in a single column, similar to stacking boxes on top of each other. It uses mainAxisAlignment to control vertical alignment and crossAxisAlignment to control horizontal alignment of children. Column is perfect for creating vertical layouts like forms, lists of items, or any UI elements that need to be displayed one above another.

**Stack** overlays widgets on top of each other, allowing you to position widgets at specific coordinates within a bounded area. Unlike Row and Column which arrange widgets linearly, Stack allows widgets to overlap and be positioned absolutely or relatively. Stack is commonly used for creating complex layouts with overlapping elements, badges, floating action buttons, or custom positioned widgets.

### Q2: What is the difference between Expanded and Flexible?

**Answer:**

**Expanded** is a specialized Flexible widget that forces its child to take up all available space in the main axis (horizontal for Row, vertical for Column). It has a flex factor of 1 by default and doesn't allow the child to be smaller than the available space. Expanded is ideal when you want a widget to fill remaining space, such as making a button stretch to fill available width or making a content area expand to fill screen height.

**Flexible** allows its child to take up space based on a flex factor, but the child can choose to be smaller than the available space if it doesn't need it. Unlike Expanded, Flexible doesn't force the child to fill all available space - it just gives it the opportunity to grow. Flexible is useful when you want proportional sizing but the widget might not need all the space, or when you want more control over how space is distributed among multiple flexible children.

### Q3: Explain Container vs SizedBox vs Padding.

**Answer:**

**Container** is a versatile widget that can have decoration (colors, borders, shadows), alignment, size constraints, margins, and padding all in one. It's like a Swiss Army knife for layout - you can use it for styling, sizing, positioning, and more. However, Container is heavier than specialized widgets, so use SizedBox or Padding when you only need their specific features for better performance.

**SizedBox** is a lightweight widget that only provides size constraints (width and/or height) without any decoration or padding. It's more efficient than Container when you only need to set dimensions. SizedBox is perfect for adding spacing between widgets, setting explicit sizes, or creating empty spaces of specific dimensions. It's the preferred choice when you don't need decoration or other Container features.

**Padding** is a specialized widget that only adds padding (space inside the widget) around its child. It's more efficient than Container when you only need padding without decoration or size constraints. Padding is ideal for adding space around content, creating margins, or spacing elements. Use Padding when you need simple spacing without the overhead of Container's additional features.

### Q4: How do you create custom widgets?

**Answer:**

To create custom widgets, you extend either **StatelessWidget** for widgets that don't need to manage state, or **StatefulWidget** for widgets that need to maintain and update state. You then implement the `build()` method which returns a widget tree describing how your widget should be rendered. Custom widgets allow you to encapsulate reusable UI components, making your code more modular, maintainable, and easier to test. They help you follow the DRY (Don't Repeat Yourself) principle by extracting common UI patterns into reusable components.

### Q5: Explain widget composition in Flutter.

**Answer:**

**Widget composition** is the practice of building complex user interfaces by combining simpler, reusable widgets together. Instead of creating one large monolithic widget, you break down the UI into smaller, focused widgets that each handle a specific part of the interface. These smaller widgets are then composed together to create the complete UI. This approach makes code more maintainable, testable, and reusable. For example, a login screen might be composed of a HeaderWidget, EmailInputWidget, PasswordInputWidget, and LoginButtonWidget, each handling its own specific functionality.

### Q6: What are Material vs Cupertino widgets?

**Answer:**

**Material widgets** follow Google's Material Design guidelines, which is the design language used on Android platforms. These widgets provide the look and feel of Android apps with features like Material buttons, cards, dialogs, and navigation patterns. Material widgets are ideal when you want your app to feel native on Android devices or when you want a consistent Material Design experience across platforms.

**Cupertino widgets** follow Apple's Human Interface Guidelines, which is the design language used on iOS platforms. These widgets provide the look and feel of iOS apps with features like Cupertino buttons, switches, navigation bars, and alert dialogs. Cupertino widgets are ideal when you want your app to feel native on iOS devices. You can also mix Material and Cupertino widgets in the same app to provide platform-specific experiences.

### Q7: How do you handle responsive layouts?

**Answer:**

To handle responsive layouts in Flutter, you can use **MediaQuery** to get screen dimensions and device information, allowing you to adjust widget sizes and layouts based on available space. **LayoutBuilder** provides constraints that you can use to build widgets that adapt to their parent's size, making it perfect for creating layouts that respond to different container sizes. Additionally, you can use responsive packages like `flutter_screenutil` or `responsive_framework` that provide utilities for creating responsive designs. The key is to design your layouts to be flexible and adapt to different screen sizes rather than using fixed dimensions.

### Q8: Explain ConstrainedBox and UnconstrainedBox.

**Answer:**

**ConstrainedBox** adds additional constraints to its child widget, effectively limiting the maximum or minimum size the child can be. It's useful when you want to ensure a widget doesn't exceed certain dimensions or meets minimum size requirements. For example, you might use ConstrainedBox to limit an image's maximum width or ensure a button has a minimum height. The child widget must still respect these constraints, but ConstrainedBox provides a way to enforce size limits.

**UnconstrainedBox** removes constraints from its child, allowing the child to size itself based on its intrinsic dimensions rather than parent constraints. This is useful when you want a widget to size itself naturally without being constrained by its parent. However, UnconstrainedBox can cause overflow issues if the child is larger than the available space, so it should be used carefully and often wrapped with overflow handling widgets like SingleChildScrollView or OverflowBox.

### Q9: How do you optimize widget rebuilds?

**Answer:**

To optimize widget rebuilds, use **const constructors** whenever possible for widgets that don't change, as const widgets are created at compile-time and don't rebuild. Use **keys** (like ValueKey or ObjectKey) to help Flutter identify which widgets have changed, allowing it to preserve state and avoid unnecessary rebuilds. Implement **selective rebuilds** by splitting large widgets into smaller widgets, so only the parts that actually change get rebuilt. Additionally, use widgets like `Consumer` in Provider or `BlocBuilder` in BLoC to rebuild only specific parts of the UI rather than entire widget trees. These techniques help maintain smooth 60fps performance by minimizing unnecessary widget reconstructions.

---

## Navigation

**Previous:** [State Management Comparison](state-management-comparison.md)

**Next:** [Navigation](navigation.md)

