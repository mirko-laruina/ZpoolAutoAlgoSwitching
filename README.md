# ZpoolAutoAlgoSwitching
Automatic algorithm-switching script written in Python
Using zpool multialgo feature (http://www.zpool.ca/site/multialgo), it automatically sets profitability factors reading them from a csv file (by default: algo.csv) which you have to manually set.
The miner is called on every algorithm listed in your csv and available in zpool.
In order to minimize delays given by changing algos, they are stored sorted by the time spent on them (most used first).
Currency and wallet address are set directly in the script, change them ( leave if you want to offer me a coffee ;) ).