# Orchestrator (abbr O)

- Provider connect to O, and produces data to O
  - Provider create the initialize data
  - then produces more message through time, and dispatch to O
- Consumer subscribe to the changes of data by requesting O
- Reducer combines the old data and the incoming messages
- O figures out the changes of data, and emit to Consumers
- Strategies inherit from Consumers
- Persistencers also inherit from Consumers to save the data to databases

- Everything above has nothing to do with code names
- DataTypes together with their corresponding parameters, we call it Vectors
- The store is a dict of codes
- A code is a dict of vector-dataframe or vector-object pairs

```python
store = {
  code: {
    vector: object
  }
}
```

- A strategies is codename-agnostic
- There is also somewhere to store parameters from manual tuning which we call it `Tuning`
- We could define Tuning of a codename by call tune method of O

- Consumers could only subscribe to vectors, but not code
- Reducers could only access `store[code]`, but not the store itself

- Consumers could also define whether the data emitting should be throttled
