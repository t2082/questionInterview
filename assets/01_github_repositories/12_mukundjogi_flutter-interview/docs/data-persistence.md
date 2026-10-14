# Data Persistence

## Table of Contents
- [SharedPreferences vs Hive vs SQLite](#sharedpreferences-vs-hive-vs-sqlite)
- [Hive Usage](#hive-usage)
- [SQLite with sqflite](#sqlite-with-sqflite)
- [Database Migrations](#database-migrations)
- [Offline-First Architecture](#offline-first-architecture)
- [Interview Questions & Answers](#interview-questions--answers)

## SharedPreferences vs Hive vs SQLite

**SharedPreferences - Simple Key-Value Storage:**

```dart
final prefs = await SharedPreferences.getInstance();
await prefs.setString('username', 'john');
final username = prefs.getString('username');
```

**Hive - Fast NoSQL Database:**

```dart
await Hive.initFlutter();
final box = await Hive.openBox('myBox');
box.put('key', 'value');
final value = box.get('key');
```

**SQLite - Relational Database:**

```dart
final db = await openDatabase('my_db.db');
await db.insert('users', {'name': 'John'});
final users = await db.query('users');
```

## Hive Usage

**Using Hive:**

```dart
// Initialize
await Hive.initFlutter();

// Open box
final box = await Hive.openBox('settings');

// Store data
box.put('theme', 'dark');
box.put('user', User(name: 'John'));

// Read data
final theme = box.get('theme');
final user = box.get('user');

// Delete
box.delete('theme');
```

## SQLite with sqflite

**Using sqflite:**

```dart
final db = await openDatabase(
  'my_db.db',
  version: 1,
  onCreate: (db, version) {
    db.execute('''
      CREATE TABLE users(
        id INTEGER PRIMARY KEY,
        name TEXT
      )
    ''');
  },
);

// Insert
await db.insert('users', {'name': 'John'});

// Query
final users = await db.query('users');

// Update
await db.update('users', {'name': 'Jane'}, where: 'id = ?', whereArgs: [1]);

// Delete
await db.delete('users', where: 'id = ?', whereArgs: [1]);
```

## Database Migrations

**Handling Migrations:**

```dart
final db = await openDatabase(
  'my_db.db',
  version: 2,
  onUpgrade: (db, oldVersion, newVersion) {
    if (oldVersion < 2) {
      db.execute('ALTER TABLE users ADD COLUMN email TEXT');
    }
  },
);
```

## Offline-First Architecture

**Implementing Offline-First:**

```dart
class DataRepository {
  final localDb = Hive.box('data');
  final apiService = ApiService();
  
  Future<List<Item>> getItems() async {
    // Try local first
    final localItems = localDb.get('items');
    if (localItems != null) {
      return localItems;
    }
    
    // Fetch from API
    try {
      final items = await apiService.getItems();
      localDb.put('items', items);
      return items;
    } catch (e) {
      // Return cached data if available
      return localDb.get('items', defaultValue: []);
    }
  }
}
```

## Interview Questions & Answers

### Q1: Compare SharedPreferences vs Hive vs SQLite.

**Answer:**

**SharedPreferences** is a simple key-value storage solution perfect for storing small amounts of primitive data like user preferences, settings, or simple flags. It's easy to use and doesn't require any setup, but it's limited to basic data types (String, int, bool, double, List<String>) and isn't suitable for complex objects or large amounts of data. SharedPreferences is ideal for storing app settings, user preferences, or simple configuration data.

**Hive** is a fast, lightweight NoSQL database written in pure Dart that provides excellent performance for storing structured data. It supports complex objects through TypeAdapters, provides type-safe boxes, and works well for medium-sized datasets. Hive is faster than SQLite for simple operations and doesn't require native code, making it perfect for storing user data, cached API responses, or app state that needs to persist across sessions.

**SQLite** (via sqflite package) is a full-featured relational database that supports complex queries, relationships, transactions, and ACID properties. It's ideal for applications that need to store large amounts of structured data with relationships between entities, perform complex queries, or require database features like joins, indexes, and foreign keys. SQLite is the best choice for apps with complex data models, reporting features, or when you need the power of a relational database.

### Q2: How do you use Hive for local storage?

**Answer:**

To use Hive for local storage, first **initialize Hive** with `await Hive.initFlutter()` in your app's startup code. Then **open a box** (which is like a table or collection) using `await Hive.openBox('boxName')` to create or access a storage container. Once you have a box reference, use **put() method** to store data with a key (like `box.put('key', value)`) and **get() method** to retrieve data (like `box.get('key')`). For complex objects, register TypeAdapters using `Hive.registerAdapter()` to enable serialization. Hive boxes persist data automatically, so you can close and reopen boxes across app sessions. Use `box.delete()` to remove data and `box.clear()` to empty the entire box.

### Q3: Explain Room database in Flutter (sqflite).

**Answer:**

**sqflite** is a Flutter plugin that provides SQLite database support, allowing you to use a full-featured relational database in your Flutter apps. It provides APIs to execute SQL queries, manage database transactions, and handle database migrations through version management. Unlike Room (which is Android-specific), sqflite works across all Flutter platforms. You can create tables using SQL CREATE TABLE statements, insert/update/delete data using SQL or helper methods, and query data using SQL SELECT statements or the query() method. sqflite supports database migrations through the `onUpgrade` callback, allowing you to modify schema as your app evolves. It's ideal for apps that need complex data relationships, advanced queries, or the reliability of ACID transactions.

### Q4: How do you handle database migrations?

**Answer:**

To handle database migrations in sqflite, use the **onUpgrade callback** in the `openDatabase()` method, which is called when the database version increases. The callback receives the database instance, old version number, and new version number, allowing you to write migration logic that modifies the schema based on version changes. Common migration tasks include adding new columns using `ALTER TABLE`, creating new tables, modifying existing tables, or migrating data from old schema to new schema. Always increment the database version in your `openDatabase()` call when making schema changes. For complex migrations, you can use a switch statement or if-else chain to handle different version upgrades incrementally, ensuring users upgrading from any previous version can migrate successfully.

### Q5: How do you implement offline-first architecture?

**Answer:**

To implement offline-first architecture, **cache data locally** using Hive, SQLite, or SharedPreferences so your app can function without network connectivity. Design your data layer to **try local storage first** - when data is requested, check the local cache first and return cached data immediately to provide instant user experience. Then, **sync with server when online** by fetching fresh data from the API in the background and updating the local cache. Use a Repository pattern that abstracts the data source, allowing your app to seamlessly switch between local and remote data. Implement sync strategies like periodic background sync, sync on app launch, or manual refresh. Handle conflicts when local and remote data differ, using strategies like "last write wins" or merging changes. This approach ensures your app works offline while keeping data fresh when connectivity is available.

### Q6: Explain encryption for local storage.

**Answer:**

To encrypt sensitive data in local storage, use packages like **encrypt** for general encryption needs or **flutter_secure_storage** for storing sensitive data like tokens, passwords, or API keys. `flutter_secure_storage` uses platform-specific secure storage mechanisms (Keychain on iOS, KeyStore on Android) to store encrypted data, providing better security than regular storage. For encrypting data in Hive or SQLite, you can use the `encrypt` package to encrypt data before storing it and decrypt it when retrieving. Always encrypt sensitive information like authentication tokens, user passwords, payment information, or any personally identifiable information (PII). Never store sensitive data in plain text, and consider using secure storage even for non-critical data to protect user privacy.

### Q7: How do you sync local and remote data?

**Answer:**

To sync local and remote data, implement sync logic that **compares local and remote data** using timestamps, version numbers, or change logs to determine what needs to be updated. Fetch data from the remote API and compare it with local data to identify differences - new items, updated items, or deleted items. Update the local database accordingly by inserting new records, updating modified records, and removing deleted records. Handle sync conflicts when both local and remote data have been modified, using strategies like timestamp-based resolution, conflict markers, or user intervention. Implement incremental sync by only fetching changes since the last sync timestamp to reduce data transfer. Use background tasks or periodic sync to keep data synchronized, and provide user feedback about sync status. Always handle network failures gracefully and ensure partial syncs don't corrupt local data.

### Q8: What are the best practices for data persistence?

**Answer:**

**Best Practices for Data Persistence:**
- **Choose the right storage** for your needs: SharedPreferences for simple key-value data, Hive for structured NoSQL data, SQLite for complex relational data with queries.
- **Handle migrations properly** by incrementing database versions and implementing onUpgrade callbacks to modify schema without losing user data.
- **Encrypt sensitive data** using flutter_secure_storage or encryption packages to protect user privacy and comply with data protection regulations.
- **Implement offline-first architecture** when your app needs to work without connectivity, caching data locally and syncing when online.
- **Sync data properly** by implementing conflict resolution strategies, incremental sync, and handling network failures gracefully.
- **Handle errors gracefully** by catching exceptions, providing fallback data, and informing users about data issues.
- **Use Repository pattern** to abstract data sources, making it easy to switch between local and remote data or change storage implementations.
- **Clean up old data** periodically to prevent storage from growing indefinitely and maintain app performance.

---

## Navigation

**Previous:** [Networking](networking.md)

**Next:** [Dependency Injection](dependency-injection.md)

