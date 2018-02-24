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
    ylim(0, 75000) +
    geom_point(alpha=0.5)

ggsave(output_file, plot)
