# Illustrate the normal/exponential distribution behaviors.

library(rmutil)
library(ggplot2)
library(scales)

x = seq(0, 900000, by=1000)
normal = 2 * dnorm(x, 0, 100000)
exponential = dexp(x, 1/100000)

xx = x + 10000

norDF = data.frame(xx, y=normal)
expDF = data.frame(xx, y=exponential)

norDF$id = "normal"
expDF$id = "exponential"

data = rbind(norDF, expDF)

plot = ggplot(data, aes(x=xx, y=y, color=id)) +
    xlab("$/BTC") +
    ylab("Probability density") +
    scale_x_log10(labels=comma) +
    scale_y_log10() +
    geom_line()
plot$labels$colour = ""

ggsave("plt_distributions.png", plot)
