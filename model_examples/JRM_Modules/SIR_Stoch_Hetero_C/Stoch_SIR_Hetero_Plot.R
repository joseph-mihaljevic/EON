# Author: JR Mihaljevic
# SIR with seasonal forcing

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------

# Load libraries, options
# Make sure relevant packages are loaded:
library(tidyverse)
library(grid)
library(gridExtra)
options(dplyr.width = Inf, dplyr.print_max = 1e9)

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
home_dir = getwd()

# Run the C program and Plot:
{
  
  # Parameters:
  n_year = 1;
  n_iter = 10;
  time_step = 1;
  
  beta_bar = 0.25;
  beta_var = 5; # really beta_sd...
  hetero_A = 0; #not used here
  gam = 1 / 21; 
  mu = 1 / (50*365); #not used here
  N0 = 1000
  Y0 = 5
  X0 = N0 - Y0
  
  # Run the program with the proper input arguments (need to be in correct order!):
  setwd(home_dir)
  system("rm ./output/Stoch_SIR_Hetero.dat") # remove any previous versions
  system(paste("./C/Stoch_SIR_Hetero", n_year, n_iter, time_step, beta_bar, beta_var, hetero_A, gam, mu, N0, Y0, X0))
  
  # Read in the output data:
  df_sir = read_table2("./output/Stoch_SIR_Hetero.dat", col_names = F)
  colnames(df_sir) = c("Iter", "Day", "S", "I")
  
  # Calculate number of years:
  df_sir = mutate(df_sir, Year = Day / 365)
  
  # Filter and plot:
  max_I = max(df_sir$I, na.rm = T)
  min_I = min(df_sir$I, na.rm = T)
  
  # NUMBER INFECTED
  plot(NA,NA, 
       #xlim = c((max(df_sir$Year) - 11), round(max(df_sir$Year)-1)), 
       xlim = c(0, round(max(df_sir$Year))),
       ylim = c(0, max_I),
       xlab = "Year", ylab = "Number Infectives")
  
  for(i in 1:n_iter){
    
    df_sir_sub = 
      df_sir %>%
      #filter(Year <= round(max(Year)-1), Year >=(max(Year) - 11)) %>%
      filter(Iter == i)
    
    lines(df_sir_sub$I ~ df_sir_sub$Year)
    
  }
  
  # FRACTION INFECTED
  
  plot(NA,NA,
       xlim = c(0, round(max(df_sir$Year))),
       ylim = c(0, 1),
       xlab = "Year", ylab = "Fraction Infected")

  for(i in 1:n_iter){

    df_sir_sub =
      df_sir %>%
      filter(Iter == i) %>%
      mutate(FractI = I / N0)

    lines(df_sir_sub$FractI ~ df_sir_sub$Year)

  }
  
  # FREQUENCY OF OBSERVING NUMBER INFECTED
  
  these_times = c(0.01, 0.15, 0.2, 0.25)
  plots = list()
  
  for(i in 1:4){
    
    df_sir_sub = 
      df_sir %>%
      filter(Year > (these_times[i] - 0.01), Year < (these_times[i] + 0.01))
    
    plots[[i]] = 
      ggplot(df_sir_sub, aes(x = I)) +
      geom_density() +
      scale_x_continuous(limits = c(0, 580)) +
      theme_classic() +
      annotate("text", label = paste0("t = ", these_times[i]), x = 250, y = 0.05) +
      labs(x = "Number of Infectives", y = "Density")
    
  }
  
  plot_times = arrangeGrob(grobs = plots, nrow = 2, ncol = 2)
  
  quartz()
  grid.arrange(plot_times)
  
  
  
}
