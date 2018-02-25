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

# Illustrate the beta distribution behaviors.

library(rmutil)
library(ggplot2)
library(scales)

scaling = (10000000 - 10000)

xx = seq(10000, 10000000, by=1000)
x = (log10(xx) - log10(10000))/(log10(10000000) - log10(10000))
# Re-normalize with the CDF (pexp)
maxpoint = dexp(2 * x, 2) / pexp(2, 2)
survive = (1 - x) * (x - 0.5)^2 + 0.99 * x^4 * 4^(1-x)

maxDF = data.frame(xx, y=maxpoint)
surDF = data.frame(xx, y=survive)

maxDF$id = "Max value"
surDF$id = "Survival chance"

data = rbind(maxDF, surDF)

plot = ggplot(data, aes(x=xx, y=y, color=id)) +
    xlab("$/BTC") +
    ylab("Probability density OR probability") +
    ylim(0, 2) +
    scale_x_log10(labels=comma) +
    geom_line()
plot$labels$colour = ""

ggsave("plt_beta_distributions.png", plot)
