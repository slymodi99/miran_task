
## 1. How would you scale this data model for 10M orders a month?

**Database scaling**

### Vertical scaling

Vertical scaling, also known as scaling up, involves adding more resources such as CPU, RAM, or disk capacity to an existing database server.Such powerful servers can store and handle vast amounts of data.

However, vertical scaling has significant drawbacks:

- There are hardware limits to how much CPU, RAM, or storage can be added to a single server. For very large user bases, a single machine may not be sufficient.  
- It creates a greater risk of a single point of failure.  
- High-end servers with more resources are considerably more expensive, increasing overall costs.

### Horizontal scaling

Horizontal scaling, also known as sharding, involves adding more database servers instead of relying on one machine. It partitions a large database into smaller, more manageable parts called shards. Each shard holds a unique subset of the data but shares the same schema as the others.

Horizontal scaling allows the system to handle larger loads by distributing data and requests across multiple servers, improving fault tolerance and scalability.

---

## 2. DB indexes:

### 1. Composite Index on (`Product`.`name`, `Product`.`price`)

**Why this index?**

- The model supports **search by name** and **ordering by price**. Combining these into a composite index optimizes queries where users filter by name and order the results by price.  
- For example:  
  - **Query**: Search for products with a name containing "phone" and order them by price in ascending order.  
- With this index, the database can optimize both the filtering (`name`) and sorting (`price`) in a single pass.

**Trade-Offs**

- **Read Performance**: Query performance improves significantly for compound queries involving both `name` and `price`.  
- **Write Performance**: Insertions or updates to `Product` (e.g., updating `price`) may take slightly longer, as the composite index must also be updated.

### 2. Composite Index on (`Order`.`customer_id`, `Order`.`status`)

**Why this index?**

- The API allows **filtering orders by customer name and status**. Since filtering by customer and status is a common use case:  
- A composite index on `customer_id` (from the ForeignKey) and `status` will optimize queries that use these conditions together.  
- Example:  
  - **Query**: Retrieve orders for a specific customer (`customer_id=5`) with the status `pending`.

**Trade-Offs**

- **Read Performance**: Improves query performance significantly when filtering on both `customer` and `status`.  
- **Write Performance**: Inserts or updates may take longer as the index must be updated.

---

## 3. How would you handle ensuring consistency if multiple orders are decrementing product inventory at the same time?​

To ensure data consistency during concurrent inventory updates, there are a couple of common approaches:

### 1. Implemented Solution: Database Transactions with Row-Level Locking

- The entire order creation process is wrapped in a `transaction.atomic()` block to ensure atomicity.  
- Relevant product rows are queried using `select_for_update()`, which places a row-level lock to prevent concurrent modifications.  
- Inventory is decremented safely using a conditional update with `Case` and `When` expressions, ensuring efficient and atomic stock updates.  
- This approach prevents race conditions and maintains consistency by serializing access to the inventory records.

### 2. Alternative Approach: Request Queueing via Cache

- Incoming order requests can be queued in a fast, in-memory store like Redis.  
- A background worker sequentially processes the queue, updating inventory one request at a time.  
- This serializes inventory modifications externally, avoiding database locking contention.  
- The queue approach can improve throughput and scalability, especially under very high concurrency.  
- However, it adds complexity with background workers and requires careful handling of failure and retries.
"""

