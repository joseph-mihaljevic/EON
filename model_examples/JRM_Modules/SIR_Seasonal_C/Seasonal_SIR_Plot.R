# Author: JR Mihaljevic
# SIR with seasonal forcing

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------

# Load libraries, options
# Make sure relevant packages are loaded:
library(tidyverse)
options(dplyr.width = Inf, dplyr.print_max = 1e9)

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
home_dir = getwd()

# Run the C program and Plot:
{
  
  # Parameters:
  n_year = 50;
  
  beta0 = 1.5; 
  beta1 = 0.25;
  gam = 1/13;
  mu = 1/(50*365);
  S0 = 0.75; 
  I0 = 1 - S0;
  
  # Run the program with the proper input arguments (need to be in correct order!):
  setwd(home_dir)
  system("rm ./output/output.csv") # remove any previous versions
  system(paste("./C/Seasonal_SIR", n_year, beta0, beta1, gam, mu, S0, I0))
  
  # Read in the output data:
  df_sir = read_csv("./output/output.csv")
  
  # Filter and plot:
  df_sir_sub = filter(df_sir, Year <= round(max(Year)-1), Year >= 10)
                      #Year >=(max(Year) - 11))
  plot(df_sir_sub$I ~ df_sir_sub$Year, type = "l",
       xlab = "Year", ylab = "Fraction Infectious")
  
}
