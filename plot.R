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

library(ggplot2)

cmd_args = commandArgs(trailingOnly=TRUE)

ideal_file = cmd_args[1]
real_file = cmd_args[2]
output_file = cmd_args[3]

ideal_raw <- read.csv(file=ideal_file, head=TRUE, sep=",")
real_raw <- read.csv(file=real_file, head=TRUE, sep=",")

ideal_raw$id <- "ideal"
real_raw$id <- "real"

data <- rbind(ideal_raw, real_raw)

plot = ggplot(data, aes(x=fraction, y=money, color=id)) +
    xlab("Sell fraction") + ylab("$ from 1 BTC") +
    ylim(0, 75000) +
    geom_jitter(alpha=0.3, size=0.3, height=200) +
    geom_smooth(method="loess", span=0.5)
plot$labels$colour = ""

ggsave(output_file, plot)
