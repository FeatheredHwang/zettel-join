What you need to know before writing notes to ZK :
# Rules of Formulating Knowledge

## Avoid sets

Bad practice:

There are four collection data types in the Python programming language:

1. List
2. Tuple
3. Set
4. Dictionary

---

The above example works ill for memorize, due to ["Avoid sets" rule](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge), you'd better to convert a set into a meaningful listing.

Good practice:

- **List** is a collection which is ordered and changeable. Allows duplicate members.
- **Tuple** is a collection which is ordered and **unchangeable**. Allows duplicate members.
- ...

---

Make a table for comparison would also work nice.

| collection data types | ordered               | changeable   | duplicate |
| --------------------- | --------------------- | ------------ | --------- |
| List                  | ordered               |              | allow     |
| Tuple                 | ordered               | unchangeable | allow     |
| Set                   | unordered (unindexed) | unchangeable | no        |
| Dictionary            | ordered               | changeable   | no        |
