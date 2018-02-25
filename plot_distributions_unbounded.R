################################################################################
## Copyright 2018 "Nathan Hwang" <thenoviceoof>
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
################################################################################

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
