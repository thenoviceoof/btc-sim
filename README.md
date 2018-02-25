# BTC simulations

Some Monte Carlo simulations of simple asset selling strategies.

See the blog post (coming soon) for more details.

# Running

To run the simulations:

```
python simulation.py
```

This will call out to `plot.R`.

To produce some extra figures used in the blog post:

```
Rscript plot_distributions_unbounded.R
```

```
Rscript plot_distributions_bounded.R
```

# Dependencies

You will need:

- Python
  - Scipy (probability distribution sampling)
- R
  - ggplot2 (graphing)
  - rmutils (exponential distribution)

# License

All code is licensed under Apache 2: see LICENSE for details.
