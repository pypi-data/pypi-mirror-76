#tabspy

This is the documentation for ```tabspy``` package

## Installation:
```
pip install tabspy
```

## Usage
Sample Code:
```
import tabspy.utils as ut
import tabspy.strategy.strategy as st

a = ut.welcome('SomeName')
b = st.Strategy('SomeName')
b.welcome()
```
Output:
```
Welcome SomeName : tabspy >> utils.welcome()
Welcome SomeName : tabspy >> strategy >> strategy.Strategy.welcome()
```